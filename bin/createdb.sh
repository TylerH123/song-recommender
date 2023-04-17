#!/bin/bash

rm -rf var/db.sqlite3
sqlite3 var/db.sqlite3 < db/schema.sql