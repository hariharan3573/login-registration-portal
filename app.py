from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"user('{self.name}', '{self.email}')"


@app.route("/add_users")
def add_user():
    try:
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        return "Users added!"
    except IntegrityError:
        db.session.rollback()
        return "User already exists. Duplicate email not allowed."


@app.route("/users")
def users():
    all_users = User.query.all()
    return str(all_users)


@app.route("/delete_all")
def delete_all():
    db.session.query(User).delete()
    db.session.commit()
    return "All users deleted!"


@app.route("/users_page")
def users_page():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
