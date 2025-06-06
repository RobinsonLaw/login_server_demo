"""
Database setup script for Vercel deployment
Run this locally to set up your database before deploying
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_database():
    """Set up database tables and initial data"""
    try:
        # Import after setting up the path
        from api.index import app, db, User, Post
        
        with app.app_context():
            print("🔧 Setting up database for Vercel deployment...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we need to create sample data
            if User.query.count() == 0:
                print("📝 Creating sample users...")
                
                # Create sample users
                users_data = [
                    {"username": "admin", "email": "admin@example.com", "password": "admin123"},
                    {"username": "demo", "email": "demo@example.com", "password": "demo123"},
                ]
                
                for user_data in users_data:
                    user = User(
                        username=user_data["username"],
                        email=user_data["email"]
                    )
                    user.set_password(user_data["password"])
                    db.session.add(user)
                
                db.session.commit()
                print(f"✅ Created {len(users_data)} sample users")
                
                # Create sample posts
                print("📝 Creating sample posts...")
                admin_user = User.query.filter_by(username="admin").first()
                demo_user = User.query.filter_by(username="demo").first()
                
                posts_data = [
                    {"title": "Welcome to Vercel!", "content": "This Flask app is now running on Vercel serverless platform.", "user": admin_user},
                    {"title": "SQLAlchemy on Serverless", "content": "Using SQLAlchemy ORM with PostgreSQL on Vercel works great!", "user": demo_user},
                    {"title": "API Documentation", "content": "Check out all the available endpoints at the root URL.", "user": admin_user},
                ]
                
                for post_data in posts_data:
                    post = Post(
                        title=post_data["title"],
                        content=post_data["content"],
                        user_id=post_data["user"].id
                    )
                    db.session.add(post)
                
                db.session.commit()
                print(f"✅ Created {len(posts_data)} sample posts")
            
            # Display summary
            user_count = User.query.count()
            post_count = Post.query.count()
            
            print(f"\n📊 Database Summary:")
            print(f"Users: {user_count}")
            print(f"Posts: {post_count}")
            print(f"\n🎉 Database setup completed successfully!")
            print(f"🚀 Ready for Vercel deployment!")
            
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1)
