#!/usr/bin/env python3
"""Create searchable index of guidelines"""
import os
import json
import re
from pathlib import Path

def extract_info_from_filename(filepath):
    """Extract metadata from PDF filename"""
    name = Path(filepath).stem
    source = Path(filepath).parent.name
    
    # Extract guideline ID if present
    id_match = re.search(r'(CG|NG|QS|TA|HTG)\d+', name)
    guideline_id = id_match.group(0) if id_match else None
    
    # Clean up title
    title = name.replace('_', ' ').replace('-', ' ')
    title = re.sub(r'\s+', ' ', title).strip()
    
    return {
        'id': guideline_id,
        'title': title,
        'source': source,
        'filename': Path(filepath).name,
        'path': str(filepath),
        'size_kb': os.path.getsize(filepath) // 1024
    }

def categorize_guideline(info):
    """Assign clinical categories based on title/content"""
    title_lower = info['title'].lower()
    categories = []
    
    # Clinical categories
    category_keywords = {
        'mental-health': ['mental', 'psychiatric', 'psychosis', 'depression', 'anxiety', 'self-harm', 'suicide', 'section 136', 'behavioural'],
        'pain-sedation': ['pain', 'sedation', 'analgesia', 'ketamine', 'opioid'],
        'cardiovascular': ['cardiac', 'heart', 'coronary', 'acs', 'stemi', 'mi ', 'aortic', 'hypertension', 'chest pain', 'arrhythmia'],
        'respiratory': ['asthma', 'copd', 'pneumonia', 'oxygen', 'respiratory', 'pleural', 'thoracic', 'pulmonary'],
        'toxicology': ['poison', 'overdose', 'drug misuse', 'intoxication', 'antidote', 'toxicity', 'cannabinoid'],
        'trauma': ['trauma', 'injury', 'fracture', 'wound', 'head injury', 'spinal'],
        'infection': ['sepsis', 'infection', 'antibiotic', 'pneumonia', 'meningitis'],
        'paediatric': ['child', 'paediatric', 'pediatric', 'infant', 'neonatal'],
        'neurology': ['stroke', 'seizure', 'epilepsy', 'headache', 'neurological'],
        'safeguarding': ['safeguard', 'abuse', 'domestic', 'fgm', 'vulnerable'],
        'operational': ['consent', 'discharge', 'screening', 'policy', 'guideline template'],
    }
    
    for category, keywords in category_keywords.items():
        for kw in keywords:
            if kw in title_lower:
                categories.append(category)
                break
    
    if not categories:
        categories.append('general')
    
    return list(set(categories))

def main():
    base_dir = Path('/home/exedev/eolas-guidelines')
    index = {
        'generated': '2024-02-16',
        'total_files': 0,
        'sources': {},
        'categories': {},
        'guidelines': []
    }
    
    # Process each source directory
    for source_dir in ['RCEM', 'NICE', 'BTS']:
        source_path = base_dir / source_dir
        if not source_path.exists():
            continue
            
        index['sources'][source_dir] = {'count': 0, 'size_mb': 0}
        
        for pdf_file in sorted(source_path.glob('*.pdf')):
            info = extract_info_from_filename(pdf_file)
            info['categories'] = categorize_guideline(info)
            
            index['guidelines'].append(info)
            index['sources'][source_dir]['count'] += 1
            index['sources'][source_dir]['size_mb'] += info['size_kb'] / 1024
            
            # Track categories
            for cat in info['categories']:
                if cat not in index['categories']:
                    index['categories'][cat] = []
                index['categories'][cat].append(info['filename'])
    
    index['total_files'] = len(index['guidelines'])
    
    # Round sizes
    for src in index['sources'].values():
        src['size_mb'] = round(src['size_mb'], 1)
    
    # Write index
    with open(base_dir / 'index.json', 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"Created index with {index['total_files']} guidelines")
    print("\nBy source:")
    for src, data in index['sources'].items():
        print(f"  {src}: {data['count']} files ({data['size_mb']} MB)")
    print("\nBy category:")
    for cat, files in sorted(index['categories'].items()):
        print(f"  {cat}: {len(files)} files")

if __name__ == '__main__':
    main()
