# How to add a new mod

## 1 — Prepare the mod folder

In VSCode, inside the repo root, create a folder named **exactly** like the mod (same name as the DCS install folder):

```
DCS-mods/
└── FG_my_new_mod/       ← create this folder
```

## 2 — Update entry.lua before zipping

Make sure your `entry.lua` contains these fields inside the **first** `declare_plugin()` call:

```lua
declare_plugin("FG_my_new_mod",
{
    installed     = true,
    state         = "installed",
    developerName = "FullGas",
    version       = __DCS_VERSION__,          -- or "1.0", "2.7", etc.
    description   = "One sentence describing the mod.",
    category      = "Helipad",                -- see allowed values below
})
```

**Allowed `category` values:**

| Value | Use for |
|---|---|
| `"Cargo"` | Cargo loads and freight objects |
| `"Helipad"` | Helipads and helicopter landing zones |
| `"Static Personnel"` | Static human figures |
| `"Infantry"` | Playable infantry units |
| `"Vehicle"` | Ground vehicles |
| `"Naval"` | Naval units |
| `"Aircraft"` | Aircraft |
| `"Misc"` | Anything else |

> Don't forget the **commas** after `description` and `category` — missing commas crash DCS on load.

## 3 — Place the ZIP in the mod folder

Drop `FG_my_new_mod.zip` into the folder you just created.
The ZIP name **must match** the folder name exactly.

```
DCS-mods/
└── FG_my_new_mod/
    └── FG_my_new_mod.zip    ← ZIP name = folder name
```

## 4 — Add screenshots (optional)

Create a `media/` subfolder and drop your screenshots there.
The first image will appear automatically at the top of the mod's README.

```
DCS-mods/
└── FG_my_new_mod/
    ├── FG_my_new_mod.zip
    └── media/
        ├── screenshot_01.jpg
        └── screenshot_02.jpg
```

## 5 — Ask Claude to commit

Tell Claude: **"j'ai ajouté le mod FG_my_new_mod"**

Claude will run:
```
git add  →  git commit  →  git push  (to develop)
```

Git LFS handles the ZIP automatically — nothing special to do.

## 6 — CI generates the README

After the push to `develop`, GitHub Actions detects the new folder and creates a default `README.md` automatically. Pull to get it locally:

```
git pull
```

Then complete the README — fill in **Usage** and any extra details.

## 7 — Add screenshots to README (if applicable)

If you added screenshots in step 4 but the README was generated before them,
manually add this line between the title and `## Description`:

```markdown
![FG_my_new_mod screenshot](media/screenshot_01.jpg)
```

Ask Claude to commit: **"README mis à jour"**

## 8 — Merge to main → catalog updated automatically

When the mod is ready to publish, merge `develop` into `main`.
Ask Claude: **"merge develop sur main"**

GitHub Actions rebuilds the root catalog (`README.md`) automatically.
The new mod appears in the catalog within seconds.

---

## Quick reference

```
New mod checklist:
[ ] Folder name = ZIP name = DCS install folder name
[ ] entry.lua has: description, category (with commas!)
[ ] ZIP is inside the mod folder
[ ] Screenshots in media/ (optional)
[ ] Tell Claude to commit → push to develop
[ ] Pull → complete README
[ ] Merge to main when ready
```
