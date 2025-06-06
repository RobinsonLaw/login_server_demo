from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import os

# Initialize Flask app
app = Flask(__name__)

# Vercel-specific configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'connect_timeout': 10,
        'application_name': 'flask_vercel_app'
    }
}

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Auto-Migration System
def run_auto_migrations():
    """Automatically run database migrations on startup"""
    try:
        # Check if migrations directory exists
        migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'migrations')
        
        if os.path.exists(migrations_dir):
            print("🔄 Running database migrations...")
            
            # Import flask-migrate commands
            from flask_migrate import upgrade
            
            # Run migrations
            with app.app_context():
                try:
                    upgrade()
                    print("✅ Database migrations completed successfully")
                    return True
                except Exception as migration_error:
                    print(f"⚠️ Migration failed: {migration_error}")
                    print("🔧 Falling back to table creation...")
                    return False
        else:
            print("📝 No migrations directory found, using table creation")
            return False
            
    except Exception as e:
        print(f"❌ Auto-migration error: {e}")
        return False

# Models (inline for Vercel)
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=True):
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data['email'] = self.email
        return data

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self, include_author=True):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id
        }
        if include_author and self.author:
            data['author'] = self.author.username
        return data

# Database initialization with auto-migration
with app.app_context():
    try:
        # Try auto-migration first
        migration_success = run_auto_migrations()
        
        if not migration_success:
            # Fallback to table creation
            print("🔧 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Helper function
def require_auth():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    return None

# Routes
@app.route('/')
@app.route('/api')
def home():
    return jsonify({
        "message": "Flask API Server on Vercel",
        "database": "PostgreSQL with SQLAlchemy",
        "platform": "Vercel Serverless",
        "version": "2.1.0-auto-migration",
        "features": {
            "auto_migration": "Enabled",
            "flask_migrate": "Integrated",
            "fallback_creation": "Available"
        },
        "endpoints": {
            "POST /api/register": "Register a new user",
            "POST /api/login": "Login user",
            "POST /api/logout": "Logout user",
            "GET /api/profile": "Get user profile (requires login)",
            "PUT /api/profile": "Update user profile (requires login)",
            "GET /api/users": "Get all users (paginated)",
            "POST /api/posts": "Create a new post (requires login)",
            "GET /api/posts": "Get all posts (paginated)",
            "GET /api/posts/<id>": "Get specific post",
            "PUT /api/posts/<id>": "Update post (requires login)",
            "DELETE /api/posts/<id>": "Delete post (requires login)",
            "GET /api/health": "Health check"
        }
    })

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters long"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        if '@' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Username and password are required"}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            
            return jsonify({
                "message": "Login successful",
                "user": user.to_dict()
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/profile', methods=['GET'])
def get_profile():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({"user": user.to_dict()}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile', methods=['PUT'])
def update_profile():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if 'email' in data:
            email = data['email'].strip().lower()
            if '@' not in email:
                return jsonify({"error": "Invalid email format"}), 400
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({"error": "Email already exists"}), 409
            
            user.email = email
        
        if 'password' in data:
            if len(data['password']) < 6:
                return jsonify({"error": "Password must be at least 6 characters long"}), 400
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            "message": "Profile updated successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        
        users = User.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            "users": [user.to_dict(include_email=False) for user in users.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": users.total,
                "pages": users.pages,
                "has_next": users.has_next,
                "has_prev": users.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({"error": "Title and content are required"}), 400
        
        title = data['title'].strip()
        content = data['content'].strip()
        
        if len(title) < 1 or len(content) < 1:
            return jsonify({"error": "Title and content cannot be empty"}), 400
        
        post = Post(
            title=title,
            content=content,
            user_id=session['user_id']
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            "message": "Post created successfully",
            "post": post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "posts": [post.to_dict() for post in posts.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": posts.total,
                "pages": posts.pages,
                "has_next": posts.has_next,
                "has_prev": posts.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify({"post": post.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": "Post not found"}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({"error": "Title and content are required"}), 400
        
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != session['user_id']:
            return jsonify({"error": "Unauthorized to update this post"}), 403
        
        post.title = data['title'].strip()
        post.content = data['content'].strip()
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "message": "Post updated successfully",
            "post": post.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({"error": "Post not found"}), 404
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != session['user_id']:
            return jsonify({"error": "Unauthorized to delete this post"}), 403
        
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({"message": "Post deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({"error": "Post not found"}), 404
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        
        user_count = User.query.count()
        post_count = Post.query.count()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "PostgreSQL with SQLAlchemy - Connected",
            "platform": "Vercel Serverless",
            "version": "2.1.0-auto-migration",
            "migration_system": "Flask-Migrate with Auto-Upgrade",
            "stats": {
                "users": user_count,
                "posts": post_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": f"PostgreSQL - Error: {str(e)}",
            "platform": "Vercel Serverless",
            "version": "2.1.0-auto-migration"
        }), 503

# HTML Pages Routes
@app.route('/web')
@app.route('/web/')
def web_home():
    return render_template('index.html')

@app.route('/web/register')
def web_register():
    return render_template('register.html')

@app.route('/web/login')
def web_login():
    return render_template('login.html')

@app.route('/web/dashboard')
def web_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('web_login'))
    
    user = User.query.get(session['user_id'])
    user_posts = Post.query.filter_by(user_id=session['user_id']).order_by(Post.created_at.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', user=user, user_posts=user_posts, recent_posts=recent_posts)

@app.route('/web/posts')
def web_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('posts.html', posts=posts)

@app.route('/web/posts/<int:post_id>')
def web_post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/web/create-post')
def web_create_post():
    if 'user_id' not in session:
        return redirect(url_for('web_login'))
    return render_template('create_post.html')

@app.route('/web/profile')
def web_profile():
    if 'user_id' not in session:
        return redirect(url_for('web_login'))
    
    user = User.query.get(session['user_id'])
    user_posts = Post.query.filter_by(user_id=session['user_id']).order_by(Post.created_at.desc()).all()
    
    return render_template('profile.html', user=user, user_posts=user_posts)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True)
