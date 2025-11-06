#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Keyboard Statistics Dialog - Shows individual keyboard key totals
#

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from basedialog import BaseDialog
from database import Database


class KeyboardStatsDialog(BaseDialog):
    """Dialog to show individual keyboard key statistics"""

    def __init__(self):
        BaseDialog.__init__(self, 'Keyboard Statistics', None,
                            ok_button=False, cancel_button=False,
                            modal=False)
        self.set_size_request(500, 600)

    def init_ui(self):
        BaseDialog.init_ui(self)

        # Get data from database
        db = Database()
        key_totals = db.get_total_keyboard_keys()

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)
        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="xx-large" weight="bold">⌨️  Keyboard Statistics</span>')
        main_box.pack_start(title_label, False, False, 0)

        # Separator
        main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        # Info text
        info_label = Gtk.Label()
        info_label.set_markup('<span size="small" style="italic">Total presses for each keyboard key</span>')
        info_label.set_halign(Gtk.Align.START)
        main_box.pack_start(info_label, False, False, 0)

        # Total keys
        total_keys = sum(key_totals.values()) if key_totals else 0
        total_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        total_label = Gtk.Label()
        total_label.set_markup('<b>Total Keystrokes:</b>')
        total_label.set_halign(Gtk.Align.START)

        total_value = Gtk.Label()
        total_value.set_markup(f'<span size="x-large" weight="bold" color="#ffffff">{total_keys:,}</span>')
        total_value.set_halign(Gtk.Align.END)

        total_box.pack_start(total_label, True, True, 0)
        total_box.pack_start(total_value, False, False, 0)
        main_box.pack_start(total_box, False, False, 5)

        main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        # Scrolled window for keys list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(400)

        # Keys list container
        keys_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        # Display keys
        if key_totals:
            # Already sorted by count (DESC) from database
            for key_name, count in key_totals.items():
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

                name_label = Gtk.Label()
                name_label.set_markup(f'<b>{key_name}:</b>')
                name_label.set_halign(Gtk.Align.START)
                name_label.set_size_request(200, -1)

                count_label = Gtk.Label()
                count_label.set_markup(f'<span size="large" color="#ffffff">{count:,}</span>')
                count_label.set_halign(Gtk.Align.END)

                hbox.pack_start(name_label, True, True, 0)
                hbox.pack_start(count_label, False, False, 0)
                keys_box.pack_start(hbox, False, False, 0)
        else:
            no_data = Gtk.Label()
            no_data.set_markup('<span style="italic" size="large">No keyboard data yet. Start typing!</span>')
            no_data.set_halign(Gtk.Align.CENTER)
            keys_box.pack_start(no_data, True, True, 0)

        scrolled.add(keys_box)
        main_box.pack_start(scrolled, True, True, 0)

        # Close button
        main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)
        close_button = Gtk.Button.new_with_label('Close')
        close_button.connect('clicked', lambda w: self.close())
        main_box.pack_start(close_button, False, False, 0)

        self.grid.attach(main_box, 0, 0, 1, 1)

    def close(self):
        self.hide()


if __name__ == '__main__':
    dialog = KeyboardStatsDialog()
    dialog.run()
