# Rapport Detaille - Mini-Projet DevOps

## Informations generales

- **Intitule du projet** : Application web de gestion de formations
- **Technologies principales** : Python, Flask, SQLite, HTML, CSS, Docker, Docker Compose, GitHub Actions
- **Cadre du projet** : Mini-projet d'automatisation / DevOps

---

## 1. Introduction

Ce mini-projet a pour objectif de concevoir une application web simple permettant de gerer une liste de formations. L'application offre une interface permettant d'afficher les formations disponibles, d'ajouter une nouvelle formation et de supprimer une formation existante.

L'interet pedagogique de ce projet ne se limite pas au developpement web. Il permet aussi de mettre en pratique plusieurs notions DevOps importantes, notamment :

- la structuration d'une application Python avec Flask ;
- la gestion des donnees avec SQLite ;
- la conteneurisation avec Docker ;
- l'orchestration locale avec Docker Compose ;
- l'automatisation de verification avec GitHub Actions.

Ce projet constitue donc un exemple complet d'une mini-application metier, accompagnee de son environnement d'execution et de son pipeline d'integration continue.

---

## 2. Objectifs du projet

Les objectifs du mini-projet sont les suivants :

- developper une application web fonctionnelle avec Flask ;
- stocker les donnees dans une base SQLite ;
- proposer une interface simple, lisible et exploitable ;
- dockeriser l'application pour faciliter son execution ;
- preparer un fichier Docker Compose pour simplifier le deploiement local ;
- automatiser certaines verifications via GitHub Actions ;
- documenter l'ensemble du travail de facon claire et professionnelle.

---

## 3. Presentation generale de l'application

L'application developpee est une plateforme simple de gestion de formations. Elle contient trois parcours principaux :

- une page d'accueil ;
- une page d'affichage des formations ;
- une page d'ajout d'une nouvelle formation.

Une fonctionnalite supplementaire a egalement ete integree :

- la suppression d'une formation depuis la liste des formations.

### Fonctionnalites principales

1. **Afficher les formations**
   L'utilisateur peut consulter la liste des formations enregistrees dans la base de donnees.

2. **Ajouter une formation**
   L'utilisateur peut remplir un formulaire contenant le titre, la description et la duree.

3. **Supprimer une formation**
   L'utilisateur peut supprimer une formation directement depuis la liste via un bouton dedie.

---

## 4. Architecture technique du projet

Le projet suit une architecture simple et facile a maintenir.

### Structure des fichiers

```text
mini-projet-devops/
|-- app.py
|-- config.py
|-- models.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- formations.db
|-- static/
|   `-- style.css
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- formations.html
|   `-- add_formation.html
`-- .github/
    `-- workflows/
        `-- ci.yml
```

### Role des principaux fichiers

- `app.py` : point d'entree principal de l'application Flask ;
- `config.py` : configuration generale de l'application ;
- `models.py` : definition du modele de donnees ;
- `templates/` : vues HTML avec Jinja2 ;
- `static/style.css` : mise en forme visuelle ;
- `Dockerfile` : creation de l'image Docker ;
- `docker-compose.yml` : lancement de l'application avec Docker Compose ;
- `.github/workflows/ci.yml` : pipeline CI ;
- `formations.db` : base de donnees SQLite.

---

## 5. Analyse du code source

## 5.1 Configuration de l'application

Le fichier `config.py` centralise les parametres de l'application. Cette approche permet de separer la configuration de la logique metier.

### Code

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "devops-mini-projet-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "formations.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Explication

- `basedir` recupere le chemin absolu du projet ;
- `SECRET_KEY` est une cle de configuration Flask ;
- `SQLALCHEMY_DATABASE_URI` indique que la base utilisee est SQLite ;
- `SQLALCHEMY_TRACK_MODIFICATIONS = False` evite des surcharges inutiles.

### Espace capture

**Capture a inserer ici :** configuration generale du projet ou structure des fichiers.

---

## 5.2 Modele de donnees

Le modele de donnees est defini dans `models.py`. Il represente une formation.

### Code

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Formation(db.Model):
    __tablename__ = "formations"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    duree = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Formation {self.titre}>"
```

### Explication

Ce modele contient :

- `id` : identifiant unique de la formation ;
- `titre` : nom de la formation ;
- `description` : resume de son contenu ;
- `duree` : duree estimee de la formation.

Le mot-cle `nullable=False` garantit que ces champs sont obligatoires.

### Espace capture

**Capture a inserer ici :** contenu de la base ou visualisation de la table `formations`.

---

## 5.3 Logique principale de l'application Flask

Le coeur du projet se trouve dans `app.py`.

### Initialisation de Flask

```python
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Formation

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
```

### Explication

- `Flask(__name__)` cree l'application ;
- `app.config.from_object(Config)` charge la configuration ;
- `db.init_app(app)` relie SQLAlchemy a Flask.

