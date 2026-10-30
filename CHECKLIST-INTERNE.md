# FBA Consulting Group — checklist interne (ne pas publier)

## À faire approuver par Fatoumata Ba
- [ ] Chiffres LinkedIn : +80 000 abonnés, +28 millions d'impressions cumulées (vérifier dans les statistiques LinkedIn). Mettre `stats.confirmed` à true après vérification.
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
