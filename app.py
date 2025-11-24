from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import json
import os
import sys
from datetime import datetime
import hashlib

# Verificar e instalar dependências automaticamente
try:
    from flask import Flask
    print("✅ Flask já está instalado!")
except ImportError:
    print("📦 Instalando Flask...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'tenis_store_2024_modern_key'

# Arquivo do banco de dados
DB_FILE = 'database.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'users': [],
        'products': [],
        'user_behaviors': [],
        'cart_items': [],
        'orders': [],
        'favorites': []
    }

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_default_data():
    data = load_db()
    
    # Garantir que todas as chaves necessárias existam
    required_keys = ['users', 'products', 'user_behaviors', 'cart_items', 'orders', 'favorites']
    for key in required_keys:
        if key not in data:
            data[key] = []
    
    # Usuário admin padrão
    if not any(user['username'] == 'admin' for user in data['users']):
        data['users'].append({
            'id': 1,
            'username': 'admin',
            'email': 'admin@tenisstore.com',
            'password': hash_password('admin123'),
            'role': 'admin',
            'created_at': datetime.now().isoformat()
        })
    
    # Produtos padrão com todas as marcas
    if not data['products']:
        data['products'] = [
            {
                'id': 1,
                'name': 'Tênis Nike Air Max 270 - EDIÇÃO LIMITADA',
                'description': 'Tênis esportivo com tecnologia Air Max para máximo conforto e estilo urbano.',
                'price': 899.99,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
                'category': 'Esportivo',
                'brand': 'Nike',
                'featured': True,
                'stock': 8,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'name': 'Tênis Adidas Ultraboost 5.0',
                'description': 'Tênis de corrida com tecnologia Boost para amortecimento superior e performance máxima.',
                'price': 799.99,
                'image_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500',
                'category': 'Corrida',
                'brand': 'Adidas',
                'featured': True,
                'stock': 12,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'name': 'Tênis Puma RS-X',
                'description': 'Tênis casual com design retrô inspirado nos anos 80 e conforto moderno.',
                'price': 499.99,
                'image_url': 'https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=500',
                'category': 'Casual',
                'brand': 'Puma',
                'featured': False,
                'stock': 25,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 4,
                'name': 'Tênis New Balance 574',
                'description': 'Clássico atemporal com conforto duradouro e estilo versátil para o dia a dia.',
                'price': 449.99,
                'image_url': 'https://images.unsplash.com/photo-1549289524-06cf8837ace5?w=500',
                'category': 'Casual',
                'brand': 'New Balance',
                'featured': False,
                'stock': 30,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 5,
                'name': 'Tênis Nike Air Jordan 1',
                'description': 'Ícone do basquete com design clássico e tecnologia moderna.',
                'price': 1299.99,
                'image_url': 'https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500',
                'category': 'Basquete',
                'brand': 'Jordan',
                'featured': False,
                'stock': 5,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 6,
                'name': 'Tênis Adidas Superstar',
                'description': 'Clássico atemporal com design icônico e conforto superior.',
                'price': 599.99,
                'image_url': 'https://images.unsplash.com/photo-1543508282-6319a3e2621f?w=500',
                'category': 'Casual',
                'brand': 'Adidas',
                'featured': False,
                'stock': 15,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 7,
                'name': 'Tênis Mizuno Wave Rider',
                'description': 'Tênis de corrida com tecnologia Wave para excelente amortecimento e estabilidade.',
                'price': 699.99,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
                'category': 'Corrida',
                'brand': 'Mizuno',
                'featured': False,
                'stock': 10,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 8,
                'name': 'Tênis Vans Old Skool',
                'description': 'Clássico do skate com design icônico e durabilidade comprovada.',
                'price': 349.99,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
                'category': 'Skate',
                'brand': 'Vans',
                'featured': False,
                'stock': 20,
                'created_at': datetime.now().isoformat()
            }
        ]
    
    save_db(data)

def is_admin():
    return session.get('role') == 'admin'

