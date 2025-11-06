#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Clean up test data from database
"""

from database import Database

def clean_test_data():
    """Remove the test entry from 2025-10-05"""

    db = Database()
    conn = db.connect()
    cursor = conn.cursor()

    # Delete the test data
    cursor.execute("DELETE FROM daily_stats WHERE date = ?", ('2025-10-05',))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    print(f"✅ Removed {deleted} test record(s)")
    print("\nCurrent data:")

    # Show remaining data
    all_stats = db.get_all_stats()
    for date, stats in sorted(all_stats.items()):
        print(f"  {date}: distance={stats['distance']}, clicks={stats['clicks']}, keys={stats['keys']}")

if __name__ == '__main__':
    clean_test_data()
