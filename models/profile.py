from extensions import db
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    full_name = db.Column(db.String(120))
    bio = db.Column(db.Text)

    skills = db.Column(db.String(200))
    experience = db.Column(db.String(200))

    github = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))