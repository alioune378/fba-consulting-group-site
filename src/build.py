"""FBA Consulting Group — static site builder.   python3 build.py  ->  ../dist
Config: site.json · Clients: clients.json · LinkedIn posts: posts.json · Case studies: cases.json · Talents: talents.json
(all editable without touching the design — see README.md)."""
import json, shutil, re, html, hashlib, os, urllib.parse
from pathlib import Path

SRC = Path(__file__).parent; DIST = SRC.parent / "dist"
def load(n): return json.loads((SRC / n).read_text(encoding="utf-8"))
S = load("site.json"); CLIENTS = load("clients.json"); CASES = load("cases.json")
POSTS = [p for p in load("posts.json") if p.get("url")]
TALENTS = [t for t in load("talents.json") if t.get("approved")]
TESTIS = [t for t in load("testimonials.json") if t.get("published")]
e = lambda s: html.escape(str(s), quote=True)
FLAGS = S["review_flags"]
DRAFT = S.get("draft_placeholders", False)        # internal draft: show labelled placeholders where material is missing
SHOW = os.environ.get("SHOW_UNAPPROVED") == "1"   # private preview only: shows unapproved client names
V = {f: hashlib.md5((SRC / "assets" / f).read_bytes()).hexdigest()[:8] for f in ("style.css", "app.js")}
NUM = re.sub(r"\D", "", S["whatsapp_number"])
WA = f"https://wa.me/{NUM}?text={urllib.parse.quote(S['whatsapp_message'])}" if NUM else "contact.html#whatsapp"
BASE = (S["domain"] or S.get("preview_url", "")).rstrip("/")
ST = S["stats"]; RK = S.get("ranking", {}); LI = S["social"]["linkedin_founder"]
fr = lambda n: f"{n:,}".replace(",", " ")

ICONS = {
 "wa": '<path d="M20.5 3.5A11 11 0 0 0 3.2 16.8L2 22l5.3-1.4A11 11 0 1 0 20.5 3.5Zm-8.5 17a9 9 0 0 1-4.6-1.3l-.3-.2-3.1.8.8-3-.2-.3a9 9 0 1 1 7.4 4Zm5-6.7c-.3-.1-1.6-.8-1.9-.9s-.5-.1-.6.1l-.9 1.1c-.2.2-.3.2-.6.1a7.4 7.4 0 0 1-3.7-3.2c-.3-.5.3-.5.8-1.5.1-.2 0-.3 0-.5l-.9-2.1c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.8 11.8 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3Z" fill="currentColor" stroke="none"/>',
 "in": '<path d="M4.5 9h3v10h-3zM6 4a1.75 1.75 0 1 1 0 3.5A1.75 1.75 0 0 1 6 4Zm4 5h2.9v1.4h.1c.4-.8 1.4-1.7 3-1.7 3.1 0 3.7 2 3.7 4.7V19h-3v-5c0-1.2 0-2.7-1.7-2.7S13 12.6 13 14v5h-3Z" fill="currentColor" stroke="none"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "menu": '<path d="M4 8h16M4 16h16"/>', "close": '<path d="M6 6l12 12M18 6 6 18"/>',
 "cal": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
 "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="2.8"/>',
 "mega": '<path d="M4 10v4l11 4V6L4 10Z"/><path d="M7 14.5 8.5 20h3L10 15.5M18.5 9.5a3.5 3.5 0 0 1 0 5"/>',
 "post": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>',
 "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 13h18"/>',
 "star": '<path d="m12 3.5 2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8 6.8 19.5l1-5.8L3.6 9.6l5.8-.8L12 3.5Z"/>',
 "rocket": '<path d="M12 3c3.5 2 5.5 5.5 5 10l-2 2.5h-6L7 13c-.5-4.5 1.5-8 5-10Z"/><circle cx="12" cy="9.5" r="1.5"/><path d="M9 15.5 7 20l3-1.5M15 15.5l2 4.5-3-1.5"/>',
 "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/>',
 "doc": '<path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20V3.5Z"/><path d="M14 3.5V8h4M10 12h5M10 15.5h5"/>',
 "chat": '<path d="M4.5 5.5h15v10h-8l-4.5 3.5v-3.5h-2.5z"/><path d="M8.5 9.5h7M8.5 12.5h4"/>',
 "search": '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
 "shield": '<path d="M12 3.5 19 6v5.5c0 4.4-3 7.8-7 9-4-1.2-7-4.6-7-9V6l7-2.5Z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
 "ext": '<path d="M14 4.5h5.5V10M19.5 4.5 11 13M18 14v5.5H4.5V6H10"/>',
}
def ic(n, cls=""): return f'<svg class="ic {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[n]}</svg>'

