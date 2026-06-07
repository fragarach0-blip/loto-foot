# Loto Foot 2026

Application web familiale pour pronostiquer la Coupe du Monde 2026.

Le site est volontairement simple à utiliser sur mobile : chaque joueur choisit son nom, saisit ses scores, puis suit le classement en temps réel.

## Site en ligne

https://melodious-figolla-46b637.netlify.app

Tout le monde joue sur cette même URL. Les données sont synchronisées en temps réel avec Firebase Firestore.

## Fonctionnalités

### Jeu

- 104 matchs : 72 matchs de groupes + 32 matchs de phase finale.
- Pronostics par joueur.
- Scores officiels saisis par l'administrateur ou synchronisés via football-data.org.
- Classement en temps réel.
- Podium et tableau détaillé.
- Stats fun : taux de scores exacts, série en cours, spécialité groupes/finale.
- Barème différent pour la phase finale.
- Verrouillage automatique des pronostics après coup d'envoi.
- Badge live quand l'API marque un match `IN_PLAY` ou `PAUSED`.

### Joueurs

- Nom, couleur et photo de profil optionnelle.
- PIN optionnel par joueur pour protéger l'accès aux pronostics.
- Photos compressées côté navigateur avant stockage.

### Mobile / PWA

- Application installable grâce à `manifest.json`, `sw.js` et `icon.svg`.
- Fonctionne comme site statique hébergé sur Netlify.
- Notifications web masquées pour le moment, le code reste présent mais aucune demande de permission n'est déclenchée.

### Interface

- Navigation compacte : Jouer, Score, TV, Admin.
- Page Jouer avec actions rapides : Pronos, Score, Partager.
- Mode TV/famille pour afficher le classement et les matchs à suivre sur un écran posé.
- Partage rapide via Web Share API ou copie du lien.
- Drapeaux affichés via images FlagCDN pour éviter les soucis de rendu emoji.

### API externes

- football-data.org : synchronisation des statuts et résultats.
- The Odds API : support optionnel des cotes 1/N/2 si une clé est configurée.
- FlagCDN : images de drapeaux.

## Règles du jeu

| Phase | Score exact | Bon résultat | Mauvais résultat |
|---|---:|---:|---:|
| Groupes | 3 pts | 1 pt | 0 pt |
| Phase finale | 5 pts | 2 pts | 0 pt |

Un bon résultat signifie que le joueur a trouvé le bon sens du match : victoire équipe 1, nul ou victoire équipe 2.

## Comment jouer

1. Ouvrir le site.
2. Cliquer sur `Ajouter` pour créer les joueurs.
3. Cliquer sur `Pronos`.
4. Choisir son nom.
5. Remplir les scores.
6. Suivre le classement dans `Score` ou `TV`.

Si un joueur a un PIN, l'app le demande avant d'ouvrir ses pronostics.

## Admin

Le code admin par défaut est :

```text
1234
```

L'onglet `Admin` permet :

- de saisir les résultats manuellement ;
- de synchroniser les résultats via football-data.org ;
- de synchroniser les cotes si une clé The Odds API est configurée ;
- de filtrer par groupe ou phase finale.

## Données Firestore

Tout l'état partagé est stocké dans un seul document :

```text
Collection: state
Document: main
```

Structure principale :

```js
{
  players: [
    { id, name, color, photo, pin }
  ],
  preds: {
    [playerId]: {
      [matchId]: { s1, s2 }
    }
  },
  results: {
    [matchId]: { s1, s2 }
  },
  matchMeta: {
    [matchId]: {
      status,
      utcDate,
      winner,
      odds,
      t1,
      t2
    }
  },
  adminCode: "1234"
}
```

### Champs importants

- `players` : joueurs, couleur, photo base64 compressée, PIN optionnel.
- `preds` : pronostics par joueur et par match.
- `results` : scores officiels.
- `matchMeta` : métadonnées API, statut live, dates exactes, vainqueur, cotes et noms d'équipes résolus.
- `adminCode` : code admin.

## Synchronisation temps réel

Au chargement :

1. `load()` lit `state/main`.
2. `startSync()` ouvre un `onSnapshot`.
3. Chaque écriture appelle `save()`.
4. Les autres appareils reçoivent la mise à jour automatiquement.

La variable `saving` évite qu'un appareil se re-rende immédiatement pendant sa propre saisie.

## Verrouillage des pronostics

Un prono est verrouillé si :

- l'heure de coup d'envoi est passée ;
- ou le statut API est `IN_PLAY`, `PAUSED`, `LIVE`, `FINISHED` ou `AWARDED`.

