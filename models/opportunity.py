from extensions import db

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    skills = db.Column(db.String(300))
    match_score = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    applications = db.relationship("Application", backref="job_ref", lazy=True)