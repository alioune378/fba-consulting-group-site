"""FBA Consulting Group — static site builder.   python3 build.py  ->  ../dist
Config: site.json · Clients: clients.json · Case studies: cases.json (all editable without touching design)."""
import json, shutil, re, html, hashlib, os, urllib.parse
from pathlib import Path

SRC = Path(__file__).parent; DIST = SRC.parent / "dist"
S = json.loads((SRC / "site.json").read_text(encoding="utf-8"))
CLIENTS = json.loads((SRC / "clients.json").read_text(encoding="utf-8"))
TALENTS = [t for t in json.loads((SRC / "talents.json").read_text(encoding="utf-8")) if t.get("approved")]
CASES = json.loads((SRC / "cases.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(str(s), quote=True)
FLAGS = S["review_flags"]
SHOW = os.environ.get("SHOW_UNAPPROVED") == "1"   # private preview only: shows unapproved client names
V = {f: hashlib.md5((SRC / "assets" / f).read_bytes()).hexdigest()[:8] for f in ("style.css", "app.js")}
NUM = re.sub(r"\D", "", S["whatsapp_number"])
WA = f"https://wa.me/{NUM}?text={urllib.parse.quote(S['whatsapp_message'])}" if NUM else "contact.html#whatsapp"

def draft(t="À confirmer"): return f'<span class="draft">{e(t)}</span>' if FLAGS else ""

ICONS = {
 "wa": '<path d="M20.5 3.5A11 11 0 0 0 3.2 16.8L2 22l5.3-1.4A11 11 0 1 0 20.5 3.5Zm-8.5 17a9 9 0 0 1-4.6-1.3l-.3-.2-3.1.8.8-3-.2-.3a9 9 0 1 1 7.4 4Zm5-6.7c-.3-.1-1.6-.8-1.9-.9s-.5-.1-.6.1l-.9 1.1c-.2.2-.3.2-.6.1a7.400 7.400 0 0 1-3.700-3.200c-.3-.5.3-.5.8-1.500.1-.2 0-.3 0-.5l-.9-2.100c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.200 5.200 5.200 0 0 0 1.100 2.800 11.800 11.800 0 0 0 4.600 4c1.700.7 2.400.8 3.200.7a2.700 2.700 0 0 0 1.800-1.300 2.200 2.200 0 0 0 .2-1.300c-.1-.1-.2-.2-.5-.3Z" fill="currentColor" stroke="none"/>',
 "in": '<path d="M4.500 9h3v10h-3zM6 4a1.750 1.750 0 1 1 0 3.500A1.750 1.750 0 0 1 6 4Zm4 5h2.900v1.400h.1c.4-.8 1.400-1.700 3-1.700 3.100 0 3.700 2 3.700 4.700V19h-3v-5c0-1.200 0-2.700-1.700-2.700S13 12.600 13 14v5h-3Z" fill="currentColor" stroke="none"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "check": '<path d="M5 12.500l4.500 4.500L19 7.500"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>', "close": '<path d="M6 6l12 12M18 6 6 18"/>',
 "cal": '<rect x="3.500" y="5" width="17" height="15" rx="2"/><path d="M8 3v4M16 3v4M3.500 10h17"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.500 7 8.500 6 8.500-6"/>',
 "eye": '<path d="M2.500 12S6 5.500 12 5.500 21.500 12 21.500 12 18 18.500 12 18.500 2.500 12 2.500 12Z"/><circle cx="12" cy="12" r="2.800"/>',
 "mega": '<path d="M4 10v4l11 4V6L4 10Z"/><path d="M7 14.500 8.500 20h3L10 15.500M18.500 9.500a3.500 3.500 0 0 1 0 5"/>',
 "post": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 "user": '<circle cx="12" cy="8" r="3.500"/><path d="M5 20c.8-3.600 3.600-5.500 7-5.500s6.200 1.900 7 5.500"/>',
 "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.500A1.500 1.500 0 0 1 10.500 4h3A1.500 1.500 0 0 1 15 5.500V7M3 13h18"/>',
 "star": '<path d="m12 3.500 2.600 5.300 5.800.8-4.200 4.100 1 5.800L12 16.800 6.800 19.500l1-5.800L3.600 9.600l5.800-.8L12 3.500Z"/>',
 "rocket": '<path d="M12 3c3.500 2 5.500 5.500 5 10l-2 2.500h-6L7 13c-.5-4.500 1.500-8 5-10Z"/><circle cx="12" cy="9.500" r="1.500"/><path d="M9 15.500 7 20l3-1.500M15 15.500l2 4.500-3-1.500"/>',
 "pin": '<path d="M12 21s-6.500-5.600-6.500-11a6.500 6.500 0 0 1 13 0c0 5.400-6.500 11-6.500 11Z"/><circle cx="12" cy="10" r="2.300"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.500 2.500M15.500 15.500 18 18M18 6l-2.500 2.500M8.500 15.500 6 18"/>',
}
def ic(n, cls=""): return f'<svg class="ic {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[n]}</svg>'

SERVICES = [
 ("Visibilité LinkedIn", "Développez votre présence et votre audience sur LinkedIn.", "eye"),
 ("Promotion d’entreprise ou de projet", "Faites connaître votre offre aux bonnes audiences.", "mega"),
 ("Publications sponsorisées", "Diffusez vos messages auprès de la communauté FBA.", "post"),
 ("Personal branding", "Construisez une image professionnelle cohérente.", "user"),
 ("Accompagnement des chercheurs d’emploi", "Valorisez votre parcours auprès des recruteurs.", "brief"),
 ("Valorisation des talents", "Mettez en lumière vos compétences et réalisations.", "star"),
 ("Promotion de projets entrepreneuriaux", "Donnez de la visibilité à votre initiative.", "rocket"),
]
CATEGORIES = [
 ("Entreprises", "Gagner en notoriété et valoriser votre marque employeur et vos offres."),
 ("Entrepreneurs et porteurs de projets", "Présenter votre initiative et attirer clients, partenaires et opportunités."),
 ("Professionnels et cadres", "Renforcer votre image professionnelle et votre réseau."),
 ("Chercheurs d’emploi", "Valoriser votre parcours et accroître votre visibilité."),
 ("Recruteurs", "Échanger sur vos besoins et entrer en relation avec des talents."),
 ("Institutions et organisations", "Communiquer vos initiatives et renforcer votre présence en ligne."),
]
JOBSVC = {"Accompagnement des chercheurs d’emploi", "Valorisation des talents"}
INQUIRY = ["Visibilité LinkedIn", "Promotion d’entreprise ou de projet", "Publications sponsorisées", "Personal branding",
           "Accompagnement chercheur d’emploi", "Valorisation de talents", "Promotion de projet entrepreneurial", "Partenariat"]
TIMELINES = ["Dès que possible", "Sous 1 mois", "Dans 1 à 3 mois", "Pas encore défini"]
NAV = [("index.html", "Accueil"), ("a-propos.html", "À propos"), ("services.html", "Nos services"),
       ("realisations.html", "Réalisations & Références"), ("contact.html", "Contact")]

def social(cls=""):
    items = [("linkedin_founder", "LinkedIn de Fatoumata Ba"), ("linkedin_company", "Page LinkedIn de FBA Consulting Group")]
    out = [f'<a class="soc" href="{e(S["social"][k])}" target="_blank" rel="noopener noreferrer" aria-label="{e(l)}">{ic("in")}</a>' for k, l in items if S["social"][k]]
    out += [f'<a class="soc" href="{e(o["url"])}" target="_blank" rel="noopener noreferrer" aria-label="{e(o["label"])}">{e(o["label"][:2])}</a>' for o in S["social"]["other"]]
    return f'<div class="socials {cls}">{"".join(out)}</div>' if out else ""

def page(fn, title, desc, body, og_title=None):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == fn else ""}>{l}</a>' for h, l in NAV)
    canon = f'<link rel="canonical" href="{S["domain"].rstrip("/")}/{"" if fn=="index.html" else fn}">' if S["domain"] else ""
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": S["name"], "description": S["tagline"], "founder": {"@type": "Person", "name": S["founder"]}, "areaServed": "SN", "telephone": "+" + NUM, "address": {"@type": "PostalAddress", "addressLocality": "Thiès", "addressCountry": "SN"}}
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="noindex, nofollow">{canon}
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:title" content="{e(og_title or title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:site_name" content="{e(S["name"])}">
<meta name="theme-color" content="#0B2D5B"><link rel="icon" href="img/favicon.png" type="image/png"><link rel="apple-touch-icon" href="img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/style.css?v={V["style.css"]}"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body data-wa="{e(WA)}"><a class="skip" href="#main">Aller au contenu</a>
<header class="header"><div class="wrap bar"><a class="brand" href="index.html" aria-label="FBA Consulting Group, accueil"><img src="img/fba-logo-420.webp" width="420" height="121" alt="FBA Consulting Group"></a>
<nav class="nav" id="nav" aria-label="Navigation principale">{nav}<a class="btn btn--sm nav-cta" href="contact.html#rendez-vous">Prendre rendez-vous</a></nav>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu">{ic("menu")}</button></div></header>
<main id="main" tabindex="-1">{body}</main>
<footer class="footer"><div class="wrap fgrid"><div class="f-brand"><img class="flogo" src="img/fba-logo-dark.png" width="150" height="130" alt="FBA Consulting Group" loading="lazy"><p>Visibilité LinkedIn, image professionnelle et promotion de projets pour entreprises, entrepreneurs et professionnels.</p>{social("on-dark")}</div>
<nav aria-label="Pied de page"><h2>Navigation</h2><ul>{"".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV + [("emploi-talents.html", "Emploi &amp; Talents")])}</ul></nav>
<div><h2>Contact</h2><ul><li><a href="contact.html#rendez-vous">Prendre rendez-vous</a></li><li><a href="contact.html#demande">Demande de devis</a></li><li><a href="{e(WA)}" target="_blank" rel="noopener">WhatsApp · {e(S["whatsapp_display"])}</a></li>{f'<li><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></li>' if S["email"] else ""}<li class="loc">{ic("pin")} {e(S["city"])}</li></ul></div></div>
<div class="wrap fbottom"><span>© <span id="yr">2026</span> FBA Consulting Group. Tous droits réservés.</span><span class="flinks"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Politique de confidentialité</a></span><span class="credit">Site web par Dalal Technologies</span></div></footer>
<a class="wa-float" href="{e(WA)}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp : {e(S["whatsapp_display"])}">{ic("wa")}<span>WhatsApp</span></a>
<script src="assets/app.js?v={V["app.js"]}" defer></script></body></html>'''

def head(eyebrow, h1, lede=""):
    return f'<section class="phero"><div class="wrap"><p class="eyebrow">{e(eyebrow)}</p><h1>{h1}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}</div></section>'

def cta_block():
    return f'''<section class="band band--navy cta"><div class="wrap cta-in reveal"><div><p class="eyebrow">Passons à l’action</p><h2>Parlons de votre visibilité et de vos projets.</h2><p>Choisissez le canal qui vous convient : un rendez-vous, une demande de devis ou un message WhatsApp.</p></div>
<div class="btn-row"><a class="btn" href="contact.html#rendez-vous">{ic("cal")} Prendre rendez-vous</a><a class="btn btn--ghost" href="contact.html#demande">Demander un devis</a><a class="btn btn--ghost" href="{e(WA)}" {"target=_blank rel=noopener" if NUM else ""}>{ic("wa")} WhatsApp</a></div></div></section>'''

# ---------- clients (data-driven) ----------
def client_visible(c): return c["authorized"] or SHOW
def client_tile(c):
    if c["authorized"] and c["logo"]:
        inner = f'<img src="img/clients/{e(c["logo"])}" alt="Logo {e(c["name"])}" loading="lazy" decoding="async">'
    else:
        inner = f'<span class="wordmark">{e(c["name"])}</span>'
    return f'<li class="tile"><div class="tile-box">{inner}</div></li>'

def clients_section(link=True):
    vis = [c for c in CLIENTS if client_visible(c)]
    if not vis: return ""
    more = '<p class="center"><a class="textlink" href="realisations.html">Voir les références ' + ic("arrow") + '</a></p>' if link else ""
    return f'''<section class="band band--paper clients" id="clients"><div class="wrap"><div class="shead center-h reveal"><p class="eyebrow">Références</p><h2>Ils nous font confiance</h2>
<p class="lede">Des entreprises et organisations qui font appel à FBA Consulting Group pour accompagner leurs ambitions de visibilité et de communication.</p></div>
<ul class="tiles reveal" aria-label="Clients de FBA Consulting Group">{"".join(client_tile(c) for c in vis)}</ul>{more}</div></section>'''

FIELDS = [("sector", "Secteur"), ("service", "Service fourni"), ("objectives", "Objectifs de la collaboration"), ("work", "Travail réalisé"), ("outcomes", "Résultats vérifiés")]
def client_card(c):
    rows = "".join(f'<div class="kv"><dt>{l}</dt><dd>{e(c[k])}</dd></div>' for k, l in FIELDS if c.get(k))
    quote = f'<figure class="quote"><blockquote>“{e(c["testimonial"])}”</blockquote><figcaption>{e(c["testimonial_author"])}</figcaption></figure>' if c.get("testimonial") and c.get("testimonial_author") else ""
    if not (rows or quote): return ""
    logo = f'<img src="img/clients/{e(c["logo"])}" alt="Logo {e(c["name"])}" loading="lazy" decoding="async">' if c["authorized"] and c["logo"] else f'<span class="wordmark">{e(c["name"])}</span>'
    return f'<article class="rcard reveal" id="{e(c["id"])}"><div class="rlogo">{logo}</div><div class="rbody"><h3>{e(c["name"])}</h3>{f"<dl class=kvs>{rows}</dl>" if rows else ""}{quote}</div></article>'

def case_card(c):
    def sec(k, l): return f'<div class="kv"><dt>{l}</dt><dd>{e(c[k])}</dd></div>' if c.get(k) else ""
    imgs = "".join(f'<img src="{e(i["src"])}" alt="{e(i.get("alt",""))}" loading="lazy" decoding="async">' for i in c.get("images", []))
    links = "".join(f'<li><a href="{e(l["url"])}" target="_blank" rel="noopener noreferrer">{e(l["label"])}</a></li>' for l in c.get("links", []))
    return f'<article class="case reveal"><h3>{e(c["title"])}</h3>{f"<p class=muted>{e(c["sector"])}</p>" if c.get("sector") else ""}<dl class="kvs">{sec("objective","Objectif de communication")}{sec("strategy","Stratégie mise en œuvre")}{sec("results","Résultats")}</dl>{f"<div class=cimgs>{imgs}</div>" if imgs else ""}{f"<ul class=clinks>{links}</ul>" if links else ""}</article>'

# ---------- pages ----------
PILLARS = [
 ("Entreprises & Entrepreneurs", "Promotion d’entreprise, visibilité de projets, publications stratégiques et communication professionnelle.", "pillar-entreprises.webp", "Promouvoir mon entreprise", "contact.html?service=" + urllib.parse.quote("Promotion d’entreprise ou de projet") + "#demande", "Fatoumata Ba, fondatrice de FBA Consulting Group, tenant une tablette"),
 ("Emploi & Talents", "Révision de CV, optimisation du profil LinkedIn, visibilité professionnelle et soutien aux chercheurs d’emploi.", "pillar-emploi.webp", "Valoriser mon profil", "emploi-talents.html", "Fatoumata Ba à son bureau"),
 ("Personal Branding & Influence", "Positionnement professionnel, valorisation de l’expertise, visibilité des dirigeants et personal branding sur LinkedIn.", "pillar-branding.webp", "Développer mon image", "contact.html?service=Personal%20branding#demande", "Portrait de Fatoumata Ba"),
]
def pillars():
    cards = "".join(f'''<li class="pillar{" pillar--feat" if i == 1 else ""} reveal"><a class="pillar-img" href="{h}" tabindex="-1" aria-hidden="true"><img src="img/{img}" width="800" height="600" alt="" loading="lazy" decoding="async"></a><div class="pillar-body"><h3>{e(t)}</h3><p>{e(d)}</p><a class="btn {"" if i == 1 else "btn--outline"}" href="{h}">{e(cta)} {ic("arrow")}</a></div></li>''' for i, (t, d, img, cta, h, alt) in enumerate(PILLARS))
    return f'''<section class="band" id="services"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Nos services</p><h2>Trois façons de gagner en visibilité</h2></div><ul class="pillars">{cards}</ul><p class="center"><a class="textlink" href="services.html">Voir nos sept services {ic("arrow")}</a></p></div></section>'''

BENEFITS = ["Révision et amélioration du CV", "Optimisation du profil LinkedIn", "Présentation et positionnement professionnels", "Visibilité des profils approuvés", "Préparation aux entretiens", "Exposition auprès d’audiences professionnelles"]
DISCLAIM = "Service de mise en visibilité et de réseautage professionnel. Aucun entretien, offre d’emploi ou recrutement n’est garanti."
def emploi_band():
    ben = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in BENEFITS)
    return f'''<section class="band band--navy emploi" id="emploi"><div class="wrap emploi-in"><div class="reveal"><p class="eyebrow on-dark">Emploi &amp; Talents</p><h2>Votre talent mérite d’être découvert.</h2><p class="lede">FBA Consulting Group accompagne les chercheurs d’emploi et les professionnels dans la valorisation de leur parcours, l’optimisation de leur présence LinkedIn et la mise en visibilité de leurs compétences auprès d’une communauté professionnelle.</p>
<div class="btn-row"><a class="btn" href="emploi-talents.html#candidature">Faire connaître mon profil</a><a class="btn btn--ghost" href="emploi-talents.html">Découvrir l’accompagnement emploi</a></div>
<p class="recruit-line">Vous recrutez ? <a href="emploi-talents.html#recruteurs">Parlons de vos besoins.</a></p></div>
<ul class="benefits reveal">{ben}</ul></div></section>'''

AUDIENCES = [
 ("Entreprises en quête de visibilité", "Demander un devis", "contact.html#demande"),
 ("Entrepreneurs qui promeuvent un projet", "Parler de mon projet", "contact.html?service=" + urllib.parse.quote("Promotion de projets entrepreneuriaux") + "#demande"),
 ("Professionnels qui construisent leur marque", "Développer mon image", "contact.html?service=Personal%20branding#demande"),
 ("Chercheurs d’emploi en quête d’exposition", "Faire connaître mon profil", "emploi-talents.html#candidature"),
 ("Recruteurs qui cherchent des talents", "Parlons de vos besoins", "emploi-talents.html#recruteurs"),
]
def talents_spotlight():
    if not TALENTS: return ""
    def row(k, l, t): return f'<div class="kv"><dt>{l}</dt><dd>{e(t[k])}</dd></div>' if t.get(k) else ""
    cards = "".join(f'<article class="case reveal"><dl class="kvs">{row("background","Parcours",t)}{row("challenge","Défi de visibilité",t)}{row("support","Accompagnement",t)}{row("publication","Publication",t)}{row("outcome","Résultat vérifié",t)}</dl></article>' for t in TALENTS)
    return f'<section class="band band--paper"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Impact</p><h2>Des talents mis en lumière.</h2></div><div class="cases">{cards}</div></div></section>'

def home():
    st = S["stats"]
    aud = "".join(f'<li class="reveal"><a class="aud" href="{h}"><span>{e(t)}</span><b>{e(c)} {ic("arrow")}</b></a></li>' for t, c, h in AUDIENCES)
    why = [("Une audience LinkedIn active", "Une communauté de plus de 83 000 abonnés pour porter vos messages."), ("Un interlocuteur direct", "Vous échangez avec la fondatrice pour cadrer votre besoin."), ("Une approche orientée image", "Chaque action sert votre crédibilité et vos objectifs."), ("Plusieurs façons de commencer", "Rendez-vous, devis ou message WhatsApp, à votre convenance.")]
    whyh = "".join(f'<li class="why reveal">{ic("check")}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for t, d in why)
    testi = [c for c in CLIENTS if c["authorized"] and c.get("testimonial") and c.get("testimonial_author")]
    tblk = ""
    if testi: tblk = f'''<section class="band band--paper"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Témoignages</p><h2>Ce que disent nos clients</h2></div><div class="grid g2">{"".join(f'<figure class="quote reveal"><blockquote>“{e(c["testimonial"])}”</blockquote><figcaption>{e(c["testimonial_author"])} · {e(c["name"])}</figcaption></figure>' for c in testi)}</div></div></section>'''
    li = f'<a class="textlink" href="{e(S["social"]["linkedin_founder"])}" target="_blank" rel="noopener noreferrer">Suivre Fatoumata sur LinkedIn {ic("arrow")}</a>' if S["social"]["linkedin_founder"] else ""
    return f'''<section class="hero"><div class="wrap hero-in"><div class="hero-copy"><p class="eyebrow on-dark">FBA Consulting Group</p>
<h1><span>Gagnez en visibilité.</span> <em>Affirmez votre expertise.</em></h1>
<p class="lede">Stratégie LinkedIn, personal branding et promotion de projets pour les entreprises, les entrepreneurs et les professionnels.</p>
<div class="cta-stack"><a class="btn btn--lg" href="contact.html#rendez-vous">{ic("cal")} Prendre rendez-vous</a><div class="cta-sec"><a class="btn btn--ghost" href="contact.html#demande">Demander un devis</a><a class="btn btn--ghost btn--wa-o" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} WhatsApp</a></div></div></div>
<figure class="hero-fig"><picture><source media="(max-width:820px)" srcset="img/fatoumata-ba-hero-900.webp"><img src="img/fatoumata-ba-hero-900.webp" width="900" height="1190" alt="Fatoumata Ba, fondatrice de FBA Consulting Group" fetchpriority="high"></picture></figure></div></section>
<section class="band band--navy stats" id="impact"><div class="wrap"><div class="stat-row"><div class="stat reveal"><b><span data-count="{st["followers"]}" data-prefix="+">+83 000</span></b><span>Abonnés LinkedIn</span></div><div class="stat reveal"><b><span data-count="{st["impressions_millions"]}" data-prefix="+" data-suffix=" millions">+28 millions</span></b><span>Impressions cumulées sur LinkedIn</span></div></div></div></section>
{clients_section()}
{pillars()}
{emploi_band()}
<section class="band band--paper"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Pour qui ?</p><h2>Un accompagnement pour chaque profil</h2></div><ul class="auds">{aud}</ul></div></section>
{talents_spotlight()}
<section class="band"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Pourquoi FBA ?</p><h2>Pourquoi travailler avec FBA Consulting Group</h2></div><ul class="grid g2">{whyh}</ul></div></section>
<section class="band band--paper founder"><div class="wrap founder-in2 reveal"><img class="avatar" src="img/fatoumata-ba-avatar.webp" width="360" height="360" alt="Fatoumata Ba" loading="lazy" decoding="async"><div><p class="eyebrow">La fondatrice</p><h2>Fatoumata Ba</h2><p class="lede">Fondatrice de FBA Consulting Group, Fatoumata Ba est une voix active sur LinkedIn, où elle fédère une communauté de plus de 83 000 abonnés.</p><p class="links"><a class="textlink" href="a-propos.html">En savoir plus {ic("arrow")}</a>{li}</p></div></div></section>
{tblk}{cta_block()}'''

def about():
    return head("À propos", "FBA Consulting Group", "Visibilité, image professionnelle et promotion de projets.") + f'''<section class="band"><div class="wrap two"><div class="reveal"><h2>Notre mission</h2><p class="lede">FBA Consulting Group aide les entreprises, les entrepreneurs et les professionnels à gagner en visibilité, à renforcer leur image professionnelle, à promouvoir leurs projets et à développer de nouvelles opportunités.</p><p>Basée à {e(S["city"])}, FBA Consulting Group accompagne ses clients sur LinkedIn à travers sept services : visibilité, promotion, publications sponsorisées, personal branding, accompagnement des chercheurs d’emploi, valorisation des talents et promotion de projets entrepreneuriaux.</p></div>
<figure class="reveal"><img src="img/fatoumata-ba-about-900.webp" width="900" height="1190" alt="Fatoumata Ba, fondatrice de FBA Consulting Group" loading="lazy" decoding="async"></figure></div></section>
<section class="band band--paper"><div class="wrap narrow reveal"><p class="eyebrow">La fondatrice</p><h2>Fatoumata Ba</h2><p class="lede">Fondatrice de FBA Consulting Group, Fatoumata Ba est une voix active sur LinkedIn, où elle fédère une communauté de plus de 83 000 abonnés.</p>{f'<a class="textlink" href="{e(S["social"]["linkedin_founder"])}" target="_blank" rel="noopener noreferrer">Suivre Fatoumata sur LinkedIn {ic("arrow")}</a>' if S["social"]["linkedin_founder"] else ""}</div></section>{cta_block()}'''

def services():
    cards = "".join(f'<li class="svc svc--lg reveal"><span class="svc-ic">{ic(i)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p><a class="textlink" href="{"emploi-talents.html" if t in JOBSVC else "contact.html?service=" + urllib.parse.quote(t) + "#demande"}">{"Découvrir l’accompagnement emploi" if t in JOBSVC else "Demander ce service"} {ic("arrow")}</a></div></li>' for t, d, i in SERVICES)
    cats = "".join(f'<li class="cat reveal"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in CATEGORIES)
    return head("Nos services", "Sept services pour développer votre visibilité", "Choisissez le service qui correspond à votre besoin, ou décrivez votre projet et nous vous orienterons.") + f'<section class="band"><div class="wrap"><ul class="grid g2 svcs">{cards}</ul></div></section><section class="band band--paper"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Solutions par profil</p><h2>Pour qui ?</h2></div><ul class="grid g3 cats">{cats}</ul></div></section>{cta_block()}'

def realisations():
    st = S["stats"]
    refs = "".join(client_card(c) for c in CLIENTS if client_visible(c))
    cases = "".join(case_card(c) for c in CASES)
    clients = clients_section(link=False)
    impact = f'''<section class="band band--navy stats"><div class="wrap"><div class="stat-row"><div class="stat reveal"><b><span data-count="{st["followers"]}" data-prefix="+">+83 000</span></b><span>Abonnés LinkedIn</span></div><div class="stat reveal"><b><span data-count="{st["impressions_millions"]}" data-prefix="+" data-suffix=" millions">+28 millions</span></b><span>Impressions cumulées sur LinkedIn</span></div></div></div></section>'''
    body = head("Réalisations & Impact", "Réalisations &amp; Impact", "Références clients et projets de FBA Consulting Group.") + impact + clients
    if refs: body += f'<section class="band" id="references"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Références clients</p><h2>Collaborations</h2></div><div class="rlist">{refs}</div></div></section>'
    if cases: body += f'<section class="band band--paper" id="etudes"><div class="wrap"><div class="shead reveal"><p class="eyebrow">Études de cas</p><h2>Projets et résultats</h2></div><div class="cases">{cases}</div></div></section>'
    else: body += '<section class="band"><div class="wrap narrow center-h reveal"><h2>Études de cas à venir</h2><p class="lede">Nous publierons prochainement des projets et des résultats. En attendant, parlons du vôtre.</p></div></section>'
    return body + cta_block()

def opts(items): return "".join(f"<option>{e(i)}</option>" for i in items)
def contact():
    mode = S["form_mode"]; fn_note = ""
    common = lambda name: f'<input type="hidden" name="form-name" value="{name}"><p class="hp" aria-hidden="true"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p><input type="hidden" name="t" value="">'
    booking = f'<a class="btn" href="{e(S["booking_url"])}" target="_blank" rel="noopener">{ic("cal")} Choisir un créneau en ligne</a>' if S["booking_url"] else ""
    return head("Contact", "Trois façons de nous contacter", "WhatsApp pour un échange immédiat, un formulaire pour une demande détaillée, ou un rendez-vous pour parler de votre projet.") + f'''
<section class="band"><div class="wrap"><div class="chan reveal"><a class="chan-c" href="#whatsapp">{ic("wa")}<h3>WhatsApp</h3><p>Écrivez-nous, réponse directe.</p></a><a class="chan-c" href="#demande">{ic("mail")}<h3>Demande d’information ou de devis</h3><p>Décrivez votre projet.</p></a><a class="chan-c" href="#rendez-vous">{ic("cal")}<h3>Rendez-vous</h3><p>Échangeons sur votre projet.</p></a></div></div></section>
<section class="band band--paper" id="whatsapp"><div class="wrap narrow reveal"><h2>WhatsApp</h2><p class="lede">Écrivez-nous directement au {e(S["whatsapp_display"])}. Un message prérempli s’ouvre dans WhatsApp.</p><a class="btn btn--wa" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} Ouvrir WhatsApp</a><p class="muted">{ic("pin","inl")} {e(S["city"])}</p></div></section>
<section class="band" id="demande"><div class="wrap narrow"><div class="shead reveal"><p class="eyebrow">Formulaire</p><h2>Demande d’information ou de devis</h2></div>
<form class="form reveal" name="demande" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("demande")}
<div class="row2"><div class="f"><label for="d-nom">Nom complet *</label><input id="d-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="d-org">Entreprise ou organisation</label><input id="d-org" name="organisation" autocomplete="organization"></div></div>
<div class="row2"><div class="f"><label for="d-email">E-mail *</label><input id="d-email" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="d-tel">WhatsApp ou téléphone *</label><input id="d-tel" name="telephone" type="tel" required autocomplete="tel"></div></div>
<div class="row2"><div class="f"><label for="d-cat">Votre profil *</label><select id="d-cat" name="categorie" required><option value="">Choisir…</option>{opts([c for c,_ in CATEGORIES])}</select></div><div class="f"><label for="d-type">Objet de la demande *</label><select id="d-type" name="type_demande" required><option value="">Choisir…</option>{opts(INQUIRY)}</select></div></div>
<div class="f"><label for="d-svc">Service souhaité</label><select id="d-svc" name="service"><option value="">À définir ensemble</option>{opts([x[0] for x in SERVICES])}</select></div>
<div class="f"><label for="d-desc">Description du projet *</label><textarea id="d-desc" name="description" rows="5" required minlength="20"></textarea></div>
<div class="row2"><div class="f"><label for="d-delai">Délai souhaité</label><select id="d-delai" name="delai"><option value="">Non précisé</option>{opts(TIMELINES)}</select></div><div class="f"><label for="d-budget">Budget estimé (facultatif)</label><input id="d-budget" name="budget" placeholder="Ex. : montant et devise"></div></div>
<div class="f chk"><input id="d-ok" name="consentement" type="checkbox" required><label for="d-ok">J’accepte que mes données soient utilisées par FBA Consulting Group pour répondre à ma demande. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn" type="submit">Envoyer ma demande</button><p class="status" role="status" aria-live="polite"></p></form></div></section>
<section class="band band--paper" id="rendez-vous"><div class="wrap narrow"><div class="shead reveal"><p class="eyebrow">Rendez-vous</p><h2>Prendre rendez-vous</h2><p class="lede">Proposez vos disponibilités pour échanger sur votre projet ou une collaboration. <strong>Un rendez-vous n’est confirmé qu’après la réponse de FBA Consulting Group</strong> par e-mail ou WhatsApp.</p></div>{booking}
<form class="form reveal" name="rendez-vous" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("rendez-vous")}
<div class="row2"><div class="f"><label for="r-nom">Nom complet *</label><input id="r-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="r-org">Entreprise ou organisation</label><input id="r-org" name="organisation"></div></div>
<div class="row2"><div class="f"><label for="r-email">E-mail *</label><input id="r-email" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="r-tel">WhatsApp ou téléphone *</label><input id="r-tel" name="telephone" type="tel" required autocomplete="tel"></div></div>
<div class="f"><label for="r-type">Sujet *</label><select id="r-type" name="type_demande" required><option value="">Choisir…</option>{opts(INQUIRY)}</select></div>
<div class="row2"><div class="f"><label for="r-date1">Date souhaitée (1er choix) *</label><input id="r-date1" name="date_1" type="date" required></div><div class="f"><label for="r-h1">Heure souhaitée *</label><input id="r-h1" name="heure_1" type="time" required></div></div>
<div class="row2"><div class="f"><label for="r-date2">2e choix (facultatif)</label><input id="r-date2" name="date_2" type="date"></div><div class="f"><label for="r-h2">Heure</label><input id="r-h2" name="heure_2" type="time"></div></div>
<div class="f"><label for="r-mode">Mode d’échange *</label><select id="r-mode" name="mode_echange" required><option value="">Choisir…</option><option>Visioconférence</option><option>Appel téléphonique</option><option>WhatsApp</option></select></div>
<div class="f"><label for="r-msg">Message (facultatif)</label><textarea id="r-msg" name="message" rows="3"></textarea></div>
<div class="f chk"><input id="r-ok" name="consentement" type="checkbox" required><label for="r-ok">J’accepte que mes données soient utilisées pour organiser ce rendez-vous. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn" type="submit">Envoyer ma demande de rendez-vous</button><p class="status" role="status" aria-live="polite"></p>
<ol class="steps"><li>Vous envoyez vos disponibilités.</li><li>FBA Consulting Group vous répond pour confirmer ou proposer un autre créneau.</li><li>Vous recevez la confirmation avec le mode d’échange.</li></ol></form></div></section>'''

def emploi():
    mode = S["form_mode"]; up = S.get("cv_upload", False)
    common = lambda name: f'<input type="hidden" name="form-name" value="{name}"><p class="hp" aria-hidden="true"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p><input type="hidden" name="t" value="">'
    ben = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in BENEFITS)
    steps = ["Vous envoyez votre candidature via le formulaire.", "FBA Consulting Group examine votre profil et vous répond.", "Nous échangeons sur la meilleure façon de valoriser votre parcours.", "Rien n’est publié sans votre accord écrit explicite."]
    cvfield = (f'<div class="f"><label for="c-cv">CV (facultatif · PDF, DOC ou DOCX · 7 Mo maximum)</label><input id="c-cv" name="cv" type="file" accept=".pdf,.doc,.docx,application/pdf" data-max="7340032"><span class="hint">Votre CV reste privé : il n’est jamais publié ni accessible par un lien public.</span></div>' if up else '<p class="hint">Vous pourrez nous transmettre votre CV après notre premier échange, par e-mail ou WhatsApp.</p>')
    enc = ' enctype="multipart/form-data"' if up else ""
    return head("Emploi & Talents", "Votre talent mérite d’être découvert.", "FBA Consulting Group accompagne les chercheurs d’emploi et les professionnels dans la valorisation de leur parcours, l’optimisation de leur présence LinkedIn et la mise en visibilité de leurs compétences auprès d’une communauté professionnelle.") + f'''
