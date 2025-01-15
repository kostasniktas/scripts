#!/bin/bash

# REQUIREMENTS
#   macOS

function usage {
  echo "$(basename $0) VOLUME" >&2
  echo "     VOLUME is a float from 0 to 10" >&2
  echo "     Special VOLUME values" >&2
  echo "        HEADPHONE|headphone = smol volum for your sony headphones (0.1)" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

case "$1" in
  HEADPHONE | headphone)
    VOLUME=0.1
    ;;
  *)
    VOLUME=$1
    ;;
esac

# (( $(echo "$num1 > $num2" |bc -l) ))
if (( $(echo "$VOLUME < 0.0" | bc -l ) )) || (( $(echo "$VOLUME > 10.0" | bc -l ) )); then
  usage
  echo "Invalid volume number: $VOLUME" >&2
  exit 1
fi

echo "Setting $VOLUME"
exit 0
osascript -e "set volume output volume $VOLUME"