def track_behavior(user_id, product_id, action, weight=1):
    """Rastreia comportamento com pesos diferentes para cada ação"""
    data = load_db()
    
    # Verificar se já existe comportamento similar recente (evitar spam)
    recent_behavior = next((b for b in data.get('user_behaviors', []) 
                          if b['user_id'] == user_id and 
                          b['product_id'] == product_id and 
                          b['action'] == action and
                          (datetime.now() - datetime.fromisoformat(b['timestamp'])).seconds < 300), None)
    
    if not recent_behavior:
        behavior = {
            'id': len(data['user_behaviors']) + 1,
            'user_id': user_id,
            'product_id': product_id,
            'action': action,
            'weight': weight,  # Peso da ação
            'timestamp': datetime.now().isoformat()
        }
        data['user_behaviors'].append(behavior)
        save_db(data)

def get_brand_preferences(user_id=None):
    """Calcula preferências por marca com pesos diferentes para cada ação"""
    data = load_db()
    behaviors = data.get('user_behaviors', [])
    products = data.get('products', [])
    
    # SEMPRE filtrar por usuário específico se fornecido
    if user_id:
        behaviors = [b for b in behaviors if b['user_id'] == user_id]
    else:
        return {}
    
    brand_scores = {}
    total_score = 0
    
    for behavior in behaviors:
        product = next((p for p in products if p['id'] == behavior['product_id']), None)
        if product:
            brand = product['brand']
            if brand not in brand_scores:
                brand_scores[brand] = 0
            
            # Diferentes pesos para diferentes ações
            weight = behavior.get('weight', 1)
            if behavior['action'] == 'favorite':
                weight = 3  # Favoritar vale mais
            elif behavior['action'] == 'cart_add':
                weight = 2  # Adicionar ao carrinho vale mais que visualizar
            elif behavior['action'] == 'view':
                weight = 1
            
            brand_scores[brand] += weight
            total_score += weight
    
    # Calcular porcentagens
    brand_percentages = {}
    for brand, score in brand_scores.items():
        percentage = (score / total_score) * 100 if total_score > 0 else 0
        brand_percentages[brand] = round(percentage, 1)
    
    return brand_percentages

def get_user_recommendations(user_id):
    """Gera recomendações baseadas nas preferências do usuário"""
    if not user_id:
        return []
    
    user_preferences = get_brand_preferences(user_id)
    if not user_preferences:
        # Se não houver preferências, retorna produtos em destaque
        data = load_db()
        return [p for p in data['products'] if p['featured']][:4]
    
    # Ordenar marcas por preferência
    sorted_brands = sorted(user_preferences.items(), key=lambda x: x[1], reverse=True)
    
    # Pegar a marca mais preferida
    top_brand = sorted_brands[0][0] if sorted_brands else None
    
    if not top_brand:
        return []
    
    # Buscar produtos da marca preferida
    data = load_db()
    recommended_products = [p for p in data['products'] if p['brand'] == top_brand]
    
    # Se não houver produtos suficientes da marca preferida, adicionar de outras marcas
    if len(recommended_products) < 4:
        other_products = [p for p in data['products'] if p['brand'] != top_brand and p not in recommended_products]
        recommended_products.extend(other_products[:4 - len(recommended_products)])
    
    return recommended_products[:4]

def get_user_favorites(user_id):
    """Obtém produtos favoritos do usuário"""
    if not user_id:
        return []
    
    data = load_db()
    favorites = [fav for fav in data.get('favorites', []) if fav['user_id'] == user_id]
    
    favorite_products = []
    for fav in favorites:
        product = next((p for p in data['products'] if p['id'] == fav['product_id']), None)
        if product:
            favorite_products.append(product)
    
    return favorite_products

def is_product_favorited(user_id, product_id):
    """Verifica se um produto está favoritado pelo usuário"""
    data = load_db()
    return any(fav for fav in data.get('favorites', []) 
               if fav['user_id'] == user_id and fav['product_id'] == product_id)

def get_prioritized_products(user_id=None):
    """Retorna produtos priorizados por preferências do usuário"""
    data = load_db()
    all_products = data['products']
    
    if not user_id:
        # Se não estiver logado, retorna produtos normais
        return all_products
    
    user_preferences = get_brand_preferences(user_id)
    if not user_preferences:
        return all_products
    
    # Ordenar produtos por preferência da marca
    def product_score(product):
        brand_preference = user_preferences.get(product['brand'], 0)
        # Produtos em destaque ganham um pequeno bônus
        featured_bonus = 10 if product.get('featured', False) else 0
        return brand_preference + featured_bonus
    
    return sorted(all_products, key=product_score, reverse=True)

