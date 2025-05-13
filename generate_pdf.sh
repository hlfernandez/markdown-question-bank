#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 -d <markdown_models_dir> -h <heading_file> -c <css_file>"
    exit 1
}

# Parse command-line arguments
while getopts "d:h:c:" opt; do
    case $opt in
        d) MARDOWN_MODELS_DIR="$OPTARG" ;;
        h) HEADING="$OPTARG" ;;
        c) CSS="$OPTARG" ;;
        *) usage ;;
    esac
done

# Check if all arguments are provided
if [ -z "$MARDOWN_MODELS_DIR" ] || [ -z "$HEADING" ] || [ -z "$CSS" ]; then
    usage
fi

# Main logic
for file in $(find "$MARDOWN_MODELS_DIR" -type f -name "*.md"); do
    DIR=$(dirname "$file")
    FILE=$(basename "$file")

    # Check if HEADING is a Jinja2 template
    if [[ "$HEADING" == *.jinja2 ]]; then
        # Render the Jinja2 template
        RENDERED_HEADING=$(mktemp)
        jinja2 "$HEADING" -D filename="$FILE" > "$RENDERED_HEADING"
        pandoc "$RENDERED_HEADING" "$file" --css="$CSS" --pdf-engine=weasyprint -o "$DIR/$FILE.pdf"
        rm "$RENDERED_HEADING"
    else
        # Use the HEADING file directly
        pandoc "$HEADING" "$file" --css="$CSS" --pdf-engine=weasyprint -o "$DIR/$FILE.pdf"
    fi
done
