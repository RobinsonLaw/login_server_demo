from app import app, db, User, Post
from werkzeug.security import generate_password_hash

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        print("🌱 Seeding database with sample data...")
        
        # Clear existing data
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create sample users
        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password123"},
            {"username": "bob", "email": "bob@example.com", "password": "password123"},
            {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
            {"username": "diana", "email": "diana@example.com", "password": "password123"},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"]
            )
            user.set_password(user_data["password"])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create sample posts
        posts_data = [
            {"title": "Welcome to SQLAlchemy", "content": "This is my first post using Flask-SQLAlchemy!", "user_idx": 0},
            {"title": "Database Relationships", "content": "SQLAlchemy makes handling relationships between models very easy.", "user_idx": 1},
            {"title": "ORM vs Raw SQL", "content": "Object-Relational Mapping provides a higher level abstraction over raw SQL queries.", "user_idx": 0},
            {"title": "Flask-Migrate Tutorial", "content": "Database migrations are essential for managing schema changes in production.", "user_idx": 2},
            {"title": "Query Optimization", "content": "SQLAlchemy provides many tools for optimizing database queries.", "user_idx": 1},
            {"title": "Advanced SQLAlchemy", "content": "Exploring advanced features like hybrid properties and custom types.", "user_idx": 3},
            {"title": "Testing with SQLAlchemy", "content": "Best practices for testing applications that use SQLAlchemy.", "user_idx": 2},
            {"title": "Deployment Considerations", "content": "Things to consider when deploying Flask apps with SQLAlchemy to production.", "user_idx": 3},
        ]
        
        posts = []
        for post_data in posts_data:
            post = Post(
                title=post_data["title"],
                content=post_data["content"],
                user_id=users[post_data["user_idx"]].id
            )
            posts.append(post)
            db.session.add(post)
        
        db.session.commit()
        print(f"✅ Created {len(posts)} posts")
        
        # Display summary
        print("\n📊 Database Summary:")
        print(f"Users: {User.query.count()}")
        print(f"Posts: {Post.query.count()}")
        
        print("\n👥 Users created:")
        for user in User.query.all():
            print(f"  - {user.username} ({user.email}) - {len(user.posts)} posts")
        
        print("\n📝 Recent posts:")
        for post in Post.query.order_by(Post.created_at.desc()).limit(3):
            print(f"  - '{post.title}' by {post.author.username}")
        
        print("\n🎉 Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
