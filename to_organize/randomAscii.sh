#!/bin/sh

if [ $# -lt 1 ]; then
  echo Usage: $(basename $0) SIZEINBYTES
  exit 1
fi

tr -dc A-Za-z0-9\\n < /dev/urandom | head -c $1

