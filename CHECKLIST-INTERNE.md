# FBA Consulting Group — checklist interne (ne pas publier)

## À faire approuver par Fatoumata Ba
- [x] Abonnés LinkedIn : profil affiché à 83 214 abonnés le 30/10/2026 → le site indique « +83 000 ».
- [ ] +28 millions d'impressions cumulées : à vérifier dans les statistiques LinkedIn (non visible sur le profil). **Masqué sur le site** tant que `impressions_verified` = false.
- [ ] Ne pas publier « Top 1 % Sénégal » / « Top 3 Sénégal » (deux classements différents sur son profil et sa bannière, non vérifiables).
- [ ] Autorisation écrite de chaque client (nom + logo) : N2M SÉCURITÉ, NVI FACILITY, DPM CONSULTING SENEGAL, N2M ELECTRONICS, PRO Ingénierie TECH. Rien n'est publié tant que `authorized` = false dans `src/clients.json`.
- [ ] Logos originaux des 5 clients (fichiers non modifiés) → `src/img/clients/`.
- [ ] Les 6 catégories de clients et les formulations « Pourquoi FBA ».
- [ ] Biographie / parcours (la mention « parmi les profils les plus visibles du Sénégal » n'est PAS publiée tant qu'elle n'est pas vérifiable).
- [ ] Courriel professionnel, page LinkedIn de l'entreprise, autres réseaux (`src/site.json` → social). Aucune icône n'est affichée sans URL.
- [ ] Mentions légales : forme juridique, n° RCCM / NINEA, directeur de la publication.
- [ ] Politique de confidentialité : validation du texte (responsable du traitement, durée de conservation).
- [ ] Photos : confirmer l'usage public des portraits.

## Configuration technique
- [ ] Déployer sur Netlify ; activer Forms → notifications e-mail (formulaires `demande` et `rendez-vous`).
- [ ] Envoyer une demande réelle de chaque formulaire et vérifier la réception.
- [ ] Tester le lien WhatsApp sur un téléphone avec WhatsApp installé (+221 77 641 78 41).
- [ ] Option : `booking_url` (Calendly, Cal.com…) pour un vrai agenda.
- [ ] Domaine : renseigner `domain`, retirer `noindex` et `Disallow` (robots) au lancement.
- [ ] Remplacer les logos FBA (recadrages raster) par les fichiers vectoriels d'origine.
- [ ] Lighthouse / contrôle de vitesse après déploiement (polices Google chargées en ligne).

## Emploi & Talents (nouveau)
- [ ] Fatoumata valide l'offre : révision de CV, optimisation LinkedIn, préparation aux entretiens, visibilité des profils approuvés (les 6 bénéfices affichés).
- [ ] Confirmer le statut : le site se présente comme « mise en visibilité et réseautage professionnel », sans promesse d'embauche et sans se dire agence de recrutement agréée.
- [ ] Téléversement de CV DÉSACTIVÉ (`cv_upload: false` dans `src/site.json`). Le code est prêt (PDF/DOC/DOCX, 7 Mo, consentement séparé). Avant de l'activer : vérifier sur Netlify que les fichiers ne sont accessibles qu'avec le compte administrateur (jamais par URL publique) et ajouter un contrôle serveur du type de fichier. Tant que ce n'est pas validé, ne pas activer.
- [ ] Après le premier déploiement : tester les 3 formulaires `candidature`, `recruteur`, `demande`, `rendez-vous` ; activer les notifications e-mail Netlify.
- [ ] L'URL `/emploi-talents` est redirigée par `netlify.toml` : vérifier sur le site en ligne.
- [ ] « Des talents mis en lumière » : masqué tant que `src/talents.json` est vide. N'y ajouter que des cas approuvés par écrit (`"approved": true`).
- [ ] Photos des cartes : portraits de Fatoumata (trois photos fournies). Remplacer si elle souhaite d'autres visuels.

## Classement Favikon (ajouté le 30/10/2026)
- [ ] Affiché : « N° 2 · Créateurs LinkedIn au Sénégal · classement Favikon, octobre 2026 » (d'après la capture de Fatoumata : score 94,3/100). Source : photo d'écran envoyée par Fatoumata, non vérifiée directement sur favikon.com.
- [ ] Avant le lancement : confirmer le rang sur favikon.com et mettre à jour `ranking.rank` / `ranking.asof` dans `src/site.json` à chaque changement. Mettre `ranking.enabled` à false pour le retirer.
- [ ] Formulation utilisée : « Créateurs LinkedIn les plus influents au Sénégal · classement Favikon, octobre 2026 » (reprend le mot « influent » de Fatoumata, toujours attribué à Favikon et daté ; le classement affiché est celui des créateurs).
- [ ] Ne pas utiliser le logo Favikon sans autorisation.

## Refonte premium 2.0 (30/10/2026)
- [ ] « Notre influence en action » : fournir 3 à 6 vraies publications ou campagnes (lien, date, image, accord du client ou de la personne mise en avant) → `src/posts.json`. Chiffres de performance uniquement s'ils sont vérifiés (capture des statistiques LinkedIn).
- [ ] Parcours de la fondatrice (formation, expériences, dates) → `founder_bio`. La mention « professionnelle de la communication » est à confirmer par Fatoumata.
- [ ] Au lancement : `draft_placeholders` → false (retire tous les cadres « à fournir »).
- [ ] Illustrations des trois expertises : SVG originaux. Option : remplacer par des photos commandées (pas de banque d'images générique).
