# Loto Foot – Coupe du Monde 2026

Application web familiale pour pronostiquer les 72 matchs de la phase de groupes de la Coupe du Monde 2026.

---

## URL de l'application

**https://melodious-figolla-46b637.netlify.app**

Tout le monde joue sur la même URL. Les pronostics et le classement sont synchronisés en temps réel grâce à Firebase.

---

## Règles du jeu

| Résultat | Points |
|----------|--------|
| Score exact (ex : 2-1 prédit et 2-1 réel) | **3 pts** |
| Bon résultat (victoire / nul / défaite correct) | **1 pt** |
| Mauvais résultat | **0 pt** |

---

## Comment jouer

1. Ouvrir l'URL ci-dessus
2. Cliquer **"Ajouter un joueur"** — choisir un prénom, une couleur, et optionnellement une photo de profil
3. Aller dans **Pronos**, sélectionner son nom et saisir ses scores pour tous les matchs
4. Le tournoi commence le **11 juin 2026** — les pronostics doivent être saisis avant le coup d'envoi de chaque match
5. Consulter le **Classement** en temps réel après chaque journée

---

## Accès administrateur

Le code admin (pour saisir les vrais résultats) est : **`1234`**

---

## Fonctionnement technique détaillé

### Vue d'ensemble de l'architecture

```
Navigateur (HTML/CSS/JS)
        │
        ├── Lit et écrit les données  →  Firebase Firestore (base de données cloud)
        │                                       │
        │   ←── Reçoit les mises à jour en temps réel (onSnapshot)
        │
        └── Fichiers hébergés sur  →  Netlify (serveur web statique)
```

L'application est un **fichier HTML unique** (`loto-foot-app.html`) qui contient tout le code : HTML, CSS et JavaScript. Il n'y a aucun serveur backend, aucun langage serveur (PHP, Node.js, etc.), aucun build nécessaire.

---

### Firebase Firestore — la base de données

**Pourquoi Firebase ?**  
Sans base de données, chaque joueur aurait ses données stockées localement sur son téléphone, et personne ne verrait les pronostics des autres. Firebase est une base de données cloud gratuite (dans les limites du plan Spark) qui permet à tous les joueurs de partager le même état en temps réel.

**Structure des données**  
Tout l'état de l'application est stocké dans un seul document Firestore :

```
Collection : state
  └── Document : main
        ├── players : [{ id, name, color, photo }]
        ├── preds   : { "player_id": { "match_id": { s1, s2 } } }
        ├── results : { "match_id": { s1, s2 } }
        └── adminCode : "1234"
```

**Comment ça fonctionne en pratique**

1. Au chargement de la page, `load()` lit le document Firestore une première fois pour afficher l'état actuel.
2. `startSync()` ouvre une connexion permanente (`onSnapshot`) — Firebase envoie automatiquement les nouvelles données à chaque modification, sans que l'utilisateur ait besoin de rafraîchir la page.
3. À chaque saisie (prono ou résultat), `save()` écrit tout le document dans Firestore. Les autres appareils reçoivent la mise à jour en moins d'une seconde.

**Protection contre les boucles de re-rendu**  
Quand on écrit dans Firestore, `onSnapshot` se déclenche aussi sur l'appareil qui vient d'écrire. Pour éviter que la page se re-rende pendant la saisie (ce qui effacerait le chiffre en cours de frappe), un booléen `saving` est positionné à `true` pendant l'écriture et bloque le traitement de `onSnapshot`.

**Photos de profil**  
Les photos sont compressées côté client (canvas, max 200×200 px, qualité JPEG 65%) avant d'être stockées en base64 dans Firestore (~15–30 Ko par photo). Le document Firestore a une limite de 1 Mo, ce qui permet environ 30 joueurs avec photos.

---

### Netlify — l'hébergement web

**Pourquoi Netlify ?**  
Netlify est un service d'hébergement gratuit pour les sites statiques (HTML/CSS/JS sans serveur). Il fournit une URL publique accessible depuis n'importe quel appareil dans le monde.

**Comment le déploiement fonctionne**  
Netlify expose une API REST. Pour déployer, on utilise le protocole "Files API" en deux étapes :

