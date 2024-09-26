from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "author": self.author
        }