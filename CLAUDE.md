# Lookyloo demo sites

This repository contains websites used to demonstrate website analysis with Lookyloo. It contains the pages and resources that Lookyloo captures, rather than the Lookyloo application itself.

The aim is to give a presenter useful, repeatable examples: what a page loads, which hosts it contacts, how redirects work, and which resources connect otherwise different websites. A convincing screenshot matters, but the requests behind the page are part of the demo too.

## Before making changes

Read the README and the relevant files first. Follow the current checkout when its structure or deployment differs from this guidance. Use the hosting model below when developing sites. Do not assume a particular server, framework or deployment configuration unless it is present or documented.

For each requested site, identify the behaviour being demonstrated and the evidence a presenter should find in Lookyloo. Keep the implementation focused on that behaviour. Do not add every possible demo feature to every site.

## Repository structure

Keep each site easy to locate and serve. Follow the existing layout. For a new repository, a simple starting point is:

| Path | Purpose |
| --- | --- |
| `sites/<site-name>/` | A site's HTML, CSS, JavaScript and local assets, served at the root of its own subdomain. |
| `README.md` | How to serve the sites, capture them and demonstrate the expected findings. |

Use descriptive names. A site can start with `index.html`, `style.css` and an `assets/` directory. Add JavaScript only when the page or scenario needs it. 

## Coding conventions

- Always prefer simple, straightforward code. Choose the obvious implementation when two approaches work.
- Use plain HTML, CSS and vanilla JavaScript by default. Do not introduce a framework, package manager, bundler or build step for a static page.
- Use existing tools and dependencies. Add a dependency only when it solves a concrete requirement that is awkward to handle without it.
- Use local JavaScript, not loaded from a CDN.
- Do not introduce classes, abstractions, generic configuration systems or design patterns without an immediate need. A few sites do not need a site-generation platform.
- Keep functions short and focused. Use descriptive names and direct control flow.
- Keep styling in ordinary CSS. Use CSS variables for repeated values when useful, without building a design system for a handful of pages.
- Handle actual failure cases. Avoid redundant checks, broad exception handling, silent fallbacks and defensive wrappers around predictable local code.
- Do not add retries, caching, background jobs or extensibility hooks without a specific requirement.
- Follow the surrounding formatting. Keep changes focused and avoid unrelated refactoring or renaming.
- Do not generate stub functions, placeholder logic or TODO comments unless explicitly requested.

Write code and comments as a maintainer would. Avoid LLM-style scaffolding: unnecessary helper layers, inflated names, repetitive explanations, decorative comment banners and numbered comments that narrate each step.

Comments should explain a non-obvious reason, constraint or intentional demo behaviour. Do not describe what the next line plainly does. Do not add docstrings or comments mechanically to every function. Put the presenter walkthrough in documentation rather than repeating it throughout the source.

## Build for useful captures

Lookyloo captures a page in a browser. Implement the requests and behaviour the scenario needs, then check that they actually occur.

- Keep CSS, images, scripts and fonts as separate files when inspecting those resources is part of the demo. Avoid bundling everything into HTML or embedding resources as data URLs in those cases.
- Make sure intended resources are used. A font declaration alone is insufficient: apply the font to visible text. Referenced images and styles must load in the rendered page.
- Make the main demo behaviour happen on initial navigation. Do not depend on clicks, scrolling, form submission or a long timer unless interaction is explicitly part of the scenario and documented.
- Keep requests finite and predictable. Avoid random resource selection, cache-busting timestamps, endless polling and unnecessary animations.
- Use real browser requests for simulated analytics or tracking. A label saying that tracking happens does not demonstrate a request.
- Keep the resource tree readable. Every additional host or request should serve the scenario or the page.

Each site should have an identifiable title, plausible content and a clear visual purpose. Avoid generic landing-page filler, repeated card grids and unnecessary dashboards. Use realistic copy for the fictional service being represented.

## Relationships between sites

When demonstrating resource correlation, deliberately reuse selected files across sites. Useful examples include an image, favicon, stylesheet or script.

- Keep a resource byte-for-byte identical when its matching body hash is the intended connection. Reformatting a shared script or changing an image's metadata can break that example.
- Distinguish a shared URL from shared content. Different URLs can return the same file; matching filenames alone do not establish matching content.
- Keep unrelated resources distinct where the demo needs a clear comparison. Document any intentional differences between variants.
- Before changing a shared file, check every site that uses it and update the expected findings if necessary.

A useful pair of sites can look different while loading one identical resource. Explain that a shared resource is an investigative lead; a common font or library does not establish common ownership.

## Hosting and HTTP behaviour

The pages will be hosted on a dedicated test domain, for example `internetpolice.com`. Each test site will have its own subdomain, for example `test1.internetpolice.com` and `test2.internetpolice.com`. These names are examples; use the actual domain chosen for the deployment.

Develop each site for this layout from the start:

| Site directory | Example public URL |
| --- | --- |
| `sites/test1/` | `https://test1.internetpolice.com/` |
| `sites/test2/` | `https://test2.internetpolice.com/` |

