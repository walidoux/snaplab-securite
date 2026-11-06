# SnapLab — Démonstration de cybersécurité

Projet universitaire sur la reconnaissance du phishing et la sécurité des formulaires de connexion. Interface statique et responsive développée en HTML/CSS/JavaScript.

## Fonctionnement

- Formulaire de démonstration avec trois profils **100 % fictifs** (e-mails `@snaplab.test` et codes `FICTIF-LAB-...`). Les champs sont modifiables à des fins de simulation visuelle, mais leur contenu n'est jamais lu, stocké ou transmis. Le tableau de bord montre uniquement les valeurs fictives prédéfinies du profil.
- Aucun identifiant libre ou réel ne peut être envoyé : seul l'ID d'un profil de test prédéfini est transmis au backend.
- Un clic sur « Se connecter » affiche une explication pédagogique, enregistre un événement horodaté local et transmet seulement `{ "event": "demo_submit", "demo_profile": "lab-01" }` (ou un autre ID prédéfini) à Render.
- Ce site est indépendant de Snapchat et n'effectue aucune authentification auprès de ce service.

## Publication sur GitHub Pages

1. Ouvrir **Settings > Pages** dans le dépôt GitHub.
2. Choisir **Deploy from a branch** sous **Build and deployment**.
3. Sélectionner **main** et **/(root)**, puis cliquer sur **Save**.
4. Consulter l'adresse GitHub Pages fournie par GitHub une fois le déploiement effectué.

GitHub Pages héberge des fichiers statiques, sans serveur Flask ni base de données.

## Tableau de bord

Ouvrir `dashboard.html` depuis le site public pour consulter le nombre de soumissions, l'activité sur 7 jours et les dix derniers événements. Les cartes et graphiques locaux utilisent `localStorage` et sont **propres à chaque navigateur**. Un panneau distinct permet de consulter les événements centralisés via Render ainsi que les e-mails et codes de **démonstration prédéfinis** en saisissant le jeton secret `ADMIN_TOKEN` défini dans les variables d'environnement Render. Les identifiants ne sont pas interceptés depuis les champs du navigateur : ils sont reconstruits depuis le profil fictif choisi. Le jeton n'est pas enregistré par la page.

## Contexte

USTHB — Master 2 Réseaux et Télécommunications — Module Sécurité informatique. Projet de démonstration et de sensibilisation à l'ingénierie sociale.

## Backend de démonstration sur Render

- Service : `https://snaplab-securite.onrender.com` ; santé : `/health`.
- Les requêtes ne contiennent **aucune donnée personnelle saisie dans le formulaire** : seulement un ID parmi trois profils fictifs autorisés. Le serveur refuse les champs libres.
- Dans le dashboard, les e-mails et mots de passe `@snaplab.test` / `FICTIF-LAB-...` sont des valeurs **prédéfinies pour la démonstration**, pas des secrets collectés.
- L'API `/api/admin/stats` nécessite `Authorization: Bearer <ADMIN_TOKEN>`.
- Sur l'instance Free, la base SQLite enregistrée dans `/tmp` est temporaire et peut être effacée au redémarrage.
- Ne jamais inscrire la valeur d'`ADMIN_TOKEN` dans le dépôt GitHub, les captures d'écran ou du JavaScript public.