---

## 5.4 Route de la page d'accueil

### Code

```python
@app.route("/")
def home():
    return render_template("index.html")
```

### Explication

Cette route affiche la page d'accueil. C'est la premiere page visible lorsqu'on ouvre l'application.

### Espace capture

**Capture a inserer ici :** page d'accueil de l'application.

---

## 5.5 Route d'affichage des formations

### Code

```python
@app.route("/formations")
def formations():
    formations_list = Formation.query.all()
    return render_template("formations.html", formations=formations_list)
```

### Explication

Cette route :

- interroge la base de donnees ;
- recupere toutes les formations ;
- transmet les donnees au template `formations.html`.

Le template affiche ensuite dynamiquement chaque formation.

### Espace capture

**Capture a inserer ici :** page de liste des formations.

---

## 5.6 Route d'ajout d'une formation

### Code

```python
@app.route("/add", methods=["GET", "POST"])
def add_formation():
    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description")
        duree = request.form.get("duree")

        if titre and description and duree:
            nouvelle_formation = Formation(
                titre=titre,
                description=description,
                duree=duree
            )
            db.session.add(nouvelle_formation)
            db.session.commit()

            return redirect(url_for("formations"))

    return render_template("add_formation.html")
```

### Explication

Cette route gere deux comportements :

- en `GET`, elle affiche le formulaire ;
- en `POST`, elle recupere les donnees saisies puis enregistre une nouvelle formation.

Une fois l'ajout effectue, l'utilisateur est redirige vers la liste des formations.

### Espace capture

**Capture a inserer ici :** formulaire d'ajout d'une formation.

**Capture a inserer ici :** resultat apres ajout d'une nouvelle formation.

---

## 5.7 Route de suppression d'une formation

Cette fonctionnalite a ete ajoutee pour rendre l'application plus complete.

### Code

```python
@app.route("/formations/<int:formation_id>/delete", methods=["POST"])
def delete_formation(formation_id):
    formation = Formation.query.get_or_404(formation_id)
    db.session.delete(formation)
    db.session.commit()
    return redirect(url_for("formations"))
```

### Explication

Cette route permet :

- d'identifier une formation par son identifiant ;
- de verifier qu'elle existe ;
- de la supprimer de la base de donnees ;
- de recharger la liste des formations.

L'utilisation de `POST` pour la suppression est plus propre qu'une suppression via un simple lien `GET`.

### Espace capture

**Capture a inserer ici :** bouton de suppression visible dans la liste.

**Capture a inserer ici :** liste mise a jour apres suppression.

---

## 6. Interface utilisateur

L'interface a ete construite avec des templates HTML et une feuille de style CSS.

## 6.1 Template de base

Le fichier `base.html` sert de squelette commun a toutes les pages.

### Code

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Formation App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>Formation App DevOps</h1>
        <p>Application web simple avec Flask, SQLite et Docker</p>
    </header>

    <nav>
        <a href="/">Accueil</a>
        <a href="/formations">Formations</a>
        <a href="/add">Ajouter</a>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### Explication

L'avantage principal de `base.html` est d'eviter la repetition. Toutes les autres pages l'etendent et ne remplacent que le contenu utile.

---

## 6.2 Page d'accueil

La page d'accueil presente le projet de facon simple et propose un acces rapide a la liste des formations.

### Espace capture

**Capture a inserer ici :** page d'accueil complete.

---

## 6.3 Page de liste des formations

Cette page affiche les donnees enregistrees dans la base. Chaque bloc contient :

- le titre ;
- la duree ;
- la description ;
- le bouton de suppression.

### Espace capture

**Capture a inserer ici :** liste complete des formations.

---

## 6.4 Page d'ajout

Cette page contient un formulaire clair avec trois champs obligatoires :

- titre ;
- description ;
- duree.

Le formulaire est relie directement a la route `/add`.

### Espace capture

**Capture a inserer ici :** page d'ajout.

---

## 6.5 Mise en forme CSS

Le fichier `static/style.css` ameliore l'aspect visuel de l'application. Il definit :

- la palette de couleurs ;
- les cartes ;
- les boutons ;
- l'espacement ;
- l'alignement des elements ;
- l'apparence de la liste des formations.

### Extrait de code

```css
.formation-item {
    background: var(--bg-panel);
    border: 1px solid var(--border-soft);
    border-left: 5px solid var(--green-600);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: var(--shadow-soft);
}

.formation-actions {
    margin-top: 14px;
    display: flex;
    justify-content: flex-end;
}

.btn-danger {
    background-color: #c0392b;
}
```

### Explication

Cette feuille de style permet d'obtenir une interface plus professionnelle, plus lisible et plus agreable a utiliser.

---

## 7. Initialisation de la base de donnees

