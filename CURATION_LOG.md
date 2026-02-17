# Guidelines Curation & Development Log

## Project Overview
Building a comprehensive collection of UK medical guidelines for Emergency Medicine.

---

## 2024-02-16: Initial Setup & Analysis

### Session 1: Eolas Exploration
- **Goal**: Understand Eolas Medical's structure for guideline access
- **Method**: Browser automation with login
- **Findings**:
  - Eolas uses React with client-side routing
  - Login requires `document.execCommand('insertText')` for React inputs
  - Navigation requires `history.pushState` + `popstate` event
  - PDF viewer uses Apryse (PDFTron) WebViewer
  - API endpoint: `api.eolas.click/nice/v1/guidelines/{ID}`
  - Auth: Cognito tokens in localStorage (expire ~1 hour)

### Session 2: Direct Source Downloads
- **RCEM**: Successfully scraped 52 PDFs from rcem.ac.uk
  - URL pattern: `rcem.ac.uk/wp-content/uploads/{year}/{month}/{filename}.pdf`
  - Used sitemap: `rcem.ac.uk/post-sitemap.xml`
  
- **NICE via Eolas**: Downloaded 56 PDFs
  - Problem: Used manually curated ID list, not systematic
  - Problem: File names are just IDs (CG51.pdf), not descriptive
  - TODO: Scrape NICE directly for proper naming and complete coverage

- **BTS**: Downloaded 5 PDFs
  - URL pattern: `brit-thoracic.org.uk/document-library/...` triggers direct PDF download
  - Some require authentication

### Gaps Identified
1. Resuscitation Council UK - ALS, PALS, anaphylaxis algorithms
2. Stroke guidelines - NICE NG128, RCP guidelines
3. Sepsis - Surviving Sepsis Campaign, UK Sepsis Trust
4. SIGN - Scottish guidelines
5. Paediatric emergencies - fever, bronchiolitis, safeguarding

---

## 2024-02-16: Session 3 - Filling Gaps

### Strategy
1. Visit each source website in browser
2. Understand structure and PDF access patterns
3. Create targeted scraping scripts
4. Use descriptive naming: `{Source}_{Topic}_{Year}.pdf`

### Naming Convention
```
{SOURCE}_{GUIDELINE_ID}_{Short_Title}_{Year}.pdf

Examples:
NICE_NG128_Stroke_and_TIA_2019.pdf
RCUK_Adult_ALS_Algorithm_2021.pdf
BTS_Emergency_Oxygen_2017.pdf
```

### Current Task: NICE Website Analysis
- Visit nice.org.uk/guidance
- Understand filtering and PDF download patterns
- Create proper scraping strategy


### NICE Scraping Progress
- Created `scrape_nice.py` with BeautifulSoup
- URL pattern: `nice.org.uk/guidance/{ID}/resources/{slug}-pdf-{hash}`
- Filtering by EM-relevant keywords (240 of 500 guidelines matched)
- Running full scrape...


### NICE Scraping Complete
- Downloaded 156 EM-relevant guidelines from NICE
- Total: 156 PDFs with proper naming (NICE_{ID}_{Title}.pdf)
- Topics covered: sepsis, stroke, cardiac, respiratory, paediatric, mental health, trauma, etc.

### Next: Resuscitation Council UK

### Resuscitation Council UK (RCUK) Complete
- Downloaded 15 algorithm PDFs from resus.org.uk
- Includes: Adult BLS, Adult ALS, Paediatric BLS/ALS, Choking, Arrhythmias, Anaphylaxis
- PDF locations discovered via scraping individual guideline pages
- URL pattern: `resus.org.uk/sites/default/files/{year-month}/{filename}.pdf`

### Next: SIGN Scottish Guidelines

### SIGN Guidelines Added
- Downloaded 4 EM-relevant SIGN guidelines
- SIGN 158: Asthma Management (BTS/SIGN joint)
- SIGN 167: Care of Deteriorating Patients
- SIGN 168: Dementia
- SIGN 173: Chronic Pain (Part 1)

---

## Final Status

