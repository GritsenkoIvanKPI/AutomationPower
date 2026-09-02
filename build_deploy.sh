#!/bin/bash
# Assembles deploy/ — exactly what goes on the hosting, nothing else.
# Source photos, build scripts and the rembg venv stay out of it.
set -e
rm -rf deploy && mkdir -p deploy

# pages
cp index.html 21700.html high-density.html ev-packs.html deploy/

# only the assets the pages actually reference (see /tmp/needed.txt generation in the brief)
while read -r f; do mkdir -p "deploy/$(dirname "$f")"; cp "$f" "deploy/$f"; done < /tmp/needed.txt

# form endpoint + template for the file the client creates on the server
cp send-form.php config.example.php deploy/

# discovery
cp robots.txt sitemap.xml llms.txt deploy/

echo "deploy/ assembled:"
echo "  files: $(find deploy -type f | wc -l | tr -d ' ')"
echo "  size:  $(du -sh deploy | cut -f1)"
