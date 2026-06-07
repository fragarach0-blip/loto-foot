# 🏆 Loto Foot – Coupe du Monde 2026

Application web familiale pour pronostiquer les 72 matchs de la phase de groupes de la Coupe du Monde 2026 (Canada, Mexique, États-Unis).

---

## 🌐 Application en ligne

**URL à partager à la famille :**  
👉 https://melodious-figolla-46b637.netlify.app

Tout le monde joue sur la même URL. Les pronostics et le classement sont **synchronisés en temps réel** grâce à Firebase.

---

## 🎯 Règles du jeu

| Résultat | Points |
|----------|--------|
| Score exact (ex : 2-1 prédit et 2-1 réel) | **3 pts** |
| Bon résultat (victoire / nul / défaite) | **1 pt** |
| Mauvais résultat | **0 pt** |

---

## 📱 Fonctionnalités

- **Accueil** — Liste des joueurs avec leurs scores et progression
- **Pronos** — Saisie des scores prédits pour les 72 matchs, filtrables par groupe (A à L)
- **Résultats** (admin) — Saisie des vrais scores au fil des matchs
- **Classement** — Podium et tableau de classement en temps réel

---

## 👥 Comment jouer

1. Ouvrir l'URL ci-dessus sur son téléphone ou ordinateur
2. Cliquer **"Ajouter un joueur"** et choisir un prénom, une couleur et une icône
3. Aller dans **Pronos**, sélectionner son nom et remplir ses scores pour tous les matchs
4. Le tournoi commence le **11 juin 2026** — les pronostics doivent être saisis avant le coup d'envoi !
5. Consulter le **Classement** après chaque journée de matchs

---

## 🔒 Accès administrateur

Le code admin (pour saisir les vrais résultats) est : **`1234`**

Pour le modifier : aller dans la zone Résultats → entrer le code → modifier le champ "Code admin" dans les paramètres.

---

## 🗂️ Structure du projet

```
loto-foot/
├── loto-foot-app.html   # Application web complète (HTML + CSS + JS en un seul fichier)
├── A REMPLIR.xlsx       # Fichier Excel de pronostics (version hors-ligne)
└── README.md            # Cette documentation
```

---

## ⚙️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Frontend  | HTML / CSS / JavaScript vanilla (single-file) |
| Base de données | Firebase Firestore (temps réel) |
| Hébergement | Netlify (gratuit) |
| Données stockées | Joueurs, pronostics, résultats, code admin |

### Structure des données Firebase (collection `state`, document `main`)

```json
{
  "players": [
    { "id": "p1234", "name": "Charlotte", "color": "#e74c3c", "icon": "👧" }
  ],
  "preds": {
    "p1234": {
      "1": { "s1": "2", "s2": "0" },
      "2": { "s1": "1", "s2": "1" }
    }
  },
  "results": {
    "1": { "s1": "2", "s2": "1" }
  },
  "adminCode": "1234"
}
```

---

## 🚀 Redéployer après modification

Si tu modifies `loto-foot-app.html` et veux mettre à jour le site en ligne, exécuter dans PowerShell :

```powershell
$py = "C:\Users\Charlotte\AppData\Local\Python\bin\python.exe"
$script = @'
import urllib.request, json, hashlib

token = "TON_TOKEN_NETLIFY"   # Voir : app.netlify.com → User settings → Applications → Personal access tokens
site_id = "TON_SITE_ID"        # Voir dans l'URL du site sur app.netlify.com/sites/
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
print("Déployé ! https://melodious-figolla-46b637.netlify.app")
'@
$tmpFile = "$env:TEMP\netlify_deploy.py"
[System.IO.File]::WriteAllText($tmpFile, $script, [System.Text.Encoding]::UTF8)
& $py $tmpFile
```

---

## 📅 Calendrier des matchs

72 matchs répartis en 12 groupes (A à L), du 11 juin au 27 juin 2026.

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
