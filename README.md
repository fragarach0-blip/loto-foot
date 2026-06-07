# PRONO '26

Application familiale de pronostics pour la Coupe du Monde 2026.

L'app est une PWA statique en HTML/CSS/JavaScript, sauvegardée avec Firebase Firestore et deployée sur GitHub Pages.

## Deux facons de jouer

### Matchs

L'onglet **Matchs** suit le calendrier reel.

- Chaque joueur pronostique le score des vrais matchs.
- Les matchs de groupes peuvent etre remplis des le depart.
- Pour les matchs de phase finale reels, il faut attendre que les vraies equipes soient connues.
- Si un score de phase finale est nul, il faut aussi choisir le vainqueur aux tirs au but.
- Les pronostics se verrouillent quand le match commence ou quand il est deja en cours/termine.

Bareme des matchs :

- Score exact en phase de groupes : 3 pts
- Bon resultat en phase de groupes : 1 pt
- Score exact en phase finale : 5 pts
- Bon resultat en phase finale : 2 pts

### Tournoi

L'onglet **Tournoi** simule le scenario complet d'un joueur.

- Le joueur doit d'abord remplir tous ses scores de phase de groupes dans **Matchs**.
- L'app calcule ensuite les equipes qualifiees selon ses propres scores.
- Les scores des 32es calculent les equipes des 8es.
- Les scores des 8es calculent les quarts.
- Puis quarts -> demies -> finale -> champion.
- En cas d'egalite en phase finale, le vainqueur aux tirs au but fait avancer l'equipe choisie.

Autrement dit :

**Matchs = calendrier reel.**
**Tournoi = scenario complet du joueur.**

Bareme Tournoi :

- Equipe correcte en 8es : 1 pt
- Equipe correcte en quarts : 2 pts
- Equipe correcte en demies : 4 pts
- Equipe correcte en finale : 7 pts
- Champion correct : 10 pts

Total maximum Tournoi : 72 pts.

## Classement

Le classement additionne :

- les points des pronostics de matchs ;
- les points du scenario Tournoi.

Le total affiche donc le score general du joueur.

## Structure

- `index.html` : toute l'application HTML/CSS/JS.
- `manifest.json` : configuration PWA.
- `sw.js` : service worker.
- `icon.svg` : icone de l'app.

## Developpement local

Depuis le dossier du repo :

```bash
python -m http.server 8080
```

Puis ouvrir :

```text
http://127.0.0.1:8080
```

## Deploiement

Le site est deploye via la branche `gh-pages`.

Workflow utilise :

1. Modifier l'app sur la branche de travail.
2. Pousser la branche de travail.
3. Synchroniser `gh-pages`.
4. Pousser `gh-pages` pour deployer GitHub Pages.

URL de production :

```text
https://fragarach0-blip.github.io/loto-foot/
```
