from app import db
from flask_login import UserMixin

# Association table
library = db.Table(
    "library",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("game_id", db.Integer, db.ForeignKey("games.id")),
)


class Game(db.Model):
    __tablename__: str = "games"

    id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String(80), nullable=False)
    game_progress = db.Column(db.Integer)

    def __repr__(self):
        return f"<Game {self.game_title}>"


class User(UserMixin, db.Model):
    __tablename__: str = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    games = db.relationship("Game", secondary=library, backref="users")

    def __repr__(self):
        return f"<User {self.username}>"