### Collection Complete: 232 PDFs across 5 sources

| Source | Count | Topics |
|--------|-------|--------|
| NICE | 156 | Full EM coverage - sepsis, stroke, cardiac, respiratory, etc. |
| RCEM | 52 | ED-specific - pain, sedation, mental health, toxicology |
| RCUK | 15 | Resuscitation algorithms - ALS, BLS, anaphylaxis |
| BTS | 5 | Respiratory - oxygen, asthma, pneumonia, pleural |
| SIGN | 4 | Scottish guidelines - asthma, deteriorating patients, pain |

### Scraping Strategies Summary

1. **NICE**: BeautifulSoup scraper filtering by EM keywords
   - Pagination handled via table scraping
   - PDFs downloaded via direct URLs from guideline pages
   
2. **RCEM**: Sitemap-based scraping
   - Posts contain PDF download links
   - Direct URL pattern: `rcem.ac.uk/wp-content/uploads/`

3. **RCUK**: Manual URL discovery
   - No sitemap, PDFs embedded in guideline pages
   - URL pattern: `resus.org.uk/sites/default/files/`

4. **BTS**: Document library pattern
   - Some URLs trigger direct PDF download
   - Authentication required for some resources

5. **SIGN**: Individual page scraping
   - PDFs in media folder
   - URL pattern: `sign.ac.uk/media/{id}/{filename}.pdf`

### Remaining Gaps
- Surviving Sepsis Campaign (subscription/purchase required)
- More SIGN guidelines (can be expanded)
- Newborn Life Support full guidelines
- Some BTS guidelines require authentication

### Files Produced
- `SUMMARY.md` - Collection overview
- `CURATION_LOG.md` - This development log
- `index.json` - Searchable metadata
- `metadata.json` - NICE scraping metadata
- Various scraping scripts

---

## 2024-02-16: Quality Audit

### NICE Collection Review
- **Total downloaded**: 156 PDFs
- **Page range**: 12-198 pages (appears to be full guidelines, not quick refs)
- **Problem**: Many guidelines NOT relevant to Emergency Medicine

### EM-Relevant Categories Identified:
1. **Core ED presentations**: ACS, stroke, trauma, sepsis, anaphylaxis, head injury
2. **Common ED conditions**: Fractures, infections, pain, respiratory
3. **Mental health emergencies**: Self-harm, psychosis, delirium
4. **Paediatric emergencies**: Fever, bronchiolitis, meningitis

### Questionable/Non-EM Guidelines Found:
- Cancer screening/management (breast, prostate, colorectal, lung)
- Autism spectrum guidelines
- Dementia management
- Pregnancy management (unless emergency)
- Rehabilitation guidelines
- Service delivery/commissioning
- Long-term condition management

### Action Required:
1. Create explicit EM-relevant list based on RCEM curriculum
2. Re-scrape with tighter filtering
3. Remove non-relevant guidelines from collection
4. Better file naming with clinical category

### NICE Collection Curated
**Date**: 2024-02-16

**Before**: 156 PDFs (39 MB)
**After**: 71 PDFs (16 MB) 
**Removed**: 85 non-EM-relevant guidelines

**Curation Criteria**:
- Core ED presentations (cardiac, neurological, trauma, respiratory)
- Common ED conditions (infections, pain, mental health)
- Paediatric emergencies
- Antimicrobial prescribing guidelines

**Removed categories**:
- Cancer management (not ED acute care)
- Autism/developmental disorders
- Dementia/rehabilitation
- Pregnancy management (kept only emergencies)
- Prevention/screening programs
- Service delivery guidelines
- Incontinence (non-acute)

**Key Guidelines Retained**:
- NG185: Acute coronary syndromes
- NG128: Stroke and TIA
- NG232: Head injury
- NG39-41: Major trauma, spinal injury
- NG253-255: Sepsis (all age groups)
- NG240: Meningitis
- CG134: Anaphylaxis
- NG37-38: Fractures
- NG245: Asthma
- NG114: COPD exacerbation
- NG225: Self-harm
- NG143: Fever in under 5s
- CG50: Acutely ill adults
