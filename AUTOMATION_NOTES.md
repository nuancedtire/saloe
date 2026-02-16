# Eolas Medical PDF Extraction - Automation Notes

## Summary
Successfully downloaded:
- **52 RCEM PDFs** (Royal College of Emergency Medicine) - directly from rcem.ac.uk
- **65 NICE PDFs** (National Institute for Health and Care Excellence) - via Eolas API

## Key Findings

### Authentication
- Login uses React forms - must use `document.execCommand('insertText')` + `form.requestSubmit()`
- Auth tokens stored in localStorage as Cognito tokens
- Token key pattern: `CognitoIdentityServiceProvider.{app-id}.{user-id}.accessToken`
- App ID: `4kbkv8lhbsp9al108amu7ao1dd`

### Navigation
- Site uses React Router v6
- Direct URL navigation often shows "no items found"
- **Working method**: `history.pushState({}, '', '/path') + dispatchEvent(new PopStateEvent('popstate'))`

### URL Patterns
- NICE Guidelines viewer: `/knowledge/niceGuidelines/viewer/{ID}` (e.g., QS165, NG64, CG51, CG52)
- National Guidelines viewer: `/knowledge/nationalGuidelines/viewer/{ID}`

### PDF Extraction via WebViewer
- Uses Apryse (PDFTron) WebViewer
- Web component: `<apryse-webviewer>`
- Instance access: `document.querySelector('apryse-webviewer').instance`
- Extract PDF: 
  ```javascript
  const doc = instance.Core.documentViewer.getDocument();
  const data = await doc.getFileData();
  // data is ArrayBuffer - convert to base64 for transfer
  ```

### API (More Efficient Method)
- Base: `https://api.eolas.click`
- **NICE Guidelines**: `GET /nice/v1/guidelines/{ID}` 
  - Returns JSON with `url` field containing S3 signed URL
  - Requires Bearer token from localStorage
  - S3 URLs valid for 1 hour
- NICE IDs: CG*, NG*, QS*, TA* (e.g., CG51, NG64, QS165, TA1045)

### Direct Source Downloads (Most Efficient)
- **RCEM**: Download directly from `rcem.ac.uk/wp-content/uploads/` 
  - Use sitemap: `https://rcem.ac.uk/post-sitemap.xml`
  - Parse best-practice pages for PDF links
- **NICE**: Use Eolas API for signed S3 URLs, then curl download

## Scripts Created

### download_nice_via_eolas.sh
Downloads NICE guidelines using Eolas API with a list of IDs:
```bash
./download_nice_via_eolas.sh <bearer_token> [output_dir] [ids_file]
```

### scrape_rcem.sh
Downloads RCEM PDFs directly from their website:
```bash
./scrape_rcem.sh
```

## Working Process

### For NICE Guidelines:
1. Login to Eolas via browser
2. Extract access token from localStorage
3. Use API: `curl -H "Authorization: Bearer $TOKEN" "https://api.eolas.click/nice/v1/guidelines/{ID}"`
4. Download PDF from returned S3 URL

### For RCEM Guidelines:
1. Fetch sitemap from rcem.ac.uk
2. Extract best-practice page URLs
3. Visit each page and find PDF links
4. Download directly with curl

## Known NICE Drug Misuse Guidelines (Downloaded)
- QS165 - Drug misuse prevention
- NG64 - Drug misuse prevention: targeted interventions  
- CG51 - Drug misuse in over 16s: psychosocial interventions
- CG52 - Drug misuse in over 16s: opioid detoxification

## File Locations
- RCEM PDFs: `/home/exedev/eolas-guidelines/RCEM/`
- NICE PDFs: `/home/exedev/eolas-guidelines/NICE/`
- Scripts: `/home/exedev/eolas-guidelines/`
