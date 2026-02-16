#!/bin/bash
# Download BTS (British Thoracic Society) Guidelines

OUTPUT_DIR="${1:-BTS}"
mkdir -p "$OUTPUT_DIR"

# Key EM-relevant BTS guidelines (document library URLs that trigger PDF downloads)
declare -A guidelines=(
  ["BTS_Oxygen"]="https://www.brit-thoracic.org.uk/document-library/guidelines/emergency-oxygen/bts-guideline-for-oxygen-use-in-adults-in-healthcare-and-emergency-settings/"
  ["BTS_CAP_2009"]="https://www.brit-thoracic.org.uk/document-library/guidelines/pneumonia-adults/bts-guidelines-for-the-management-of-community-acquired-pneumonia-in-adults-2009-update/"
  ["BTS_CAP_QuickRef"]="https://www.brit-thoracic.org.uk/document-library/guidelines/pneumonia-adults/quick-reference-guide-bts-guidelines-for-the-management-of-community-acquired-pneumonia-in-adults/"
  ["BTS_Pleural_2023"]="https://www.brit-thoracic.org.uk/document-library/guidelines/pleural-disease/bts-guideline-for-pleural-disease/"
  ["BTS_Asthma"]="https://www.brit-thoracic.org.uk/document-library/guidelines/chronic-asthma/btsand-sign-national-guideline-for-the-management-of-asthma-british-guideline-for-asthma-management-2024/"
  ["BTS_Severe_Asthma"]="https://www.brit-thoracic.org.uk/document-library/guidelines/severe-asthma/bts-and-nice-guideline-on-severe-asthma/"
  ["BTS_PE"]="https://www.brit-thoracic.org.uk/document-library/guidelines/pulmonary-embolism/bts-guideline-for-the-initial-outpatient-management-of-pulmonary-embolism-pe/"
  ["BTS_NIV"]="https://www.brit-thoracic.org.uk/document-library/guidelines/niv/bts-and-ics-guideline-for-the-ventilatory-management-of-acute-hypercapnic-respiratory-failure-in-adults/"
)

for name in "${!guidelines[@]}"; do
  url="${guidelines[$name]}"
  outfile="$OUTPUT_DIR/${name}.pdf"
  
  if [ -f "$outfile" ]; then
    echo "Skipping $name (exists)"
    continue
  fi
  
  echo -n "Downloading $name... "
  # Follow redirects and save
  curl -sL -o "$outfile" "$url" 2>/dev/null
  
  # Check if valid PDF
  if file "$outfile" | grep -q "PDF"; then
    size=$(stat -c%s "$outfile")
    echo "OK ($(numfmt --to=iec $size))"
  else
    echo "FAILED (not a PDF)"
    rm -f "$outfile"
  fi
done

echo ""
echo "Downloaded $(ls -1 $OUTPUT_DIR/*.pdf 2>/dev/null | wc -l) BTS guidelines"
