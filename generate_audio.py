#!/usr/bin/env python3
"""
generate_audio.py
Downloads all Japanese TTS audio files for japanese_coach.html.

Covers:
  - Every kana syllable (hiragana, voiced, semi-voiced, compounds) — 129 sounds
  - All 1,299 Joyo kanji (characters + readings)                  — ~2,100 files
  - All lesson phrases from the 30-day plan                        —   235 phrases
  Total: ~2,469 unique audio files, ~10 MB

Run once from the root of your repository:
    pip install requests
    python generate_audio.py

Re-running is safe — existing files are skipped automatically.
"""
import json, os, time, sys
import urllib.parse

try:
    import requests
except ImportError:
    sys.exit("Please run:  pip install requests")

MANIFEST  = "audio_manifest.json"
AUDIO_DIR = "audio"
HEADERS   = {"User-Agent": "Mozilla/5.0 (compatible; JapaneseCoachAudio/1.0)"}

URL_TEMPLATES = [
    "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=ja&ttsspeed=0.75&q={q}",
    "https://translate.googleapis.com/translate_tts?ie=UTF-8&client=gtx&tl=ja&ttsspeed=0.75&q={q}",
]

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(MANIFEST, encoding="utf-8") as f:
    manifest = json.load(f)

total, done, skipped, failed = len(manifest), 0, 0, []
print(f"Starting download of {total} audio files into {AUDIO_DIR}/")
print("-" * 50)

for text, filepath in manifest.items():
    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        skipped += 1
        continue

    success = False
    for url_tmpl in URL_TEMPLATES:
        url = url_tmpl.format(q=urllib.parse.quote(text))
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            ct = r.headers.get("content-type", "")
            is_audio = ("audio" in ct) or (
                r.status_code == 200 and len(r.content) > 500
                and r.content[:4] != b'<!DO'
            )
            if r.status_code == 200 and is_audio:
                with open(filepath, "wb") as f:
                    f.write(r.content)
                done += 1
                success = True
                print(f"  [{done+skipped:>4}/{total}] {text[:28]:28s} -> {filepath}")
                break
        except Exception:
            continue

    if not success:
        print(f"  FAILED: {text[:40]}")
        failed.append(text)

    time.sleep(0.25)

print("-" * 50)
print(f"Done. Downloaded: {done}  Skipped: {skipped}  Failed: {len(failed)}")
if failed:
    print("Failed items (re-run to retry):")
    for t in failed:
        print(f"  {t}")