SERVICES = [
 ("Visibilité LinkedIn", "Développez votre présence et votre audience sur LinkedIn.", "eye", "branding"),
 ("Promotion d’entreprise ou de projet", "Faites connaître votre offre aux bonnes audiences.", "mega", "entreprises"),
 ("Publications sponsorisées", "Diffusez vos messages auprès de la communauté FBA.", "post", "entreprises"),
 ("Personal branding", "Construisez une image professionnelle cohérente.", "user", "branding"),
 ("Accompagnement des chercheurs d’emploi", "Valorisez votre parcours auprès des recruteurs.", "brief", "emploi"),
 ("Valorisation des talents", "Mettez en lumière vos compétences et réalisations.", "star", "emploi"),
 ("Promotion de projets entrepreneuriaux", "Donnez de la visibilité à votre initiative.", "rocket", "entreprises"),
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
NAV = [("index.html", "Accueil"), ("a-propos.html", "À propos"), ("services.html", "Services"),
       ("emploi-talents.html", "Emploi & Talents"), ("realisations.html", "Réalisations"), ("contact.html", "Contact")]

def svc_href(t): return "emploi-talents.html" if t in JOBSVC else "contact.html?service=" + urllib.parse.quote(t) + "#demande"

def social(cls=""):
    items = [("linkedin_founder", "LinkedIn de Fatoumata Ba"), ("linkedin_company", "Page LinkedIn de FBA Consulting Group")]
    out = [f'<a class="soc" href="{e(S["social"][k])}" target="_blank" rel="noopener noreferrer" aria-label="{e(l)}">{ic("in")}</a>' for k, l in items if S["social"][k]]
    out += [f'<a class="soc" href="{e(o["url"])}" target="_blank" rel="noopener noreferrer" aria-label="{e(o["label"])}">{e(o["label"][:2])}</a>' for o in S["social"]["other"]]
    return f'<div class="socials {cls}">{"".join(out)}</div>' if out else ""

def page(fn, title, desc, body, og_title=None):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == fn else ""}>{e(l)}</a>' for h, l in NAV)
    canon = f'<link rel="canonical" href="{S["domain"].rstrip("/")}/{"" if fn=="index.html" else fn}">' if S["domain"] else ""
    url = f'{BASE}/{"" if fn=="index.html" else fn}'
    ogimg = f'<meta property="og:image" content="{BASE}/img/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">' if BASE else ""
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": S["name"], "description": S["tagline"], "founder": {"@type": "Person", "name": S["founder"]}, "areaServed": "SN", "telephone": "+" + NUM, "address": {"@type": "PostalAddress", "addressLocality": "Thiès", "addressCountry": "SN"}}
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="noindex, nofollow">{canon}
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:title" content="{e(og_title or title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:site_name" content="{e(S["name"])}">{f'<meta property="og:url" content="{e(url)}">' if BASE else ""}{ogimg}
<meta name="theme-color" content="#071A36"><link rel="icon" href="img/favicon.png" type="image/png"><link rel="apple-touch-icon" href="img/favicon.png">
<link rel="preload" href="fonts/lora.woff" as="font" type="font/woff" crossorigin><link rel="preload" href="fonts/inter-regular.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/style.css?v={V["style.css"]}"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body data-wa="{e(WA)}"><a class="skip" href="#main">Aller au contenu</a>
<header class="header"><div class="wrap bar"><a class="brand" href="index.html" aria-label="FBA Consulting Group, accueil"><img src="img/fba-logo-420.webp" width="420" height="121" alt="FBA Consulting Group"></a>
<nav class="nav" id="nav" aria-label="Navigation principale">{nav}<a class="btn btn--navy btn--sm nav-cta" href="contact.html#rendez-vous">Prendre rendez-vous</a></nav>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span></span><span></span></button></div></header>
<main id="main" tabindex="-1">{body}</main>
<footer class="footer"><div class="wrap fgrid"><div class="f-brand"><img class="flogo" src="img/fba-logo-dark.png" width="150" height="130" alt="FBA Consulting Group" loading="lazy"><p>Visibilité LinkedIn, image professionnelle et promotion de projets pour entreprises, entrepreneurs et professionnels.</p>{social("on-dark")}</div>
<nav aria-label="Pied de page"><h2>Navigation</h2><ul>{"".join(f'<li><a href="{h}">{e(l)}</a></li>' for h, l in NAV)}</ul></nav>
<div><h2>Contact</h2><ul><li><a href="contact.html#rendez-vous">Prendre rendez-vous</a></li><li><a href="contact.html#demande">Demande de devis</a></li><li><a href="{e(WA)}" target="_blank" rel="noopener">WhatsApp · {e(S["whatsapp_display"])}</a></li>{f'<li><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></li>' if S["email"] else ""}<li class="loc">{ic("pin")} {e(S["city"])}</li></ul></div></div>
<div class="wrap fbottom"><span>© <span id="yr">2026</span> FBA Consulting Group. Tous droits réservés.</span><span class="flinks"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Politique de confidentialité</a></span><span class="credit">Site web par Dalal Technologies</span></div></footer>
<a class="wa-float" href="{e(WA)}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp : {e(S["whatsapp_display"])}">{ic("wa")}<span>WhatsApp</span></a>
<script src="assets/app.js?v={V["app.js"]}" defer></script></body></html>'''

def head(eyebrow, h1, lede="", extra=""):
    return f'<section class="phero"><div class="wrap"><p class="eyebrow on-dark">{e(eyebrow)}</p><h1>{h1}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}{extra}</div></section>'

def shead(eyebrow, h2, lede="", cls="", dark=False):
    return f'<div class="shead {cls} reveal"><p class="eyebrow{" on-dark" if dark else ""}">{e(eyebrow)}</p><h2>{h2}</h2>{f"<p class=lede>{lede}</p>" if lede else ""}</div>'

def placeholder_note(t): return f'<p class="ph-note">{ic("doc","inl")} {e(t)}</p>' if DRAFT else ""

def cta_block():
    return f'''<section class="band band--ink cta"><div class="wrap cta-in reveal"><div><p class="eyebrow on-dark">Travaillons ensemble</p><h2>Parlons de votre visibilité et de vos projets.</h2><p>Un rendez-vous, une demande de devis ou un message WhatsApp : choisissez le canal qui vous convient.</p></div>
<div class="cta-actions"><a class="btn btn--gold btn--lg" href="contact.html#rendez-vous">{ic("cal")} Prendre rendez-vous</a><div class="cta-sec"><a class="btn btn--ghost" href="contact.html#demande">Demander un devis</a><a class="btn btn--ghost" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} WhatsApp</a></div></div></div></section>'''

# ---------- audience / metrics (only verified, always attributed) ----------
def proof_dialog():
    if not (ST.get("impressions_verified") and ST.get("impressions_proof")): return ""
    return f'''<dialog class="proof-dlg" id="preuve-linkedin" aria-labelledby="preuve-t"><div class="proof-dlg-in"><div class="proof-dlg-h"><p id="preuve-t">Statistiques LinkedIn · {e(ST["impressions_period"])} · {e(ST["impressions_asof"])}</p><button type="button" class="proof-close" data-close aria-label="Fermer">{ic("close")}</button></div>
<img src="{e(ST["impressions_proof"])}" width="1290" height="1822" alt="Capture des statistiques LinkedIn de Fatoumata Ba : {fr(ST["impressions"])} impressions sur 365 jours, +{ST["impressions_growth_pct"]} % par rapport aux 365 jours précédents." loading="lazy" decoding="async"><p class="m-src">{e(ST["impressions_source"])}. Capture originale, recadrée uniquement pour retirer les bandes noires.</p></div></dialog>'''

def metrics(cls=""):
    kpis = []
    imp = ST.get("impressions_verified")
    if imp:
        kpis.append(f'''<div class="kpi kpi--lead reveal"><p class="kpi-k">Impressions · {e(ST["impressions_period"])}</p><p class="kpi-v"><span data-count="29" data-prefix="+" data-suffix=" M">+29 M</span></p><p class="kpi-l">Plus de {e(ST["impressions_display"])} d’impressions sur LinkedIn en {e(ST["impressions_period"])}</p>
<p class="kpi-g">{ic("arrow","up")}<b>+{ST["impressions_growth_pct"]}&nbsp;%</b> d’impressions par rapport à la période précédente</p><p class="m-src">{fr(ST["impressions"])} impressions · {e(ST["impressions_asof"])}</p></div>''')
    if ST.get("followers_verified"):
        kpis.append(f'<div class="kpi reveal"><p class="kpi-k">Communauté</p><p class="kpi-v"><span data-count="{ST["followers"]}" data-prefix="+">+{fr(ST["followers"])}</span></p><p class="kpi-l">abonnés LinkedIn</p><p class="m-src">{e(ST["followers_source"])} · relevé le {e(ST["followers_asof"])}</p></div>')
    if RK.get("enabled"):
        kpis.append(f'<div class="kpi reveal"><p class="kpi-k">Reconnaissance</p><p class="kpi-v">N°&nbsp;{RK["rank"]}</p><p class="kpi-l">{e(RK["scope"])}</p><p class="m-src">Classement {e(RK["source"])} · {e(RK["asof"])}</p></div>')
    if not kpis: return ""
    growth = ""
    if imp:
        g = ST["impressions_growth_pct"]; prev = round(100 / (100 + g) * 100, 1)
        growth = f'''<div class="growth reveal" role="img" aria-label="Croissance des impressions : +{g} % par rapport aux 365 jours précédents"><p class="kpi-k">Croissance des impressions</p>
<div class="gbar"><span class="gbar-l">365 jours précédents</span><span class="gbar-t"><span class="gbar-f gbar-f--prev" style="--w:{prev}%"></span></span></div>
<div class="gbar"><span class="gbar-l">365 derniers jours</span><span class="gbar-t"><span class="gbar-f" style="--w:100%"></span></span><b>+{g}&nbsp;%</b></div>
<p class="m-src">Proportions calculées à partir de la croissance affichée par LinkedIn. Aucune donnée mensuelle n’est reconstituée.</p></div>'''
    proof = f'''<figure class="proof reveal"><a class="proof-shot" href="{e(ST["impressions_proof"])}" target="_blank" rel="noopener" data-dialog="preuve-linkedin" aria-label="Voir la capture des statistiques LinkedIn en grand"><img src="{e(ST["impressions_proof_small"])}" width="720" height="1017" alt="Capture des statistiques LinkedIn : {fr(ST["impressions"])} impressions en 365 jours, +{ST["impressions_growth_pct"]} %" loading="lazy" decoding="async"></a>
<figcaption><span>Capture originale · LinkedIn</span><a class="textlink" href="{e(ST["impressions_proof"])}" target="_blank" rel="noopener" data-dialog="preuve-linkedin">Voir les statistiques {ic("arrow")}</a></figcaption></figure>''' if imp and ST.get("impressions_proof") else ""
    li = f'<a class="textlink" href="{e(LI)}" target="_blank" rel="noopener noreferrer">{ic("in")} Voir le profil LinkedIn {ic("ext")}</a>' if LI else ""
    src = f'Source : statistiques LinkedIn communiquées par Fatoumata Ba, période de {e(ST["impressions_period"])} se terminant en {e(ST["impressions_asof"])}.' if imp else ""
    return f'''<section class="band band--ink dash {cls}" id="audience"><div class="wrap">{shead("L’audience", "Une audience établie, en forte croissance.", "Les chiffres clés de la communauté LinkedIn de Fatoumata Ba, chacun présenté avec sa source.", dark=True)}
<div class="dash-grid"><div class="dash-main"><div class="kpis">{"".join(kpis)}</div>{growth}</div>{proof}</div>
<div class="dash-foot reveal"><p class="m-src">{src} Abonnés : {e(ST["followers_source"])}, relevé le {e(ST["followers_asof"])}.{f" Classement : {e(RK['source'])}, {e(RK['asof'])}." if RK.get("enabled") else ""}</p>{li}</div></div></section>{proof_dialog()}'''

BENEFITS_FOR = [
 ("Entreprises", "brief", ["Présenter vos offres, événements ou recrutements à une large audience professionnelle.", "Associer votre marque à une voix reconnue sur LinkedIn.", "Des publications rédigées et calibrées pour ce réseau."], "Promouvoir mon entreprise", "contact.html?service=" + urllib.parse.quote("Promotion d’entreprise ou de projet") + "#demande"),
 ("Entrepreneurs", "rocket", ["Faire découvrir un projet, un produit ou un lancement.", "Toucher des clients et partenaires potentiels au-delà de votre réseau.", "Clarifier votre message et votre positionnement."], "Parler de mon projet", "contact.html?service=" + urllib.parse.quote("Promotion de projets entrepreneuriaux") + "#demande"),
 ("Chercheurs d’emploi", "user", ["Un CV et un profil LinkedIn plus clairs pour les recruteurs.", "Une mise en visibilité auprès d’une communauté professionnelle, avec votre accord écrit.", "Mieux présenter votre parcours en entretien."], "Valoriser mon profil", "emploi-talents.html"),
]
def benefits_for():
    cards = "".join(f'''<li class="bcard reveal"><span class="offer-ic">{ic(i)}</span><h3>{e(t)}</h3><ul>{"".join(f"<li>{ic('check')}<span>{e(x)}</span></li>" for x in items)}</ul><a class="textlink" href="{h}">{e(cta)} {ic("arrow")}</a></li>''' for t, i, items, cta, h in BENEFITS_FOR)
    return f'''<section class="band band--ivory benefits-for"><div class="wrap">{shead("Ce que cette audience vous apporte", "Une visibilité au service de vos objectifs.", "Chaque accompagnement est construit autour de votre objectif : vendre, lancer, recruter ou être recruté.")}
<ul class="bcards">{cards}</ul><p class="fine-l reveal">La portée d’une publication varie selon le sujet et le moment. Aucun résultat commercial, entretien ou recrutement n’est garanti.</p></div></section>'''

# ---------- pillars ----------
PILLARS = [
 ("entreprises", "01", "Entreprises & Entrepreneurs", "Promotion d’entreprise, visibilité de projets, publications stratégiques et communication professionnelle.", "Promouvoir mon entreprise", "contact.html?service=" + urllib.parse.quote("Promotion d’entreprise ou de projet") + "#demande"),
 ("emploi", "02", "Emploi & Talents", "Révision de CV, optimisation du profil LinkedIn, visibilité professionnelle et soutien aux chercheurs d’emploi.", "Valoriser mon profil", "emploi-talents.html"),
 ("branding", "03", "Personal Branding & Influence", "Positionnement professionnel, valorisation de l’expertise, visibilité des dirigeants et personal branding sur LinkedIn.", "Développer mon image", "contact.html?service=Personal%20branding#demande"),
]
def pillars():
    cards = "".join(f'''<li class="pillar reveal"><a class="pillar-link" href="{h}"><span class="pillar-img"><img src="img/pillar-{k}.svg" width="800" height="600" alt="" loading="lazy" decoding="async"></span>
<span class="pillar-body"><span class="pillar-n">{n}</span><span class="pillar-t">{e(t)}</span><span class="pillar-d">{e(d)}</span><span class="pillar-cta">{e(cta)} {ic("arrow")}</span></span></a></li>''' for k, n, t, d, cta, h in PILLARS)
    return f'''<section class="band" id="services"><div class="wrap">{shead("Nos expertises", "Trois leviers pour gagner en visibilité.")}<ul class="pillars">{cards}</ul><p class="more reveal"><a class="textlink" href="services.html">Voir le détail des sept services {ic("arrow")}</a></p></div></section>'''

# ---------- influence in action (real posts only; labelled placeholders in the internal draft) ----------
PH_POSTS = [("Publication sponsorisée", "Une offre ou un événement présenté à la communauté FBA."), ("Promotion d’entreprise", "La mise en avant d’une entreprise cliente, avec son accord."), ("Visibilité d’un talent", "Un profil valorisé, après validation écrite de la personne.")]
def post_card(p):
    img = f'<img class="post-img" src="{e(p["image"])}" alt="{e(p.get("image_alt",""))}" loading="lazy" decoding="async">' if p.get("image") else ""
    mt = "".join(f'<li><b>{e(m["value"])}</b> {e(m["label"])}</li>' for m in p.get("metrics", [])) if p.get("metrics_verified") else ""
    mt = f'<ul class="post-metrics">{mt}</ul><p class="m-src">{e(p.get("metrics_source",""))}</p>' if mt else ""
    return f'''<li class="post reveal"><article><header class="post-h"><img class="post-av" src="img/fatoumata-ba-avatar.webp" width="40" height="40" alt="" loading="lazy"><span><b>Fatoumata Ba</b><small>{e(p.get("date",""))}</small></span><span class="post-kind">{e(p.get("kind","Publication"))}</span></header>
<h3>{e(p["title"])}</h3>{f'<p>{e(p["excerpt"])}</p>' if p.get("excerpt") else ""}{img}{mt}<a class="textlink" href="{e(p["url"])}" target="_blank" rel="noopener noreferrer">Voir sur LinkedIn {ic("ext")}</a></article></li>'''
def ph_card(kind, d):
    return f'''<li class="post post--ph reveal" aria-label="Emplacement réservé : {e(kind)}"><article><header class="post-h"><span class="post-av ph-av"></span><span><b>Fatoumata Ba</b><small>Date de publication</small></span><span class="post-kind">{e(kind)}</span></header>
<span class="ph-line w90"></span><span class="ph-line w70"></span><span class="ph-img"><span>{e(d)}</span></span><p class="ph-tag">{ic("doc","inl")} Publication authentique à fournir</p></article></li>'''
def influence(dark=True):
    if POSTS: cards = "".join(post_card(p) for p in POSTS)
    elif DRAFT: cards = "".join(ph_card(k, d) for k, d in PH_POSTS)
    else: return ""
    note = '' if POSTS else placeholder_note("Brouillon interne : ces cadres seront remplacés par de vraies publications et campagnes LinkedIn (src/posts.json). Ils ne s’affichent pas une fois draft_placeholders désactivé.")
    return f'''<section class="band band--ink influence" id="influence"><div class="wrap">{shead("Notre influence en action", "Des messages portés auprès d’une audience qui écoute.", "Publications et campagnes réalisées sur LinkedIn, présentées avec l’accord des personnes et entreprises concernées.", dark=True)}
<ul class="posts" tabindex="0" aria-label="Publications LinkedIn">{cards}</ul>{note}</div></section>'''

# ---------- clients (data-driven; names/logos only once authorized) ----------
def client_visible(c): return c["authorized"] or SHOW
def client_tile(c, i):
    if c["authorized"] and c["logo"]: inner = f'<img src="img/clients/{e(c["logo"])}" alt="Logo {e(c["name"])}" loading="lazy" decoding="async">'
    elif client_visible(c): inner = f'<span class="wordmark">{e(c["name"])}</span>'
    else: inner = '<span class="wordmark wordmark--ph">Logo client<small>autorisation en attente</small></span>'
    return f'<li class="tile{"" if client_visible(c) else " tile--ph"}"><span class="tile-n">{i:02d}</span>{inner}</li>'
def clients_section(link=True):
    vis = [c for c in CLIENTS if client_visible(c)]
    shown = CLIENTS if (DRAFT and not SHOW and len(vis) < len(CLIENTS)) else vis
    if not shown: return ""
    more = f'<p class="more reveal"><a class="textlink" href="realisations.html">Voir les références {ic("arrow")}</a></p>' if link and vis else ""
    note = placeholder_note("Brouillon interne : les noms et logos des clients n’apparaissent qu’après leur autorisation écrite (src/clients.json → authorized).") if len(vis) < len(CLIENTS) else ""
    return f'''<section class="band band--ivory clients" id="clients"><div class="wrap">{shead("Références", "Ils nous font confiance.", "Des entreprises sénégalaises qui font appel à FBA Consulting Group pour leur visibilité et leur communication.", "center-h")}
<ul class="tiles reveal" aria-label="Clients de FBA Consulting Group">{"".join(client_tile(c, i+1) for i, c in enumerate(shown))}</ul>{more}{note}</div></section>'''

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

# ---------- testimonials (real messages only; see testimonials.json) ----------
TCAT = {"candidat": ("Candidats", "user"), "entreprise": ("Entreprises", "brief")}
def testi_card(t):
    who = t["author"] if t.get("identity_authorized") and t.get("author") else t["label"]
    sub = " · ".join(x for x in [t.get("role") if t.get("identity_authorized") else "", t.get("channel", ""), t.get("date", "")] if x)
    mt = "".join(f'<li><b>{e(m["value"])}</b> {e(m["label"])}</li>' for m in t.get("metrics", []))
    mt = f'<ul class="t-metrics" aria-label="{e(t.get("metrics_source",""))}">{mt}</ul>' if mt else ""
    did = f'temoignage-{t["id"]}'
    dlg = f'''<dialog class="proof-dlg" id="{did}" aria-labelledby="{did}-t"><div class="proof-dlg-in"><div class="proof-dlg-h"><p id="{did}-t">Témoignage original · {e(t["label"])}</p><button type="button" class="proof-close" data-close aria-label="Fermer">{ic("close")}</button></div>
<img src="{e(t["capture"])}" width="{t["capture_w"]}" height="{t["capture_h"]}" alt="Capture du témoignage : {e(t["excerpt"])}" loading="lazy" decoding="async"><p class="m-src">{e(t.get("capture_note",""))}</p></div></dialog>'''
    cat, icn = TCAT[t["category"]]
    return f'''<li class="tcard tcard--{t["category"]} reveal" data-cat="{t["category"]}"><figure><span class="t-badge">{ic(icn)} {e(t["label"])}</span>
<span class="t-mark" aria-hidden="true">“</span><blockquote><p>{e(t["excerpt"])}</p></blockquote><p class="t-ex">Extrait fidèle du message original</p>
{f'<p class="t-out">{ic("check")}<span>{e(t["outcome"])}</span></p>' if t.get("outcome") else ""}{mt}
<figcaption><span><b>{e(who)}</b>{f"<small>{e(sub)}</small>" if sub else ""}</span><a class="textlink" href="{e(t["capture"])}" target="_blank" rel="noopener" data-dialog="{did}">Voir le témoignage original {ic("arrow")}</a></figcaption></figure>{dlg}</li>'''
def testimonials():
    if not TESTIS: return ""
    order = sorted(TESTIS, key=lambda t: t["category"] != "candidat")
    cats = {t["category"] for t in TESTIS}
    filt = ""
    if len(TESTIS) >= 6 and len(cats) > 1:
        btn = lambda v, l, on=False: f'<button type="button" class="tf{" is-on" if on else ""}" data-filter="{v}" aria-pressed="{str(on).lower()}">{l}</button>'
        filt = f'<div class="tfilters reveal" role="group" aria-label="Filtrer les témoignages">{btn("all","Tous",True)}{btn("candidat","Candidats")}{btn("entreprise","Entreprises")}</div>'
    return f'''<section class="band band--ivory testis" id="temoignages"><div class="wrap">{shead("Témoignages", "Ils nous ont fait confiance. Voici leurs résultats.", "Derrière chaque opportunité se trouvent des parcours, des rencontres et des réussites. Découvrez les retours de ceux que nous avons accompagnés.")}
{filt}<ul class="tcards">{"".join(testi_card(t) for t in order)}</ul>
<div class="t-cta reveal"><a class="btn btn--navy btn--lg" href="emploi-talents.html#candidature">{ic("user")} Je recherche un emploi</a><a class="btn btn--outline btn--lg" href="emploi-talents.html#recruteurs">{ic("brief")} Je souhaite recruter</a></div>
<p class="fine-l reveal">Messages reçus par Fatoumata Ba, présentés en extraits sans modification des propos. Les noms sont masqués faute d’autorisation de publication. Chaque parcours est unique : aucun résultat n’est garanti.</p></div></section>'''

# ---------- emploi & talents ----------
OFFERS = [
 ("search", "Visibilité des candidats", "Votre profil présenté à une communauté professionnelle, uniquement après votre accord écrit sur le contenu."),
 ("doc", "Révision du CV", "Un CV plus clair et mieux structuré, qui met en avant vos compétences et vos réalisations."),
 ("in", "Optimisation LinkedIn", "Titre, résumé, expériences : un profil cohérent et lisible par les recruteurs."),
 ("chat", "Préparation aux entretiens", "Présenter votre parcours avec assurance et clarté."),
]
DISCLAIM = "Service de mise en visibilité et de réseautage professionnel. Aucun entretien, offre d’emploi ou recrutement n’est garanti."
def offers_list(cls=""):
    return f'<ul class="offers {cls}">' + "".join(f'<li class="offer reveal"><span class="offer-ic">{ic(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, t, d in OFFERS) + '</ul>'
def pathways():
    return f'''<div class="paths reveal"><a class="path path--gold" href="emploi-talents.html#candidature"><span class="path-k">Candidats</span><b>Je cherche une opportunité</b><span>Faire connaître mon profil {ic("arrow")}</span></a>
<a class="path" href="emploi-talents.html#recruteurs"><span class="path-k">Recruteurs</span><b>Je recrute</b><span>Parlons de vos besoins {ic("arrow")}</span></a></div>'''
def emploi_band():
    return f'''<section class="band band--sand emploi" id="emploi"><div class="wrap"><div class="emploi-top"><div>{shead("Emploi & Talents", "Votre talent mérite d’être découvert.", "Révision de CV, optimisation LinkedIn et mise en visibilité : un accompagnement pour les chercheurs d’emploi et les professionnels qui veulent être vus.")}</div>
<figure class="emploi-art reveal"><img src="img/pillar-emploi.svg" width="800" height="600" alt="" loading="lazy" decoding="async"></figure></div>
{offers_list()}{pathways()}<p class="fine-l reveal">{e(DISCLAIM)}</p></div></section>'''

def talents_spotlight():
    if not TALENTS: return ""
    def row(k, l, t): return f'<div class="kv"><dt>{l}</dt><dd>{e(t[k])}</dd></div>' if t.get(k) else ""
    cards = "".join(f'<article class="case reveal"><dl class="kvs">{row("background","Parcours",t)}{row("challenge","Défi de visibilité",t)}{row("support","Accompagnement",t)}{row("publication","Publication",t)}{row("outcome","Résultat vérifié",t)}</dl></article>' for t in TALENTS)
    return f'<section class="band band--ivory"><div class="wrap">{shead("Impact", "Des talents mis en lumière.")}<div class="cases">{cards}</div></div></section>'

# ---------- founder story (confirmed facts only) ----------
def founder_story(full=False):
    rk = f' En {e(RK["asof"])}, le classement {e(RK["source"])} la place au <strong>n°&nbsp;{RK["rank"]}</strong> des {e(RK["scope"][0].lower() + RK["scope"][1:])}.' if RK.get("enabled") else ""
    bio = "".join(f"<p>{e(x)}</p>" for x in S.get("founder_bio", []))
    if not bio: bio = placeholder_note("Brouillon interne : parcours détaillé (formation, expériences, dates clés) à fournir et valider par Fatoumata Ba (src/site.json → founder_bio).")
    facts = [("Audience", f"+{fr(ST['followers'])} abonnés LinkedIn", f"relevé le {ST['followers_asof']}")]
    if ST.get("impressions_verified"): facts.append(("Portée", f"+{ST['impressions_display']} d’impressions", f"{ST['impressions_period']} · {ST['impressions_asof']} · +{ST['impressions_growth_pct']} %"))
    if RK.get("enabled"): facts.append(("Reconnaissance", f"N° {RK['rank']} · {RK['source']}", RK["asof"]))
    facts.append(("Ancrage", S["city"], "au service des entreprises et des talents sénégalais"))
    fh = "".join(f'<div class="fact"><dt>{e(a)}</dt><dd><b>{e(b)}</b><small>{e(c)}</small></dd></div>' for a, b, c in facts)
    li = f'<a class="textlink" href="{e(LI)}" target="_blank" rel="noopener noreferrer">Suivre Fatoumata sur LinkedIn {ic("ext")}</a>' if LI else ""
    more = "" if full else f'<a class="textlink" href="a-propos.html">Découvrir son parcours {ic("arrow")}</a>'
    return f'''<section class="band founder" id="fondatrice"><div class="wrap founder-in"><figure class="founder-fig reveal"><picture><source media="(max-width:640px)" srcset="img/fatoumata-ba-about-480.webp"><img src="img/fatoumata-ba-about-900.webp" width="900" height="1205" alt="Fatoumata Ba, fondatrice de FBA Consulting Group" loading="lazy" decoding="async"></picture><figcaption>Fatoumata Ba · Fondatrice</figcaption></figure>
<div class="founder-copy reveal"><p class="eyebrow">La fondatrice</p><h2>Fatoumata Ba</h2>
<p class="lede">Créatrice de contenu sur LinkedIn et professionnelle de la communication, Fatoumata Ba a fondé FBA Consulting Group pour mettre sa voix et son audience au service des entreprises, des entrepreneurs et des talents.</p>
<p>Sur LinkedIn, elle fédère une communauté de plus de {fr(ST["followers"])} abonnés.{rk}</p>
<p>Sa mission : aider chacun à gagner en visibilité, à renforcer son image professionnelle et à ouvrir de nouvelles opportunités.</p>{bio if full or not S.get("founder_bio") else ""}
<dl class="facts">{fh}</dl><p class="links">{more}{li}</p></div></div></section>'''

AUDIENCES = [
 ("Entreprises en quête de visibilité", "Demander un devis", "contact.html#demande"),
 ("Entrepreneurs qui promeuvent un projet", "Parler de mon projet", "contact.html?service=" + urllib.parse.quote("Promotion de projets entrepreneuriaux") + "#demande"),
 ("Professionnels qui construisent leur marque", "Développer mon image", "contact.html?service=Personal%20branding#demande"),
 ("Chercheurs d’emploi en quête d’exposition", "Faire connaître mon profil", "emploi-talents.html#candidature"),
 ("Recruteurs qui cherchent des talents", "Parlons de vos besoins", "emploi-talents.html#recruteurs"),
]

# ---------- pages ----------
def hero():
    chips = []
    if ST.get("followers_verified"): chips.append(f'<span class="chip chip--a"><b>+{fr(ST["followers"])}</b> abonnés LinkedIn</span>')
    if RK.get("enabled"): chips.append(f'<span class="chip chip--b"><b>N°&nbsp;{RK["rank"]}</b> {e(RK["source"])} · {e(RK["asof"])}</span>')
    return f'''<section class="hero"><div class="wrap hero-in"><div class="hero-copy"><p class="eyebrow on-dark hero-k">FBA Consulting Group <span aria-hidden="true">·</span> Sénégal</p>
<h1 class="hero-h"><span>Votre visibilité.</span> <span>Notre influence.</span> <em>De nouvelles opportunités.</em></h1>
<p class="lede">Stratégie LinkedIn, personal branding et promotion de projets, portés par la communauté de Fatoumata Ba : plus de {fr(ST["followers"])} abonnés{" et plus de " + ST["impressions_display"] + " d’impressions en " + ST["impressions_period"] if ST.get("impressions_verified") else ""} sur LinkedIn.</p>
<div class="hero-cta"><a class="btn btn--gold btn--lg" href="contact.html#rendez-vous">{ic("cal")} Prendre rendez-vous</a><a class="btn btn--ghost btn--lg" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} WhatsApp</a></div>
<p class="hero-alt"><a href="contact.html#demande">Demander un devis {ic("arrow")}</a><a href="emploi-talents.html">Vous cherchez un emploi ? {ic("arrow")}</a></p></div>
<figure class="hero-fig"><div class="portrait"><picture><source media="(max-width:640px)" srcset="img/fatoumata-ba-hero-480.webp"><img src="img/fatoumata-ba-hero-900.webp" width="900" height="1181" alt="Fatoumata Ba, fondatrice de FBA Consulting Group" fetchpriority="high"></picture></div>{"".join(chips)}</figure></div>
<p class="wrap hero-src">{e(ST["followers_source"])}, relevé le {e(ST["followers_asof"])}.{f" Classement {e(RK['source'])} : {e(RK['scope'])}, {e(RK['asof'])}." if RK.get("enabled") else ""}</p></section>'''

def home():
    aud = "".join(f'<li class="reveal"><a class="aud" href="{h}"><span>{e(t)}</span><b>{e(c)} {ic("arrow")}</b></a></li>' for t, c, h in AUDIENCES)
    testi = [c for c in CLIENTS if c["authorized"] and c.get("testimonial") and c.get("testimonial_author")]
    tblk = f'''<section class="band band--ivory"><div class="wrap">{shead("Témoignages", "Ce que disent nos clients")}<div class="grid g2">{"".join(f'<figure class="quote reveal"><blockquote>“{e(c["testimonial"])}”</blockquote><figcaption>{e(c["testimonial_author"])} · {e(c["name"])}</figcaption></figure>' for c in testi)}</div></div></section>''' if testi else ""
    return f'''{hero()}{metrics()}{benefits_for()}{pillars()}{clients_section()}{testimonials()}{influence()}{emploi_band()}{talents_spotlight()}{founder_story()}{tblk}{cta_block()}'''

def about():
    return head("À propos", "Une voix, une audience, une mission.", "FBA Consulting Group aide les entreprises, les entrepreneurs et les professionnels à gagner en visibilité, à renforcer leur image et à promouvoir leurs projets.") + founder_story(full=True) + metrics() + f'''