L'application contient une fonction `init_db()` qui :

- cree les tables si elles n'existent pas ;
- insere un jeu initial de formations si la base est vide.

### Code

```python
def init_db():
    with app.app_context():
        db.create_all()

        if Formation.query.count() == 0:
            formations_data = [
                Formation(
                    titre="Introduction au DevOps",
                    description="Decouvrir les bases du DevOps et de l'automatisation.",
                    duree="4 semaines"
                ),
                Formation(
                    titre="Docker pour debutants",
                    description="Apprendre a conteneuriser une application avec Docker.",
                    duree="3 semaines"
                )
            ]

            db.session.add_all(formations_data)
            db.session.commit()
```

### Explication

Ce mecanisme facilite les demonstrations et les tests, car l'application n'est pas vide au premier lancement.

### Espace capture

**Capture a inserer ici :** premier lancement avec les donnees initiales.

---

## 8. Dockerisation du projet

La dockerisation permet d'executer l'application dans un environnement isole et reproductible.

## 8.1 Dockerfile

### Code

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Explication detaillee

- `FROM python:3.11-slim` : utilisation d'une image Python legere ;
- `WORKDIR /app` : definition du dossier de travail ;
- `COPY requirements.txt .` : copie de la liste des dependances ;
- `RUN pip install --no-cache-dir -r requirements.txt` : installation des bibliotheques ;
- `COPY . .` : copie du code source ;
- `EXPOSE 5000` : ouverture du port de l'application ;
- `CMD ["python", "app.py"]` : commande de demarrage.

### Commandes utiles

```bash
docker build -t formation-app .
docker run -p 5000:5000 formation-app
```

### Espace capture

**Capture a inserer ici :** resultat de `docker build`.

**Capture a inserer ici :** conteneur en execution ou application lancee via Docker.

---

## 9. Docker Compose

Docker Compose simplifie le lancement du projet.

### Code

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: formation-compose
    ports:
      - "5000:5000"
    volumes:
      - ./formations.db:/app/formations.db
    restart: always
```

### Explication

- `build: .` : construit l'image a partir du projet courant ;
- `container_name` : attribue un nom fixe au conteneur ;
- `ports` : relie le port local au port du conteneur ;
- `volumes` : conserve la base SQLite entre les executions ;
- `restart: always` : redemarre automatiquement le conteneur si necessaire.

### Commandes utiles

```bash
docker compose up --build
docker compose down
```

### Espace capture

**Capture a inserer ici :** execution de `docker compose up --build`.

---

## 10. Integration continue avec GitHub Actions

Le projet contient un pipeline CI defini dans `.github/workflows/ci.yml`.

### Code

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main
      - master
  pull_request:
    branches:
      - main
      - master

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Installer les dependances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Test simple de syntaxe
        run: |
          python -m py_compile app.py
          python -m py_compile models.py
          python -m py_compile config.py

      - name: Build image Docker
        run: |
          docker build -t formation-app .

      - name: Verification Docker Compose
        run: |
          docker compose config
```

### Explication du pipeline

Ce pipeline effectue automatiquement plusieurs verifications a chaque `push` ou `pull request` :

1. recuperation du code source ;
2. installation de Python ;
3. installation des dependances ;
4. verification syntaxique des fichiers Python ;
5. construction de l'image Docker ;
6. validation du fichier Docker Compose.

### Interet DevOps

L'utilisation de GitHub Actions permet :

- de detecter les erreurs plus tot ;
- de fiabiliser l'integration du projet ;
- d'automatiser les controles repetitifs ;
- de preparer le terrain pour un futur deploiement automatise.

### Espace capture

**Capture a inserer ici :** execution reussie du workflow GitHub Actions.

---

## 11. Dependances du projet

Les dependances sont listees dans `requirements.txt`.

### Extrait

```text
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.49
Werkzeug==3.1.8
Jinja2==3.1.6
```

### Explication

- `Flask` : framework web principal ;
- `Flask-SQLAlchemy` : integration ORM avec Flask ;
- `SQLAlchemy` : gestion de la couche base de donnees ;
- `Jinja2` : moteur de templates ;
- `Werkzeug` : outils bas niveau utilises par Flask.

---

## 12. Procedure d'execution du projet

## 12.1 Execution en local

### Commandes

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

L'application devient accessible a l'adresse :

```text
http://127.0.0.1:5000
```

### Espace capture

**Capture a inserer ici :** terminal montrant le lancement local de l'application.

---

## 12.2 Execution avec Docker

### Commandes

```bash
docker build -t formation-app .
docker run -p 5000:5000 formation-app
```

---

## 12.3 Execution avec Docker Compose

### Commandes

```bash
docker compose up --build
```

---

## 13. Tests et verifications

Dans ce mini-projet, les verifications automatisees actuelles portent principalement sur :

