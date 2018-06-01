#!/bin/bash

clear

while true; do
  ROWS=$(tput lines)
  COLS=$(tput cols)
  UNITS=$(expr $COLS / 5)
  WIDTH=$(expr $UNITS \* 5)
  HEIGHT=$(expr $ROWS - 5 )

  COUNT=$(expr $UNITS \* $HEIGHT)
  DATA=$(dd if=/dev/urandom bs=2 count=$COUNT 2> /dev/null | od -x | awk '{$1=""; print $0}' | tr -d '\n' | sed 's/^ *//')

  printf '\033[;H'  # move cursor to the top

  for i in {1..8}; do
    if [ "${ROWS}" != $(tput lines) ]; then
      clear
      break
    fi
    if [ "${COLS}" != $(tput cols) ]; then
      clear
      break
    fi

    BYTE_MATCH=$(od -vN "1" -An -tx1 /dev/urandom | tr -d ' \n')

    for j in {1..12}; do
      BYTE_MATCH="${BYTE_MATCH}|$(od -vN "1" -An -tx1 /dev/urandom | tr -d ' \n')"
    done

    printf '\033[;H'  # move cursor to the top
    
    #echo $DATA | shasum
    #echo $BYTE_MATCH
    #echo r $ROWS     c  $COLS     u $UNITS     w $WIDTH    h  $HEIGHT     c $COUNT

    fold -sw${WIDTH} <(echo $DATA) | tail -n +1 | grep --color=auto -E "(${BYTE_MATCH})|$"
    sleep 0.3
  done

done