<section class="band band--sand"><div class="wrap two-c"><div class="reveal"><p class="eyebrow">Notre mission</p><h2>Rendre visibles celles et ceux qui ont quelque chose à apporter.</h2></div><div class="reveal"><p class="lede">FBA Consulting Group aide les entreprises, les entrepreneurs et les professionnels à gagner en visibilité, à renforcer leur image professionnelle, à promouvoir leurs projets et à développer de nouvelles opportunités.</p><p>Basée à {e(S["city"])}, l’agence accompagne ses clients sur LinkedIn à travers sept services, regroupés en trois expertises : entreprises et entrepreneurs, emploi et talents, personal branding et influence.</p><a class="textlink" href="services.html">Voir nos services {ic("arrow")}</a></div></div></section>
{cta_block()}'''

def services():
    blocks = ""
    for k, n, t, d, cta, h in PILLARS:
        items = "".join(f'<li class="svc reveal"><span class="svc-ic">{ic(i)}</span><div><h3>{e(st)}</h3><p>{e(sd)}</p><a class="textlink" href="{svc_href(st)}">{"Découvrir l’accompagnement emploi" if st in JOBSVC else "Demander ce service"} {ic("arrow")}</a></div></li>' for st, sd, i, p in SERVICES if p == k)
        blocks += f'''<section class="band svc-block{" band--ivory" if k == "emploi" else ""}" id="{k}"><div class="wrap svc-in"><figure class="svc-art reveal"><img src="img/pillar-{k}.svg" width="800" height="600" alt="" loading="lazy" decoding="async"></figure>
