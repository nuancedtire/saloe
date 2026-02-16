# Medical Guidelines Collection

A curated collection of UK medical guidelines relevant to Emergency Medicine.

## Summary

| Source | Count | Size |
|--------|-------|------|
| RCEM (Royal College of Emergency Medicine) | 52 | 22.6 MB |
| NICE (National Institute for Health and Care Excellence) | 56 | 10.4 MB |
| BTS (British Thoracic Society) | 5 | 12.5 MB |
| **Total** | **113** | **45.5 MB** |

## Directory Structure

```
├── RCEM/          # Royal College of Emergency Medicine guidelines
├── NICE/          # NICE guidelines (CG, NG, QS, TA series)
├── BTS/           # British Thoracic Society guidelines
├── index.json     # Searchable metadata index
└── scripts/       # Automation scripts
```

## Clinical Categories

Guidelines are tagged in `index.json` by clinical category:
- **mental-health**: Section 136, behavioural disturbance, psychiatric emergencies
- **pain-sedation**: Analgesia, ketamine, procedural sedation
- **cardiovascular**: ACS, cardiac arrest, aortic dissection
- **respiratory**: Asthma, COPD, pneumonia, oxygen therapy, pleural disease
- **toxicology**: Overdose, poisoning, antidotes
- **trauma**: Major trauma, head injury
- **infection**: Sepsis, antibiotics
- **paediatric**: Children-specific guidelines
- **safeguarding**: Domestic abuse, FGM, vulnerable patients
- **operational**: Consent, discharge, policy

## Key Guidelines

### RCEM Highlights
- Acute Behavioural Disturbance (2023)
- Pain Management (Adults & Children)
- Procedural Sedation & Ketamine
- Section 136 Mental Health
- Aortic Dissection
- Traumatic Cardiac Arrest

### NICE Highlights
- NG185: Acute Coronary Syndromes
- NG94: Emergency/Acute Medical Care
- Drug misuse guidelines (CG51, CG52, NG64, QS165)

### BTS Highlights
- Emergency Oxygen Use
- Community Acquired Pneumonia
- Pleural Disease (2023)

## Known Gaps

See `EM_GAP_ANALYSIS.md` for detailed analysis. Key missing sources:
- Resuscitation Council UK (ALS/PALS algorithms)
- SIGN Scottish Guidelines
- Stroke guidelines (NG128)
- Surviving Sepsis Campaign

## Automation Scripts

- `download_nice_via_eolas.sh` - Download NICE PDFs via Eolas API
- `download_bts.sh` - Download BTS guidelines
- `scrape_rcem.sh` - Scrape RCEM website
- `create_index.py` - Generate searchable index

## Usage

```bash
# Search for a topic
jq '.guidelines[] | select(.title | test("pain"; "i"))' index.json

# List by category
jq '.categories["respiratory"]' index.json
```

## Data Sources

- RCEM: Downloaded directly from rcem.ac.uk
- NICE: Extracted via Eolas Medical API (requires authentication)
- BTS: Downloaded from brit-thoracic.org.uk document library
