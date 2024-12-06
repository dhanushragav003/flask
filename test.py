from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Set the database URI (replace with your actual PostgreSQL details)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # Explicitly define the table name as 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/users')
def show_users():
    # Query all users from the database
    users = User.query.all()
    return render_template('users.html', users=users)
# Create Page (Form for adding a new item)
@app.route('/create', methods=['GET', 'POST'])
def create_item():
    """Create a new item"""
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        Email = request.form.get('email')
        new_user = User(username=name, email=Email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('show_users'))
    return render_template('create.html')


@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    user= User.query.get_or_404(id)
    if request.method=='POST':
        user.username=request.form['username']
        user.email=request.form['email']
        db.session.commit()
        return redirect(url_for('show_users'))
    return render_template('update.html',user=user)

@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
    user= User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))


if __name__ == '__main__':
    app.run(debug=True)
