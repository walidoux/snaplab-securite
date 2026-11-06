# Backend SnapLab — événements de simulation

Service Flask hébergeable sur Render. Il enregistre **uniquement** le type d'événement et son horodatage ; aucun identifiant, mot de passe ou IP.

## Déploiement
1. Sur Render, créer un nouveau Web Service à partir du dépôt GitHub `walidoux/snaplab-securite`.
2. Choisir `backend` comme Root Directory.
3. Build command : `pip install -r requirements.txt`.
4. Start command : `gunicorn --bind 0.0.0.0:$PORT app:app`.
5. Ajouter `ADMIN_TOKEN` avec une valeur longue et aléatoire, et `SITE_ORIGIN=https://walidoux.github.io`.
6. Le stockage SQLite par défaut (`/tmp`) est **éphémère** sur certains hébergeurs. Utiliser un disque persistant et définir `SNAPLAB_DB` pour conserver les statistiques après redémarrage.

## API
- `GET /health` : test de disponibilité.
- `POST /api/events` : accepte seulement `{"event":"demo_submit"}` depuis l'origine GitHub Pages configurée.
- `GET /api/admin/stats` : statistiques protégées par `Authorization: Bearer <ADMIN_TOKEN>`.

Attention : la restriction d'origine CORS n'est pas une authentification. Ce service sert à une démonstration et ne doit pas être utilisé pour collecter des secrets.
