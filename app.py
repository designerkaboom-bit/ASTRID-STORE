from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# 1. Initialization ng Flask App
app = Flask(__name__)
app.secret_key = 'astrid_super_secret_key'

# 2. Initialization at Setup ng LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Kailangan mo munang mag-sign in bago makapag-add to cart."

# Simple User Database (Admin at Regular User Accounts)
USERS = {
    "admin": {"password": "adminpassword", "role": "admin", "name": "Admin User"},
    "user": {"password": "userpassword", "role": "user", "name": "Customer User"}
}

# User Model para sa Flask-Login
class User(UserMixin):
    def __init__(self, id, role, name):
        self.id = id
        self.role = role
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        u = USERS[user_id]
        return User(id=user_id, role=u['role'], name=u['name'])
    return None

# In-memory List ng Produkto
PRODUCTS = [
    {
        "id": 1,
        "name": "Butterfly Alchemy Tee",
        "brand": "ASTRID",
        "category": "MEN",
        "price": 599,
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
        "description": "Premium black oversized tee featuring a cyan butterfly graphic print."
    },
    {
        "id": 2,
        "name": "NYX Graphic Shirt",
        "brand": "ASTRID",
        "category": "MEN",
        "price": 599,
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500",
        "description": "Vibrant anime mythological goddess back print on heavy cotton fabric."
    },
    {
        "id": 3,
        "name": "Barkada Tee (Cream)",
        "brand": "ASTRID",
        "category": "WOMEN",
        "price": 549,
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500",
        "description": "Relaxed fit cream shirt with beach chill aesthetic back illustration."
    },
    {
        "id": 4,
        "name": "Barkada Tee (Khaki)",
        "brand": "ASTRID",
        "category": "MEN",
        "price": 549,
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
        "description": "Earthy khaki tone street shirt with outdoor squad graphic print."
    },
    {
        "id": 5,
        "name": "Pakudos v1 Tribal Tee",
        "brand": "ASTRID",
        "category": "MEN",
        "price": 599,
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500",
        "description": "Royal blue streetwear shirt with geometric indigenous pattern design."
    },
    {
        "id": 6,
        "name": "Cookies and Cream Tee",
        "brand": "ASTRID",
        "category": "KIDS",
        "price": 499,
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500",
        "description": "Light cyan pop tee with dripping ice cream typography illustration."
    },
    {
        "id": 7,
        "name": "Coffea Liberica Tee",
        "brand": "ASTRID",
        "category": "MEN",
        "price": 549,
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
        "description": "Botanical coffee artwork back print on high-grade black fabric."
    },
    {
        "id": 8,
        "name": "Artemis Cyberpunk Tee",
        "brand": "ASTRID",
        "category": "LUXURY",
        "price": 599,
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500",
        "description": "Futuristic neon archer artwork print with Japanese kanji details."
    },
    {
        "id": 9,
        "name": "Astrid Safari Hat (Tan)",
        "brand": "ASTRID",
        "category": "BEAUTY",
        "price": 399,
        "image": "https://images.unsplash.com/photo-1533827432537-70133748f5c8?w=500",
        "description": "Durable khaki outdoor boonie hat with embroidered Astrid logo patch."
    },
    {
        "id": 10,
        "name": "Astrid Safari Hat (Black)",
        "brand": "ASTRID",
        "category": "BEAUTY",
        "price": 399,
        "image": "https://images.unsplash.com/photo-1521369984125-65d27b436374?w=500",
        "description": "Classic black utility bucket hat for sunny beach days and hikes."
    }
]

@app.route('/')
def home():
    category = request.args.get('category')
    search_query = request.args.get('search')
    
    filtered_products = PRODUCTS
    if category:
        filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
    if search_query:
        filtered_products = [p for p in filtered_products if search_query.lower() in p['name'].lower() or search_query.lower() in p['brand'].lower()]
        
    cart = session.get('cart', [])
    user = session.get('user')
    return render_template('index.html', products=filtered_products, cart_count=len(cart), selected_category=category, search_query=search_query, user=user)

# --- LOGIN & LOGOUT ---
# --- REGISTER ROUTE ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS:
            flash('Username is already taken! Please choose another one.', 'danger')
        elif not username or not password or not name:
            flash('Please fill out all fields.', 'warning')
        else:
            # I-save ang bagong user sa USERS dictionary
            USERS[username] = {
                "password": password,
                "role": "user",
                "name": name
            }
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            user_obj = User(id=username, role=USERS[username]['role'], name=USERS[username]['name'])
            login_user(user_obj)
            session['user'] = {
                'username': username,
                'name': USERS[username]['name'],
                'role': USERS[username]['role']
            }
            flash('Login successful!', 'success')
            if USERS[username]['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# --- ADMIN PANEL ROUTES ---
@app.route('/admin')
def admin_dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('login'))
        
    return render_template('admin.html', products=PRODUCTS, user=user)

@app.route('/admin/add-product', methods=['POST'])
def add_product():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return redirect(url_for('login'))
        
    name = request.form.get('name')
    brand = request.form.get('brand', 'ASTRID')
    category = request.form.get('category')
    price = float(request.form.get('price', 0))
    image = request.form.get('image')
    description = request.form.get('description')
    
    new_id = max([p['id'] for p in PRODUCTS], default=0) + 1
    new_product = {
        "id": new_id,
        "name": name,
        "brand": brand,
        "category": category,
        "price": price,
        "image": image or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
        "description": description
    }
    PRODUCTS.append(new_product)
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return redirect(url_for('login'))
        
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        product['name'] = request.form.get('name')
        product['brand'] = request.form.get('brand')
        product['category'] = request.form.get('category')
        product['price'] = float(request.form.get('price', 0))
        product['image'] = request.form.get('image')
        product['description'] = request.form.get('description')
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('edit_product.html', product=product, user=user)

@app.route('/admin/delete-product/<int:product_id>')
def delete_product(product_id):
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return redirect(url_for('login'))
        
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p['id'] != product_id]
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# --- USER CART & CHECKOUT ---
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    cart_items = [p for p in PRODUCTS if p['id'] in cart]
    total_price = sum(p['price'] for p in cart_items)
    user = session.get('user')
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, cart_count=len(cart), user=user)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', [])
    user = session.get('user')
    if request.method == 'POST':
        session['cart'] = []
        return render_template('checkout.html', success=True, user=user)
        
    cart_items = [p for p in PRODUCTS if p['id'] in cart]
    total_price = sum(p['price'] for p in cart_items)
    return render_template('checkout.html', success=False, cart_items=cart_items, total_price=total_price, user=user)

if __name__ == '__main__':
    app.run(debug=True)