#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View individual mouse button statistics
"""

from database import Database

def view_buttons():
    """Display mouse button statistics"""

    db = Database()

    print("=" * 60)
    print("MOUSE BUTTON TRACKER")
    print("=" * 60)

    # Get total counts for each button
    button_totals = db.get_total_mouse_buttons()

    # Button names (excluding scroll buttons 4 and 5)
    button_names = {
        1: "Left Button (MB1)",
        2: "Middle Button (MB2)",
        3: "Right Button (MB3)",
        6: "Side Button 3",
        7: "Side Button 4",
        8: "Extra Button 1",
        9: "Extra Button 2"
    }

    print("\n🖱️  Total Clicks Per Button:")
    print("-" * 60)

    if button_totals:
        for button_num in sorted(button_totals.keys()):
            button_name = button_names.get(button_num, f"Button {button_num}")
            count = button_totals[button_num]
            print(f"  {button_name:30s}: {count:,}")
    else:
        print("  No button data yet. Click some buttons!")

    # Show daily breakdown
    print("\n📅 Daily Breakdown:")
    print("-" * 60)

    all_buttons = db.get_all_mouse_buttons()
    if all_buttons:
        for date in sorted(all_buttons.keys(), reverse=True):
            print(f"\n  {date}:")
            for button_num in sorted(all_buttons[date].keys()):
                button_name = button_names.get(button_num, f"Button {button_num}")
                count = all_buttons[date][button_num]
                print(f"    {button_name:28s}: {count:,}")
    else:
        print("  No daily data available yet")

    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    view_buttons()
