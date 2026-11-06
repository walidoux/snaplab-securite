# SnapLab — démonstration de cybersécurité (M2 RT)

Projet universitaire de sensibilisation aux risques de phishing : formulaire public de **données inventées**, serveur Flask sur Render, base SQLite et tableau de bord protégé.

## Test de bout en bout
1. Ouvrir https://walidoux.github.io/snaplab-securite/
2. Choisir un profil A/B/C pour préremplir, puis **modifier librement** les champs dans les formats imposés :
   - Adresse de laboratoire : `walid12@snaplab.test` (domaine réservé aux exemples).
   - Code de laboratoire : `LAB-AB1234` (préfixe LAB-, puis 4 à 12 lettres majuscules ou chiffres).
3. Cliquer sur **Envoyer le test** et vérifier la confirmation du serveur.
4. Ouvrir https://walidoux.github.io/snaplab-securite/dashboard.html
5. Coller le secret `ADMIN_TOKEN` défini dans Render (ne jamais l'envoyer à autrui) puis cliquer sur **Afficher les événements**.
6. Le tableau affiche les **valeurs de laboratoire réellement saisies** (et non les valeurs du profil prédéfini).

## Données transmises et limites
- Seules les adresses `@snaplab.test`, les codes de laboratoire `LAB-...` et un ID de profil optionnel sont autorisés.
- Tout autre domaine, code non conforme, champ `password` ou champ inattendu est refusé par le serveur.
- Ce service **ne collecte pas de véritables e-mails ou mots de passe**. Il n'est pas lié à Snapchat.
- L'API des statistiques est protégée par un jeton serveur `ADMIN_TOKEN`. Ne pas publier ce jeton.
- Sur Render Free, le stockage SQLite dans `/tmp` est éphémère : les données peuvent disparaître au redémarrage.

## Architecture
`GitHub Pages (HTML/JS) → HTTPS POST /api/events → Flask/Render → SQLite → GET /api/admin/stats → dashboard.html`

## API
- Santé : https://snaplab-securite.onrender.com/health
- POST `/api/events` : `{"event":"demo_submit","demo_profile":"lab-01","demo_email":"walid12@snaplab.test","demo_code":"LAB-AB1234"}`
- GET `/api/admin/stats` : nécessite `Authorization: Bearer <ADMIN_TOKEN>`.

## Contexte
USTHB — Master 2 Réseaux et Télécommunications — module Sécurité informatique.
