#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: command FILE"
  exit 1
fi

for i in `cat $1`; do echo "$RANDOM $i"; done | sort | sed -r 's/^[0-9]+ //'

