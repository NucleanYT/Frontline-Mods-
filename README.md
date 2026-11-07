# Frontline mods

Maps for Frontline, the world war simulator: scenarios on today's world and whole made-up worlds.
The game's **Mods → Mod place** reads `index.json` from this repository, so anything listed there can be
installed with one click. Nobody gets a mod they didn't pick.

| Mod | Kind | |
|---|---|---|
| 1789: The French Revolution | scenario | the Bastille falls; Poland–Lithuania, Venice and the Holy Roman Empire still stand |
| 1812: Napoleon Marches on Russia | scenario | the Grande Armée crosses the Niemen; the Peninsular War and the War of 1812 |
| 1821: The Greek War of Independence | scenario | Greece rises against the Ottomans; Ali Pasha revolts in Epirus |
| 1861: The American Civil War | scenario | Fort Sumter; the Taiping Rebellion; Italy newly united |
| Cold War 1962: The Cuban Missile Crisis | scenario | Soviet missiles in Cuba; a divided Berlin and Vietnam; the Congo Crisis |
| Cold War 1985 | scenario | NATO against the Warsaw Pact; Afghanistan, Iran–Iraq and Angola at war |
| Empires Reborn | scenario | an alternate 2031: the Ottomans, Byzantium, Austria-Hungary, Persia, the Inca … are back |
| The Shattered Isles | made-up world | 60 nations on a new planet of ragged continents and islands |

## Adding a mod

1. Put `<id>.frontline` in `mods/` (the format is in [MODDING.md](MODDING.md)).
2. Run `python3 build_index.py .` here to update `index.json`.
3. Commit both.

The generators for the three mods above are in the game's source (`tools/mods/`).
