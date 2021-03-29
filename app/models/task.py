from app.models import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)
    title = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, worker_id, admin_id, title, completed=False):
        self.worker_id = worker_id
        self.admin_id = admin_id
        self.title = title
        self.completed = completed

    def save(self):
        db.session.add(self)
        db.session.commit()
        