L'heure vient de `matchMeta.utcDate` quand l'API l'a fournie. Sinon l'app utilise la date locale du calendrier avec une heure par défaut.

## Phase finale

Les matchs 73 à 104 couvrent :

- 16 matchs de 32es de finale ;
- 8 huitièmes ;
- 4 quarts ;
- 2 demies ;
- petite finale ;
- finale.

L'app peut remplacer automatiquement les placeholders :

- `1er A`, `2e B`, etc. avec le classement de groupe ;
- `3e A/B/C/...` avec les meilleurs troisièmes quand ils sont déductibles ;
- `Vainqueur M73`, `Perdant M101`, etc. avec les résultats des matchs précédents.

En cas de nul en phase finale, l'app peut utiliser `matchMeta.winner` si l'API indique le vainqueur officiel.

## Cotes

Le support des cotes est optionnel.

L'app utilise The Odds API sur le marché `h2h` :

- équipe 1 ;
- nul ;
- équipe 2.

La constante HTML reste vide localement :

```js
const ODDS_API_KEY = '';
```

Au déploiement, `deploy-netlify.py` injecte la valeur de `ODDS_API_TOKEN` depuis `.env.local` si elle existe.

## Fichiers du projet

```text
loto-foot/
├── loto-foot-app.html   # App complète HTML/CSS/JS
├── manifest.json        # Manifest PWA
├── sw.js                # Service worker PWA/cache
├── icon.svg             # Icône PWA
├── deploy-netlify.py    # Déploiement Netlify via API
├── dev-server.py        # Serveur local + proxy football-data
├── A REMPLIR.xlsx       # Ancien fichier Excel hors-ligne
├── README.md            # Documentation
└── .env.local           # Tokens locaux, ignoré par git
```

## Variables locales

Le fichier `.env.local` est volontairement ignoré par git.

Format attendu :

```env
NETLIFY_TOKEN=...
FOOTBALL_DATA_TOKEN=...
ODDS_API_TOKEN=...
```

Notes :

- `NETLIFY_TOKEN` sert au script de déploiement.
- `FOOTBALL_DATA_TOKEN` est documenté localement, mais la clé actuellement utilisée est encore dans le HTML pour les appels navigateur.
- `ODDS_API_TOKEN` est injecté dans le HTML déployé si configuré.

## Déploiement

Le déploiement publie plusieurs fichiers :

- `index.html` généré depuis `loto-foot-app.html` ;
- `manifest.json` ;
- `sw.js` ;
- `icon.svg`.

Commande :

```powershell
Set-Location "C:\Users\Charlotte\Desktop\loto foot"
& "C:\Users\Charlotte\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" deploy-netlify.py
```

Le script :

1. lit `.env.local` ;
2. calcule les SHA1 des fichiers ;
3. crée un déploiement Netlify avec la Files API ;
4. uploade uniquement les fichiers demandés par Netlify ;
5. affiche l'URL publiée.

## Test local

Le plus simple :

```powershell
Set-Location "C:\Users\Charlotte\Desktop\loto foot"
& "C:\Users\Charlotte\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" dev-server.py
```

Puis ouvrir :

```text
http://localhost:8082/loto-foot-app.html
```

`dev-server.py` sert les fichiers et proxifie les appels football-data.org pour éviter les problèmes CORS en local.

## Vérification rapide avant déploiement

Vérifier que le JavaScript embarqué est syntaxiquement valide :

```powershell
& "C:\Users\Charlotte\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" -e "const fs=require('fs'); const html=fs.readFileSync('loto-foot-app.html','utf8'); const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]); for (const s of scripts) new Function(s); console.log('JS syntax OK')"
```

## Sécurité

Points à connaître :

- Firestore semble fonctionner en mode lecture/écriture publique. C'est acceptable pour un usage familial, mais pas pour une app publique large.
- Le code admin `1234` n'est pas une vraie sécurité serveur. Il protège surtout contre les modifications accidentelles.
- Les tokens API ne doivent pas être commités.
- `.env.local` est ignoré par git.
- Le token Netlify déjà collé dans une conversation doit idéalement être révoqué et remplacé.
- Les clés utilisées côté navigateur sont visibles par nature. Pour une sécurité plus forte, il faudrait déplacer les appels API derrière une fonction serveur.

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

## Roadmap possible

- Ajouter une vraie authentification Firebase.
- Déplacer les clés API dans une fonction Netlify.
- Ajouter export PDF/Excel.
- Ajouter une fiche joueur détaillée.
- Ajouter un historique des modifications.
- Réactiver les notifications avec une stratégie mobile fiable.