def get_brand_color(brand):
    colors = {
        'Nike': '#ff6b6b',
        'Adidas': '#4ecdc4',
        'Puma': '#45b7d1',
        'New Balance': '#96ceb4',
        'Mizuno': '#feca57',
        'Jordan': '#ff9ff3',
        'Vans': '#54a0ff'
    }
    return colors.get(brand, '#6366f1')

# Registrar a função no Jinja2
app.jinja_env.globals.update(get_brand_color=get_brand_color)
app.jinja_env.globals.update(is_product_favorited=is_product_favorited)

# Middleware para verificar admin
@app.before_request
def check_admin():
    if request.path.startswith('/admin') and not is_admin():
        return redirect('/login?next=' + request.path)

# Rotas Principais
@app.route('/')
def home():
    data = load_db()
    
    # Obter produtos priorizados por preferências
    prioritized_products = get_prioritized_products(session.get('user_id'))
    
    # Separar em destacados e outros
    featured_products = [p for p in prioritized_products if p['featured']]
    other_products = [p for p in prioritized_products if not p['featured']]
    
    # Obter recomendações personalizadas se o usuário estiver logado
    user_recommendations = []
    if 'user_id' in session:
        user_recommendations = get_user_recommendations(session['user_id'])
    
    return render_template('index.html',
                         featured_products=featured_products,
                         other_products=other_products,
                         user_recommendations=user_recommendations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_db()
        user = next((u for u in data['users'] if u['username'] == username and u['password'] == hash_password(password)), None)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            session['email'] = user.get('email', '')
            
            next_page = request.args.get('next', '')
            if next_page.startswith('/admin'):
                return redirect('/admin')
            return redirect('/')
        else:
            flash('Usuário ou senha incorretos!', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'error')
            return render_template('register.html')
        
        data = load_db()
        
        # Verificar se usuário já existe
        if any(u['username'] == username for u in data['users']):
            flash('Nome de usuário já existe!', 'error')
            return render_template('register.html')
        
        if any(u['email'] == email for u in data['users']):
            flash('Email já cadastrado!', 'error')
            return render_template('register.html')
        
        # Criar novo usuário
        new_user = {
            'id': len(data['users']) + 1,
            'username': username,
            'email': email,
            'password': hash_password(password),
            'role': 'user',
            'created_at': datetime.now().isoformat()
        }
        
        data['users'].append(new_user)
        save_db(data)
        
        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect('/')

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')
    
    data = load_db()
    user_cart = [item for item in data.get('cart_items', []) if item['user_id'] == session['user_id']]
    
    cart_with_products = []
    total = 0
    for item in user_cart:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            cart_with_products.append({
                **item,
                'product': product,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_with_products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não logado'})
    
    data = load_db()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    
    # Verificar se o produto já está no carrinho
    cart_item = next((item for item in data.get('cart_items', []) 
                     if item['user_id'] == session['user_id'] and item['product_id'] == product_id), None)
    
    if cart_item:
        cart_item['quantity'] += 1
    else:
        new_item = {
            'id': len(data.get('cart_items', [])) + 1,
            'user_id': session['user_id'],
            'product_id': product_id,
            'quantity': 1
        }
        if 'cart_items' not in data:
            data['cart_items'] = []
        data['cart_items'].append(new_item)
    
    # Rastrear comportamento - ADIÇÕES AO CARRINHO (peso 2)
    track_behavior(session['user_id'], product_id, 'cart_add', weight=2)
    
    save_db(data)
    return jsonify({'success': True, 'message': 'Produto adicionado ao carrinho!'})

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    if 'user_id' not in session:
        return jsonify({'success': False})
    
    data = load_db()
    cart_item = next((item for item in data.get('cart_items', []) 
                     if item['id'] == item_id and item['user_id'] == session['user_id']), None)
    
    if cart_item:
        quantity = request.json.get('quantity', 1)
        if quantity <= 0:
            data['cart_items'] = [item for item in data.get('cart_items', []) if item['id'] != item_id]
        else:
            cart_item['quantity'] = quantity
        
        save_db(data)
        return jsonify({'success': True})
    
    return jsonify({'success': False})

# Rotas de Favoritos
@app.route('/favorite/<int:product_id>', methods=['POST'])
def toggle_favorite(product_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não logado'})
    
    data = load_db()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    
    # Verificar se já é favorito
    favorite = next((fav for fav in data.get('favorites', []) 
                    if fav['user_id'] == session['user_id'] and fav['product_id'] == product_id), None)
    
    if favorite:
        # Remover dos favoritos
        data['favorites'] = [fav for fav in data.get('favorites', []) 
                           if not (fav['user_id'] == session['user_id'] and fav['product_id'] == product_id)]
        is_favorited = False
    else:
        # Adicionar aos favoritos
        new_favorite = {
            'id': len(data.get('favorites', [])) + 1,
            'user_id': session['user_id'],
            'product_id': product_id,
            'created_at': datetime.now().isoformat()
        }
        if 'favorites' not in data:
            data['favorites'] = []
        data['favorites'].append(new_favorite)
        is_favorited = True
        
        # Rastrear comportamento - FAVORITAR (peso 3)
        track_behavior(session['user_id'], product_id, 'favorite', weight=3)
    
    save_db(data)
    
    return jsonify({
        'success': True, 
        'is_favorited': is_favorited,
        'message': 'Produto favoritado!' if is_favorited else 'Produto removido dos favoritos!'
    })

# Rotas de Perfil do Usuário
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    data = load_db()
    user = next((u for u in data['users'] if u['id'] == session['user_id']), None)
    
    if not user:
        session.clear()
        return redirect('/login')
    
    user_preferences = get_brand_preferences(session['user_id'])
    user_recommendations = get_user_recommendations(session['user_id'])
    user_favorites = get_user_favorites(session['user_id'])
    
    return render_template('profile.html',
                         user=user,
                         user_preferences=user_preferences,
                         user_recommendations=user_recommendations,
                         user_favorites=user_favorites)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não logado'})
    
    data = load_db()
    user = next((u for u in data['users'] if u['id'] == session['user_id']), None)
    
    if not user:
        return jsonify({'success': False, 'message': 'Usuário não encontrado'})
    
    username = request.json.get('username')
    email = request.json.get('email')
    
    # Verificar se username já existe (excluindo o usuário atual)
    if username != user['username']:
        if any(u['username'] == username for u in data['users'] if u['id'] != session['user_id']):
            return jsonify({'success': False, 'message': 'Nome de usuário já existe'})
    
    # Verificar se email já existe (excluindo o usuário atual)
    if email != user['email']:
        if any(u['email'] == email for u in data['users'] if u['id'] != session['user_id']):
            return jsonify({'success': False, 'message': 'Email já cadastrado'})
    
    # Atualizar dados
    user['username'] = username
    user['email'] = email
    
    # Atualizar sessão
    session['username'] = username
    session['email'] = email
    
    save_db(data)
    return jsonify({'success': True, 'message': 'Perfil atualizado com sucesso!'})

@app.route('/profile/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não logado'})
    
    data = load_db()
    user = next((u for u in data['users'] if u['id'] == session['user_id']), None)
    
    if not user:
        return jsonify({'success': False, 'message': 'Usuário não encontrado'})
    
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')
    
    # Verificar senha atual
    if hash_password(current_password) != user['password']:
        return jsonify({'success': False, 'message': 'Senha atual incorreta'})
    
    # Verificar se as novas senhas coincidem
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'As novas senhas não coincidem'})
    
    # Atualizar senha
    user['password'] = hash_password(new_password)
    save_db(data)
    
    return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'})

# Rotas de Preferências
@app.route('/profile/preferences')
def user_preferences():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_preferences = get_brand_preferences(session['user_id'])
    user_recommendations = get_user_recommendations(session['user_id'])
    
    return render_template('preferences.html',
                         user_preferences=user_preferences,
                         user_recommendations=user_recommendations)

# Rota para rastrear visualizações de produtos
@app.route('/track_view/<int:product_id>')
def track_view(product_id):
    if 'user_id' in session:
        track_behavior(session['user_id'], product_id, 'view', weight=1)
    return jsonify({'success': True})

# API para dados do carrinho (para o contador)
@app.route('/cart/data')
def cart_data():
    if 'user_id' not in session:
        return jsonify({'total_items': 0})
    
    data = load_db()
    user_cart = [item for item in data.get('cart_items', []) if item['user_id'] == session['user_id']]
    total_items = sum(item['quantity'] for item in user_cart)
    
    return jsonify({'total_items': total_items})

# Rotas de Administração (mantidas do código anterior)
@app.route('/admin')
def admin_dashboard():
    if not is_admin():
        return redirect('/login?next=/admin')
    
    data = load_db()
    
    stats = {
        'total_products': len(data['products']),
        'total_users': len(data['users']),
        'total_orders': len(data.get('orders', [])),
        'featured_products': len([p for p in data['products'] if p['featured']]),
        'total_revenue': sum(order.get('total', 0) for order in data.get('orders', []))
    }
    
    # Preferências globais (apenas para admin)
    brand_preferences = {}
    all_behaviors = data.get('user_behaviors', [])
    if all_behaviors:
        brand_counts = {}
        total_actions = 0
        
        for behavior in all_behaviors:
            product = next((p for p in data['products'] if p['id'] == behavior['product_id']), None)
            if product:
                brand = product['brand']
                if brand not in brand_counts:
                    brand_counts[brand] = 0
                brand_counts[brand] += behavior.get('weight', 1)
                total_actions += behavior.get('weight', 1)
        
        for brand, count in brand_counts.items():
            percentage = (count / total_actions) * 100 if total_actions > 0 else 0
            brand_preferences[brand] = round(percentage, 1)
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         brand_preferences=brand_preferences,
                         products=data['products'])

