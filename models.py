from extensions import db

from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String, nullable = False)


    def hashear_password(self, password_original):
        self.password = generate_password_hash(password_original)

    def verificar_password(self, password_plano):
        return check_password_hash(self.password,password_plano)
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
