# SnapLab — Démonstration de cybersécurité

Projet universitaire sur la reconnaissance du phishing et la sécurité des formulaires de connexion. Interface statique et responsive développée en HTML/CSS/JavaScript.

## Fonctionnement

- Formulaire de démonstration avec champs e-mail et mot de passe.
- Aucune donnée saisie n'est lue, enregistrée, transmise ou comparée à un compte réel.
- Un clic sur « Se connecter » affiche une explication pédagogique de sécurité et enregistre uniquement un événement horodaté dans le stockage local du navigateur.
- Ce site est indépendant de Snapchat et n'effectue aucune authentification auprès de ce service.

## Publication sur GitHub Pages

1. Ouvrir **Settings > Pages** dans le dépôt GitHub.
2. Choisir **Deploy from a branch** sous **Build and deployment**.
3. Sélectionner **main** et **/(root)**, puis cliquer sur **Save**.
4. Consulter l'adresse GitHub Pages fournie par GitHub une fois le déploiement effectué.

GitHub Pages héberge des fichiers statiques, sans serveur Flask ni base de données.

## Tableau de bord

Ouvrir `dashboard.html` depuis le site public pour consulter le nombre de soumissions, l'activité sur 7 jours et les dix derniers événements. Les données utilisent `localStorage` et sont **propres à chaque navigateur** : ce n'est pas un suivi centralisé des visiteurs et aucun identifiant n'est reçu ni conservé.

## Contexte

USTHB — Master 2 Réseaux et Télécommunications — Module Sécurité informatique. Projet de démonstration et de sensibilisation à l'ingénierie sociale.
