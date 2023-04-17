#!/bin/bash

rm -rf var/
mkdir var
sqlite3 var/db.sqlite3 < db/schema.sql