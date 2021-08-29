from assignment_logic.assignment2.config import db

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    done = db.Column(db.Boolean,default=False)

db.create_all()