from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'password')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'flask_app')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
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
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=True):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self, include_author=True):
        """Convert post to dictionary"""
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
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Create tables
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Helper function to check authentication
def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    return None

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Flask API Server with SQLAlchemy",
        "database": "PostgreSQL with SQLAlchemy ORM",
        "version": "2.0.0",
        "endpoints": {
            "POST /register": "Register a new user",
            "POST /login": "Login user",
            "POST /logout": "Logout user",
            "GET /profile": "Get user profile (requires login)",
            "PUT /profile": "Update user profile (requires login)",
            "GET /users": "Get all users (paginated)",
            "GET /users/<id>": "Get specific user",
            "POST /posts": "Create a new post (requires login)",
            "GET /posts": "Get all posts (paginated)",
            "GET /posts/<id>": "Get specific post",
            "PUT /posts/<id>": "Update post (requires login)",
            "DELETE /posts/<id>": "Delete post (requires login)",
            "GET /users/<id>/posts": "Get user's posts",
            "GET /health": "Health check"
        }
    })

# User Registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate input
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters long"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        if '@' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409
        
        # Create new user
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

# User Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Username and password are required"}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Find user
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

# User Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

# Get User Profile (Protected Route)
@app.route('/profile', methods=['GET'])
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

# Update User Profile (Protected Route)
@app.route('/profile', methods=['PUT'])
def update_profile():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update fields if provided
        if 'email' in data:
            email = data['email'].strip().lower()
            if '@' not in email:
                return jsonify({"error": "Invalid email format"}), 400
            
            # Check if email is already taken by another user
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

# Get All Users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page
        
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

# Get Specific User
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({"user": user.to_dict(include_email=False)}), 200
    except Exception as e:
        return jsonify({"error": "User not found"}), 404

# Get User's Posts
@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "user": user.to_dict(include_email=False),
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
        return jsonify({"error": "User not found"}), 404

# Create Post (Protected Route)
@app.route('/posts', methods=['POST'])
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
        
        # Create new post
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

# Get All Posts
@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
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

# Get Single Post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify({"post": post.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": "Post not found"}), 404

# Update Post (Protected Route)
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({"error": "Title and content are required"}), 400
        
        post = Post.query.get_or_404(post_id)
        
        # Check if user owns the post
        if post.user_id != session['user_id']:
            return jsonify({"error": "Unauthorized to update this post"}), 403
        
        # Update post
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

# Delete Post (Protected Route)
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check if user owns the post
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

# Search Posts
@app.route('/posts/search', methods=['GET'])
def search_posts():
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        # Search in title and content
        posts = Post.query.filter(
            db.or_(
                Post.title.ilike(f'%{query}%'),
                Post.content.ilike(f'%{query}%')
            )
        ).order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "query": query,
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

# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        
        # Get some stats
        user_count = User.query.count()
        post_count = Post.query.count()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "PostgreSQL with SQLAlchemy - Connected",
            "version": "2.0.0",
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
            "version": "2.0.0"
        }), 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    """
    Flask CLI entry point for local development
    This file makes Flask CLI commands work properly
    """
    import os
    import sys
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Import the Flask app from api/index.py
    #from api.index import app, db #This line is not needed since app and db are already imported

    # Make sure we're in the right context
    with app.app_context():
        app.run(debug=True, host='0.0.0.0', port=5000)
