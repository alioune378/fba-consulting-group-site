# FBA Consulting Group — site (FR)
Static site. `cd src && python3 build.py` → `dist/`. Netlify: build `cd src && python3 build.py`, publish `dist` (see netlify.toml).

## Edit without touching the design
- `src/site.json`: WhatsApp number (digits, e.g. 221XXXXXXXXX), email, LinkedIn URLs (founder / company), booking_url (Calendly etc.), `review_flags` (false at launch removes all "À confirmer" tags), stats `confirmed`.
- `src/clients.json`: one entry per client. Put the supplied logo in `src/img/clients/` (original file, unmodified), set `logo`, fill known fields, and set `authorized: true` ONLY once the client has approved public use. Empty fields stay unpublished.
- `src/cases.json`: case studies (title, sector, objective, strategy, results, images, links). Empty = "en préparation".
- Forms use Netlify Forms (`demande`, `rendez-vous`). After the first deploy: Netlify → Forms → enable e-mail notifications. Submissions are private (visible only in the Netlify dashboard) and carry `type_demande` so they can be filtered by inquiry type.
- Launch: remove `Disallow` in robots.txt / `noindex` meta, set `domain` in site.json.

## Not yet verified
Real delivery of forms (needs a Netlify deploy), WhatsApp number, social URLs, client logos & authorizations, founder bio, stats vs LinkedIn analytics.
