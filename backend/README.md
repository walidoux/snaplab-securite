# Backend SnapLab — événements de simulation

Service Flask hébergeable sur Render. Il enregistre **uniquement** le type d'événement, son horodatage et l'ID d'un profil de simulation connu. Aucun e-mail libre, mot de passe réel ou IP n'est enregistré. Les identifiants de laboratoire sont des valeurs prédéfinies dans le code, distinctes de tout compte réel.

## Déploiement
1. Sur Render, créer un nouveau Web Service à partir du dépôt GitHub `walidoux/snaplab-securite`.
2. Choisir `backend` comme Root Directory.
3. Build command : `pip install -r requirements.txt`.
4. Start command : `gunicorn --bind 0.0.0.0:$PORT app:app`.
5. Ajouter `ADMIN_TOKEN` avec une valeur longue et aléatoire, et `SITE_ORIGIN=https://walidoux.github.io`.
6. Le stockage SQLite par défaut (`/tmp`) est **éphémère** sur certains hébergeurs. Utiliser un disque persistant et définir `SNAPLAB_DB` pour conserver les statistiques après redémarrage.

## API
- `GET /health` : test de disponibilité.
- `POST /api/events` : accepte `{"event":"demo_submit","demo_profile":"lab-01"}` (ou `lab-02`, `lab-03`) depuis l'origine GitHub Pages configurée. Refuse tout champ supplémentaire, y compris e-mail et mot de passe.
- `GET /api/admin/stats` : statistiques protégées par `Authorization: Bearer <ADMIN_TOKEN>` ; les entrées du journal comprennent les identifiants factices associés aux IDs de simulation.

Attention : la restriction d'origine CORS n'est pas une authentification. Ce service sert à une démonstration et ne doit pas être utilisé pour collecter des secrets.
