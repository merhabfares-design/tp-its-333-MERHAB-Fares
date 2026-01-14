from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'pincode': self.pincode
        }