@app.route('/admin/products')
def admin_products():
    if not is_admin():
        return redirect('/login?next=/admin/products')
    
    data = load_db()
    return render_template('admin/products.html', products=data['products'])

@app.route('/admin/users')
def admin_users():
    if not is_admin():
        return redirect('/login?next=/admin/users')
    
    data = load_db()
    return render_template('admin/users.html', users=data['users'])

@app.route('/admin/analytics')
def admin_analytics():
    if not is_admin():
        return redirect('/login?next=/admin/analytics')
    
    # Preferências globais (apenas para admin)
    data = load_db()
    brand_preferences = {}
    all_behaviors = data.get('user_behaviors', [])
    if all_behaviors:
        brand_counts = {}
        total_actions = 0
        
        for behavior in all_behaviors:
            product = next((p for p in data['products'] if p['id'] == behavior['product_id']), None)
            if product:
                brand = product['brand']
                if brand not in brand_counts:
                    brand_counts[brand] = 0
                brand_counts[brand] += behavior.get('weight', 1)
                total_actions += behavior.get('weight', 1)
        
        for brand, count in brand_counts.items():
            percentage = (count / total_actions) * 100 if total_actions > 0 else 0
            brand_preferences[brand] = round(percentage, 1)
    
    # Estatísticas de comportamento
    total_views = len([b for b in data.get('user_behaviors', []) if b['action'] == 'view'])
    total_cart_adds = len([b for b in data.get('user_behaviors', []) if b['action'] == 'cart_add'])
    total_favorites = len([b for b in data.get('user_behaviors', []) if b['action'] == 'favorite'])
    
    return render_template('admin/analytics.html',
                         brand_preferences=brand_preferences,
                         total_views=total_views,
                         total_cart_adds=total_cart_adds,
                         total_favorites=total_favorites)

