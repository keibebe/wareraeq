# WarEra Crafting Calculator

Real-time equipment crafting cost calculator for [warera.io](https://warera.io), using live market prices from the WarEra API.

## Files

```
index.html        ← GitHub Pages frontend
proxy/
  worker.js       ← Cloudflare Worker (CORS proxy)
  wrangler.toml   ← Worker config
```

---

## Step 1 — Deploy the Cloudflare Worker proxy

The browser can't call the WarEra API directly due to CORS. The Worker sits in between and adds the right headers.

### 1a. Create a free Cloudflare account

Go to [cloudflare.com](https://cloudflare.com) and sign up (free, no credit card needed).

### 1b. Install Wrangler (Cloudflare's CLI)

```bash
npm install -g wrangler
```

### 1c. Log in

```bash
wrangler login
```

This opens a browser window — authorize it and come back.

### 1d. Edit `proxy/worker.js`

Open `proxy/worker.js` and change this line to match your GitHub username:

```js
const ALLOWED_ORIGINS = [
  "https://YOUR_GITHUB_USERNAME.github.io",   // ← change this
  ...
```

For example: `"https://johndoe.github.io"`

### 1e. Deploy the Worker

```bash
cd proxy
wrangler deploy
```

You'll see output like:

```
Deployed warera-proxy to https://warera-proxy.YOUR_NAME.workers.dev
```

**Copy that URL** — you'll need it in the next step.

---

## Step 2 — Deploy the GitHub Pages site

### 2a. Create a GitHub repo

Create a new repo called `warera-calc` (or any name you like) at [github.com/new](https://github.com/new).

### 2b. Push the files

```bash
git init
git add index.html
git commit -m "Add WarEra crafting calculator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/warera-calc.git
git push -u origin main
```

### 2c. Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select **Deploy from branch**
4. Choose **main** branch, **/ (root)** folder
5. Click **Save**

Your site will be live at `https://YOUR_USERNAME.github.io/warera-calc` within ~1 minute.

---

## Step 3 — Configure the calculator

1. Open your GitHub Pages site
2. In the **Proxy URL** field, paste the Worker URL from Step 1e:
   `https://warera-proxy.YOUR_NAME.workers.dev`
3. In the **API key** field, paste your WarEra API key (`wae_...`)
4. Click **Refresh** — prices should load!

Both values are saved to localStorage so you only need to enter them once.

---

## Troubleshooting

**"Origin not allowed" error**
→ Make sure `ALLOWED_ORIGINS` in `worker.js` exactly matches your GitHub Pages URL (no trailing slash).

**Worker returns 502**
→ The WarEra API may be down, or the endpoint changed. Try again in a few minutes.

**Prices show "N/A"**
→ The item keys returned by the API didn't match "steel" or "scrap". Open browser DevTools → Network tab → look at the proxy response to see what item names are returned, then adjust `worker.js` accordingly.

---

## Crafting recipes

Base recipes (multiplied by tier):

| Equipment    | Steel (base) | Scrap (base) |
|-------------|-------------|-------------|
| Weapon      | 10          | 5           |
| Helmet      | 8           | 4           |
| Chest armor | 12          | 6           |
| Pants       | 9           | 4           |
| Boots       | 7           | 3           |
| Gloves      | 6           | 3           |

Tier multipliers: Common ×1 · Uncommon ×2 · Rare ×4 · Epic ×8 · Legendary ×16

> Recipes are based on community data and may not be 100% accurate. Pull requests welcome!

---

*Unofficial tool. Not affiliated with WarEra.*
