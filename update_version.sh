#!/bin/bash
# update_version.sh
# Usage: ./update_version.sh <new_version>
# Updates version in pyproject.toml and src/markdown_question_bank/__init__.py

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <new_version>"
    exit 1
fi

NEW_VERSION="$1"

# Update pyproject.toml
sed -i -E "s/^version = \"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "Updated pyproject.toml to version $NEW_VERSION"

# Update __init__.py
INIT_FILE="src/markdown_question_bank/__init__.py"
if grep -q "^__version__ =" "$INIT_FILE"; then
    sed -i -E "s/^__version__ = \"[0-9]+\.[0-9]+\.[0-9]+\"/__version__ = \"$NEW_VERSION\"/" "$INIT_FILE"
else
    echo "__version__ = \"$NEW_VERSION\"" >> "$INIT_FILE"
fi

echo "Updated $INIT_FILE to version $NEW_VERSION"