<div><p class="eyebrow"><span class="pillar-n">{n}</span> Expertise</p><h2>{e(t)}</h2><p class="lede">{e(d)}</p><ul class="svcs">{items}</ul></div></div></section>'''
    cats = "".join(f'<li class="cat reveal"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in CATEGORIES)
    return head("Nos services", "Sept services, trois expertises.", "Choisissez le service qui correspond à votre besoin, ou décrivez votre projet et nous vous orienterons.") + blocks + f'<section class="band band--sand"><div class="wrap">{shead("Solutions par profil", "Pour qui ?")}<ul class="grid g3 cats">{cats}</ul></div></section>{cta_block()}'

def realisations():
    refs = "".join(client_card(c) for c in CLIENTS if client_visible(c))
    cases = "".join(case_card(c) for c in CASES)
    body = head("Réalisations & Impact", "Une influence mesurée, des références réelles.", "Audience, publications et références clients de FBA Consulting Group.") + clients_section(link=False) + testimonials() + metrics()
    if refs: body += f'<section class="band" id="references"><div class="wrap">{shead("Références clients", "Collaborations")}<div class="rlist">{refs}</div></div></section>'
    if cases: body += f'<section class="band" id="etudes"><div class="wrap">{shead("Études de cas", "Projets et résultats")}<div class="cases">{cases}</div></div></section>'
    else: body += f'<section class="band"><div class="wrap narrow center-h reveal"><p class="eyebrow">Études de cas</p><h2>Études de cas à venir</h2><p class="lede">Nous publierons prochainement des projets détaillés, avec l’accord de nos clients. En attendant, parlons du vôtre.</p></div></section>'
    return body + influence() + cta_block()

def opts(items): return "".join(f"<option>{e(i)}</option>" for i in items)
def common(name): return f'<input type="hidden" name="form-name" value="{name}"><p class="hp" aria-hidden="true"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p><input type="hidden" name="t" value="">'

def contact():
    mode = S["form_mode"]
    booking = f'<a class="btn" href="{e(S["booking_url"])}" target="_blank" rel="noopener">{ic("cal")} Choisir un créneau en ligne</a>' if S["booking_url"] else ""
    return head("Contact", "Trois façons de nous contacter.", "WhatsApp pour un échange immédiat, un formulaire pour une demande détaillée, ou un rendez-vous pour parler de votre projet.") + f'''
