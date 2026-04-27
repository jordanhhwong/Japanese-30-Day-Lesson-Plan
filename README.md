# 🇯🇵 Japanese Holiday Coach — 30-Day Learning Plan

A fully self-contained web app to take you from beginner to holiday-ready Japanese in 30 days, with under 30 minutes of study per day.

---

## 📁 Repository structure

```
japanese_coach.html     ← The entire app (single file)
audio_manifest.json     ← Maps every Japanese phrase to its local MP3 path
generate_audio.py       ← One-time script to download all 235 audio files
audio/                  ← MP3 files (created by running generate_audio.py)
README.md
```

---

## 🔊 Setting up local audio (recommended — fixes all mobile sound issues)

The app plays audio from three sources in priority order:

| Priority | Source | Works offline? | Requires setup? |
|----------|--------|---------------|-----------------|
| 1st | Local MP3 files in `audio/` | ✅ Yes | Run script once |
| 2nd | Google Translate TTS | ❌ No | None |
| 3rd | Device SpeechSynthesis | ❌ No | None |

Local files are the most reliable — they play from GitHub Pages with no network requests, no rate-limiting, and correct media-stream audio routing on mobile.

### To generate all audio files (do this once):

```bash
pip install requests
python generate_audio.py
```

This downloads **235 MP3 files** (~8 MB total) into the `audio/` directory, then commit and push them:

```bash
git add audio/
git commit -m "Add local TTS audio files"
git push
```

After this, every 🔊 button plays a local file. The badge in the app header shows `🔊 Local audio ✓` in green when it's working.

---

## 🚀 Deploying to GitHub Pages

1. Fork or create this repository
2. Upload `japanese_coach.html`, `audio_manifest.json`, `generate_audio.py`, `README.md`, and the `audio/` folder
3. Go to **Settings → Pages → Source → main branch / root**
4. Your app is live at:
   ```
   https://YOUR-USERNAME.github.io/REPO-NAME/japanese_coach.html
   ```
5. Bookmark that URL on your phone

---

## 💾 Progress across sessions and devices

Progress saves automatically in `localStorage` every time you complete a task. It persists as long as you use the same browser on the same device.

**To move progress to another device:**
- Tap **💾 Export progress** in the app header → saves a `.json` file
- On the new device, tap **📂 Import progress** → select the file

---

## 🎤 Microphone on Xiaomi / HyperOS

Chrome's site settings (the 🔒 lock icon) are not the only permission layer. If you see "Permission denied" even though site settings show "allowed", check this:

**Settings → Apps → Chrome → Permissions → Microphone → Allow**

This is Android's app-level permission for Chrome, separate from Chrome's own site settings. After changing it, fully close Chrome and reopen the page.

HyperOS 3 does **not** have a microphone toggle in the notification panel. The Android app permission above is the only other layer to check.

If the mic still doesn't work, a **text fallback** appears automatically — type what you said in romaji and the app grades your pronunciation.

---

## 🗓 Study Plan Overview

| Week | Theme | Days |
|------|-------|------|
| Week 1 | Survival Basics | 1–7 |
| Week 2 | Conversations & Context | 8–14 |
| Week 3 | Deeper Conversations | 15–21 |
| Week 4 | Polish & Confidence | 22–30 |

Every 7th day includes a full review and an 8-question mini-test.

---

*Built for October 2026 Japan holidays 🍁*
