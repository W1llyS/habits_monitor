#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Migration script to convert keyboard tracking from per-day to total counts
# This preserves all existing data by summing up the counts

import sqlite3
import os
from config import CONFIG_DIR

DB_FILE = os.path.join(CONFIG_DIR, 'habits.db')

def migrate_keyboard_to_total():
    """Migrate keyboard_keys table from per-day tracking to total tracking"""

    if not os.path.exists(DB_FILE):
        print("Database file not found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if old table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keyboard_keys'")
    if not cursor.fetchone():
        print("keyboard_keys table not found. Nothing to migrate.")
        conn.close()
        return

    print("Starting migration...")

    # Get current data summary
    cursor.execute("SELECT COUNT(*) FROM keyboard_keys")
    old_count = cursor.fetchone()[0]
    print(f"Found {old_count} records in old keyboard_keys table")

    # Create new table structure (without date)
    print("Creating new keyboard_keys_total table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyboard_keys_total (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT UNIQUE NOT NULL,
            count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migrate data: sum all counts per key across all dates
    print("Migrating data (summing all per-day counts)...")
    cursor.execute('''
        INSERT INTO keyboard_keys_total (key_name, count)
        SELECT key_name, SUM(count) as total
        FROM keyboard_keys
        GROUP BY key_name
    ''')

    # Verify migration
    cursor.execute("SELECT COUNT(*), SUM(count) FROM keyboard_keys_total")
    new_stats = cursor.fetchone()
    new_count = new_stats[0]
    new_total = new_stats[1]

    cursor.execute("SELECT SUM(count) FROM keyboard_keys")
    old_total = cursor.fetchone()[0]

    print(f"Migration complete:")
    print(f"  - Old table: {old_count} records, total count: {old_total}")
    print(f"  - New table: {new_count} unique keys, total count: {new_total}")

    if old_total == new_total:
        print("✓ Data verification passed - no data lost!")

        # Backup old table
        print("Backing up old table to keyboard_keys_old...")
        cursor.execute("DROP TABLE IF EXISTS keyboard_keys_old")
        cursor.execute("ALTER TABLE keyboard_keys RENAME TO keyboard_keys_old")

        # Rename new table to keyboard_keys
        print("Renaming keyboard_keys_total to keyboard_keys...")
        cursor.execute("ALTER TABLE keyboard_keys_total RENAME TO keyboard_keys")

        print("✓ Migration successful! Old table backed up as keyboard_keys_old")
        print("  (You can manually drop keyboard_keys_old later if everything works)")
    else:
        print("✗ Data verification failed! Counts don't match.")
        print("  Rolling back... (new table not renamed)")
        cursor.execute("DROP TABLE keyboard_keys_total")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_keyboard_to_total()
