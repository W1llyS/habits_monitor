#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Date Range Selector Dialog for habits app
#

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from datetime import datetime, timedelta
from basedialog import BaseDialog
from config import _


class DateRangeDialog(BaseDialog):
    """Dialog for configuring statistics date range settings"""

    def __init__(self, parent=None):
        # Load current preference BEFORE calling BaseDialog.__init__
        # because BaseDialog calls init_ui() which needs self.selected_range
        from configurator import Configuration
        configuration = Configuration()
        preferences = configuration.get('preferences')
        self.selected_range = preferences.get('stats-date-range', 14)  # Default to 14 days
        self.custom_start_date = None
        self.custom_end_date = None

        BaseDialog.__init__(
            self,
            _('Statistics Settings'),
            parent,
            ok_button=True,
            cancel_button=True
        )

    def init_ui(self):
        BaseDialog.init_ui(self)

        # Create button group for quick selections
        label = Gtk.Label(label=_('Default time range for statistics:'))
        label.set_halign(Gtk.Align.START)
        self.grid.attach(label, 0, 0, 2, 1)

        # Radio buttons for quick date range selection
        self.radio_14 = Gtk.RadioButton.new_with_label_from_widget(None, _('Last 14 days'))
        self.radio_14.set_active(self.selected_range == 14)
        self.radio_14.connect('toggled', self.on_quick_select, 14)
        self.grid.attach(self.radio_14, 0, 1, 2, 1)

        self.radio_30 = Gtk.RadioButton.new_with_label_from_widget(self.radio_14, _('Last 30 days'))
        self.radio_30.set_active(self.selected_range == 30)
        self.radio_30.connect('toggled', self.on_quick_select, 30)
        self.grid.attach(self.radio_30, 0, 2, 2, 1)

        self.radio_90 = Gtk.RadioButton.new_with_label_from_widget(self.radio_14, _('Last 90 days'))
        self.radio_90.set_active(self.selected_range == 90)
        self.radio_90.connect('toggled', self.on_quick_select, 90)
        self.grid.attach(self.radio_90, 0, 3, 2, 1)

        self.radio_all = Gtk.RadioButton.new_with_label_from_widget(self.radio_14, _('All time'))
        self.radio_all.set_active(self.selected_range == -1)
        self.radio_all.connect('toggled', self.on_quick_select, -1)
        self.grid.attach(self.radio_all, 0, 4, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(separator, 0, 5, 2, 1)

        # Custom date range section
        self.radio_custom = Gtk.RadioButton.new_with_label_from_widget(self.radio_14, _('Custom range'))
        self.radio_custom.set_active(self.selected_range == 0)
        self.radio_custom.connect('toggled', self.on_custom_toggled)
        self.grid.attach(self.radio_custom, 0, 6, 2, 1)

        # Start date
        label_start = Gtk.Label(label=_('Start date:'))
        label_start.set_halign(Gtk.Align.START)
        self.grid.attach(label_start, 0, 7, 1, 1)

        self.calendar_start = Gtk.Calendar()
        self.calendar_start.set_sensitive(False)
        self.grid.attach(self.calendar_start, 0, 8, 2, 1)

        # End date
        label_end = Gtk.Label(label=_('End date:'))
        label_end.set_halign(Gtk.Align.START)
        self.grid.attach(label_end, 0, 9, 1, 1)

        self.calendar_end = Gtk.Calendar()
        self.calendar_end.set_sensitive(False)
        # Set end date to today
        today = datetime.now()
        self.calendar_end.select_month(today.month - 1, today.year)
        self.calendar_end.select_day(today.day)
        self.grid.attach(self.calendar_end, 0, 10, 2, 1)

        # Set start date to 14 days ago by default
        start_date = today - timedelta(days=14)
        self.calendar_start.select_month(start_date.month - 1, start_date.year)
        self.calendar_start.select_day(start_date.day)

    def on_quick_select(self, button, days):
        """Handle quick selection button toggle"""
        if button.get_active():
            self.selected_range = days
            self.calendar_start.set_sensitive(False)
            self.calendar_end.set_sensitive(False)

    def on_custom_toggled(self, button):
        """Handle custom range radio button toggle"""
        if button.get_active():
            self.selected_range = 0  # Custom range indicator
            self.calendar_start.set_sensitive(True)
            self.calendar_end.set_sensitive(True)

    def get_selected_range(self):
        """Get the selected date range preference

        Returns:
            int: Number of days (-1 for all time, 0 for custom)
            tuple: (start_date, end_date) if custom range selected
        """
        if self.selected_range == 0:
            # Custom range - return the dates
            start_year, start_month, start_day = self.calendar_start.get_date()
            end_year, end_month, end_day = self.calendar_end.get_date()

            start_date = datetime(start_year, start_month + 1, start_day).date()
            end_date = datetime(end_year, end_month + 1, end_day).date()

            # Ensure start is before end
            if start_date > end_date:
                start_date, end_date = end_date, start_date

            return 0, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        else:
            return self.selected_range, None

    def save_preference(self):
        """Save the selected date range preference to database"""
        from configurator import Configuration
        configuration = Configuration()
        preferences = configuration.get('preferences')

        # For custom range, we save 0 and also save the custom dates
        if self.selected_range == 0:
            preferences['stats-date-range'] = 0
            selected_range, dates = self.get_selected_range()
            if dates:
                preferences['stats-custom-start'] = dates[0]
                preferences['stats-custom-end'] = dates[1]
        else:
            preferences['stats-date-range'] = self.selected_range
            # Clear custom dates when using preset
            if 'stats-custom-start' in preferences:
                del preferences['stats-custom-start']
            if 'stats-custom-end' in preferences:
                del preferences['stats-custom-end']

        configuration.set('preferences', preferences)
        configuration.save()


if __name__ == '__main__':
    dialog = DateRangeDialog()
    response = dialog.run()
    if response == Gtk.ResponseType.ACCEPT:
        selected = dialog.get_selected_range()
        if selected == -1:
            print("Selected: All time")
        else:
            print(f"Selected: Last {selected} days")
        dialog.save_preference()
    dialog.destroy()
