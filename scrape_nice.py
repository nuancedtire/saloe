#!/usr/bin/env python3
"""NICE Guidelines Scraper - v3"""

import requests
import re
import json
import time
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = 'https://www.nice.org.uk'

EM_KEYWORDS = [
    'emergency', 'acute', 'sepsis', 'stroke', 'cardiac', 'heart', 'chest pain',
    'trauma', 'fracture', 'head injury', 'poisoning', 'overdose', 'self-harm',
    'suicide', 'mental health', 'psychosis', 'anaphylaxis', 'asthma', 'copd',
    'pneumonia', 'respiratory', 'diabetes', 'hypoglycaemia', 'seizure', 'epilepsy',
    'meningitis', 'fever', 'infection', 'antibiotic', 'pain', 'falls',
    'atrial fibrillation', 'venous thromboembolism', 'pulmonary embolism', 'dvt',
    'delirium', 'dementia', 'alcohol', 'drug misuse', 'violence', 'safeguarding',
    'child', 'paediatric', 'pregnancy', 'obstetric', 'neonatal', 'cancer',
    'uti', 'urinary', 'kidney', 'renal', 'ischaemic', 'tia', 'transient'
]

class NICEScraper:
    def __init__(self, output_dir='NICE_new'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.guidelines = {}
        
    def get_published_guidelines(self):
        """Fetch all published NICE guidelines"""
        # Use larger page size
        url = f'{BASE_URL}/guidance/published?ngt=NICE+guidelines&ps=500'
        
        print("Fetching all guidelines...")
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        table = soup.find('table')
        if not table:
            print("No table found!")
            return []
            
        rows = table.find_all('tr')[1:]
        print(f"Found {len(rows)} rows in table")
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                title_link = cells[0].find('a')
                if title_link:
                    href = title_link.get('href', '')
                    if href.startswith('/'):
                        href = BASE_URL + href
                    gid = cells[1].text.strip()
                    self.guidelines[gid] = {
                        'title': title_link.text.strip(),
                        'url': href,
                        'id': gid,
                        'published': cells[2].text.strip() if len(cells) > 2 else ''
                    }
            
        return list(self.guidelines.values())
    
    def is_em_relevant(self, guideline):
        title_lower = guideline['title'].lower()
        return any(kw in title_lower for kw in EM_KEYWORDS)
    
    def get_pdf_url(self, guideline_url):
        try:
            resp = self.session.get(guideline_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Look for download PDF link
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.text.lower()
                
                if 'download' in text and 'pdf' in text:
                    if href.startswith('/'):
                        href = BASE_URL + href
                    return href
                    
            # Fallback: find any resource link with pdf
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/resources/' in href and '-pdf-' in href:
                    if href.startswith('/'):
                        href = BASE_URL + href
                    return href
                    
        except Exception as e:
            pass
        return None
    
    def download_pdf(self, url, guideline):
        id_str = guideline['id']
        title_clean = re.sub(r'[^\w\s-]', '', guideline['title'])
        title_clean = re.sub(r'\s+', '_', title_clean)[:50]
        
        filename = f"NICE_{id_str}_{title_clean}.pdf"
        filepath = self.output_dir / filename
        
        if filepath.exists():
            return 'skip', filepath
            
        try:
            resp = self.session.get(url, stream=True, timeout=30)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                # Verify PDF
                with open(filepath, 'rb') as f:
                    header = f.read(5)
                    if header != b'%PDF-':
                        filepath.unlink()
                        return 'invalid', None
                        
                return 'ok', filepath
            return 'http_error', None
        except Exception as e:
            if filepath.exists():
                filepath.unlink()
            return 'error', None
    
    def run(self, em_only=True, limit=None):
        print("=== NICE Guidelines Scraper ===\n")
        
        guidelines = self.get_published_guidelines()
        print(f"Found {len(guidelines)} unique guidelines\n")
        
        if em_only:
            guidelines = [g for g in guidelines if self.is_em_relevant(g)]
            print(f"Filtered to {len(guidelines)} EM-relevant guidelines\n")
            
        if limit:
            guidelines = guidelines[:limit]
        
        stats = {'ok': 0, 'skip': 0, 'failed': 0}
        
        for i, g in enumerate(guidelines):
            print(f"[{i+1}/{len(guidelines)}] {g['id']}: {g['title'][:40]}...", end=' ')
            pdf_url = self.get_pdf_url(g['url'])
            
            if pdf_url:
                result, fpath = self.download_pdf(pdf_url, g)
                if result == 'ok':
                    stats['ok'] += 1
                    size = fpath.stat().st_size // 1024
                    print(f"OK ({size}KB)")
                elif result == 'skip':
                    stats['skip'] += 1
                    print("SKIP")
                else:
                    stats['failed'] += 1
                    print(f"FAIL ({result})")
            else:
                stats['failed'] += 1
                print("NO URL")
                
            time.sleep(0.2)
        
        print(f"\n=== Summary ===")
        print(f"New downloads: {stats['ok']}")
        print(f"Already existed: {stats['skip']}")
        print(f"Failed: {stats['failed']}")
        
        # Save metadata
        with open(self.output_dir / 'metadata.json', 'w') as f:
            json.dump(guidelines, f, indent=2)

if __name__ == '__main__':
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    scraper = NICEScraper(output_dir='NICE_new')
    scraper.run(em_only=True, limit=limit)
