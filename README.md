# Frontline mods

Maps for Frontline, the world war simulator: scenarios on today's world and whole made-up worlds.
The game's **Mods → Mod place** reads `index.json` from this repository, so anything listed there can be
installed with one click. Nobody gets a mod they didn't pick.

| Mod | Kind | |
|---|---|---|
| Cold War 1985 | scenario | NATO against the Warsaw Pact; Afghanistan, Iran–Iraq and Angola at war |
| Empires Reborn | scenario | an alternate 2031: the Ottomans, Byzantium, Austria-Hungary, Persia, the Inca … are back |
| The Shattered Isles | made-up world | 60 nations on a new planet of ragged continents and islands |

## Adding a mod

1. Put `<id>.frontline` in `mods/` (the format is in [MODDING.md](MODDING.md)).
2. Run `python3 build_index.py .` here to update `index.json`.
3. Commit both.

The generators for the three mods above are in the game's source (`tools/mods/`).
