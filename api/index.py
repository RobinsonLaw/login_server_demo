flask_admin = False
import json
import os
import requests
import sys
import flask
from flask import Flask, request, jsonify, session, render_template, redirect, url_for,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import secrets
import logging
from dotenv import load_dotenv
from importlib.metadata import version as flask_version_info
if flask_admin:
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
from flasgger import Swagger, swag_from
load_dotenv()


# def get_environment_info2():
#     import sys
#     import flask
#     host = 'localhost:5001'
#     try:
#         if request:
#             host = request.host
#     except Exception:
#         pass

#     db_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL') or ''
#     masked_db = ''
#     if db_url:
#         try:
#             remaining = db_url.split('@')[-1]
#             parts = remaining.split('/')
#             if len(parts) >= 2:
#                 host_port = parts[0]
#                 db_name = parts[1].split('?')[0]
#                 masked_db = f"{host_port}/{db_name}"
#             else:
#                 masked_db = remaining
#         except Exception:
#             masked_db = 'undisclosed'

#     return {
#         'host': host,
#         'environment': os.getenv('FLASK_ENV', 'development'),
#         'python_version': sys.version.split()[0],
#         'flask_version': flask.__version__,
#         'database': masked_db
#     }

# Load Flask version dynamically
try:
    app_version = f"{flask_version_info('flask')}-flask-cli"
except Exception:
    app_version = 'unknown-flask-cli'

# Initialize Flask appUSERNAME = os.getenv('ADMIN_USERNAME')
app = Flask(__name__, static_folder=None)
# Fix for Flask 3.0+: prevents escaping < and > to \u003C and \u003E
app.json.ensure_ascii = False
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

db_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
logger = logging.getLogger(__name__)
# Auto-Migration System
_LOCK_CONN = None
def run_auto_migrations():
    """Automatically run database migrations on startup"""
    global _LOCK_CONN

    if _LOCK_CONN is not None:
        return True
    try:
        # Check if migrations directory exists
        migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'migrations')
        
        if os.path.exists(migrations_dir):
    
            # Import flask-migrate commands
            from flask_migrate import upgrade
            from sqlalchemy import text
            LOCK_ID = 8273918237
            # Run migrations
            with app.app_context():
                
                db = app.extensions.get("sqlalchemy")
                if db:
                    conn = db.engine.connect()
                    acquired = conn.execute(text(f"SELECT pg_try_advisory_lock({LOCK_ID})")).scalar()
                    if not acquired:
                        print("⏩ Another worker/instance is running migrations, skipping.")
                        conn.close()
                        return True
                    _LOCK_CONN = conn

                    print("🔄 Running database migrations...")
                    try:    
                        upgrade()
                        print("✅ Database migrations completed successfully")
                        return True
                    except Exception as migration_error:
                        print(f"⚠️ Migration failed: {migration_error}")
                        print("🔧 Falling back to table creation...")
                        if _LOCK_CONN:
                            _LOCK_CONN.close()
                            _LOCK_CONN = None
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
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
if flask_admin:
    admin = Admin(app, name='Login Server Admin')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
# Configure Flasgger with ReDoc interface enabled
# swagger_config = {
#     "headers": [],
#     "specs": [
#         {
#             "endpoint": 'apispec',
#             "route": '/apispec.json',
#             "rule_filter": lambda rule: True,  # Include all routes automatically
#             "model_filter": lambda model: True,
#         }
#     ],
#     "static_url_path": "/flasgger_static",
#     "swagger_ui": True,
#     "specs_route": "/apidocs/"
# }

# template = {
#     "swagger": "2.0",
#     "info": {
#         "title": "Login Server API",
#         "description": "API Overview & Documentation",
#         "version": app_version
#     }
# }

# swagger = Swagger(app, config=swagger_config, template=template, parse=True)
swagger = Swagger(app, template_file='swagger.yml')
@app.before_request
def update_swagger_host():
    # Automatically update Swagger host when fetching spec
    if request.path == '/apispec_1.json':
        swagger.template['host'] = get_environment_info()['host']
# Helper function
def require_auth():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    return None

# Routes
@app.route('/')
def home():
    return redirect(url_for('web_home'))
