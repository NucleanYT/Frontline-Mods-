# Making Frontline mods

A Frontline mod is a new map: either a **scenario** on today's world (other borders, countries, armies,
alliances and wars — like the built-in 1914 and 1939 start dates) or a whole **made-up world** with its own
continents. Players install only the mods they want: in the game, **Mods** (main menu) → *Mod place*, or
*Add a mod* → a file or a link. Installed mods appear under **New game**.

A mod is **one JSON file** called `<id>.frontline`. It contains only data — no code, no HTML, no SVG.
Frontline checks every mod before using it: names are cleaned, numbers are clamped and lists are capped, so a
broken or hostile file can't do anything but fail to load (with a message saying why).

## The smallest scenario

```json
{
  "frontline": "mod", "format": 1, "id": "iberian-union", "kind": "scenario",
  "title": "Iberian Union", "year": 2030, "date": "2030-05-01",
  "tagline": "Spain and Portugal united", "description": "What if Spain and Portugal became one country?",
  "states": [
    { "code": "IBU", "name": "Iberian Union", "take": ["ESP", "PRT"], "form": "iberia", "cap": "Madrid" }
  ]
}
```

Every country you don't mention stays as it is today.

## Fields (both kinds)

| Field | What it is |
|---|---|
| `frontline` | always `"mod"` |
| `format` | always `1` |
| `id` | 3–40 lower-case letters, digits and dashes, e.g. `"cold-war-1985"`. The file must be called `<id>.frontline`. |
| `kind` | `"scenario"` or `"world"` |
| `title`, `tagline`, `description` | shown on the cards (50 / 120 / 600 characters) |
| `year`, `date` | the start date (`"YYYY-MM-DD"`, years 1–9999) |
| `version`, `author` | e.g. `"1.2"`; a higher version in the mod place offers an update |
| `minGame` | the oldest Frontline that can play it, e.g. `"3.3.0"` |
| `intro` | up to 8 lines written to the news log at the start |
| `gdpScale`, `popScale` | multiply the economy and population of every country you *don't* list (e.g. 0.35 and 0.6 for 1985) |
| `noAir` | `true`: no air forces (before ~1915) |
| `states` | the countries you define (below) |
| `parts` | pieces of today's countries handed to another state (below) |
| `names` | old city names, e.g. `{ "Saint Petersburg": "Leningrad" }` |
| `alliances` | `[{ "name": "Warsaw Pact", "color": "#be2828", "members": ["SOV", "POL"] }]` |
| `relations` | `[["SOV", "USA", -60], …]` from −100 (hatred) to 100 (friendship) |
| `wars` | wars already going: `[{ "a": "IRQ", "b": "IRN", "name": "Iran–Iraq War", "join": [["AFG", 0]] }]` — `0` joins side a, `1` side b |
| `occupied` | `[{ "by": "ISR", "from": "PSX", "poly": [[lon, lat], …] }]` — land held by another country at the start |
| `forts` | `[["DDR", "DEU", 2, "Inner German Border"]]` — fortified line: owner, facing, depth 1–6 cells, name |
| `hesitant` | allies that wait before joining a war, e.g. `["ITA"]` |

### A state

```json
{ "code": "SOV", "name": "Soviet Union", "take": ["RUS", "UKR", "BLR"],
  "s": [6400, 278, 900, 5300, 6000, 90, 0.95, 95, 0.9],
  "form": "soviet-union", "color": [170, 40, 40], "cap": "Moscow", "continent": "Europe" }
```

