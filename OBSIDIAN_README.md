# Obsidian Setup — LIFE System Vault

This repo is now a working **Obsidian vault**. Edit notes, see backlinks, catch drift visually.

## Install (one-time, ~5 minutes)

### 1. Install Obsidian
Download from [obsidian.md](https://obsidian.md). Free for personal use. Mac, Windows, iOS, Android.

### 2. Clone the repo locally
```bash
git clone https://github.com/ammoncovino/LIFE-system.git ~/LIFE-system
```

### 3. Open as a vault
- Launch Obsidian → **"Open folder as vault"** → pick `~/LIFE-system`
- Trust the author when prompted (it's you)

### 4. Install three plugins
Settings → **Community plugins** → Turn on, then Browse:

1. **Obsidian Git** — auto-commits and pushes your changes to GitHub
2. **Templater** — enforces structure when you create new species/SOP/sign notes
3. **Dataview** — powers the auto-generated lists in `INDEX.md`

After installing each, click **Enable**.

### 5. Configure Obsidian Git
Settings → Obsidian Git:
- **Auto-pull on startup:** ON
- **Auto-commit-and-sync:** every 30 minutes
- **Commit message:** `vault: {{date}} {{numFiles}} files`

That's it. You're now editing the LIFE system live, with version history and graph view.

---

## How to Use

### Daily workflow
- Open `INDEX.md` — it's the home page. Auto-lists every species, every draft, every SOP.
- Click any `[[wiki link]]` to jump. Use `Cmd+O` (Quick Switcher) to find anything by name.
- The **graph view** (left sidebar icon) shows every link visually. Broken links light up red.

### When you change a locked phrase
- Edit `locked_phrases/LOCKED_PHRASES.md` only.
- All species notes, signs, and SOPs reference it — change once, the source of truth updates everywhere.
- Then re-run the build scripts in `08_build/` to regenerate PDFs.

### When you add a new species
- Right-click `species/` → New note → use the **Species template** (Templater will offer it)
- Fill in frontmatter (`species_key`, `scientific`, etc.)
- It appears in `INDEX.md` automatically.

### When something feels off
- Open the **graph view** — orphan notes (no links in or out) are drift.
- Run `INDEX.md` → "Drift Watch" section lists anything still in `status: draft`.

---

## What's in the Vault

| Folder | What's inside |
|---|---|
| `species/` | One `.md` per species (18 today). Source for diet cards. |
| `locked_phrases/` | Canonical strings — the only place to edit them. |
| `templates/` | Templater starting points for new notes. |
| `01_master/` to `08_build/` | Existing system docs (untouched, now navigable). |
| `releases/` | Final printable PDFs by version. |
| `.obsidian/` | Vault config (committed so Kevin gets the same setup). |

---

## For Kevin

The repo is a vault. `.obsidian/` is committed. When you clone and open, you get the same plugin list, same settings. Use Obsidian Git to keep your local in sync — same as any other Git workflow but with a UI for non-devs.

Build scripts (`08_build/`, plus the parameterized `/tmp/build_diet_card.py` we use here) read from the markdown notes and emit PDFs. The vault is the source; the PDFs are the output.

---

## Drift Defense

Three layers, all automatic once set up:

1. **Backlinks panel** — every note shows what references it. Rename a species, broken links surface immediately.
2. **Graph view** — orphans (no incoming or outgoing links) are visible as isolated dots. Drift = isolation.
3. **Dataview INDEX** — auto-lists by `status: draft` so nothing sits half-done unnoticed.

This is what Kevin meant. Obsidian doesn't add discipline — it makes the discipline you already have **visible**.