# Nova rota para visualizar preferências do usuário
@app.route('/admin/debug/preferences')
def debug_preferences():
    if not is_admin():
        return redirect('/login?next=/admin/debug/preferences')
    
    data = load_db()
    
    # Estatísticas gerais
    total_behaviors = len(data.get('user_behaviors', []))
    total_users = len(data.get('users', []))
    
    # Preferências por usuário (INDIVIDUAIS)
    user_preferences = {}
    for user in data.get('users', []):
        user_preferences[user['id']] = {
            'username': user['username'],
            'preferences': get_brand_preferences(user['id']),
            'behavior_count': len([b for b in data.get('user_behaviors', []) if b['user_id'] == user['id']]),
            'favorites_count': len([f for f in data.get('favorites', []) if f['user_id'] == user['id']])
        }
    
    # Detalhes dos comportamentos
    behaviors_details = []
    for behavior in data.get('user_behaviors', []):
        product = next((p for p in data['products'] if p['id'] == behavior['product_id']), None)
        user = next((u for u in data['users'] if u['id'] == behavior['user_id']), None)
        
        if product and user:
            behaviors_details.append({
                'id': behavior['id'],
                'user': user['username'],
                'product': product['name'],
                'brand': product['brand'],
                'action': behavior['action'],
                'weight': behavior.get('weight', 1),
                'timestamp': behavior['timestamp']
            })
    
    return render_template('admin/debug_preferences.html',
                         total_behaviors=total_behaviors,
                         total_users=total_users,
                         user_preferences=user_preferences,
                         behaviors_details=behaviors_details)

