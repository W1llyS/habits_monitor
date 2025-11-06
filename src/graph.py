#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of habits
#
# Copyright (c) 2019 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('WebKit2', '4.1')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import WebKit2
from gi.repository import GLib
import config
from basedialog import BaseDialog
from configurator import Configuration


class Graph(BaseDialog):
    def __init__(self, title='', subtitle='', days='', distance='', clics='',
                 keys=''):
        self.title = title
        self.subtitle = subtitle
        self.days = days
        self.distance = distance
        self.clics = clics
        self.keys = keys
        self.is_fullscreen = False
        BaseDialog.__init__(self, title, None, ok_button=False,
                            cancel_button=False, modal=False,
                            resizable=True)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow1.set_hexpand(True)
        self.scrolledwindow1.set_vexpand(True)
        self.grid.attach(self.scrolledwindow1, 0, 0, 1, 1)

        # Set up user content manager BEFORE creating WebView
        content_manager = WebKit2.UserContentManager()
        content_manager.register_script_message_handler('fullscreen')
        content_manager.connect('script-message-received::fullscreen',
                                self.on_fullscreen_message)

        # Create WebView with the content manager
        self.viewer = WebKit2.WebView(user_content_manager=content_manager)
        self.viewer.set_hexpand(True)
        self.viewer.set_vexpand(True)

        # Enable console logging
        settings = self.viewer.get_settings()
        settings.set_property('enable-developer-extras', True)
        settings.set_property('enable-write-console-messages-to-stdout', True)

        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        self.viewer.load_uri('file://' + config.HTML_GRAPH)
        self.viewer.connect('load-changed', self.load_changed)
        self.viewer.connect('decide-policy', self.on_decide_policy)
        self.viewer.connect('notify::title', self.on_title_changed)
        self.set_focus(self.viewer)

        # Allow F11 to exit fullscreen
        self.connect('key-press-event', self.on_key_press)

    def update(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        units = preferences['units']
        distance = []
        if units == 'feets':
            for i in self.distance:
                distance.append(i/3.28084)
        else:
            distance = self.distance

        self.web_send('title="{}";subtitle="{}";days={};distance={};\
            clics={};keys={};draw_graph(title,subtitle,days,distance,\
                clics, keys);'.format(self.title, self.subtitle, self.days,
                                      distance, self.clics, self.keys))

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.update()
            configuration = Configuration()
            preferences = configuration.get('preferences')
            distance_color = preferences['distance-color']
            clics_color = preferences['clics-color']
            keys_color = preferences['keys-color']
            units = preferences['units']
            self.web_send('set_colors("{}", "{}", "{}");'.format(
                distance_color, clics_color, keys_color
            ))
            self.web_send('set_units("{}");'.format(units))
            while Gtk.events_pending():
                Gtk.main_iteration()
            GLib.idle_add(self._reflow_chart)

    def web_send(self, msg):
        self.viewer.run_javascript(msg, None, None, None)

    def on_fullscreen_message(self, content_manager, js_result):
        """Handle fullscreen message from JavaScript"""
        print("DEBUG: Fullscreen message received!")
        self.toggle_fullscreen()

    def on_title_changed(self, webview, param):
        """Handle messages from JavaScript via document.title (fallback method)"""
        import json
        title = webview.get_title()
        print(f"DEBUG on_title_changed: Title changed to: '{title}'")
        if title and title != "null" and title != "My-Weather-Indicator (Evolution)":
            try:
                message = json.loads(title)
                print(f"DEBUG on_title_changed: Parsed message: {message}")
                if isinstance(message, dict) and message.get('action') == 'fullscreen':
                    print("DEBUG on_title_changed: Fullscreen action detected via title, toggling...")
                    self.toggle_fullscreen()
            except (json.JSONDecodeError, ValueError) as e:
                print(f"DEBUG on_title_changed: Not JSON or parse error: {e}")
                pass  # Not a JSON message, ignore

    def toggle_fullscreen(self):
        """Toggle fullscreen mode for the dialog window"""
        print(f"DEBUG toggle_fullscreen: Called! Current state: {self.is_fullscreen}")
        if self.is_fullscreen:
            print("DEBUG toggle_fullscreen: Exiting fullscreen")
            self.unfullscreen()
            self.is_fullscreen = False
        else:
            print("DEBUG toggle_fullscreen: Entering fullscreen")
            self.fullscreen()
            self.is_fullscreen = True
        print(f"DEBUG toggle_fullscreen: New state: {self.is_fullscreen}")
        GLib.idle_add(self._reflow_chart)

    def _reflow_chart(self):
        """Force Highcharts to resize after the WebView geometry changes"""
        if getattr(self, 'viewer', None):
            self.viewer.run_javascript(
                'if (typeof chart !== "undefined") { chart.reflow(); }',
                None, None, None)
        return False

    def on_key_press(self, widget, event):
        """Handle keyboard events (F11 for fullscreen toggle)"""
        from gi.repository import Gdk
        if event.keyval == Gdk.KEY_F11:
            self.toggle_fullscreen()
            return True
        return False

    def on_decide_policy(self, web_view, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            nav_action = decision.get_navigation_action()
            uri = nav_action.get_request().get_uri()

            # Handle data URI downloads (from offline-exporting)
            if uri and uri.startswith('data:'):
                import base64
                import os
                from gi.repository import GLib

                # Parse the data URI
                try:
                    # Format: data:mime/type;base64,data
                    header, data = uri.split(',', 1)
                    mime_type = header.split(';')[0].split(':')[1]

                    # Determine file extension from mime type
                    ext_map = {
                        'image/png': '.png',
                        'image/jpeg': '.jpg',
                        'application/pdf': '.pdf',
                        'image/svg+xml': '.svg'
                    }
                    ext = ext_map.get(mime_type, '.png')

                    # Decode base64 data
                    file_data = base64.b64decode(data)

                    # Create file chooser dialog
                    dialog = Gtk.FileChooserDialog(
                        title="Save Chart",
                        parent=self,
                        action=Gtk.FileChooserAction.SAVE
                    )
                    dialog.add_buttons(
                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK
                    )
                    dialog.set_do_overwrite_confirmation(True)
                    dialog.set_current_name(f"chart{ext}")

                    response = dialog.run()
                    if response == Gtk.ResponseType.OK:
                        filename = dialog.get_filename()
                        with open(filename, 'wb') as f:
                            f.write(file_data)

                    dialog.destroy()

                except Exception as e:
                    print(f"Error saving chart: {e}")

                decision.ignore()
                return True

        return False


if __name__ == '__main__':
    title = 'Titulo'
    subtitle = 'Subtitulo'
    days = ['2019-12-25', '2019-12-26', '2019-12-27', 10]
    distance = [25, 30, 35]
    clics = [50, 60, 70]
    keys = [1230, 2550, 2600]
    graph = Graph(title, subtitle, days, distance, clics, keys)
    graph.run()
