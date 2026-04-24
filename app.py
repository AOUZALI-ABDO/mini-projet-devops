from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Formation

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/formations")
def formations():
    formations_list = Formation.query.all()
    return render_template("formations.html", formations=formations_list)

@app.route("/formations/<int:formation_id>/delete", methods=["POST"])
def delete_formation(formation_id):
    formation = Formation.query.get_or_404(formation_id)
    db.session.delete(formation)
    db.session.commit()
    return redirect(url_for("formations"))

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

def init_db():
    with app.app_context():
        db.create_all()

        if Formation.query.count() == 0:
            formations_data = [
                Formation(
                    titre="Introduction au DevOps",
                    description="Découvrir les bases du DevOps et de l'automatisation.",
                    duree="4 semaines"
                ),
                Formation(
                    titre="Docker pour débutants",
                    description="Apprendre à conteneuriser une application avec Docker.",
                    duree="3 semaines"
                ),
                Formation(
                    titre="CI/CD avec GitHub Actions",
                    description="Mettre en place un pipeline simple d'intégration et déploiement continus.",
                    duree="2 semaines"
                ),
                Formation(
                    titre="Kubernetes Essentials",
                    description="Comprendre les bases de l'orchestration des conteneurs.",
                    duree="5 semaines"
                ),
                Formation(
                    titre="Cloud Fundamentals",
                    description="Introduction aux services cloud et aux architectures modernes.",
                    duree="4 semaines"
                )
            ]

            db.session.add_all(formations_data)
            db.session.commit()
            print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
