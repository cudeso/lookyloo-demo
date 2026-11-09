# Lookyloo demo sites

Three fictional websites for demonstrating website analysis with [Lookyloo](https://github.com/Lookyloo/lookyloo/). They look unrelated: an underground forum, a website-monitoring company and a news publication. They deliberately serve some byte-identical files, so a capture of each can be linked through matching resource hashes.

All names, people, companies, listings and data are invented. Each site shows a visible demo notice. No form sends or stores anything.

## Sites

| Site | Document root | Public URL | Entry pages |
| --- | --- | --- | --- |
| Ashmarket (forum) | `sites/market/` | `https://market.internetpolice.com/` | `/`, `/thread.html`, `/login.html`, `/rules.html` |
| HFH Network Services (website monitoring) | `sites/hfh/` | `https://hfh.internetpolice.com/` | `/`, `/report.html`, `/services` (redirect) |
| The Northline Dispatch (news) | `sites/newscorp/` | `https://newscorp.internetpolice.com/` | `/`, `/outage-monitoring.html`, `/forum-reputation.html` |

All site paths are relative.

## Running the server

One script serves all the sites and picks the document root from the `Host` header.

```bash
python3 server.py
```

Settings are at the top of `server.py` and can be overridden with environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEMO_BASE_DOMAIN` | `internetpolice.com` | Sites answer on `market.`, `hfh.` and `newscorp.` under this domain. This is the only place the domain is configured. |
| `DEMO_BIND` | `127.0.0.1` | Listen address. Keep the default behind a reverse proxy. |
| `DEMO_PORT` | `8000` | Listen port. |

Requests for any other hostname get a `404`. Directory listings are disabled.

## Deployment

1. Create DNS records for `market`, `hfh` and `newscorp` under the chosen domain, pointing at the server or add the entries to the hosts file (of the Lookyloo host and your workstation)
2. Run `python3 server.py`. If you bind to port 80 then you will have to use sudo.

## Headers, cookies and the JSON request

`server.py` adds an `X-Demo-Site` header to every response and sets a cookie on the homepage (`/` and `/index.html`) only.

| Site | `X-Demo-Site` | Cookie |
| --- | --- | --- |
| Market | `market` | `ash_guest=guest-4471` |
| HFH | `hfh` | `hfh_visitor=v-20261020-0815` |
| NewsCorp | `newscorp` | `nld_reader=reader-0042` |

The cookies use `Path=/; HttpOnly; SameSite=Lax` without a `Domain`, so each one stays on its own subdomain. They have no `Secure` flag, so they also work over plain HTTP.

After the page loads, `ui-helper.js` fetches `/api/session.json` and shows its message in the header. If the capture starts at `/`, that request and the later asset requests carry the cookie. A capture that starts on a subpage has no cookie.

## Shared resources

Each site serves its own copy of these files. No page loads anything from another demo subdomain.

| Resource | Served by | SHA-256 |
| --- | --- | --- |
| `/assets/css/common.css` | Market, HFH, NewsCorp | `b68b98c01bfd32fe0040e7cf839573955bb2113933a32ae437ffff8e620a8925` |
| `/assets/js/ui-helper.js` | Market, HFH, NewsCorp | `34bd9ef2b5642a48b9b833c6d314e2677420f31115282215a2183ec82321125f` |
| `/assets/img/badge-verified.svg` | Market, NewsCorp | `e6e170496721d014cf2a8b3ac65fd33f0c07d72847fbb5ab1c687e74f36254f5` |
| `/assets/img/network-topology.svg` (HFH), `/assets/img/stories/europe-outage-monitoring.svg` (NewsCorp) | HFH, NewsCorp | `a1a3858d0367f593a32b2f3bf660f6ccf1e742811ea22752f57bde40af454619` |
| Bootstrap 4.2.1 grid from an external site (see below) | NewsCorp | `e6d573b7daafdee530dc4204ffb40f9bd192b3f65ed11a0bf02b18b909bca8a8` |

### Fonts and background images

Each site stylesheet loads its own font and background image. The stylesheet is the `Referer`, so Lookyloo shows these requests one level below the page resources. They differ per site and do not link the sites.

| Site | Stylesheet | Font | Background image |
| --- | --- | --- | --- |
| Market | `market.css` | `Go-Mono.ttf` | `bg-mesh.svg` |
| HFH | `hfh.css` | `Inter-ExtraBold.otf` | `hero-dots.svg` |
| NewsCorp | `newscorp.css` | `EBGaramond12-Bold.ttf` | `compass-rose.svg` (hidden on narrow screens) |

The fonts are unmodified copies of openly licensed fonts, with each licence file next to its font.

## External resource on NewsCorp

NewsCorp loads the Bootstrap 4.2.1 grid (MIT) directly from an external site and uses it for its page layout. The URL is in the `link` tag of each NewsCorp page. This is the only third-party request on the demo pages, apart from the end of the HFH redirect chain below. On 20 October 2026 it returned `200`, `text/css` and 48,488 bytes with the hash above.

If you capture both NewsCorp and the site that hosts the file, the same URL and hash appear in both trees. That only shows NewsCorp links to a public file on that site. **It does not mean the owner of that site operates or endorses any demo site.** It is a useful counter-example: a matching resource often just comes from a common library.

If the file changes or disappears, the NewsCorp layout breaks and the hash no longer matches. Check it before presenting:

```bash
url=$(grep -o 'https://[^"]*bootstrap-grid.min.css' sites/newscorp/index.html)
curl -s "$url" | sha256sum
```

## Redirect chain on HFH

Capture `http://hfh.internetpolice.com/services` on its own to show how Lookyloo follows redirects. `server.py` answers both hops with a real `302`, so there are no `services.html` or `external.html` files.

| Request | Response |
| --- | --- |
| `/services` | `302`, `Location: /external` |
| `/external` | `302`, `Location: https://www.cudeso.be/` |

Expected in Lookyloo, not yet checked in a capture: the tree starts on `hfh.internetpolice.com` and continues on `www.cudeso.be`, with all three URLs listed as the redirect chain. The two HFH responses carry `X-Demo-Site: hfh` and no cookie.

`www.cudeso.be` is a live site, so the capture browser needs internet access, and the resources it loads can change between captures.

## Presenting with Lookyloo

Capture these in order and let indexing finish before looking for correlations:

1. `https://market.internetpolice.com/`
2. `https://hfh.internetpolice.com/`
3. `https://newscorp.internetpolice.com/`
4. The site that hosts the Bootstrap file

### Expected findings

These are what the sites are built to show. They have not been checked against a Lookyloo instance yet.

| Where to look | What you should see | What it means |
| --- | --- | --- |
| Screenshots | Three pages that look nothing alike. | Appearance gives no hint of a link. |
| Capture tree | One host per demo site, plus the Bootstrap host on NewsCorp. | No request connects the demo sites to each other. |
| `common.css`, `ui-helper.js` | The same hash in all three captures. | The sites share code. A lead, not proof. |
| `badge-verified.svg` | The same hash on Market and NewsCorp. | An image copied between sites. |
| `europe-outage-monitoring.svg` | The same hash as HFH's `network-topology.svg`. | Content matches despite a different name and path. |
| `bootstrap-grid.min.css` | The same URL and hash on NewsCorp and the site that hosts it. | A shared third-party file. Weak evidence. |
| URL node for `/` | `Set-Cookie` and `X-Demo-Site`. | A server-set, host-only cookie. |
| `/api/session.json` | The request sends the homepage cookie. | The cookie is used on a later request. |

## Screenshots

![screenshots/market.png](screenshots/market.png)

![screenshots/newscorp.png](screenshots/newscorp.png)

![screenshots/hfh.png](screenshots/hfh.png)