# PRONO '26

Application web familiale pour pronostiquer la Coupe du Monde 2026.

Simple sur mobile : chaque joueur choisit son nom, saisit ses scores, et suit le classement en temps réel.

## Site en ligne

https://fragarach0-blip.github.io/loto-foot/

Tout le monde joue sur cette même URL. Les données sont synchronisées en temps réel avec Firebase Firestore.

## Fonctionnalités

### Jeu

- 104 matchs : 72 matchs de groupes + 32 matchs de phase finale.
- Pronostics par joueur.
- Scores officiels synchronisés automatiquement via football-data.org.
- Cotes 1/N/2 synchronisées via The Odds API (une fois par jour).
- Classement en temps réel avec podium et tableau détaillé.
- Verrouillage automatique des pronostics après le coup d'envoi.
- Badge EN DIRECT quand l'API marque un match `IN_PLAY` ou `PAUSED`.

### Joueurs

- Nom, couleur et photo de profil optionnelle.
- PIN optionnel par joueur pour protéger l'accès aux pronostics.
- Photos compressées côté navigateur avant stockage.

### Mobile / PWA

- Application installable grâce à `manifest.json`, `sw.js` et `icon.svg`.
- Hébergée sur GitHub Pages (déploiements illimités).
- Notifications web : code présent, aucune demande de permission déclenchée.

### Interface

- Navigation : Jouer, Score, TV.
- Lien Admin discret en bas de la page d'accueil.
- Mode TV/famille pour afficher le classement sur un grand écran.
- Règlement affiché directement sur la page d'accueil.
- Drapeaux via FlagCDN (pas d'emoji).

### API externes

- football-data.org : résultats et statuts, token en paramètre URL.
- The Odds API : cotes 1/N/2, sync automatique 1×/jour.
- FlagCDN : images de drapeaux.
- Firebase Firestore : état partagé en temps réel.

## Règles du jeu

| Phase | Score exact | Bon résultat | Mauvais résultat |
|---|---:|---:|---:|
| Groupes | 3 pts | 1 pt | 0 pt |
| Phase finale | 5 pts | 2 pts | 0 pt |

## Comment jouer

1. Ouvrir le site.
2. Cliquer sur `Ajouter` pour créer les joueurs.
3. Cliquer sur `Pronos`.
4. Choisir son nom.
5. Remplir les scores.
6. Suivre le classement dans `Score` ou `TV`.

Si un joueur a un PIN, l'app le demande avant d'ouvrir ses pronostics.

## Admin

Le code admin par défaut est `1234`.

Accessible via le lien discret en bas de la page d'accueil. Permet :

- de synchroniser les résultats via football-data.org ;
- de synchroniser les cotes via The Odds API ;
- de saisir les résultats manuellement ;
- de filtrer par groupe ou phase finale.

## Données Firestore

Tout l'état est dans un seul document `state/main` :

```js
{
  players: [{ id, name, color, photo, pin }],
  preds: { [playerId]: { [matchId]: { s1, s2 } } },
  results: { [matchId]: { s1, s2 } },
  matchMeta: { [matchId]: { status, utcDate, winner, odds, t1, t2 } },
  adminCode: "1234"
}
```

## Fichiers du projet

```text
loto-foot/
├── loto-foot-app.html   # App complète HTML/CSS/JS
├── manifest.json        # Manifest PWA
├── sw.js                # Service worker (pass-through, pas de cache)
├── icon.svg             # Icône PWA
├── deploy-github.py     # Déploiement GitHub Pages
├── deploy-netlify.py    # Déploiement Netlify (backup)
├── dev-server.py        # Serveur local + proxy football-data
├── README.md            # Documentation
└── .env.local           # Tokens locaux, ignoré par git
```

## Variables locales

```env
NETLIFY_TOKEN=...
FOOTBALL_DATA_TOKEN=537561c0fa7943d69a67c7ad53c671f3
ODDS_API_TOKEN=80941ab267df6c39865e65451ebb387f
```

## Déploiement GitHub Pages

```powershell
Set-Location "C:\Users\Charlotte\Desktop\loto foot"
& "C:\Users\Charlotte\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" deploy-github.py
```

Le script copie `loto-foot-app.html` → `index.html`, adapte le manifest, et force-push vers la branche `gh-pages`.

## Test local

```powershell
Set-Location "C:\Users\Charlotte\Desktop\loto foot"
& "C:\Users\Charlotte\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" dev-server.py
```

Puis ouvrir : http://localhost:8082/loto-foot-app.html

`dev-server.py` sert les fichiers et proxifie les appels football-data.org pour éviter les problèmes CORS en local.

## Quotas API

| Service | Plan | Limite |
|---|---|---|
| football-data.org | Gratuit | 10 req/min |
| The Odds API | Gratuit | 500 req/mois (sync 1×/jour = ~30 req/mois) |
| Firebase Firestore | Spark (gratuit) | 50k lectures/jour · 20k écritures/jour |
| FlagCDN | Gratuit | Illimité |
| GitHub Pages | Gratuit | Déploiements illimités |

## Sécurité

- Firestore en lecture/écriture publique — acceptable pour usage familial.
- Le code admin `1234` protège contre les modifications accidentelles, pas contre un utilisateur malveillant.
- Les tokens API sont visibles côté navigateur par nature.
- `.env.local` est ignoré par git.

## Calendrier des groupes

| Groupe | Équipes |
|---|---|
| A | Mexique, Afrique du Sud, Corée du Sud, Rép. Tchèque |
| B | Canada, Bosnie-Herzég., Qatar, Suisse |
| C | Brésil, Maroc, Haïti, Écosse |
| D | USA, Paraguay, Australie, Turquie |
| E | Allemagne, Curaçao, Côte d'Ivoire, Équateur |
| F | Pays-Bas, Japon, Suède, Tunisie |
| G | Belgique, Égypte, Iran, Nouvelle-Zélande |
| H | Espagne, Cap-Vert, Arabie Saoudite, Uruguay |
| I | France, Sénégal, Irak, Norvège |
| J | Argentine, Algérie, Autriche, Jordanie |
| K | Portugal, RD Congo, Ouzbékistan, Colombie |
| L | Angleterre, Croatie, Ghana, Panama |
