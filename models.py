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