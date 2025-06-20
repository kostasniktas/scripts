#!/bin/bash

printf '' | fzf --print-query \
  --preview "jq -C {q} '$1' 2>&1" \
  --preview-window=up:80%
