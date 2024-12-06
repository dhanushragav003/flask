from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# In-memory "database"
items = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpass@localhost/flask_app'  # Modify with your database credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True 

# Initialize SQLAlchemy
db = SQLAlchemy(app)
# A simple route to check the connection
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'
@app.route('/check_connection')
def check_connection():
    try:
        # Use 'text()' to explicitly declare the SQL query
        result = db.session.execute(text('SELECT 1'))
        return "Database connection is successful!"
    except Exception as e:
        return f"Failed to connect to the database: {e}"

@app.route('/users')
def show_users():
    # Query all users from the database
    users = User.query.all()
    return render_template('users.html', users=users)

# Home Page (View all items)
@app.route('/')
def index():
    """View all items"""
    return render_template('home.html', items=items)

# Create Page (Form for adding a new item)
@app.route('/create', methods=['GET', 'POST'])
def create_item():
    """Create a new item"""
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        description = request.form.get('description')
        new_item = {
            'id': len(items) + 1,
            'name': name,
            'description': description
        }
        items.append(new_item)  # Add the new item
        return redirect(url_for('index'))  # Redirect to the home page
    return render_template('create.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        item['name'] = request.form.get('name')
        item['description'] = request.form.get('description')
        return redirect(url_for('index'))

    return render_template('update.html', item=item)

@app.route('/delete/<int:item_id>',methods=['POST'])
def delete_item(item_id):
   item = next((item for item in items if item['id'] == item_id), None)
   if not item:
        return "Item not found", 404
   else:
       items.remove(item)
   return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