<section class="band"><div class="wrap two-c"><div class="reveal"><h2>Ce que nous faisons</h2><ul class="benefits benefits--light">{ben}</ul><p class="fine-l">{e(DISCLAIM)}</p></div>
<div class="reveal"><h2>Comment ça se passe</h2><ol class="steps steps--lg">{"".join(f"<li>{e(s)}</li>" for s in steps)}</ol><div class="btn-row"><a class="btn" href="#candidature">Faire connaître mon profil</a><a class="btn btn--outline" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} WhatsApp</a></div></div></div></section>
{talents_spotlight()}
<section class="band band--paper" id="candidature"><div class="wrap narrow"><div class="shead reveal"><p class="eyebrow">Candidature</p><h2>Faire connaître mon profil</h2></div>
<form class="form reveal" name="candidature" method="POST" data-netlify="true" netlify-honeypot="bot-field"{enc} data-mode="{mode}" novalidate>{common("candidature")}
<div class="row2"><div class="f"><label for="c-nom">Nom complet *</label><input id="c-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="c-email">E-mail *</label><input id="c-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row2"><div class="f"><label for="c-tel">Téléphone ou WhatsApp *</label><input id="c-tel" name="telephone" type="tel" required autocomplete="tel"></div><div class="f"><label for="c-loc">Localisation *</label><input id="c-loc" name="localisation" required placeholder="Ville, pays" autocomplete="address-level2"></div></div>
<div class="row2"><div class="f"><label for="c-dom">Domaine professionnel *</label><input id="c-dom" name="domaine" required></div><div class="f"><label for="c-niv">Niveau d’expérience *</label><select id="c-niv" name="niveau" required><option value="">Choisir…</option><option>Étudiant ou jeune diplômé</option><option>Moins de 3 ans</option><option>3 à 7 ans</option><option>8 ans et plus</option></select></div></div>
<div class="f"><label for="c-opp">Opportunité recherchée *</label><input id="c-opp" name="opportunite" required placeholder="Ex. : poste, secteur, type de contrat"></div>
<div class="f"><label for="c-pres">Brève présentation professionnelle *</label><textarea id="c-pres" name="presentation" rows="5" required minlength="30"></textarea></div>
{cvfield}
<div class="f chk"><input id="c-ok" name="consentement" type="checkbox" required><label for="c-ok">J’accepte que mes données soient utilisées par FBA Consulting Group pour traiter ma candidature. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<div class="f chk"><input id="c-pub" name="consentement_publication" type="checkbox"><label for="c-pub">Facultatif : j’autorise FBA Consulting Group à présenter mon profil publiquement (réseaux sociaux, site), uniquement après validation écrite du contenu avec moi.</label></div>
<button class="btn" type="submit">Envoyer ma candidature</button><p class="status" role="status" aria-live="polite"></p></form></div></section>
<section class="band" id="recruteurs"><div class="wrap narrow"><div class="shead reveal"><p class="eyebrow">Recruteurs</p><h2>Vous recrutez ? Parlons de vos besoins.</h2><p class="lede">Décrivez le profil recherché. FBA Consulting Group vous répond pour étudier comment mettre votre opportunité en visibilité auprès de sa communauté professionnelle.</p></div>
<form class="form reveal" name="recruteur" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("recruteur")}
<div class="row2"><div class="f"><label for="r-ent">Entreprise *</label><input id="r-ent" name="entreprise" required autocomplete="organization"></div><div class="f"><label for="r-nom2">Nom du contact *</label><input id="r-nom2" name="contact" required autocomplete="name"></div></div>
<div class="row2"><div class="f"><label for="r-em">E-mail professionnel *</label><input id="r-em" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="r-loc2">Localisation *</label><input id="r-loc2" name="localisation" required></div></div>
<div class="row2"><div class="f"><label for="r-fn">Fonction ou compétences recherchées *</label><input id="r-fn" name="fonction" required></div><div class="f"><label for="r-ty">Type d’opportunité *</label><select id="r-ty" name="type_opportunite" required><option value="">Choisir…</option><option>CDI</option><option>CDD</option><option>Stage</option><option>Mission freelance</option><option>Autre</option></select></div></div>
<div class="f"><label for="r-msg2">Message</label><textarea id="r-msg2" name="message" rows="4"></textarea></div>
<div class="f chk"><input id="r-ok2" name="consentement" type="checkbox" required><label for="r-ok2">J’accepte que mes données soient utilisées pour répondre à ma demande. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn" type="submit">Envoyer ma demande</button><p class="status" role="status" aria-live="polite"></p></form></div></section>{cta_block()}'''

