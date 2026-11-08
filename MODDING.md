# Making Frontline mods

A Frontline mod is either a new map — a **scenario** on today's world (other borders, countries, armies,
alliances and wars, like the built-in 1914 and 1939 start dates) or a whole **made-up world** with its own
continents — or a **theme** that changes how the game looks. Players install only the mods they want: in the game, **Mods** (main menu) → *Mod place*, or
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
| `kind` | `"scenario"`, `"world"` or `"theme"` (from Frontline 3.4.0) |
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
| `wars` | wars already going: `[{ "a": "IRQ", "b": "IRN", "name": "Iran–Iraq War", "join": [["AFG", 0]] }]` — `0` joins side a, `1` side b. Add `"kind": "independence"` when side a fights to be free of side b: if a holds out, b may recognize it (from Frontline 3.3.5) |
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

## Themes (`"kind": "theme"`)

A theme changes colours, fonts, corners, a panel texture and the strategy map's palette. It goes on as soon as
it's installed, and players switch back in Mods → Installed or Settings → Map. In Settings → Mods players can
change the `map` numbers below for themselves (the mod file stays as it is). Like the rest of a mod it is only
data: colours are `"#rrggbb"`, fonts and textures are names from the lists below (the font files ship with the
game), and numbers are clamped. Leave anything out to keep the game's own value. Set `"minGame": "3.4.0"` (or the version the newest map setting you use is marked with: `geometric` font and 3.4.1 settings need `"3.4.1"`, 3.4.4 settings `"3.4.4"`).

```json
{
  "frontline": "mod", "format": 1, "id": "night-ops", "kind": "theme", "minGame": "3.4.0",
  "title": "Night Ops", "tagline": "Black and green",
  "theme": {
    "colors": { "panel": "#101410", "accent": "#7fbf5a", "text": "#d8f0c8", "primary": ["#4f8a32", "#2f5a1c"] },
    "fonts": { "titles": "condensed", "text": "sans", "display": "stencil", "mapNames": "condensed" },
    "caps": true, "corners": "square", "texture": "lines",
    "map": { "sea": "#16242c", "saturation": 0.5, "borderWidth": 1.5, "borderDark": 0.7 }
  }
}
```

**`colors`**

| Key | What it colours |
|---|---|
| `panel`, `raised`, `hover`, `sunken` | side panel; buttons and plates; hover; meters, inputs and the clock |
| `line`, `edge` | hairlines; the dark outline of every plate |
| `accent`, `accentHi`, `accentText` | trim, selected tabs, icons; highlights; text on an accent background |
| `text`, `textDim`, `title` | normal text; secondary text; big titles |
| `war`, `warHi`, `good`, `info` | war and alarms; their highlight; good news and meters; neutral notes |
| `glass`, `shade`, `deep` | plates floating over the map; the main menu's shadow; the dark accent behind the main menu button |
| `sea` | the loading screen |
| `bar`, `tabs`, `button`, `primary`, `danger`, `loading` | `["#top", "#bottom"]` gradients: the top bar; tabs and dialogs; buttons; main buttons (and switched-on buttons); dangerous buttons; the loading screen around `sea` |
| `buttonEdge`, `primaryEdge`, `primaryText`, `dangerEdge` | button outlines and the text on main buttons |

**Other settings**

| Key | Values |
|---|---|
| `fonts.titles`, `fonts.text`, `fonts.display`, `fonts.mapNames` | `serif`, `sans`, `condensed`, `stencil`, `typewriter`, `geometric` (3.4.1) — headings and numbers; everything else; the biggest titles; the country names on the map |
| `caps` | `true`: headings, tabs and buttons in capitals |
| `corners` | `round` (the game's), `square`, `soft` |
| `texture` | a pattern on the panels: `none`, `canvas`, `steel`, `lines`, `grid` |

**`map`**

| Key | Range (default) | What it does |
|---|---|---|
| `sea`, `seaPolar` | colours (`#1f3b4d`, `#2d4759`) | the sea near the equator and near the poles |
| `shallows` | 0–2 (1) | how much lighter the water is along the coasts |
| `border`, `borderDark`, `borderWidth` | colour (`#000000`), 0–1 (0.5), 0.5–3 (1) | the lines between countries |
| `front` | colour (`#c80000`) | borders between countries at war |
| `saturation`, `brightness` | 0–1.5 (0.8), 0.5–1.5 (0.93) | country colours: 0 is grey, 1 their full colour |
| `tint`, `tintAmount` | colour, 0–0.6 (0) | washes every country colour with one colour |
| `relief`, `grain`, `edgeShadow` | 0–2 (1), 0–2 (1), 0–3 (1) | hill shading; the painted grain; the soft shadow inside borders and coasts |
| `paper` | 0–1 (0) | an old-paper wash over the whole map |
| `vignette` | 0–1 (0.45) | the dark frame around the map |
| `names`, `namesEdge`, `namesAlpha` | colours, 0.2–1.4 (1) | the big country names on the map |
| `namesAuto` (3.4.1) | 0 or 1 (0) | 1: names in the `namesEdge` colour, edged with `names`, on light countries |
| `edgeGlow` (3.4.1) | 0–1.5 (0) | each country's colour strong along its land borders and washed out inside |
| `mottle` (3.4.1) | 0–2 (0) | a blotchy satellite-like texture over the land |
| `landLines`, `seaLines` (3.4.1) | 0–1 (0) | thin province-like lines over the land; sea-zone lines over the water (when zoomed in far enough) |
| `clouds` (3.4.1) | 0–1 (0) | clouds over the map when zoomed out |
| `smooth` (3.4.4) | 0 or 1 (0) | 1: coasts and borders run smoothly instead of in steps, with thin outlines (graphics map only) |
| `terrain` (3.4.4) | 0–1.5 (0) | the land under the colours: pale rocky mountains, darker forests, sandy deserts |
| `cityNames` (3.4.4) | 0–1 (1) | lower: city dots and names only appear when zoomed further in (capital stars always show) |
| `countries` (3.4.4) | `{ "DEU": "#5a5a55", … }` | fixed colours by country code (today's map uses ISO codes like DEU, FRA; the 1914/1939 start dates use their own, e.g. GER, SOV); up to 600 |
| `capital`, `capitalEdge`, `capitalPicked`, `capitalSize` (3.4.1) | colours (`#f6d27a`, `#1d2118`, same as `capital`), 0.6–2.2 (1) | the capital stars; the selected country's star; their size |

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
