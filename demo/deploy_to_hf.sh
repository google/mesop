#!/bin/bash

set -e

error_handler() {
    echo "Error: An error occurred. Exiting script."
    exit 1
}

# Set up error handling
trap error_handler ERR

if [ $# -eq 0 ]; then
    echo "Error: Please provide a destination path as an argument."
    exit 1
fi

DEST_PATH="$1"

if [ ! -d "$DEST_PATH" ]; then
    echo "Destination path does not exist. Creating it now."
    mkdir -p "$DEST_PATH"
fi

# Get the path of this script which is the demo dir.
DEMO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cp -R "$DEMO_DIR/" "$DEST_PATH"
echo "Demo files have been copied to $DEST_PATH"

cd "$DEST_PATH"
echo "Changed directory to $DEST_PATH"

echo "Updating allowed iframe parents to include hugging face spaces site..."
# Find all .py files and update the allowed_iframe_parents list
find . -name "*.py" -type f | while read -r file; do
    # Use sed with -i.bak so it woroks on MacOs
    sed -i.bak 's/allowed_iframe_parents=\["https:\/\/google\.github\.io"\]/allowed_iframe_parents=["https:\/\/google.github.io", "https:\/\/huggingface.co"]/' "$file"
    # Remove the backup file created by sed
    rm "${file}.bak"
done
echo "Update complete."

git init

git add .

git commit -m "Commit"

# The hf remote may already exist if the script has been run
# on this dest directory before.
git remote add hf https://huggingface.co/spaces/wwwillchen/mesop || true

git push hf --force

echo "Pushed to: https://huggingface.co/spaces/wwwillchen/mesop. Check the logs to see that it's deployed correctly."
