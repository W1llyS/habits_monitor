#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Secret Dialog - Shows total combined statistics
#

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from basedialog import BaseDialog
from configurator import Configuration
from database import Database


class SecretDialog(BaseDialog):
    """Dialog to show total combined statistics across all days"""

    def __init__(self):
        BaseDialog.__init__(self, 'Secret Statistics', None,
                            ok_button=False, cancel_button=False,
                            modal=False)
        self.set_size_request(500, 600)

    def init_ui(self):
        BaseDialog.init_ui(self)

        # Load statistics
        configuration = Configuration()
        stats = configuration.get('stats')

        # Calculate totals
        total_clicks = 0
        total_keys = 0
        total_distance = 0
        total_days = len(stats)

        for day in stats:
            if 'clics' in stats[day]:
                total_clicks += stats[day]['clics']
            if 'keys' in stats[day]:
                total_keys += stats[day]['keys']
            if 'distance' in stats[day]:
                total_distance += stats[day]['distance']

        # Convert distance to meters and kilometers
        distance_meters = total_distance / 1000.0
        distance_km = distance_meters / 1000.0

        # Create grid for displaying stats
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(20)
        grid.set_margin_start(30)
        grid.set_margin_end(30)
        grid.set_margin_top(30)
        grid.set_margin_bottom(30)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="xx-large" weight="bold">🔐 Secret Statistics</span>')
        grid.attach(title_label, 0, 0, 2, 1)

        # Separator
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator1, 0, 1, 2, 1)

        # Total Clicks
        row = 2
        clicks_label = Gtk.Label()
        clicks_label.set_markup('<b>Total Mouse Clicks:</b>')
        clicks_label.set_halign(Gtk.Align.START)
        grid.attach(clicks_label, 0, row, 1, 1)

        clicks_value = Gtk.Label()
        clicks_value.set_markup(f'<span size="large" color="#bd574e">{total_clicks:,}</span>')
        clicks_value.set_halign(Gtk.Align.END)
        grid.attach(clicks_value, 1, row, 1, 1)

        # Total Keys
        row += 1
        keys_label = Gtk.Label()
        keys_label.set_markup('<b>Total Keystrokes:</b>')
        keys_label.set_halign(Gtk.Align.START)
        grid.attach(keys_label, 0, row, 1, 1)

        keys_value = Gtk.Label()
        keys_value.set_markup(f'<span size="large" color="#142d4c">{total_keys:,}</span>')
        keys_value.set_halign(Gtk.Align.END)
        grid.attach(keys_value, 1, row, 1, 1)

        # Combined total
        row += 1
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator2, 0, row, 2, 1)

        row += 1
        combined_label = Gtk.Label()
        combined_label.set_markup('<b>Combined Total:</b>')
        combined_label.set_halign(Gtk.Align.START)
        grid.attach(combined_label, 0, row, 1, 1)

        combined_value = Gtk.Label()
        combined_total = total_clicks + total_keys
        combined_value.set_markup(f'<span size="xx-large" weight="bold" color="#445c3c">{combined_total:,}</span>')
        combined_value.set_halign(Gtk.Align.END)
        grid.attach(combined_value, 1, row, 1, 1)

        # Additional info
        row += 1
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator3, 0, row, 2, 1)

        # Total distance
        row += 1
        distance_label = Gtk.Label()
        distance_label.set_markup('<b>Total Mouse Distance:</b>')
        distance_label.set_halign(Gtk.Align.START)
        grid.attach(distance_label, 0, row, 1, 1)

        distance_value = Gtk.Label()
        distance_value.set_markup(f'<span color="#445c3c">{distance_km:.2f} km</span>')
        distance_value.set_halign(Gtk.Align.END)
        grid.attach(distance_value, 1, row, 1, 1)

        # Days tracked
        row += 1
        days_label = Gtk.Label()
        days_label.set_markup('<b>Days Tracked:</b>')
        days_label.set_halign(Gtk.Align.START)
        grid.attach(days_label, 0, row, 1, 1)

        days_value = Gtk.Label()
        days_value.set_markup(f'<span>{total_days}</span>')
        days_value.set_halign(Gtk.Align.END)
        grid.attach(days_value, 1, row, 1, 1)

        # Add close button
        row += 1
        close_button = Gtk.Button.new_with_label('Close')
        close_button.connect('clicked', lambda w: self.close())
        close_button.set_margin_top(20)
        grid.attach(close_button, 0, row, 2, 1)

        self.grid.attach(grid, 0, 0, 1, 1)

    def close(self):
        self.hide()


if __name__ == '__main__':
    secret = SecretDialog()
    secret.run()
