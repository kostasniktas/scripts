#!/bin/sh

KEY_LOCATION=/home/kniktas/Documents/SOMEKEY
COMMANDARGS="$*"
TMPSOCKET="/tmp/$(basename $0).$$.tmp"

ssh-agent -a $TMPSOCKET sh -c "SSH_AUTH_SOCK=$TMPSOCKET ssh-add $KEY_LOCATION; SSH_AUTH_SOCK=$TMPSOCKET /usr/bin/ssh $COMMANDARGS"


