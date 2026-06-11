from extensions import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("opportunity.id"), nullable=False)

    status = db.Column(db.String(50), default="applied")