Each site's directory is its document root. Its public URL must not require a repository path such as `/sites/test1/`. Make asset paths, internal links, form actions and JavaScript requests work from that subdomain's root. Keep site-local requests on the same subdomain. Use another subdomain explicitly when the scenario calls for a resource or redirect on another host.

Keep deployment-specific hostnames in one small, clearly identified place when they are needed. Do not build a generic configuration system for this. Keep cookies scoped to the site's hostname by default; use a parent-domain cookie only when sharing it between subdomains is part of the scenario.

Prefer local, versioned assets over live CDNs, remote fonts or real analytics services.

Use paths that match the documented document root. Prefer relative paths for site-local assets and explicit hostnames only where the scenario needs them. Do not scatter deployment-specific URLs through the source.

For a basic static preview, serve an individual site's directory:

```bash
python3 -m http.server 8000 --directory sites/test1
```

The site is then available at `http://localhost:8000/`, with the same path layout as its eventual subdomain. Preview another site on a separate port if needed. The default static server does not select a site by hostname; hosting multiple subdomains requires explicit routing to their document roots or server processes.

HTTP response headers may be sent by a small Python server. When a scenario needs custom headers, cookies, redirects or a simple response endpoint, a short `server.py` using the standard library's `http.server` is sufficient. A custom handler can use `send_response()`, `send_header()` and `end_headers()` to send the required status and headers. Keep its behaviour specific to the demo and avoid adding a web framework for this alone.

The static preview command above does not configure those scenario-specific responses. Document the Python server's actual start command and port when one is added. If a reverse proxy handles the public subdomains and TLS, document which site or Python process each hostname reaches, and verify the final headers received by the browser.

Use the existing web server or the smallest suitable server implementation when those behaviours are required:

- An HTTP redirect needs a real `3xx` response and a `Location` header. A JavaScript redirect or meta refresh is a different scenario and should be described accordingly.
- Server-set cookies need a real `Set-Cookie` response header. HTML metadata cannot set HTTP response headers.
- A cookie demo should include a subsequent request that can send the cookie, rather than only setting it. Account for its domain, path and relevant browser restrictions.
- Serve resources with the correct content types, especially scripts, fonts and JSON. Configure cross-origin access only where the requests require it.

All scenario hosts must resolve and be reachable from the browser doing the Lookyloo capture. A hosts-file entry on the presenter's laptop does not configure a remote capture browser. Document required DNS, TLS, ports and host mappings, and check the instance's rules for access to private addresses when relevant.

Use synthetic identities, sample values and fictional services. Simulated tracking endpoints should use fixed demo values. Do not collect real credentials, personal information or payment details, or send form contents to outside services.

## Documentation

For each scenario, keep a short walkthrough in the README or alongside the site. Include:

1. The purpose of the demo and the question it helps answer.
2. The site's subdomain, document root, entry URL and serving instructions, including the Python start command if applicable.
3. The expected requests, resources, redirects or cookies relevant to that question.
4. The other sites to capture when demonstrating shared resources.
5. Where the presenter should look in Lookyloo and what the finding means.
6. Any required interaction, browser setting or known limitation.

Distinguish expected findings from findings verified in an actual capture. Do not promise a third-party enrichment result or reputation verdict. Those depend on the Lookyloo instance, its integrations and the submitted resources.

## Validation

Use the existing checks where they help. Do not introduce a test framework for a static page or write tests that merely repeat its markup.

After changing a site, serve it over HTTP and inspect the rendered page and browser network activity. Check that the intended assets load, the console has no unexpected errors and the page is ready within the intended capture window. Check real status codes, headers and cookie behaviour for scenarios that use them. Treat deliberate failures as documented scenario behaviour.

When the subdomain deployment is available, also check the site through its public hostname. Verify that requests reach the intended subdomains, paths work from `/`, and no deployment URLs still point to localhost or repository directories.

For a correlation demo, compare the relevant served resources as well as the local files. A local check can start with:

```bash
sha256sum path/to/site-a/resource.js path/to/site-b/resource.js
```

When a Lookyloo instance is available, capture the relevant entry URLs and check the expected findings in the tree and resource details. For correlation, capture both sites and allow indexing to complete before checking the connection. A successful browser preview alone does not verify the Lookyloo demonstration.

Do not claim a capture, deployment or integration was tested when it was unavailable. State what was checked and what remains to verify. Update the walkthrough when URLs, shared assets or expected behaviour change.

## Writing and communication style

Write natural, concise British English. Keep comments, documentation and responses practical. Avoid promotional language, stock introductions, padded explanations and repeating the same point in different words.

Do not use an em dash in documentation, comments, strings or responses. Use a comma, a full stop or rewrite the sentence.

Finish work with a short account of what changed, how it was checked and any relevant limitation.

## References

- [Lookyloo usage](https://www.lookyloo.eu/docs/main/usage.html)
- [Lookyloo interface](https://www.lookyloo.eu/docs/main/lookyloo-interface.html)
- [Python HTTP server](https://docs.python.org/3/library/http.server.html)
