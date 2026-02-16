# Emergency Medicine Guidelines - Gap Analysis

## What We Have

### RCEM (52 PDFs) ✓
Good coverage of:
- Mental health in ED (Section 136, behavioral disturbance, risk pathways)
- Pain management (adults, children, procedural sedation)
- Toxicology (opioids, drug trafficking, cannabinoid hyperemesis)
- Specific conditions (aortic dissection, cardiac arrest, rAAA)
- Operational (consent, discharge, frequent attenders, safeguarding)

### NICE (65 PDFs) - Partially Relevant
Mixed bag - some highly relevant, some not EM-specific

---

## CRITICAL GAPS FOR EMERGENCY MEDICINE

### 1. **Resuscitation Council UK** ⚠️ HIGH PRIORITY
- Adult ALS algorithm
- Paediatric ALS
- Newborn life support
- Anaphylaxis guidelines
- Post-resuscitation care
- Special circumstances (drowning, hypothermia, electrocution)
- **Source**: https://www.resus.org.uk/library/2021-resuscitation-guidelines

### 2. **British Thoracic Society (BTS)** ⚠️ HIGH PRIORITY
- Acute asthma management
- COPD exacerbation
- Community-acquired pneumonia
- Pleural disease / chest drain
- Pulmonary embolism
- Oxygen therapy
- **Source**: https://www.brit-thoracic.org.uk/quality-improvement/guidelines/

### 3. **SIGN (Scottish Guidelines)** ⚠️ MEDIUM PRIORITY
Often more detailed than NICE:
- SIGN 158: British guideline on management of asthma
- SIGN 152: Acute coronary syndrome
- SIGN 141: Dental emergencies
- SIGN 108: Stroke rehabilitation
- **Source**: https://www.sign.ac.uk/our-guidelines/

### 4. **Stroke Guidelines** ⚠️ HIGH PRIORITY
- NICE NG128: Stroke and TIA
- RCP National Clinical Guideline for Stroke
- Mechanical thrombectomy criteria
- **Missing from our NICE collection**

### 5. **Cardiac Guidelines** ⚠️ HIGH PRIORITY
- NICE NG185: Acute coronary syndromes ✓ (we have this)
- ESC Guidelines (European)
- Arrhythmia management
- Heart failure acute management

### 6. **Sepsis** ⚠️ HIGH PRIORITY
- Surviving Sepsis Campaign 2021
- NICE NG51: Sepsis recognition and early management ✓ (we may have)
- UK Sepsis Trust pathways
- Paediatric sepsis

### 7. **Trauma** ⚠️ MEDIUM PRIORITY
- TARN (Trauma Audit Research Network) standards
- Major trauma pathways
- C-spine clearance protocols
- Paediatric trauma (RCEM response to RCR ✓)

### 8. **Toxicology** ⚠️ MEDIUM PRIORITY
- TOXBASE access (subscription required)
- NPIS guidelines
- Specific antidote protocols (RCEM has one ✓)
- Paracetamol overdose pathway

### 9. **Mental Health Crisis** ⚠️ MEDIUM PRIORITY
- NICE NG225: Self-harm assessment
- NICE CG16: Self-harm (older)
- Psychiatric liaison pathways
- Mental Capacity Act guidance

### 10. **Paediatric Emergencies** ⚠️ HIGH PRIORITY
- NICE fever in under 5s (NG143)
- Bronchiolitis (NG9)
- Safeguarding (we have FGM ✓)
- NAI recognition
- APLS pathways

### 11. **Obstetric/Gynae Emergencies** ⚠️ MEDIUM PRIORITY
- Ectopic pregnancy
- Miscarriage management
- Obstetric haemorrhage
- Pre-eclampsia/eclampsia

### 12. **Surgical Emergencies** ⚠️ MEDIUM PRIORITY
- Acute abdomen pathways
- Appendicitis (NICE NG164)
- Bowel obstruction
- Testicular torsion

---

## ORGANISATION ISSUES

### Current Problems:
1. **Flat structure** - all PDFs in one folder
2. **Inconsistent naming** - some have full titles, some just codes
3. **Duplicates** - QS165 appears 4 times, CG51/CG52 appear 3 times each
4. **No metadata** - can't search by topic/condition
5. **No version tracking** - guidelines get updated

### Proposed Structure:
```
guidelines/
├── RCEM/
│   ├── mental-health/
│   ├── pain-sedation/
│   ├── toxicology/
│   ├── trauma-resus/
│   ├── safeguarding/
│   └── operational/
├── NICE/
│   ├── cardiovascular/
│   ├── respiratory/
│   ├── neurology/
│   ├── mental-health/
│   ├── paediatrics/
│   ├── infections/
│   └── toxicology/
├── ResusUK/
├── BTS/
├── SIGN/
└── index.json  # Searchable metadata
```

---

## SCRAPING LOGIC FLAWS

1. **Manual ID list** - we guessed NICE IDs rather than getting complete list
2. **Token expiration** - Cognito tokens expire after ~1 hour
3. **No retry logic** - failed downloads not retried
4. **No validation** - don't check if PDF is complete/valid
5. **Missing Eolas categories** - we only searched specific terms, may have missed many
6. **No incremental updates** - can't easily check for new/updated guidelines

---

## RECOMMENDED NEXT STEPS

### Immediate:
1. Clean up duplicates in NICE folder
2. Organise into topic-based subfolders
3. Create index.json with metadata

### Short-term:
4. Scrape Resuscitation Council UK guidelines
5. Scrape BTS guidelines (publicly available)
6. Get complete NICE guideline list from Eolas

### Medium-term:
7. Set up scheduled refresh with new tokens
8. Add version tracking
9. Create searchable interface
