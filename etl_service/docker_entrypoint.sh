#!/bin/sh

# Init database
echo "Create database"
python create_db.py

# Run crawler
echo "Run crawler"
python crawler.py