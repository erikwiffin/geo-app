# Pigs · Parks · Pints

A retired little tool that pairs **one hike, one barbecue joint, and one brewery**
into a single North Carolina day trip. It picks a random anchor, finds the nearest
neighbor in each of the other two categories, and draws the loop on a map.

It used to run on a server. This version doesn't — it's a single static page that
does all the work in the browser, so it can sit quietly on GitHub Pages forever and
still work whenever someone opens it.

```
.
├── index.html   ← the whole app (markup, styles, data, logic)
├── 404.html     ← makes clean /trip/<id> permalinks resolve (don't delete)
├── CNAME        ← the custom domain: pigsparkspints.com
└── README.md
```

## How it works

- **No backend.** The place list lives inside `index.html`. Picking a trip is just a
  random draw plus a nearest-neighbor search (straight-line distance), and the map is
  [Leaflet](https://leafletjs.com/) drawing on free OpenStreetMap tiles.
- **The trip number is the trip.** A permalink like `/trip/370811614` uses the number
  as the random seed. The same number always rebuilds the same three stops, so links
  are stable and bookmarkable. "Deal me a trip" just rolls a fresh number.

## Host it on GitHub Pages

1. Create a repo (e.g. `pigsparkspints`) and put these four files at its root.
2. **Settings → Pages →** set *Source* to **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. Under **Custom domain**, enter `pigsparkspints.com` and save (the `CNAME` file already does this too). Tick **Enforce HTTPS** once it's available.
4. At your DNS registrar, point the domain at GitHub Pages:
   - Four `A` records on the apex `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - A `CNAME` record on `www` → `your-username.github.io`

   *(GitHub's apex IPs occasionally change — check the current "Configuring a custom domain" docs if a record won't verify.)*

That's it. `pigsparkspints.com` and every `/trip/<id>` link will resolve.

> Hosting it under a project path instead (e.g. `you.github.io/pigsparkspints/`)?
> Change `pathSegmentsToKeep` from `0` to `1` in `404.html`.

## Reviving it / swapping in your own places

Open `index.html` and find the block marked **`EDIT YOUR PLACES HERE`** (the `PLACES`
object). Each entry is:

```js
{ name:"Lexington Barbecue", town:"Lexington", lat:35.7935, lng:-80.2755 }
```

Add an optional `url` if you want the name on the ticket to link out. Keep the three
keys (`pig`, `park`, `pint`); add as many entries to each as you like.

The shipped list is real, well-known NC spots with **approximate** coordinates — a
starter set so the map works immediately. Verify and replace them with your own
database when you bring it back.

## Notes

- Map tiles © OpenStreetMap contributors; fine for a personal, low-traffic site.
- Distances are straight-line ("as the crow flies"), not driving miles.
- Leaflet and the web fonts load from CDNs; if either is ever blocked, the page still
  renders the trip ticket — only the map tiles need the network.
