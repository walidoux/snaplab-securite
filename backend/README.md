# Backend de démonstration SnapLab

Service Flask pour recevoir des **données fictives explicitement formatées**. Ce n'est pas un collecteur de mots de passe ni une passerelle de connexion Snapchat.

## Déployer dans Render
- Dépôt : `walidoux/snaplab-securite`, branche `main`
- Root Directory : `backend`
- Build Command : `pip install -r requirements.txt`
- Start Command : `gunicorn --bind 0.0.0.0:$PORT app:app`
- Variables : `SITE_ORIGIN=https://walidoux.github.io` et `ADMIN_TOKEN` secret généré par Render.

## API
- `GET /health` : disponibilité.
- `POST /api/events` : JSON avec `event=demo_submit`, `demo_email` au domaine réservé `@snaplab.test`, `demo_code` du type `LAB-AB1234`, `demo_profile` optionnel. Les formats sont strictement validés côté serveur. Les événements anonymes des anciens clients restent acceptés.
- `GET /api/admin/stats` : nécessite `Authorization: Bearer <ADMIN_TOKEN>`, retourne les valeurs **réellement saisies dans le format de TP** et les anciens événements historiques.

## Stockage et confidentialité
- Table SQLite avec migrations automatiques des colonnes `demo_email` et `demo_code`.
- La base `/tmp/snaplab-events.sqlite3` n'est pas persistante sur Render Free ; les données peuvent être perdues au redémarrage. Utiliser un stockage persistant si nécessaire.
- Ne soumettre ni identifiants réels, ni secrets. Le serveur refuse les domaines non fictifs, les codes de format non conforme et les champs inattendus.
- L'origine CORS limite les requêtes depuis les navigateurs mais **n'est pas une authentification**. Le tableau de bord nécessite le secret d'administration.