- la validite syntaxique du code Python ;
- la construction de l'image Docker ;
- la coherence de la configuration Docker Compose.

Ces tests sont simples, mais ils constituent deja une bonne base d'automatisation.

### Ameliorations possibles

Dans une version future, il serait pertinent d'ajouter :

- des tests unitaires Flask ;
- des tests d'integration sur les routes ;
- une verification automatique des templates ;
- un linting avec `flake8` ou `ruff`.

---

## 14. Difficultes rencontrees et solutions

Plusieurs points techniques peuvent etre rencontres dans ce type de projet :

### 1. Liaison entre Flask et SQLite

La solution a consiste a centraliser la configuration dans `config.py` et a utiliser SQLAlchemy pour simplifier les interactions avec la base.

### 2. Conservation des donnees avec Docker

Le probleme de perte des donnees au redemarrage a ete resolu grace au volume :

```yaml
volumes:
  - ./formations.db:/app/formations.db
```

### 3. Automatisation de la verification

Le pipeline GitHub Actions a permis de garantir une verification automatique a chaque mise a jour du depot.

### 4. Ergonomie de l'interface

Une feuille de style CSS personnalisee a ete mise en place pour obtenir une interface plus propre et lisible.

---

## 15. Ameliorations apportees au projet

En plus du socle principal, une amelioration utile a ete apportee :

- ajout d'un bouton de suppression pour retirer une formation directement depuis la liste.

Cette amelioration rend l'application plus proche d'un veritable outil CRUD, meme si la modification des formations n'a pas encore ete implementee.

D'autres pistes d'amelioration restent possibles :

- ajouter la modification d'une formation ;
- ajouter des messages de succes ou d'erreur ;
- ajouter une confirmation JavaScript avant suppression ;
- renforcer la validation des formulaires ;
- ajouter des tests automatises plus complets ;
- deployer l'application sur une plateforme cloud.

---

## 16. Bilan pedagogique

Ce mini-projet m'a permis de mobiliser plusieurs competences complementaires :

- developpement backend avec Flask ;
- modelisation simple de donnees ;
- integration frontend via templates HTML/CSS ;
- conteneurisation de l'application ;
- orchestration avec Docker Compose ;
- automatisation de la verification avec GitHub Actions ;
- organisation propre d'un projet logiciel.

Il montre qu'une approche DevOps ne consiste pas uniquement a ecrire du code, mais aussi a preparer un environnement fiable, reproductible et automatisable.

---

## 17. Conclusion

Ce mini-projet repond aux besoins d'une application web simple de gestion de formations tout en integrant les principaux piliers attendus dans une demarche DevOps : developpement, persistence des donnees, conteneurisation et automatisation.

L'application est fonctionnelle, claire et evolutive. Elle peut servir de base a un projet plus ambitieux, par exemple avec authentification, deploiement continu, tests plus complets et separation des environnements.

En conclusion, ce travail illustre concretement l'apport des pratiques DevOps dans la realisation d'une application moderne, meme de petite taille.

---

## 18. Annexes - Extraits de code utiles

## Annexe A - Route d'affichage

```python
@app.route("/formations")
def formations():
    formations_list = Formation.query.all()
    return render_template("formations.html", formations=formations_list)
```

## Annexe B - Route d'ajout

```python
@app.route("/add", methods=["GET", "POST"])
def add_formation():
    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description")
        duree = request.form.get("duree")
```

## Annexe C - Route de suppression

```python
@app.route("/formations/<int:formation_id>/delete", methods=["POST"])
def delete_formation(formation_id):
    formation = Formation.query.get_or_404(formation_id)
    db.session.delete(formation)
    db.session.commit()
    return redirect(url_for("formations"))
```

## Annexe D - Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Annexe E - Docker Compose

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
```

---

## 19. Emplacements recommandes pour les captures d'ecran

Pour obtenir un rapport bien equilibre et visuellement coherent, il est recommande d'ajouter les captures suivantes :

1. page d'accueil ;
2. page liste des formations ;
3. formulaire d'ajout ;
4. ajout reussi d'une formation ;
5. bouton de suppression ;
6. suppression reussie ;
7. execution locale dans le terminal ;
8. resultat de `docker build` ;
9. resultat de `docker compose up --build` ;
10. workflow GitHub Actions reussi.

---

## 20. Remarque finale

Le present rapport a ete redige de maniere detaillee afin de decrire a la fois :

- la partie developpement de l'application ;
- la partie base de donnees ;
- la partie conteneurisation ;
- la partie automatisation CI ;
- la logique globale du mini-projet.

Il peut etre reutilise comme base de rendu final, puis complete avec :

- le nom complet de l'etudiant ;
- les captures d'ecran ;
- d'eventuelles consignes specifiques de l'encadrant ;
- une mise en page finale sous Word ou PDF.
