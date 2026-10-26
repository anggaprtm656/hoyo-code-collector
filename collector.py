# -*- coding: utf-8 -*-
"""
HoYo Codes Collector
Mengumpulkan kode redeem aktif & arsip per tahun untuk:
- Genshin Impact
- Honkai: Star Rail
- Zenless Zone Zero
- Honkai Impact 3rd
"""

import os
import sys
import json
import re
import urllib.request
from datetime import datetime, timezone, timedelta

# Fix encoding on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

WIB = timezone(timedelta(hours=7))

def fetch_wikitext(domain, page):
    url = f"https://{domain}/api.php?action=parse&page={page}&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('parse', {}).get('wikitext', {}).get('*', '')

def clean_wikitext_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

# ============================================================================
# PARSER GENSHIN IMPACT
# ============================================================================
def parse_genshin():
    print("🔍 Mengambil kode Genshin Impact...")
    text = fetch_wikitext('genshin-impact.fandom.com', 'Promotional_Code')
    text = clean_wikitext_comments(text)
    
    # Ambil bagian Active Codes
    active_part = text.split('==Active Codes==')[-1].split('==')[0] if '==Active Codes==' in text else text
    blocks = re.findall(r'\{\{Code Row(.*?)\}\}', active_part, re.DOTALL)
    
    results = []
    for b in blocks:
        parts = [p.strip() for p in b.split('|') if p.strip()]
        if not parts or parts[0] == '/Header' or parts[0] == '/Footer':
            continue
        
        raw_code = parts[0]
        # Ignore non-code templates or Chinese character codes for Global
        if '{{zh|' in raw_code or not re.match(r'^[A-Za-z0-9;]+$', raw_code):
            continue
        
        sub_codes = [c.strip() for c in raw_code.split(';') if c.strip()]
        server = parts[1] if len(parts) > 1 else 'Global'
        rewards = parts[2] if len(parts) > 2 else ''
        discovery = parts[3] if len(parts) > 3 else ''
        expiry = parts[4] if len(parts) > 4 else ''
        
        for sc in sub_codes:
            results.append({
                "game": "genshin",
                "game_title": "Genshin Impact",
                "code": sc,
                "server": "Global" if server in ["G", "A", "SEA", "NA", "EU"] else server,
                "rewards": rewards.replace('*', ' x').replace(';', ', '),
                "discovery_date": discovery,
                "expiry_date": expiry,
                "status": "active"
            })
    return results

# ============================================================================
# PARSER HONKAI: STAR RAIL
# ============================================================================
def parse_star_rail():
    print("🔍 Mengambil kode Honkai: Star Rail...")
    text = fetch_wikitext('honkai-star-rail.fandom.com', 'Redemption_Code')
    text = clean_wikitext_comments(text)
    
    # Bagian Active biasanya di bawah <!--active--> sebelum expired
    blocks = re.findall(r'\{\{Redemption Code Row(.*?)\}\}', text, re.DOTALL)
    
    results = []
    # Ambil 15 blok teratas yang merupakan kode paling baru
    for b in blocks[:20]:
        parts = [p.strip() for p in b.split('|') if p.strip()]
        if not parts:
            continue
        
        raw_code = parts[0]
        if not re.match(r'^[A-Za-z0-9]+$', raw_code):
            continue
        
        # Ekstrak data
        reward_match = re.search(r'\{\{Item List\|([^|]+)', b)
        rewards = reward_match.group(1) if reward_match else ''
        
        # Cari tanggal discovery (format YYYY-MM-DD)
        dates = re.findall(r'\b202\d-\d{2}-\d{2}\b', b)
        discovery = dates[0] if dates else ''
        expiry = dates[1] if len(dates) > 1 else 'unknown'
        
        results.append({
            "game": "hsr",
            "game_title": "Honkai: Star Rail",
            "code": raw_code,
            "server": "Global",
            "rewards": rewards.replace('*', ' x').replace(';', ', '),
            "discovery_date": discovery,
            "expiry_date": expiry,
            "status": "active"
        })
    return results

# ============================================================================
# PARSER ZENLESS ZONE ZERO
# ============================================================================
def parse_zzz():
    print("🔍 Mengambil kode Zenless Zone Zero...")
    text = fetch_wikitext('zenless-zone-zero.fandom.com', 'Redemption_Code')
    text = clean_wikitext_comments(text)
    
    blocks = re.findall(r'\{\{Redemption Code Row(.*?)\}\}', text, re.DOTALL)
    results = []
    for b in blocks:
        parts = [p.strip() for p in b.split('|') if p.strip()]
        if not parts:
            continue
        raw_code = parts[0]
        if not re.match(r'^[A-Za-z0-9]+$', raw_code):
            continue
        
        reward_match = re.search(r'\{\{Item List\|([^|]+)', b)
        rewards = reward_match.group(1) if reward_match else ''
        
        dates = re.findall(r'\b202\d-\d{2}-\d{2}\b', b)
        discovery = dates[0] if dates else ''
        expiry = dates[1] if len(dates) > 1 else 'unknown'
        
        results.append({
            "game": "zzz",
            "game_title": "Zenless Zone Zero",
            "code": raw_code,
            "server": "Global",
            "rewards": rewards.replace('*', ' x').replace(';', ', '),
            "discovery_date": discovery,
            "expiry_date": expiry,
            "status": "active"
        })
    return results

