#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SQLite-based Configuration for habits app
#

import os
import json
from database import Database
from config import CONFIG_DIR, PARAMS


class Configuration(object):
    """Configuration handler using SQLite database"""

    def __init__(self, use_sqlite=True):
        self.use_sqlite = use_sqlite
        self.db = Database() if use_sqlite else None
        self.params = PARAMS.copy()
        self.check()
        self.read()

    def check(self):
        """Ensure configuration directory exists"""
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, 0o700)

    def has(self, key):
        """Check if a key exists in params"""
        return key in self.params

    def get(self, key):
        """Get a value from params"""
        try:
            return self.params[key]
        except KeyError as e:
            print(e)
            self.params[key] = PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        """Set a value in params"""
        self.params[key] = value

    def reset(self):
        """Reset to default values"""
        self.params = PARAMS.copy()
        self.save()

    def set_defaults(self):
        """Set default values"""
        self.params = PARAMS.copy()
        self.save()

    def read(self):
        """Read configuration from SQLite database"""
        if not self.use_sqlite:
            return

        self.check()

        # Read stats
        stats = self.db.get_all_stats()
        if stats:
            self.params['stats'] = stats

        # Read preferences
        prefs_from_db = self.db.get_all_preferences()

        if prefs_from_db:
            # Convert string values back to proper types
            for key, value_str in prefs_from_db.items():
                # Try to convert boolean strings
                if value_str == 'True':
                    value = True
                elif value_str == 'False':
                    value = False
                # Try to convert numbers
                elif value_str.isdigit():
                    value = int(value_str)
                else:
                    # Try to parse as float
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str

                if 'preferences' not in self.params:
                    self.params['preferences'] = {}
                self.params['preferences'][key] = value

    def save(self):
        """Save configuration to SQLite database"""
        if not self.use_sqlite:
            return

        self.check()

        # Save stats
        if 'stats' in self.params:
            for date, stats in self.params['stats'].items():
                distance = stats.get('distance', 0)
                clicks = stats.get('clicks', 0)
                keys = stats.get('keys', 0)
                self.db.save_daily_stat(date, distance, clicks, keys)

        # Save preferences
        if 'preferences' in self.params:
            for key, value in self.params['preferences'].items():
                value_str = str(value)
                self.db.save_preference(key, value_str)

    def __str__(self):
        """String representation"""
        ans = ''
        for key in sorted(self.params):
            ans += '{0}: {1}\n'.format(key, self.params[key])
        return ans


# For backward compatibility: make sure the migration runs automatically
# the first time SQLite is used
if __name__ == '__main__':
    config = Configuration(use_sqlite=True)
    print("Configuration loaded from SQLite")
    print(config)