1. **Créer un déploiement** (`POST /api/v1/sites/{site_id}/deploys`)  
   On envoie un JSON avec le hash SHA1 du fichier HTML. Netlify répond avec un `deploy_id` et indique quels fichiers il n'a pas encore.

2. **Uploader le fichier** (`PUT /api/v1/deploys/{deploy_id}/files/index.html`)  
   On envoie le contenu brut du fichier. Netlify le publie et le sert avec le bon `Content-Type: text/html`.

> **Pourquoi ne pas utiliser l'upload ZIP ?**  
> L'API ZIP de Netlify ne sert pas correctement les fichiers HTML (Content-Type incorrecte → le navigateur affiche le code source au lieu de l'exécuter). La méthode SHA1/PUT n'a pas ce problème.

**Redéployer après modification**  
Si tu modifies `loto-foot-app.html` et veux mettre à jour le site en ligne :

```powershell
$py = "C:\Users\Charlotte\AppData\Local\Python\bin\python.exe"
$script = @'
import urllib.request, json, hashlib

token = "TON_TOKEN_NETLIFY"   # app.netlify.com → User settings → Applications → Personal access tokens
site_id = "fb32884f-43ab-4175-b600-c64bd16bc52f"
html_path = r'C:\Users\Charlotte\Desktop\loto foot\loto-foot-app.html'

with open(html_path, 'rb') as f:
    content = f.read()
sha1 = hashlib.sha1(content).hexdigest()
payload = json.dumps({"files": {"index.html": sha1}}).encode()
req = urllib.request.Request(
    f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
    data=payload,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as r:
    deploy = json.loads(r.read())
deploy_id = deploy["id"]
req2 = urllib.request.Request(
    f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/index.html",
    data=content,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"},
    method="PUT"
)
with urllib.request.urlopen(req2) as r:
    r.read()
print("Deploye ! https://melodious-figolla-46b637.netlify.app")
'@
$tmpFile = "$env:TEMP\netlify_deploy.py"
[System.IO.File]::WriteAllText($tmpFile, $script, [System.Text.Encoding]::UTF8)
& $py $tmpFile
```

> Remplace `TON_TOKEN_NETLIFY` par ton token Netlify (à ne jamais committer dans git).

---

### Tester en local

Firebase ne fonctionne pas avec le protocole `file://` (restriction CORS). Pour tester localement, il faut un vrai serveur HTTP :

```powershell
$py = "C:\Users\Charlotte\AppData\Local\Python\bin\python.exe"
Set-Location "C:\Users\Charlotte\Desktop\loto foot"
& $py -m http.server 8081
# Ouvrir http://localhost:8081/loto-foot-app.html
```

---

### Sécurité

- **Firebase** : le projet utilise les règles Firestore "test mode" (lecture/écriture publique). C'est acceptable pour une application familiale sans données sensibles. Pour une utilisation plus large, il faudrait ajouter des règles de sécurité.
- **Token Netlify** : ne jamais committer le token dans git. Il est remplacé par `TON_TOKEN_NETLIFY` dans ce README.
- **Code admin** : le code `1234` est stocké en clair dans Firestore. Il protège uniquement l'interface de saisie des résultats contre les modifications accidentelles.

---

## Structure du projet

```
loto-foot/
├── loto-foot-app.html   # Application complète (HTML + CSS + JS)
├── A REMPLIR.xlsx       # Fichier Excel de pronostics (version hors-ligne)
└── README.md            # Cette documentation
```

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | HTML / CSS / JavaScript vanilla (fichier unique) |
| Base de données | Firebase Firestore (temps réel, plan Spark gratuit) |
| Hébergement | Netlify (statique, plan gratuit) |
| Déploiement | Script Python utilisant l'API REST Netlify |

---

## Calendrier des matchs

72 matchs, 12 groupes (A à L), du 11 juin au 27 juin 2026.

| Groupe | Équipes |
|--------|---------|
| A | Mexique, Afrique du Sud, Corée du Sud, Rép. Tchèque |
| B | Canada, Bosnie-Herzégovine, Qatar, Suisse |
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