# ============================================================================
# PARSER HONKAI IMPACT 3RD
# ============================================================================
def parse_hi3():
    print("🔍 Mengambil kode Honkai Impact 3rd...")
    text = fetch_wikitext('honkaiimpact3.fandom.com', 'Exchange_Rewards')
    active_part = text.split('==Legacy==')[0] if '==Legacy==' in text else text
    
    rows = re.findall(r"\|'''([A-Za-z0-9]+)'''\|\|([^|]+)\|\|([^|]+)\|\|([^\n]+)", active_part)
    results = []
    for r in rows:
        code = r[0].strip()
        date_str = r[1].strip()
        occasion = re.sub(r'\[.*?\]', '', r[2]).strip()
        
        # Ekstrak item rewards
        items = re.findall(r'\{\{Item\|([^|]+)\|.*?quantity=([0-9,]+)', r[3])
        reward_desc = ", ".join([f"{item[0]} x{item[1]}" for item in items]) if items else occasion
        
        results.append({
            "game": "hi3",
            "game_title": "Honkai Impact 3rd",
            "code": code,
            "server": "Global (NA/EU)",
            "rewards": reward_desc,
            "discovery_date": date_str,
            "expiry_date": "limited",
            "status": "active"
        })
    return results

# ============================================================================
# MAIN AGGREGATOR & ARCHIVER PER TAHUN
# ============================================================================
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    archive_dir = os.path.join(data_dir, "archive")
    code_dir = os.path.join(base_dir, "code")
    os.makedirs(archive_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    
    now_wib = datetime.now(WIB)
    current_year = str(now_wib.year)
    
    all_active = []
    
    # 1. Scraping 4 Games
    for parse_func in [parse_genshin, parse_star_rail, parse_zzz, parse_hi3]:
        try:
            codes = parse_func()
            all_active.extend(codes)
        except Exception as e:
            print(f"⚠️ Error saat scraping: {e}")
    
    # 2. Pisahkan file JSON & TXT per game
    GAME_TITLES = {
        "genshin": "GENSHIN IMPACT",
        "hsr": "HONKAI: STAR RAIL",
        "zzz": "ZENLESS ZONE ZERO",
        "hi3": "HONKAI IMPACT 3RD"
    }

    for g in ["genshin", "hsr", "zzz", "hi3"]:
        g_codes = [c for c in all_active if c["game"] == g]
        # JSON format
        with open(os.path.join(data_dir, f"active_{g}.json"), "w", encoding="utf-8") as f:
            json.dump({
                "game": g,
                "total": len(g_codes),
                "last_updated": now_wib.strftime("%Y-%m-%d %H:%M:%S WIB"),
                "codes": g_codes
            }, f, ensure_ascii=False, indent=2)

        # TXT format (per game dengan header rapi)
        txt_path = os.path.join(code_dir, f"{g}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# -------------------- {GAME_TITLES[g]} --------------------\n")
            for c in g_codes:
                f.write(f"{c['code']}\n")

    # 3. File All Active Codes (JSON & TXT dengan pembatas per game)
    with open(os.path.join(data_dir, "active_codes.json"), "w", encoding="utf-8") as f:
        json.dump({
            "total_active": len(all_active),
            "last_updated": now_wib.strftime("%Y-%m-%d %H:%M:%S WIB"),
            "codes": all_active
        }, f, ensure_ascii=False, indent=2)

    with open(os.path.join(code_dir, "all.txt"), "w", encoding="utf-8") as f:
        for idx, g in enumerate(["genshin", "hsr", "zzz", "hi3"]):
            g_codes = [c for c in all_active if c["game"] == g]
            if idx > 0:
                f.write("\n")
            f.write(f"# -------------------- {GAME_TITLES[g]} --------------------\n")
            for c in g_codes:
                f.write(f"{c['code']}\n")

    # 4. Pengelompokan Arsip Per Tahun (Biar rapi dan gak numpuk!)
    year_file = os.path.join(archive_dir, f"{current_year}.json")
    existing_archive = []
    if os.path.exists(year_file):
        try:
            with open(year_file, "r", encoding="utf-8") as f:
                existing_archive = json.load(f).get("codes", [])
        except Exception:
            existing_archive = []
    
    existing_keys = {f"{c['game']}:{c['code'].upper()}" for c in existing_archive}
    added_count = 0
    for c in all_active:
        key = f"{c['game']}:{c['code'].upper()}"
        if key not in existing_keys:
            existing_archive.append(c)
            existing_keys.add(key)
            added_count += 1
            
    with open(year_file, "w", encoding="utf-8") as f:
        json.dump({
            "year": current_year,
            "total_recorded": len(existing_archive),
            "last_updated": now_wib.strftime("%Y-%m-%d %H:%M:%S WIB"),
            "codes": existing_archive
        }, f, ensure_ascii=False, indent=2)

    print("\n" + "="*50)
    print(f"🎉 SUKSES! Total {len(all_active)} kode aktif berhasil dikumpulkan!")
    print(f"📁 Format JSON:")
    print(f"   • data/active_codes.json (Semua Game)")
    print(f"   • data/archive/{current_year}.json (Arsip Tahun {current_year})")
    print(f"   • data/active_genshin.json, active_hsr.json, dll.")
    print(f"📁 Format TXT (Folder /code):")
    print(f"   • code/genshin.txt")
    print(f"   • code/hsr.txt")
    print(f"   • code/zzz.txt")
    print(f"   • code/hi3.txt")
    print(f"   • code/all.txt")
    print("="*50)

if __name__ == "__main__":
    main()
