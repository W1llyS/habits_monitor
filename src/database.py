#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from config import CONFIG_DIR

# Database file location
DB_FILE = os.path.join(CONFIG_DIR, 'habits.db')


class Database:
    """Handle SQLite database operations for habits tracking"""

    def __init__(self):
        self.db_file = DB_FILE
        self.connection = None
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database"""
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, 0o700)

        self.connection = sqlite3.connect(self.db_file)
        self.connection.row_factory = sqlite3.Row  # Access columns by name
        return self.connection

    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()

        # Table for daily statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                distance INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                keys INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table for preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
        ''')

        # Table for individual mouse button tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mouse_buttons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                button INTEGER NOT NULL,
                count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, button)
            )
        ''')

        # Table for individual keyboard key tracking (total counts, not per-day)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keyboard_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_daily_stat(self, date, distance=0, clicks=0, keys=0):
        """Save or update daily statistics"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO daily_stats (date, distance, clicks, keys)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                distance = ?,
                clicks = ?,
                keys = ?,
                updated_at = CURRENT_TIMESTAMP
        ''', (date, distance, clicks, keys, distance, clicks, keys))

        conn.commit()
        conn.close()

    def get_daily_stat(self, date):
        """Get statistics for a specific date"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date, distance, clicks, keys
            FROM daily_stats
            WHERE date = ?
        ''', (date,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'date': row['date'],
                'distance': row['distance'],
                'clics': row['clicks'],  # Map to 'clics' for app compatibility
                'keys': row['keys']
            }
        return None

    def get_all_stats(self):
        """Get all statistics organized by date"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date, distance, clicks, keys
            FROM daily_stats
            ORDER BY date DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        stats = {}
        for row in rows:
            stats[row['date']] = {
                'distance': row['distance'],
                'clics': row['clicks'],  # Map to 'clics' for app compatibility
                'keys': row['keys']
            }

        return stats

    def get_stats_by_date_range(self, start_date, end_date):
        """Get statistics within a date range (inclusive)

        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'

        Returns:
            Dictionary of stats organized by date
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date, distance, clicks, keys
            FROM daily_stats
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', (start_date, end_date))

        rows = cursor.fetchall()
        conn.close()

        stats = {}
        for row in rows:
            stats[row['date']] = {
                'distance': row['distance'],
                'clics': row['clicks'],  # Map to 'clics' for app compatibility
                'keys': row['keys']
            }

        return stats

    def save_preference(self, key, value):
        """Save a preference setting"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO preferences (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = ?
        ''', (key, value, value))

        conn.commit()
        conn.close()

    def get_preference(self, key, default=None):
        """Get a preference value"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT value FROM preferences WHERE key = ?
        ''', (key,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return row['value']
        return default

    def get_all_preferences(self):
        """Get all preferences as a dictionary"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT key, value FROM preferences')
        rows = cursor.fetchall()
        conn.close()

        prefs = {}
        for row in rows:
            prefs[row['key']] = row['value']

        return prefs

    def save_mouse_button(self, date, button, count):
        """Save or update mouse button click count for a specific date and button"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO mouse_buttons (date, button, count)
            VALUES (?, ?, ?)
            ON CONFLICT(date, button) DO UPDATE SET
                count = ?,
                updated_at = CURRENT_TIMESTAMP
        ''', (date, button, count, count))

        conn.commit()
        conn.close()

    def get_mouse_buttons(self, date):
        """Get all mouse button counts for a specific date (excluding scroll buttons)"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT button, count
            FROM mouse_buttons
            WHERE date = ? AND button NOT IN (4, 5)
            ORDER BY button
        ''', (date,))

        rows = cursor.fetchall()
        conn.close()

        buttons = {}
        for row in rows:
            buttons[row['button']] = row['count']

        return buttons

    def get_all_mouse_buttons(self):
        """Get all mouse button statistics across all dates (excluding scroll buttons)"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date, button, count
            FROM mouse_buttons
            WHERE button NOT IN (4, 5)
            ORDER BY date DESC, button
        ''')

        rows = cursor.fetchall()
        conn.close()

        result = {}
        for row in rows:
            date = row['date']
            if date not in result:
                result[date] = {}
            result[date][row['button']] = row['count']

        return result

    def get_total_mouse_buttons(self):
        """Get total counts for each mouse button across all dates (excluding scroll buttons)"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT button, SUM(count) as total
            FROM mouse_buttons
            WHERE button NOT IN (4, 5)
            GROUP BY button
            ORDER BY button
        ''')

        rows = cursor.fetchall()
        conn.close()

        totals = {}
        for row in rows:
            totals[row['button']] = row['total']

        return totals

    def save_keyboard_key(self, key_name, count):
        """Save or update keyboard key press count (increments existing total)"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO keyboard_keys (key_name, count)
            VALUES (?, ?)
            ON CONFLICT(key_name) DO UPDATE SET
                count = count + ?,
                updated_at = CURRENT_TIMESTAMP
        ''', (key_name, count, count))

        conn.commit()
        conn.close()

    def get_keyboard_keys(self):
        """Get all keyboard key counts (total counts, not per-day)"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT key_name, count
            FROM keyboard_keys
            ORDER BY count DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        keys = {}
        for row in rows:
            keys[row['key_name']] = row['count']

        return keys

    def get_all_keyboard_keys(self):
        """Get all keyboard key statistics (no longer organized by date)"""
        # For backward compatibility, just return the keyboard keys
        return self.get_keyboard_keys()

    def get_total_keyboard_keys(self):
        """Get total counts for each keyboard key (already stored as totals)"""
        # Since we now store totals directly, just return them
        return self.get_keyboard_keys()


# Example usage and testing
if __name__ == '__main__':
    # Test the database
    db = Database()

    # Save some test data
    db.save_daily_stat('2025-10-06', distance=5000, clicks=150, keys=1200)
    db.save_daily_stat('2025-10-05', distance=4500, clicks=120, keys=1000)

    # Retrieve data
    print("Stats for 2025-10-06:")
    print(db.get_daily_stat('2025-10-06'))

    print("\nAll stats:")
    print(db.get_all_stats())

    # Save preferences
    db.save_preference('theme-light', 'True')
    db.save_preference('distance-color', '#445c3c')

    # Get preferences
    print("\nPreferences:")
    print(db.get_all_preferences())
