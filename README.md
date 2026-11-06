# SnapLab — Démonstration de cybersécurité

Projet universitaire sur la reconnaissance du phishing et la sécurité des formulaires de connexion. Interface statique et responsive développée en HTML/CSS/JavaScript.

## Fonctionnement

- Formulaire de démonstration avec champs e-mail et mot de passe.
- Aucune donnée saisie n'est lue, enregistrée, transmise ou comparée à un compte réel.
- Un clic sur « Se connecter » affiche une explication pédagogique de sécurité, enregistre un événement horodaté local et transmet uniquement `{ "event": "demo_submit" }` au backend Render. Les champs e-mail et mot de passe ne sont jamais lus ou envoyés.
- Ce site est indépendant de Snapchat et n'effectue aucune authentification auprès de ce service.

## Publication sur GitHub Pages

1. Ouvrir **Settings > Pages** dans le dépôt GitHub.
2. Choisir **Deploy from a branch** sous **Build and deployment**.
3. Sélectionner **main** et **/(root)**, puis cliquer sur **Save**.
4. Consulter l'adresse GitHub Pages fournie par GitHub une fois le déploiement effectué.

GitHub Pages héberge des fichiers statiques, sans serveur Flask ni base de données.

## Tableau de bord

Ouvrir `dashboard.html` depuis le site public pour consulter le nombre de soumissions, l'activité sur 7 jours et les dix derniers événements. Les cartes et graphiques locaux utilisent `localStorage` et sont **propres à chaque navigateur**. Un panneau distinct permet de consulter les événements anonymes centralisés via Render en saisissant le jeton secret `ADMIN_TOKEN` défini dans les variables d'environnement Render. Le jeton n'est pas enregistré par la page.

## Contexte

USTHB — Master 2 Réseaux et Télécommunications — Module Sécurité informatique. Projet de démonstration et de sensibilisation à l'ingénierie sociale.

## Backend de démonstration sur Render

- Service : `https://snaplab-securite.onrender.com` ; santé : `/health`.
- Les requêtes de soumission ne contiennent **aucune donnée personnelle saisie dans le formulaire**.
- L'API `/api/admin/stats` nécessite `Authorization: Bearer <ADMIN_TOKEN>`.
- Sur l'instance Free, la base SQLite enregistrée dans `/tmp` est temporaire et peut être effacée au redémarrage.
- Ne jamais inscrire la valeur d'`ADMIN_TOKEN` dans le dépôt GitHub, les captures d'écran ou du JavaScript public.
