# FBA Consulting Group — site (FR)
Static site. `cd src && python3 build.py` → `dist/`. Netlify: build `cd src && python3 build.py`, publish `dist` (see netlify.toml).

## Design system 2.0
Navy identity + champagne-gold accents, Lora (titles) and Inter (text), self-hosted in `src/fonts/` (OFL, no Google Fonts request). Service illustrations are original SVGs in `src/img/pillar-*.svg` (replace with commissioned photography if desired). Motion respects `prefers-reduced-motion`.

## Edit without touching the design
- `src/site.json`: WhatsApp number (digits, e.g. 221XXXXXXXXX), email, LinkedIn URLs (founder / company), booking_url (Calendly etc.), `review_flags` (false at launch removes all "À confirmer" tags), stats `confirmed`.
- `src/clients.json`: one entry per client. Put the supplied logo in `src/img/clients/` (original file, unmodified), set `logo`, fill known fields, and set `authorized: true` ONLY once the client has approved public use. Empty fields stay unpublished.
- `src/posts.json` ("Notre influence en action"): one entry per real LinkedIn post or campaign — `{"title","date","kind","excerpt","url","image","image_alt","metrics":[{"value","label"}],"metrics_verified":false,"metrics_source":""}`. `url` is required. Metrics only show when `metrics_verified` is true. Put images in `src/img/posts/`.
- `src/site.json` → `draft_placeholders`: true in the internal draft shows clearly labelled placeholder frames (posts, client logos, founder bio). **Set to false at launch**: placeholders disappear and only real material is shown.
- `src/site.json` → `stats`: every metric is shown with its source and date. Followers show only if `followers_verified`; impressions only if `impressions_verified` (fields `impressions`, `impressions_display`, `impressions_period`, `impressions_asof`, `impressions_growth_pct`, `impressions_source`, and the proof screenshot `impressions_proof` in `src/img/preuves/`). The growth bars are proportions computed from the growth % only; never add monthly figures that LinkedIn did not supply. `founder_bio`: list of paragraphs, confirmed by Fatoumata.
- `src/testimonials.json` ("Ils nous ont fait confiance"): one entry per real message. `category` = `candidat` or `entreprise`; `excerpt` copied word for word (use […] for cuts, [entreprise masquée] for hidden names); `capture` = anonymized screenshot in `src/img/temoignages/`. Names show only when `identity_authorized` is true and `author` is filled. Filters (Tous / Candidats / Entreprises) appear automatically from 6 testimonials. Set `published: false` to hide one.
- `src/cases.json`: case studies (title, sector, objective, strategy, results, images, links). Empty = "en préparation".
- Forms use Netlify Forms (`demande`, `rendez-vous`). After the first deploy: Netlify → Forms → enable e-mail notifications. Submissions are private (visible only in the Netlify dashboard) and carry `type_demande` so they can be filtered by inquiry type.
- Launch: remove `Disallow` in robots.txt / `noindex` meta, set `domain` in site.json.

## Not yet verified
Real delivery of forms (needs a Netlify deploy), WhatsApp number, social URLs, client logos & authorizations, founder bio, stats vs LinkedIn analytics.