def privacy():
    return head("Politique de confidentialité", "Confidentialité et données personnelles") + f'''<section class="band"><div class="wrap narrow prose"><p>Les informations saisies dans les formulaires (nom, organisation, e-mail, téléphone, description du projet, disponibilités, informations de candidature ou de recrutement) servent uniquement à répondre à votre demande ou à organiser un rendez-vous avec FBA Consulting Group. Elles ne sont pas affichées publiquement.</p><p>Aucun profil de candidat n’est publié sans accord écrit explicite de la personne concernée.</p><p>Les demandes sont reçues par l’intermédiaire du service de formulaires de l’hébergeur du site (Netlify) et consultées par FBA Consulting Group. Vous pouvez demander l’accès, la rectification ou la suppression de vos données par WhatsApp au {e(S["whatsapp_display"])} ou via le formulaire de contact.</p></div></section>'''

def legal():
    return head("Mentions légales", "Mentions légales") + f'''<section class="band"><div class="wrap narrow prose"><h2>Éditeur du site</h2><p>FBA Consulting Group, {e(S["city"])}.<br>Fondatrice : Fatoumata Ba.<br>Contact : WhatsApp {e(S["whatsapp_display"])}.</p><h2>Hébergement</h2><p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis.</p><h2>Propriété intellectuelle</h2><p>Les contenus, logos et photographies présents sur ce site sont la propriété de FBA Consulting Group ou de leurs titulaires respectifs et ne peuvent être réutilisés sans autorisation.</p></div></section>'''

