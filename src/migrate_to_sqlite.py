#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migration script to convert JSON configuration to SQLite database
"""

import json
import codecs
import os
from database import Database
from config import CONFIG_FILE

def migrate_json_to_sqlite():
    """Migrate existing JSON data to SQLite database"""

    # Check if JSON config exists
    if not os.path.exists(CONFIG_FILE):
        print("No JSON config file found. Nothing to migrate.")
        return

    # Read JSON data
    print(f"Reading data from: {CONFIG_FILE}")
    with codecs.open(CONFIG_FILE, 'r', 'utf-8') as f:
        data = json.loads(f.read())

    # Initialize database
    db = Database()

    # Migrate stats
    if 'stats' in data:
        print("\nMigrating statistics...")
        for date, stats in data['stats'].items():
            distance = stats.get('distance', 0)
            clicks = stats.get('clicks', 0)
            keys = stats.get('keys', 0)

            db.save_daily_stat(date, distance, clicks, keys)
            print(f"  Migrated {date}: distance={distance}, clicks={clicks}, keys={keys}")

    # Migrate preferences
    if 'preferences' in data:
        print("\nMigrating preferences...")
        for key, value in data['preferences'].items():
            # Convert value to string for storage
            value_str = str(value)
            db.save_preference(key, value_str)
            print(f"  Migrated {key}: {value_str}")

    print("\n✅ Migration completed successfully!")
    print(f"Database file: {db.db_file}")

    # Show summary
    all_stats = db.get_all_stats()
    all_prefs = db.get_all_preferences()

    print(f"\nSummary:")
    print(f"  - {len(all_stats)} days of statistics migrated")
    print(f"  - {len(all_prefs)} preferences migrated")

    # Backup original JSON file
    backup_file = CONFIG_FILE + '.backup'
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy2(CONFIG_FILE, backup_file)
        print(f"\n📋 Original JSON backed up to: {backup_file}")


if __name__ == '__main__':
    migrate_json_to_sqlite()
