#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 -d <markdown_models_dir> -h <heading_file> -c <css_file> [-k]"
    echo ""
    echo "Options:"
    echo "  -d <markdown_models_dir>  Directory containing the Markdown files to process."
    echo "  -h <heading_file>         File to be prepended to each Markdown file. If it's a .jinja2 file, it will be rendered with 'filename' variable."
    echo "  -c <css_file>             CSS file to style the PDF output."
    echo "  -k                        Keep the intermediate HTML file."
    exit 1
}

# Initialize KEEP_HTML flag
KEEP_HTML=false

# Parse command-line arguments
while getopts "d:h:c:k" opt; do
    case $opt in
        d) MARDOWN_MODELS_DIR="$OPTARG" ;;
        h) HEADING="$OPTARG" ;;
        c) CSS="$OPTARG" ;;
        k) KEEP_HTML=true ;;
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
    PDF_FILE="$DIR/$(basename "$FILE" .md).pdf"
    HTML_FILE="$DIR/$(basename "$FILE" .md).html"

    # Check if HEADING is a Jinja2 template
    if [[ "$HEADING" == *.jinja2 ]]; then
        # Render the Jinja2 template
        RENDERED_HEADING=$(mktemp /tmp/rendered_heading.XXXXXX)
        jinja2 "$HEADING" -D filename="$FILE" > "$RENDERED_HEADING"
        HEADING=$RENDERED_HEADING
    fi
    pandoc "$HEADING" "$file" --quiet --css="$CSS" --pdf-engine=weasyprint -o "$PDF_FILE"

    # Keep the html files if requested (in fact, we generate html again with pandoc and embed the CSS to be more portable)
    if [ "$KEEP_HTML" = true ]; then
        pandoc "$HEADING" "$file" --quiet --css="$CSS" --standalone -o "${HTML_FILE}.tmp"

        # Embed the CSS into the HTML file, replacing the link tag with the CSS content inside a style tag
        awk -v cssfile="$CSS" '
        /<link rel="stylesheet" href=.*\/>/ {
            print "<style>";
            while ((getline line < cssfile) > 0) print line;
            close(cssfile);
            print "</style>";
            next;
        }
        { print }
        ' "${HTML_FILE}.tmp" > "${HTML_FILE}"
        rm "${HTML_FILE}.tmp"
    fi
done
