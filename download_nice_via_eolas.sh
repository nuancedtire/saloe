#!/bin/bash
# Download NICE guidelines via Eolas API

TOKEN="$1"
OUTPUT_DIR="${2:-NICE}"
IDS_FILE="${3:-nice_ids.txt}"

if [ -z "$TOKEN" ]; then
  echo "Usage: $0 <bearer_token> [output_dir] [ids_file]"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Read IDs from file (skip comments and empty lines)
while IFS= read -r id; do
  # Skip comments and empty lines
  [[ "$id" =~ ^#.*$ || -z "$id" ]] && continue
  
  outfile="$OUTPUT_DIR/${id}.pdf"
  
  # Skip if already downloaded
  if [ -f "$outfile" ] && [ -s "$outfile" ]; then
    echo "Skipping $id (already exists)"
    continue
  fi
  
  echo -n "Fetching $id... "
  
  # Get the S3 URL from Eolas API
  response=$(curl -s -H "Authorization: Bearer $TOKEN" "https://api.eolas.click/nice/v1/guidelines/$id")
  
  # Check for error
  if echo "$response" | grep -q '"message"'; then
    echo "FAILED ($(echo "$response" | jq -r '.message' 2>/dev/null || echo 'unknown error'))"
    continue
  fi
  
  # Extract URL
  url=$(echo "$response" | jq -r '.url' 2>/dev/null)
  
  if [ -z "$url" ] || [ "$url" == "null" ]; then
    echo "FAILED (no URL in response)"
    continue
  fi
  
  # Download the PDF
  if curl -sL -o "$outfile" "$url"; then
    # Verify it's a PDF
    if file "$outfile" | grep -q "PDF"; then
      size=$(stat -c%s "$outfile")
      echo "OK ($size bytes)"
    else
      echo "FAILED (not a valid PDF)"
      rm -f "$outfile"
    fi
  else
    echo "FAILED (download error)"
    rm -f "$outfile"
  fi
  
  # Small delay to be nice to the API
  sleep 0.5
done < "$IDS_FILE"

echo ""
echo "Download complete. Files in $OUTPUT_DIR:"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null | wc -l
echo "PDFs downloaded"
