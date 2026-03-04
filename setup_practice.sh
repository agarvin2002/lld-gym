#!/bin/bash
# Run this once after cloning: bash setup_practice.sh
# It tells git to ignore local changes to all starter.py files so your
# practice work never shows up in git status or gets accidentally committed.

git ls-files "**/starter.py" "starter.py" | while read -r file; do
    git update-index --skip-worktree "$file"
    echo "  skipping: $file"
done

echo ""
echo "Done. Your edits to starter.py files will not be tracked by git."
echo "To undo this for a specific file: git update-index --no-skip-worktree <path>"
