#!/usr/bin/env python3
"""
generate_audio.py — downloads all Japanese TTS audio files for japanese_coach.html
Run once from the root of your repository:
    pip install requests
    python generate_audio.py

Creates an audio/ directory with one MP3 per Japanese phrase.
"""
import json, os, time, urllib.parse, sys
try:
    import requests
except ImportError:
    sys.exit("Please install requests first:  pip install requests")

MANIFEST = "audio_manifest.json"
AUDIO_DIR = "audio"
TTS_URL   = "https://translate.googleapis.com/translate_tts"
HEADERS   = {"User-Agent": "Mozilla/5.0"}

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(MANIFEST, encoding="utf-8") as f:
    manifest = json.load(f)

total   = len(manifest)
done    = 0
skipped = 0
failed  = []

for text, filepath in manifest.items():
    if os.path.exists(filepath):
        skipped += 1
        continue
    params = {"ie": "UTF-8", "client": "gtx", "tl": "ja", "ttsspeed": "0.75",
              "q": text}
    try:
        r = requests.get(TTS_URL, params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200 and r.headers.get("content-type","").startswith("audio"):
            with open(filepath, "wb") as f:
                f.write(r.content)
            done += 1
            print(f"  [{done+skipped}/{total}] {text[:30]}")
        else:
            print(f"  SKIP (HTTP {r.status_code}): {text[:30]}")
            failed.append(text)
    except Exception as e:
        print(f"  ERROR: {text[:30]} — {e}")
        failed.append(text)
    time.sleep(0.3)   # be polite to Google's servers

print(f"\nDone. Downloaded: {done}  Already existed: {skipped}  Failed: {len(failed)}")
if failed:
    print("Failed items:", failed)