<section class="band band--tight"><div class="wrap"><div class="chan reveal"><a class="chan-c" href="#whatsapp">{ic("wa")}<span><h3>WhatsApp</h3><p>Écrivez-nous, réponse directe.</p></span></a><a class="chan-c" href="#demande">{ic("mail")}<span><h3>Demande de devis</h3><p>Décrivez votre projet.</p></span></a><a class="chan-c" href="#rendez-vous">{ic("cal")}<span><h3>Rendez-vous</h3><p>Échangeons sur votre projet.</p></span></a></div></div></section>
<section class="band band--ivory" id="whatsapp"><div class="wrap narrow reveal"><p class="eyebrow">Échange immédiat</p><h2>WhatsApp</h2><p class="lede">Écrivez-nous directement au {e(S["whatsapp_display"])}. Un message prérempli s’ouvre dans WhatsApp.</p><a class="btn btn--wa" href="{e(WA)}" target="_blank" rel="noopener">{ic("wa")} Ouvrir WhatsApp</a><p class="muted">{ic("pin","inl")} {e(S["city"])}</p></div></section>
<section class="band" id="demande"><div class="wrap narrow">{shead("Formulaire", "Demande d’information ou de devis")}
<form class="form reveal" name="demande" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("demande")}
<div class="row2"><div class="f"><label for="d-nom">Nom complet *</label><input id="d-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="d-org">Entreprise ou organisation</label><input id="d-org" name="organisation" autocomplete="organization"></div></div>
<div class="row2"><div class="f"><label for="d-email">E-mail *</label><input id="d-email" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="d-tel">WhatsApp ou téléphone *</label><input id="d-tel" name="telephone" type="tel" required autocomplete="tel"></div></div>
<div class="row2"><div class="f"><label for="d-cat">Votre profil *</label><select id="d-cat" name="categorie" required><option value="">Choisir…</option>{opts([c for c,_ in CATEGORIES])}</select></div><div class="f"><label for="d-type">Objet de la demande *</label><select id="d-type" name="type_demande" required><option value="">Choisir…</option>{opts(INQUIRY)}</select></div></div>
<div class="f"><label for="d-svc">Service souhaité</label><select id="d-svc" name="service"><option value="">À définir ensemble</option>{opts([x[0] for x in SERVICES])}</select></div>
<div class="f"><label for="d-desc">Description du projet *</label><textarea id="d-desc" name="description" rows="5" required minlength="20"></textarea></div>
<div class="row2"><div class="f"><label for="d-delai">Délai souhaité</label><select id="d-delai" name="delai"><option value="">Non précisé</option>{opts(TIMELINES)}</select></div><div class="f"><label for="d-budget">Budget estimé (facultatif)</label><input id="d-budget" name="budget" placeholder="Ex. : montant et devise"></div></div>
<div class="f chk"><input id="d-ok" name="consentement" type="checkbox" required><label for="d-ok">J’accepte que mes données soient utilisées par FBA Consulting Group pour répondre à ma demande. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn btn--navy" type="submit">Envoyer ma demande</button><p class="status" role="status" aria-live="polite"></p></form></div></section>
<section class="band band--ivory" id="rendez-vous"><div class="wrap narrow">{shead("Rendez-vous", "Prendre rendez-vous", "Proposez vos disponibilités pour échanger sur votre projet ou une collaboration. <strong>Un rendez-vous n’est confirmé qu’après la réponse de FBA Consulting Group</strong> par e-mail ou WhatsApp.")}{booking}
<form class="form reveal" name="rendez-vous" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("rendez-vous")}
<div class="row2"><div class="f"><label for="r-nom">Nom complet *</label><input id="r-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="r-org">Entreprise ou organisation</label><input id="r-org" name="organisation"></div></div>
<div class="row2"><div class="f"><label for="r-email">E-mail *</label><input id="r-email" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="r-tel">WhatsApp ou téléphone *</label><input id="r-tel" name="telephone" type="tel" required autocomplete="tel"></div></div>
<div class="f"><label for="r-type">Sujet *</label><select id="r-type" name="type_demande" required><option value="">Choisir…</option>{opts(INQUIRY)}</select></div>
<div class="row2"><div class="f"><label for="r-date1">Date souhaitée (1er choix) *</label><input id="r-date1" name="date_1" type="date" required></div><div class="f"><label for="r-h1">Heure souhaitée *</label><input id="r-h1" name="heure_1" type="time" required></div></div>
<div class="row2"><div class="f"><label for="r-date2">2e choix (facultatif)</label><input id="r-date2" name="date_2" type="date"></div><div class="f"><label for="r-h2">Heure</label><input id="r-h2" name="heure_2" type="time"></div></div>
<div class="f"><label for="r-mode">Mode d’échange *</label><select id="r-mode" name="mode_echange" required><option value="">Choisir…</option><option>Visioconférence</option><option>Appel téléphonique</option><option>WhatsApp</option></select></div>
<div class="f"><label for="r-msg">Message (facultatif)</label><textarea id="r-msg" name="message" rows="3"></textarea></div>
<div class="f chk"><input id="r-ok" name="consentement" type="checkbox" required><label for="r-ok">J’accepte que mes données soient utilisées pour organiser ce rendez-vous. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn btn--navy" type="submit">Envoyer ma demande de rendez-vous</button><p class="status" role="status" aria-live="polite"></p>
<ol class="steps"><li>Vous envoyez vos disponibilités.</li><li>FBA Consulting Group vous répond pour confirmer ou proposer un autre créneau.</li><li>Vous recevez la confirmation avec le mode d’échange.</li></ol></form></div></section>'''

def emploi():
    mode = S["form_mode"]; up = S.get("cv_upload", False)
    steps = [("Votre candidature", "Vous présentez votre parcours et l’opportunité recherchée via le formulaire."), ("Un premier échange", "FBA Consulting Group examine votre profil et vous répond."), ("Votre plan de visibilité", "CV, profil LinkedIn, présentation : nous définissons ensemble ce qu’il faut renforcer."), ("Votre accord, toujours", "Rien n’est publié sans votre accord écrit explicite sur le contenu.")]
    stp = "".join(f'<li class="reveal"><span class="step-n">{i+1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(steps))
    faq = [("Le service garantit-il un emploi ?", DISCLAIM), ("Mon profil sera-t-il publié ?", "Uniquement si vous l’autorisez, et seulement après validation écrite du contenu avec vous."), ("Comment transmettre mon CV ?", "Vous pourrez nous le transmettre après notre premier échange, par e-mail ou WhatsApp." if not up else "Vous pouvez joindre votre CV au formulaire. Il reste privé et n’est jamais publié."), ("Je recrute : comment ça marche ?", "Décrivez le profil recherché dans le formulaire recruteurs. Nous vous répondons pour étudier comment mettre votre opportunité en visibilité.")]
    fq = "".join(f'<details class="qa reveal"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    cvfield = (f'<div class="f"><label for="c-cv">CV (facultatif · PDF, DOC ou DOCX · 7 Mo maximum)</label><input id="c-cv" name="cv" type="file" accept=".pdf,.doc,.docx,application/pdf" data-max="7340032"><span class="hint">Votre CV reste privé : il n’est jamais publié ni accessible par un lien public.</span></div>' if up else '<p class="hint">Vous pourrez nous transmettre votre CV après notre premier échange, par e-mail ou WhatsApp.</p>')
    enc = ' enctype="multipart/form-data"' if up else ""
    return f'''<section class="phero phero--emploi"><div class="wrap phero-split"><div><p class="eyebrow on-dark">Emploi &amp; Talents</p><h1>Votre talent mérite d’être <em>découvert.</em></h1><p class="lede">CV, présence LinkedIn, mise en visibilité : FBA Consulting Group accompagne les chercheurs d’emploi et les professionnels qui veulent être vus par les bonnes personnes.</p>