- `code`: 2–6 capital letters/digits, used everywhere else in the mod. If it's the code of a real country you don't take, the real one is renamed for you, but a fresh code is clearer.
- `take`: today's countries (Natural Earth `ADM0_A3` codes: `DEU`, `FRA`, `RUS`, `CYN` for Northern Cyprus, `SOL` for Somaliland, `KOS` for Kosovo …) that become this state.
- `s` (optional): `[GDP $ billion, population millions, military budget $ billion, active army thousands, reserves thousands, navy 0–100, equipment quality 0.1–2, air force 0–100, pilot skill 0.1–2]`. Without it, the economy comes from the first country in `take` (times `gdpScale`) and the army is estimated.
- Flag — one of:
  - `"iso2": "de"`: a real country's flag
  - `"form": "…"`: a built-in historic flag: `austria-hungary`, `greater-greece`, `balkan-union`, `yugoslavia`, `byzantium`, `ottoman`, `rome`, `german-empire`, `napoleon`, `great-britain`, `bulgarian-empire`, `russian-empire`, `soviet-union`, `hre`, `greater-romania`, `czechoslovakia`, `union-state`, `kalmar`, `benelux`, `iberia`, `baltic`, `uar`, `arabia`, `persia`, `korea`, `gran-colombia`, `central-america`, `kingdom-italy`, `china-1912`, `siam`, `manchukuo`, `yugoslavia-kingdom`, `egypt-kingdom`, `iraq-kingdom`, `south-africa-1928`, `mongol`
  - `"flag": { "pattern": "h3", "colors": ["#111111", "#dd0000", "#ffce00"], "emblem": "circle", "emblemColor": "#ffce00" }`: drawn by the game.
    - Patterns: `plain h2 h3 v2 v3 cross nordic saltire triangle diagonal border canton quarters`.
    - Emblems: `none star circle crescent sun crown diamond`.
- `cap`: the capital's name (or a list of names to try); `capAt: [lon, lat]` places a small capital that isn't on the map.
- `color`: `[r, g, b]` or `"#rrggbb"` for the strategy map.

### Parts: moving borders

```json
{ "to": "DDR", "from": ["DEU"], "poly": [[10.9, 55.5], [10.9, 54.0], …, [15.5, 55.5]] }
```

The polygon (longitude, latitude) is drawn over the map, and every cell of the `from` countries inside it goes
to `to`. It may spill over other countries and the sea; only `from` land changes hands. A state may have no
`take` at all and get all its land from parts (East Germany, South Yemen …).

## Made-up worlds (`"kind": "world"`)

A world mod adds a `world` object with **GeoJSON FeatureCollections**. Use the same properties as
[Natural Earth](https://www.naturalearthdata.com/), so you can draw it in QGIS or geojson.io.
- **Coordinates**: longitude −180…180, latitude −58…84; that's the part of the globe the game shows.
- **Map grid**: a quarter of a degree per cell.

| Collection | Geometry | Properties |
|---|---|---|
| `countries` (required) | Polygon / MultiPolygon | `adm0_a3` (code, required), `name`, `name_long`, `continent`, `pop_est`, `gdp_md` ($ million), `mapcolor9` (1–9, neighbours different), optional `iso_a2` for a real flag |
| `regions` | Polygon | `featurecla`: `range/mtn`, `plateau`, `foothills`, `desert`, `forest`, `jungle`, `tundra`, `wetlands`, `delta` (terrain), or `geoarea` with a `name` (named lands, used to name new countries) |
| `rivers` | LineString | `scalerank` 0–6 (bigger rivers are lower) |
| `places` | Point | `name`, `pop_max`, `adm0cap: 1` for capitals |
| `provinces` | Point | `name`, `adm0_a3`: named points inside each country; where liberated land is cut, and what it's called |

`states`, `alliances`, `wars` and the rest work on top of a world too. In a world, `take` refers to your own
country codes, and a state is the easiest way to give a country a flag spec or a real army. A country with no
flag of its own gets one made for it. Land below 66° is plains unless a region says otherwise, and land above
66° is tundra.

## Limits

- The file can be at most 25 MB, with up to 3 million coordinates in total.
- Up to 400 states, 400 parts, 40 alliances and 40 wars.
- Names can be up to 60 characters. The characters `< > " \` & \` are removed.

## Publishing to the mod place

The mod place reads `index.json` from the [Frontline-Mods-](https://github.com/NucleanYT/Frontline-Mods-) repository on GitHub. Make that file with
`python3 tools/mods/build_index.py <repo>`, which lists every `mods/*.frontline`. To share a mod outside the
list:
- send the `.frontline` file; players pick it in *Add a mod*, or drop it on the window on PC
- or give them a link to the raw file

## Testing

`node test/modsim.js my-mod.frontline 365` loads a mod exactly as the game does and simulates a year. It also
reports any state that ended up with no land.