# API para gerenciar produtos
@app.route('/admin/api/products', methods=['GET', 'POST'])
def api_products():
    if not is_admin():
        return jsonify({'success': False, 'message': 'Não autorizado'})
    
    if request.method == 'POST':
        data = load_db()
        new_product = {
            'id': len(data['products']) + 1,
            'name': request.json.get('name'),
            'description': request.json.get('description'),
            'price': float(request.json.get('price', 0)),
            'image_url': request.json.get('image_url'),
            'category': request.json.get('category'),
            'brand': request.json.get('brand'),
            'featured': bool(request.json.get('featured', False)),
            'stock': int(request.json.get('stock', 0)),
            'created_at': datetime.now().isoformat()
        }
        
        data['products'].append(new_product)
        save_db(data)
        return jsonify({'success': True, 'product': new_product})
    
    return jsonify({'success': False})

@app.route('/admin/api/products/<int:product_id>', methods=['PUT', 'DELETE'])
def api_product_detail(product_id):
    if not is_admin():
        return jsonify({'success': False, 'message': 'Não autorizado'})
    
    data = load_db()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    
    if request.method == 'PUT':
        product.update({
            'name': request.json.get('name', product['name']),
            'description': request.json.get('description', product['description']),
            'price': float(request.json.get('price', product['price'])),
            'image_url': request.json.get('image_url', product['image_url']),
            'category': request.json.get('category', product['category']),
            'brand': request.json.get('brand', product['brand']),
            'featured': bool(request.json.get('featured', product['featured'])),
            'stock': int(request.json.get('stock', product['stock']))
        })
        save_db(data)
        return jsonify({'success': True, 'product': product})
    
    elif request.method == 'DELETE':
        data['products'] = [p for p in data['products'] if p['id'] != product_id]
        save_db(data)
        return jsonify({'success': True})

# API para gerenciar usuários
@app.route('/admin/api/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    if not is_admin():
        return jsonify({'success': False, 'message': 'Não autorizado'})
    
    if user_id == 1:  # Não permitir deletar o admin principal
        return jsonify({'success': False, 'message': 'Não é possível deletar o usuário admin'})
    
    data = load_db()
    data['users'] = [u for u in data['users'] if u['id'] != user_id]
    save_db(data)
    return jsonify({'success': True})
    
if __name__ == '__main__':
    # Criar estrutura de pastas se não existir
    os.makedirs('templates/components', exist_ok=True)
    os.makedirs('templates/admin', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Inicializar dados padrão
    init_default_data()
    
    print("🎉 Servidor Tênis Store Iniciado!")
    print("🌐 Acesse: http://localhost:5000")
    print("👑 Admin: http://localhost:5000/admin")
    print("🔐 Login Admin: admin / admin123")
    print("🎯 Sistema de Recomendações Personalizadas Ativo!")
    print("❤️  Sistema de Favoritos Ativo!")
    print("📊 Probabilidades por Marca: Adidas, Nike, Mizuno, New Balance, Puma, Jordan, Vans")
    print("👤 Perfil do usuário: http://localhost:5000/profile")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)