<div class="hero-cta"><a class="btn btn--gold btn--lg" href="#candidature">Faire connaître mon profil</a><a class="btn btn--ghost btn--lg" href="#recruteurs">Je recrute</a></div></div>
<figure class="phero-art"><img src="img/pillar-emploi.svg" width="800" height="600" alt="" fetchpriority="high"></figure></div></section>
<section class="band"><div class="wrap">{shead("Ce que nous faisons", "Quatre leviers pour être remarqué.")}{offers_list("offers--4")}<p class="fine-l reveal">{e(DISCLAIM)}</p></div></section>
<section class="band band--ink"><div class="wrap two-c">{shead("Comment ça se passe", "Un parcours simple, à votre rythme.", "Vous gardez la main à chaque étape.", dark=True)}<ol class="timeline">{stp}</ol></div></section>
{talents_spotlight()}{testimonials()}
<section class="band band--sand"><div class="wrap">{shead("Deux parcours", "Candidat ou recruteur ?", cls="center-h")}{pathways()}</div></section>
<section class="band band--ivory" id="candidature"><div class="wrap narrow">{shead("Candidature", "Faire connaître mon profil", "Quelques minutes suffisent. Nous revenons vers vous après examen de votre profil.")}
<form class="form reveal" name="candidature" method="POST" data-netlify="true" netlify-honeypot="bot-field"{enc} data-mode="{mode}" novalidate>{common("candidature")}
<div class="row2"><div class="f"><label for="c-nom">Nom complet *</label><input id="c-nom" name="nom" required autocomplete="name"></div><div class="f"><label for="c-email">E-mail *</label><input id="c-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row2"><div class="f"><label for="c-tel">Téléphone ou WhatsApp *</label><input id="c-tel" name="telephone" type="tel" required autocomplete="tel"></div><div class="f"><label for="c-loc">Localisation *</label><input id="c-loc" name="localisation" required placeholder="Ville, pays" autocomplete="address-level2"></div></div>
<div class="row2"><div class="f"><label for="c-dom">Domaine professionnel *</label><input id="c-dom" name="domaine" required></div><div class="f"><label for="c-niv">Niveau d’expérience *</label><select id="c-niv" name="niveau" required><option value="">Choisir…</option><option>Étudiant ou jeune diplômé</option><option>Moins de 3 ans</option><option>3 à 7 ans</option><option>8 ans et plus</option></select></div></div>
<div class="f"><label for="c-opp">Opportunité recherchée *</label><input id="c-opp" name="opportunite" required placeholder="Ex. : poste, secteur, type de contrat"></div>
<div class="f"><label for="c-pres">Brève présentation professionnelle *</label><textarea id="c-pres" name="presentation" rows="5" required minlength="30"></textarea></div>
{cvfield}
<div class="f chk"><input id="c-ok" name="consentement" type="checkbox" required><label for="c-ok">J’accepte que mes données soient utilisées par FBA Consulting Group pour traiter ma candidature. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<div class="f chk"><input id="c-pub" name="consentement_publication" type="checkbox"><label for="c-pub">Facultatif : j’autorise FBA Consulting Group à présenter mon profil publiquement (réseaux sociaux, site), uniquement après validation écrite du contenu avec moi.</label></div>
<button class="btn btn--navy" type="submit">Envoyer ma candidature</button><p class="status" role="status" aria-live="polite"></p></form></div></section>
<section class="band" id="recruteurs"><div class="wrap narrow">{shead("Recruteurs", "Vous recrutez ? Parlons de vos besoins.", "Décrivez le profil recherché. FBA Consulting Group vous répond pour étudier comment mettre votre opportunité en visibilité auprès de sa communauté professionnelle.")}
<form class="form reveal" name="recruteur" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mode="{mode}" novalidate>{common("recruteur")}
<div class="row2"><div class="f"><label for="r-ent">Entreprise *</label><input id="r-ent" name="entreprise" required autocomplete="organization"></div><div class="f"><label for="r-nom2">Nom du contact *</label><input id="r-nom2" name="contact" required autocomplete="name"></div></div>
<div class="row2"><div class="f"><label for="r-em">E-mail professionnel *</label><input id="r-em" name="email" type="email" required autocomplete="email"></div><div class="f"><label for="r-loc2">Localisation *</label><input id="r-loc2" name="localisation" required></div></div>
<div class="row2"><div class="f"><label for="r-fn">Fonction ou compétences recherchées *</label><input id="r-fn" name="fonction" required></div><div class="f"><label for="r-ty">Type d’opportunité *</label><select id="r-ty" name="type_opportunite" required><option value="">Choisir…</option><option>CDI</option><option>CDD</option><option>Stage</option><option>Mission freelance</option><option>Autre</option></select></div></div>
<div class="f"><label for="r-msg2">Message</label><textarea id="r-msg2" name="message" rows="4"></textarea></div>
<div class="f chk"><input id="r-ok2" name="consentement" type="checkbox" required><label for="r-ok2">J’accepte que mes données soient utilisées pour répondre à ma demande. <a href="confidentialite.html">En savoir plus</a> *</label></div>
<button class="btn btn--navy" type="submit">Envoyer ma demande</button><p class="status" role="status" aria-live="polite"></p></form></div></section>
<section class="band band--ivory"><div class="wrap narrow">{shead("Questions fréquentes", "Avant de vous lancer")}<div class="faq">{fq}</div></div></section>{cta_block()}'''

def privacy():
    return head("Politique de confidentialité", "Confidentialité et données personnelles") + f'''<section class="band"><div class="wrap narrow prose"><p>Les informations saisies dans les formulaires (nom, organisation, e-mail, téléphone, description du projet, disponibilités, informations de candidature ou de recrutement) servent uniquement à répondre à votre demande ou à organiser un rendez-vous avec FBA Consulting Group. Elles ne sont pas affichées publiquement.</p><p>Aucun profil de candidat n’est publié sans accord écrit explicite de la personne concernée.</p><p>Les demandes sont reçues par l’intermédiaire du service de formulaires de l’hébergeur du site (Netlify) et consultées par FBA Consulting Group. Vous pouvez demander l’accès, la rectification ou la suppression de vos données par WhatsApp au {e(S["whatsapp_display"])} ou via le formulaire de contact.</p></div></section>'''

def legal():
    return head("Mentions légales", "Mentions légales") + f'''<section class="band"><div class="wrap narrow prose"><h2>Éditeur du site</h2><p>FBA Consulting Group, {e(S["city"])}.<br>Fondatrice : Fatoumata Ba.<br>Contact : WhatsApp {e(S["whatsapp_display"])}.</p><h2>Hébergement</h2><p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis.</p><h2>Propriété intellectuelle</h2><p>Les contenus, logos et photographies présents sur ce site sont la propriété de FBA Consulting Group ou de leurs titulaires respectifs et ne peuvent être réutilisés sans autorisation.</p></div></section>'''

def notfound():
    return head("Erreur 404", "Page introuvable", "Cette page n’existe pas ou a été déplacée.") + '<section class="band"><div class="wrap"><a class="btn btn--navy" href="index.html">Retour à l’accueil</a></div></section>'

PAGES = {
 "index.html": ("FBA Consulting Group | Visibilité LinkedIn et image professionnelle", "Votre visibilité. Notre influence. De nouvelles opportunités. Stratégie LinkedIn, personal branding et promotion de projets au Sénégal.", home()),
 "a-propos.html": ("À propos | FBA Consulting Group", "Découvrez FBA Consulting Group et sa fondatrice, Fatoumata Ba.", about()),
 "services.html": ("Nos services | FBA Consulting Group", "Visibilité LinkedIn, personal branding, promotion de projets, publications sponsorisées et accompagnement des talents.", services()),
 "realisations.html": ("Réalisations & Impact | FBA Consulting Group", "Audience, publications et références clients de FBA Consulting Group.", realisations()),
 "contact.html": ("Contact et rendez-vous | FBA Consulting Group", "Contactez FBA Consulting Group par WhatsApp, formulaire de devis ou demande de rendez-vous.", contact()),
 "mentions-legales.html": ("Mentions légales | FBA Consulting Group", "Mentions légales de FBA Consulting Group.", legal()),
 "emploi-talents.html": ("Emploi & Talents | FBA Consulting Group", "Faites connaître votre profil : CV, présence LinkedIn et visibilité professionnelle avec FBA Consulting Group. Recruteurs : parlons de vos besoins.", emploi()),
 "confidentialite.html": ("Confidentialité | FBA Consulting Group", "Politique de confidentialité de FBA Consulting Group.", privacy()),
 "404.html": ("Page introuvable | FBA Consulting Group", "Page introuvable.", notfound()),
}
if DIST.exists(): shutil.rmtree(DIST)
(DIST / "assets").mkdir(parents=True)
shutil.copytree(SRC / "img", DIST / "img")
shutil.copytree(SRC / "fonts", DIST / "fonts")
for f in ("style.css", "app.js"): shutil.copy(SRC / "assets" / f, DIST / "assets" / f)
for fn, (t, d, b) in PAGES.items(): (DIST / fn).write_text(page(fn, t, d, b), encoding="utf-8")
# Draft: search engines blocked; link-preview bots (WhatsApp, LinkedIn…) allowed so shared links show a card.
(DIST / "robots.txt").write_text("""# Brouillon : retirer le blocage avant le lancement.
User-agent: facebookexternalhit
User-agent: WhatsApp
User-agent: Facebot
User-agent: LinkedInBot
User-agent: Slackbot-LinkExpanding
User-agent: Twitterbot
User-agent: TelegramBot
Allow: /

User-agent: *
Disallow: /
""")
print(f"Built {len(PAGES)} pages -> {DIST}")
