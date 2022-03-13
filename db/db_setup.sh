#!/bin/bash

DATABASE_NAME="momo2"

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '${DATABASE_NAME}'" |  \
grep -q 1 || \
psql -U postgres -c "CREATE DATABASE ${DATABASE_NAME}"
