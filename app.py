from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "replace_this_with_a_long_random_secret"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

# Home route
@app.route("/")
def index():
    return render_template("index.html")


# Handle contact form
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required!", "error")
        return redirect(url_for("index"))

    # Save to DB
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    flash("Thanks for contacting me! I'll get back to you soon.", "success")
    return redirect(url_for("index"))

# Admin route to view all messages
@app.route("/messages")
def messages():
    all_contacts = Contact.query.all()
    return render_template("messages.html", contacts=all_contacts)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates contacts.db if it doesn’t exist
    app.run(debug=True)
