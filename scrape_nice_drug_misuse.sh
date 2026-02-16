#!/bin/bash

# NICE Drug Misuse Guidelines
NICE_DIR="/home/exedev/eolas-guidelines/NICE"
mkdir -p "$NICE_DIR"

# List of drug misuse related guidelines
declare -A GUIDELINES=(
    ["QS165"]="drug-misuse-prevention"
    ["NG64"]="drug-misuse-prevention-targeted-interventions"
    ["CG51"]="drug-misuse-in-over-16s-psychosocial-interventions"
    ["CG52"]="drug-misuse-in-over-16s-opioid-detoxification"
)

for code in "${!GUIDELINES[@]}"; do
    name="${GUIDELINES[$code]}"
    echo "Downloading $code - $name..."
    
    # Try to get the PDF link from the guidance page
    pdf_url=$(curl -sL "https://www.nice.org.uk/guidance/$code" | grep -oP 'https://www\.nice\.org\.uk/guidance/[^"]*\.pdf[^"]*' | head -1)
    
    if [ -n "$pdf_url" ]; then
        # Clean URL
        pdf_url=$(echo "$pdf_url" | sed 's/&amp;/\&/g')
        echo "  Found: $pdf_url"
        curl -sL -o "$NICE_DIR/${code}_${name}.pdf" "$pdf_url"
        echo "  Downloaded: ${code}_${name}.pdf"
    else
        # Try alternative URL pattern
        pdf_url="https://www.nice.org.uk/guidance/$code/resources/$name-pdf"
        echo "  Trying: $pdf_url"
        curl -sL -o "$NICE_DIR/${code}_${name}.pdf" "$pdf_url"
    fi
done

echo ""
echo "Done! Downloaded PDFs:"
ls -la "$NICE_DIR"
