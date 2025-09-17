#!/bin/bash


# Written with inspiration from https://quarters.captaintouch.com/blog/posts/2025-09-13-text-files-%3E-complex-tools:-a-minimalist-snippet-manager.html

#SNIPPETS_FOLDER="$(dirname "${BASH_SOURCE[0]}")/snippets"
SNIPPETS_FOLDER="$HOME/snippets"


if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename $0) SNIPPET_LOCATION"
  echo "    Assuming stdin as source"
  exit 1
fi


SNIPPET_LOCATION=$1

DIRS="$(dirname "$SNIPPET_LOCATION")"
SNIPPET="$(basename "$SNIPPET_LOCATION")"

cd $SNIPPETS_FOLDER
if [[ "$DIRS" != "." ]]; then
  mkdir -p $DIRS
fi

if [[ -f $SNIPPET_LOCATION ]]; then
  echo $SNIPPET_LOCATION exists. Maybe delete first
  exit 1
fi

echo "To $SNIPPET_LOCATION"
cp /dev/stdin $SNIPPET_LOCATION

