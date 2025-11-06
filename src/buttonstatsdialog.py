#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Button Statistics Dialog - Shows individual mouse button totals
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


class ButtonStatsDialog(BaseDialog):
    """Dialog to show individual mouse button statistics"""

    def __init__(self):
        BaseDialog.__init__(self, 'Mouse Button Statistics', None,
                            ok_button=False, cancel_button=False,
                            modal=False)
        self.set_size_request(500, 400)

    def init_ui(self):
        BaseDialog.init_ui(self)

        # Get button totals from database
        db = Database()
        button_totals = db.get_total_mouse_buttons()

        # Create grid for displaying stats
        grid = Gtk.Grid()
        grid.set_row_spacing(12)
        grid.set_column_spacing(20)
        grid.set_margin_start(30)
        grid.set_margin_end(30)
        grid.set_margin_top(30)
        grid.set_margin_bottom(30)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="xx-large" weight="bold">🖱️  Mouse Button Statistics</span>')
        grid.attach(title_label, 0, 0, 2, 1)

        # Separator
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator1, 0, 1, 2, 1)

        # Info text
        row = 2
        info_label = Gtk.Label()
        info_label.set_markup('<span size="small" style="italic">Total clicks for each mouse button across all days</span>')
        info_label.set_halign(Gtk.Align.START)
        grid.attach(info_label, 0, row, 2, 1)

        # Button names mapping (excluding scroll buttons 4 and 5)
        button_names = {
            1: "🖱️  Left Button (MB1)",
            2: "🖱️  Middle Button (MB2)",
            3: "🖱️  Right Button (MB3)",
            6: "◀️  Side Button 3",
            7: "▶️  Side Button 4",
            8: "⬆️  Extra Button 1",
            9: "⬇️  Extra Button 2"
        }

        # Calculate total
        total_all_buttons = sum(button_totals.values()) if button_totals else 0

        # Display total first
        row += 1
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator2, 0, row, 2, 1)

        row += 1
        total_label = Gtk.Label()
        total_label.set_markup('<b>Total All Buttons:</b>')
        total_label.set_halign(Gtk.Align.START)
        grid.attach(total_label, 0, row, 1, 1)

        total_value = Gtk.Label()
        total_value.set_markup(f'<span size="x-large" weight="bold" color="#bd574e">{total_all_buttons:,}</span>')
        total_value.set_halign(Gtk.Align.END)
        grid.attach(total_value, 1, row, 1, 1)

        row += 1
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator3, 0, row, 2, 1)

        # Display each button's count
        if button_totals:
            for button_num in sorted(button_totals.keys()):
                row += 1
                button_name = button_names.get(button_num, f"🖱️  Button {button_num}")
                count = button_totals[button_num]

                btn_label = Gtk.Label()
                btn_label.set_markup(f'<b>{button_name}:</b>')
                btn_label.set_halign(Gtk.Align.START)
                grid.attach(btn_label, 0, row, 1, 1)

                btn_value = Gtk.Label()
                btn_value.set_markup(f'<span size="large" color="#bd574e">{count:,}</span>')
                btn_value.set_halign(Gtk.Align.END)
                grid.attach(btn_value, 1, row, 1, 1)
        else:
            row += 1
            no_data_label = Gtk.Label()
            no_data_label.set_markup('<span style="italic">No button data yet. Start clicking!</span>')
            no_data_label.set_halign(Gtk.Align.CENTER)
            grid.attach(no_data_label, 0, row, 2, 1)

        # Add close button
        row += 1
        separator4 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator4, 0, row, 2, 1)

        row += 1
        close_button = Gtk.Button.new_with_label('Close')
        close_button.connect('clicked', lambda w: self.close())
        close_button.set_margin_top(10)
        grid.attach(close_button, 0, row, 2, 1)

        self.grid.attach(grid, 0, 0, 1, 1)

    def close(self):
        self.hide()


if __name__ == '__main__':
    dialog = ButtonStatsDialog()
    dialog.run()
