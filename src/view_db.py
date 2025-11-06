#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple script to view SQLite database contents
"""

from database import Database
import json

def view_database():
    """Display all data from the SQLite database"""

    db = Database()

    print("=" * 60)
    print("HABITS DATABASE VIEWER")
    print("=" * 60)

    # Show statistics
    print("\n📊 DAILY STATISTICS:")
    print("-" * 60)

    stats = db.get_all_stats()
    if stats:
        for date in sorted(stats.keys(), reverse=True):
            stat = stats[date]
            print(f"\n  Date: {date}")
            print(f"    Distance: {stat['distance']:,} pixels")
            print(f"    Clicks:   {stat['clics']:,}")
            print(f"    Keys:     {stat['keys']:,}")
    else:
        print("  No statistics found")

    # Show preferences
    print("\n⚙️  PREFERENCES:")
    print("-" * 60)

    prefs = db.get_all_preferences()
    if prefs:
        for key in sorted(prefs.keys()):
            print(f"  {key:20s}: {prefs[key]}")
    else:
        print("  No preferences found")

    print("\n" + "=" * 60)
    print(f"Database location: {db.db_file}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    view_database()
