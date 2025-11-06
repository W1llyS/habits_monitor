#!/bin/bash

echo "Testing Habits tracking..."
echo ""
echo "Before test:"
python3 src/view_db.py | grep "2025-10-06" -A 3

echo ""
echo "Click your mouse a few times and press some keys..."
echo "Waiting 10 seconds for you to test..."
sleep 10

echo ""
echo "After test:"
python3 src/view_db.py | grep "2025-10-06" -A 3
