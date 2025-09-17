#!/bin/bash

# Borrowed from https://quarters.captaintouch.com/blog/posts/2025-09-13-text-files-%3E-complex-tools:-a-minimalist-snippet-manager.html

# Dependencies
#
# -fzf
# -a ~/snippets folder
#

#SNIPPETS_FOLDER="$(dirname "${BASH_SOURCE[0]}")/snippets"
SNIPPETS_FOLDER="$HOME/snippets"

copy_to_clipboard() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo $OSTYPE
        if [[ "$OSTYPE" == "darwin"* ]]; then
          cat "$file" | pbcopy
        else
          cat "$file" | xclip -selection clipboard
        fi
        echo "Contents of '$file' copied to clipboard."
      	#cat "$file"
    else
        echo "Error: File '$file' not found."
    fi
}

cd "$SNIPPETS_FOLDER" || exit 1
selected_file=$(fzf --prompt="Select a snippet: ")
if [[ -z "$selected_file" ]]; then
    echo "No snippet selected. Exiting."
    exit 0
fi

copy_to_clipboard "$selected_file"
