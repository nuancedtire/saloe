#!/bin/bash

# Get all guideline URLs from sitemap
echo "Fetching RCEM guideline pages..."
curl -sL "https://rcem.ac.uk/post-sitemap.xml" | grep -oP 'https://rcem\.ac\.uk/[^<]*guideline[^<]*' | sort -u > /tmp/rcem_pages.txt
curl -sL "https://rcem.ac.uk/post-sitemap.xml" | grep -oP 'https://rcem\.ac\.uk/best-practice/[^<]*' | sort -u >> /tmp/rcem_pages.txt
curl -sL "https://rcem.ac.uk/post-sitemap.xml" | grep -oP 'https://rcem\.ac\.uk/clinical-guidelines/[^<]*' | sort -u >> /tmp/rcem_pages.txt

# Remove duplicates
sort -u /tmp/rcem_pages.txt > /tmp/rcem_pages_unique.txt
mv /tmp/rcem_pages_unique.txt /tmp/rcem_pages.txt

echo "Found $(wc -l < /tmp/rcem_pages.txt) guideline pages"

# For each page, fetch and extract PDF links
mkdir -p /home/exedev/eolas-guidelines/RCEM

while IFS= read -r url; do
    echo "Checking: $url"
    pdfs=$(curl -sL "$url" | grep -oP 'https://rcem\.ac\.uk/wp-content/uploads/[^"]*\.pdf' | sort -u)
    for pdf in $pdfs; do
        filename=$(basename "$pdf")
        if [ ! -f "/home/exedev/eolas-guidelines/RCEM/$filename" ]; then
            echo "  Downloading: $filename"
            curl -sL -o "/home/exedev/eolas-guidelines/RCEM/$filename" "$pdf"
        else
            echo "  Already exists: $filename"
        fi
    done
done < /tmp/rcem_pages.txt

echo "Done! Downloaded PDFs:"
ls -la /home/exedev/eolas-guidelines/RCEM/