@app.route('/api')
def api():
    """Returns the raw Python dictionary for API information."""
    return {
        "message": "Flask API Server on Vercel",
        "database": "PostgreSQL with SQLAlchemy",
        "platform": "Vercel Serverless",
        "version": app_version,
        "environment_info": get_environment_info(),
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
            "GET /api/posts/{id}": "Get specific post",
            "PUT /api/posts/{id}": "Update post (requires login)",
            "DELETE /api/posts/{id}": "Delete post (requires login)",
            "GET /api/health": "Health check"
        }
    }

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
                # If user is logged in, show all posts
        if 'user_id' in session:
            posts_query = Post.query.order_by(Post.created_at.desc())
        else:
            # Only show admin posts to guests
            admin_user = User.query.filter_by(username="admin").first()
            if admin_user:
                posts_query = Post.query.filter_by(user_id=admin_user.id).order_by(Post.created_at.desc())
            else:
                posts_query = Post.query.filter_by(user_id=None)  # No posts

       # FIXED: Call .paginate() on posts_query instead of Post.query
        posts = posts_query.paginate(
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
        post.updated_at = datetime.now(timezone.utc)
        
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
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": "PostgreSQL with SQLAlchemy - Connected",
            "platform": "Vercel Serverless",
        "version": app_version,
            "migration_system": "Flask-Migrate with Auto-Upgrade + Flask CLI",
            "stats": {
                "users": user_count,
                "posts": post_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": f"PostgreSQL - Error: {str(e)}",
            "platform": "Vercel Serverless",
            "version": app_version
        }), 503

# HTML Pages Routes
@app.route('/.env')
def block_env():
    return '', 404
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
    if 'user_id' in session:
        posts_query = Post.query.order_by(Post.created_at.desc())
    else:
        admin_user = User.query.filter_by(username="admin").first()
        if admin_user:
            posts_query = Post.query.filter_by(user_id=admin_user.id).order_by(Post.created_at.desc())
        else:
            posts_query = Post.query.filter_by(user_id=None)
    posts = posts_query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('posts.html', posts=posts)
# @app.route('/web/posts')
# def web_posts():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.created_at.desc()).paginate(
#         page=page, per_page=10, error_out=False
#     )
#     return render_template('posts.html', posts=posts)

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
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'public'),
        'favicon.ico',
        mimetype='image/x-icon'
    )
@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(
        os.path.join(app.root_path, 'public'),
        'favicon.png',
        mimetype='image/png'
    )

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('public/static', filename)

@app.route('/api/host')
def get_environment_info():
    """Resolves current host, environment type, and detection source."""
    
    # 1. Custom Domain via Reverse Proxy (e.g., web.iotchat.link)
    if request.headers.get("X-Forwarded-Host"):
        host = request.headers.get("X-Forwarded-Host")
        source = "X-Forwarded-Host"
    # 2. Production Environment Variable
    elif os.getenv("VERCEL_PROJECT_PRODUCTION_URL"):
        host = os.getenv("VERCEL_PROJECT_PRODUCTION_URL")
        source = "VERCEL_PROJECT_PRODUCTION_URL"
    # 3. Preview Environment Variable
    elif os.getenv("VERCEL_URL"):
        host = os.getenv("VERCEL_URL")
        source = "VERCEL_URL"
    # 4. Request Host Header / Local Fallback
    else:
        host = request.headers.get("Host", "localhost")
        source = "Host Header"

    # Environment Tagging Logic
    if "localhost" in host or "127.0.0.1" in host:
        env_tag = "local-development"
    elif os.getenv("VERCEL_ENV") == "production" or host == os.getenv("VERCEL_PROJECT_PRODUCTION_URL"):
        env_tag = "production"
    else:
        env_tag = "preview"

    return {
        "host": host,
        "environment": env_tag,
        "detection_source": source
    }

@app.route('/api/deployment-info', methods=['GET'])
def deployment_info():
    try:
        vercel_token = os.getenv('VERCEL_TOKEN')
        # project_id = os.getenv('VERCEL_PROJECT_ID')
        # team_id = os.environ.get('VERCEL_TEAM_ID')
        if not vercel_token:
            return jsonify({"error": "Missing Vercel credentials"}), 400
        
        url = f"https://api.vercel.com/v6/deployments?limit=1"
        headers = {"Authorization": f"Bearer {vercel_token}"}
        
        response = requests.get(url, headers=headers)
        deployments = response.json()
        
        if deployments['deployments']:
            latest = deployments['deployments'][0]
            return jsonify({
                "date": latest['created'],
                "status": latest['state'],
                "url": latest['url']
            }), 200
        
        return jsonify({"error": "No deployments found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

# Vercel serverless function handler
# def handler(request):
#     return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
    # app.run(ssl_context=('api/mylocal.dev.pem', 'api/mylocal.dev-key.pem'))


