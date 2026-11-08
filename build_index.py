#!/usr/bin/env python3
"""Writes index.json — the list the in-game mod place reads — from every mods/*.frontline in a mod repository.

    python3 build_index.py <repo-dir>
"""
import json, os, re, sys

repo = sys.argv[1]
mods = []
for name in sorted(os.listdir(os.path.join(repo, "mods"))):
    if not name.endswith(".frontline"):
        continue
    p = os.path.join(repo, "mods", name)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    assert d.get("frontline") == "mod" and re.fullmatch(r"[a-z0-9][a-z0-9-]{1,38}[a-z0-9]", d["id"]), name
    assert name == d["id"] + ".frontline", f"{name}: the file must be called {d['id']}.frontline"
    mods.append({k: d[k] for k in ("id", "kind", "title", "version", "author", "tagline", "description", "year", "minGame") if k in d}
                | {"file": "mods/" + name, "size": os.path.getsize(p)})
mods.sort(key=lambda m: ({"scenario": 0, "world": 1, "theme": 2}.get(m["kind"], 3), m.get("year", 0), m["title"]))
out = {"frontline": "mods", "format": 1, "mods": mods}
# game.json (optional): the newest Android app, for its Update button — {"version", "apk", "notes"}
gp = os.path.join(repo, "game.json")
if os.path.exists(gp):
    with open(gp, encoding="utf-8") as f:
        g = json.load(f)
    assert re.fullmatch(r"\d+\.\d+\.\d+", g["version"]) and g["apk"].endswith("/Frontline-%s.apk" % g["version"]), "game.json"
    out["game"] = g
with open(os.path.join(repo, "index.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(mods), "mods:", ", ".join(m["title"] for m in mods))