def notfound():
    return head("Erreur 404", "Page introuvable", "Cette page n’existe pas ou a été déplacée.") + '<section class="band"><div class="wrap"><a class="btn" href="index.html">Retour à l’accueil</a></div></section>'

PAGES = {
 "index.html": ("FBA Consulting Group | Visibilité LinkedIn et image professionnelle", "FBA Consulting Group aide entreprises, entrepreneurs et professionnels à gagner en visibilité, valoriser leur image et promouvoir leurs projets.", home()),
 "a-propos.html": ("À propos | FBA Consulting Group", "Découvrez FBA Consulting Group et sa fondatrice, Fatoumata Ba.", about()),
 "services.html": ("Nos services | FBA Consulting Group", "Visibilité LinkedIn, personal branding, promotion de projets, publications sponsorisées et accompagnement des talents.", services()),
 "realisations.html": ("Réalisations & Impact | FBA Consulting Group", "Références clients et études de cas de FBA Consulting Group.", realisations()),
 "contact.html": ("Contact et rendez-vous | FBA Consulting Group", "Contactez FBA Consulting Group par WhatsApp, formulaire de devis ou demande de rendez-vous.", contact()),
 "mentions-legales.html": ("Mentions légales | FBA Consulting Group", "Mentions légales de FBA Consulting Group.", legal()),
 "emploi-talents.html": ("Emploi & Talents | FBA Consulting Group", "Faites connaître votre profil : CV, présence LinkedIn et visibilité professionnelle avec FBA Consulting Group. Recruteurs : parlons de vos besoins.", emploi()),
 "confidentialite.html": ("Confidentialité | FBA Consulting Group", "Politique de confidentialité de FBA Consulting Group.", privacy()),
 "404.html": ("Page introuvable | FBA Consulting Group", "Page introuvable.", notfound()),
}
if DIST.exists(): shutil.rmtree(DIST)
(DIST / "assets").mkdir(parents=True)
shutil.copytree(SRC / "img", DIST / "img")
for f in ("style.css", "app.js"): shutil.copy(SRC / "assets" / f, DIST / "assets" / f)
for fn, (t, d, b) in PAGES.items(): (DIST / fn).write_text(page(fn, t, d, b), encoding="utf-8")
(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n# Brouillon : retirer avant le lancement.\n")
print(f"Built {len(PAGES)} pages -> {DIST}")
