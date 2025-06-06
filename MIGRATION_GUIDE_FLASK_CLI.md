# 🔄 Flask CLI Migration Guide

This guide covers using the **standard Flask CLI commands** for database schema management. This approach uses the official Flask-Migrate commands with our `app.py` entry point.

## 🚀 Overview

### ✅ Flask CLI Features
- **Standard approach**: Official Flask-Migrate commands
- **Industry standard**: Works with all Flask tutorials
- **Simple syntax**: Familiar `flask db` commands
- **Documentation**: Extensive official documentation
- **Integration**: Works with our auto-migration system

### 🛠️ Available Commands
- **`flask db init`** - Initialize Flask-Migrate
- **`flask db migrate`** - Generate new migrations
- **`flask db upgrade`** - Apply migrations
- **`flask db current`** - Show current revision
- **`flask db downgrade`** - Rollback migrations
- **`flask db history`** - Show migration history

## 📋 Quick Setup

### 1. Environment Configuration
\`\`\`bash
# Set Flask app entry point (required)
export FLASK_APP=app.py

# Set environment variables
export DATABASE_URL="postgresql://user:password@host:port/database"
export SECRET_KEY="your-secret-key"

# Optional: Set Flask environment
export FLASK_ENV=development
\`\`\`

### 2. First-Time Initialization
\`\`\`bash
# Initialize migrations (run once)
flask db init
\`\`\`

### 3. Create Initial Migration
\`\`\`bash
# Generate initial migration from current models
flask db migrate -m "Initial migration"

# Apply the migration
flask db upgrade
\`\`\`

## 🔧 How It Works with Auto-Migration

### Local Development
- Use Flask CLI commands for development
- Test migrations locally before deployment
- Commit migration files to version control

### Production Deployment
- Auto-migration system detects new migration files
- Runs `flask db upgrade` automatically on Vercel startup
- No manual intervention needed in production

## 📚 Command Reference

### `flask db init`
**Purpose**: Initialize Flask-Migrate for the first time

\`\`\`bash
flask db init
\`\`\`

**What it does:**
- Creates `migrations/` directory
- Sets up Alembic configuration
- Prepares project for migrations

**Output Example:**
\`\`\`
Creating directory /path/to/project/migrations ... done
Creating directory /path/to/project/migrations/versions ... done
Generating /path/to/project/migrations/alembic.ini ... done
Generating /path/to/project/migrations/env.py ... done
Generating /path/to/project/migrations/README ... done
Generating /path/to/project/migrations/script.py.mako ... done
Please edit configuration/connection/logging settings in '/path/to/project/migrations/alembic.ini' before proceeding.
\`\`\`

### `flask db migrate`
**Purpose**: Generate new migration from model changes

\`\`\`bash
flask db migrate -m "Description of changes"
\`\`\`

**Examples:**
\`\`\`bash
# Add new field
flask db migrate -m "Add user avatar URL field"

# Modify existing field
flask db migrate -m "Increase username length to 100 characters"

# Add new table
flask db migrate -m "Create categories table"

# Add index
flask db migrate -m "Add index to posts.created_at"
\`\`\`

**What it does:**
- Compares current models with database schema
- Generates migration file with upgrade/downgrade functions
- Creates timestamped file in `migrations/versions/`

### `flask db upgrade`
**Purpose**: Apply pending migrations to database

\`\`\`bash
# Apply all pending migrations
flask db upgrade

# Upgrade to specific revision
flask db upgrade <revision_id>
\`\`\`

**Output Example:**
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, Add user avatar URL field
\`\`\`

### `flask db current`
**Purpose**: Show current database revision

\`\`\`bash
flask db current
\`\`\`

**Output Example:**
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
abc123def456 (head)
\`\`\`

### `flask db history`
**Purpose**: Show migration history

\`\`\`bash
flask db history
\`\`\`

**Output Example:**
\`\`\`
abc123def456 -> def789ghi012 (head), Add user avatar URL field
123abc456def -> abc123def456, Create categories table
<base> -> 123abc456def, Initial migration
\`\`\`

### `flask db downgrade`
**Purpose**: Rollback to previous migration

\`\`\`bash
# Downgrade one revision
flask db downgrade

# Downgrade to specific revision
flask db downgrade <revision_id>

# Downgrade to base (initial state)
flask db downgrade base
\`\`\`

## 🎯 Complete Workflow Examples

### Adding New Field to Existing Table

1. **Modify the model** in `api/index.py`:
\`\`\`python
class User(db.Model):
    # ... existing fields ...
    avatar_url = db.Column(db.String(255), nullable=True)
\`\`\`

2. **Generate migration**:
\`\`\`bash
flask db migrate -m "Add user avatar URL field"
\`\`\`

3. **Review generated migration** in `migrations/versions/`:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_url')
    # ### end Alembic commands ###
\`\`\`

4. **Apply migration locally**:
\`\`\`bash
flask db upgrade
\`\`\`

5. **Verify the change**:
\`\`\`bash
flask db current
\`\`\`

6. **Commit and deploy**:
\`\`\`bash
git add migrations/versions/
git commit -m "Add user avatar URL field migration"
vercel --prod  # Auto-migration applies it
\`\`\`

### Creating New Table

1. **Add new model** in `api/index.py`:
\`\`\`python
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
\`\`\`

2. **Generate and apply migration**:
\`\`\`bash
flask db migrate -m "Create categories table"
flask db upgrade
\`\`\`

3. **Deploy**:
\`\`\`bash
git add migrations/versions/
git commit -m "Add categories table"
vercel --prod
\`\`\`

### Modifying Existing Field

1. **Change model** in `api/index.py`:
\`\`\`python
# Change from:
username = db.Column(db.String(50), unique=True, nullable=False)
# To:
username = db.Column(db.String(100), unique=True, nullable=False)
\`\`\`

2. **Generate and apply**:
\`\`\`bash
flask db migrate -m "Increase username length to 100 characters"
flask db upgrade
\`\`\`

## 🎯 Real-World Examples

### Example 1: Adding User Profile Fields

**Scenario**: Add avatar URL and bio fields to the User model

**Step 1: Set up environment**:
\`\`\`bash
export FLASK_APP=app.py
export DATABASE_URL="postgresql://user:password@host:port/database"
\`\`\`

**Step 2: Modify the model** in `api/index.py`:
\`\`\`python
# BEFORE
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# AFTER
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_url = db.Column(db.String(255), nullable=True)  # NEW
    bio = db.Column(db.Text, nullable=True)                # NEW
    is_verified = db.Column(db.Boolean, default=False)     # NEW
\`\`\`

**Step 3: Generate migration**:
\`\`\`bash
flask db migrate -m "Add user profile fields: avatar_url, bio, is_verified"
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'users.avatar_url'
INFO  [alembic.autogenerate.compare] Detected added column 'users.bio'
INFO  [alembic.autogenerate.compare] Detected added column 'users.is_verified'
  Generating /path/to/migrations/versions/002_add_user_profile_fields.py ... done
\`\`\`

**Step 4: Review generated migration file** (`migrations/versions/002_add_user_profile_fields.py`):
\`\`\`python
"""Add user profile fields: avatar_url, bio, is_verified

Revision ID: def789ghi012
Revises: abc123def456
Create Date: 2024-12-01 14:30:22.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'def789ghi012'
down_revision = 'abc123def456'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_url', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'avatar_url')
    # ### end Alembic commands ###
\`\`\`

**Step 5: Apply migration locally**:
\`\`\`bash
flask db upgrade
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade abc123def456 -> def789ghi012, Add user profile fields: avatar_url, bio, is_verified
\`\`\`

**Step 6: Verify changes**:
\`\`\`bash
flask db current
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
def789ghi012 (head)
\`\`\`

**Step 7: Deploy to production**:
\`\`\`bash
git add migrations/versions/002_add_user_profile_fields.py
git commit -m "Add user profile fields migration"
vercel --prod
\`\`\`

### Example 2: Creating Categories Table with Relationships

**Scenario**: Add a categories system for posts

**Step 1: Add Category model** in `api/index.py`:
\`\`\`python
# Add this new model
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#6B7280')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    posts = db.relationship('Post', backref='category', lazy=True)

# Modify Post model to add category relationship
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)  # NEW
\`\`\`

**Step 2: Generate migration**:
\`\`\`bash
flask db migrate -m "Create categories table and add category_id to posts"
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'categories'
INFO  [alembic.autogenerate.compare] Detected added column 'posts.category_id'
INFO  [alembic.autogenerate.compare] Detected added foreign key (posts.category_id)(categories.id) on table 'posts'
  Generating /path/to/migrations/versions/003_create_categories_table.py ... done
\`\`\`

**Step 3: Review and apply**:
\`\`\`bash
# Review the migration
cat migrations/versions/003_create_categories_table.py

# Apply the migration
flask db upgrade
\`\`\`

**Step 4: Verify with history**:
\`\`\`bash
flask db history
\`\`\`

**Output**:
\`\`\`
abc123def456 -> def789ghi012, Add user profile fields: avatar_url, bio, is_verified
def789ghi012 -> ghi012jkl345 (head), Create categories table and add category_id to posts
<base> -> abc123def456, Initial migration
\`\`\`

### Example 3: Adding Database Indexes for Performance

**Scenario**: Add indexes to improve query performance

**Step 1: Create empty migration**:
\`\`\`bash
flask db revision -m "Add performance indexes to posts and users tables"
\`\`\`

**Output**:
\`\`\`
  Generating /path/to/migrations/versions/004_add_performance_indexes.py ... done
\`\`\`

**Step 2: Edit the generated migration file manually**:
\`\`\`python
"""Add performance indexes to posts and users tables

Revision ID: jkl345mno678
Revises: ghi012jkl345
Create Date: 2024-12-01 15:45:33.789012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'jkl345mno678'
down_revision = 'ghi012jkl345'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands manually added for performance ###
    op.create_index('idx_posts_created_at', 'posts', ['created_at'])
    op.create_index('idx_posts_user_id_created_at', 'posts', ['user_id', 'created_at'])
    op.create_index('idx_posts_category_id', 'posts', ['category_id'])
    op.create_index('idx_users_email_verified', 'users', ['email', 'is_verified'])
    # ### end manual commands ###

def downgrade():
    # ### commands manually added for performance ###
    op.drop_index('idx_users_email_verified', table_name='users')
    op.drop_index('idx_posts_category_id', table_name='posts')
    op.drop_index('idx_posts_user_id_created_at', table_name='posts')
    op.drop_index('idx_posts_created_at', table_name='posts')
    # ### end manual commands ###
\`\`\`

**Step 3: Apply the migration**:
\`\`\`bash
flask db upgrade
\`\`\`

### Example 4: Data Migration with Schema Change

**Scenario**: Add a `full_name` field and populate it from existing data

**Step 1: Add field to User model**:
\`\`\`python
class User(db.Model):
    # ... existing fields ...
    full_name = db.Column(db.String(100), nullable=True)  # NEW
\`\`\`

**Step 2: Generate migration**:
\`\`\`bash
flask db migrate -m "Add full_name field to users"
\`\`\`

**Step 3: Edit migration to include data migration**:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(length=100), nullable=True))
    
    # Data migration: populate full_name from username
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE users SET full_name = username WHERE full_name IS NULL")
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###
\`\`\`

**Step 4: Apply and verify**:
\`\`\`bash
flask db upgrade
flask db current
\`\`\`

### Example 5: Rollback Scenario

**Scenario**: The last migration caused issues and needs to be rolled back

**Step 1: Check current status**:
\`\`\`bash
flask db current
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
mno678pqr901 (head)
\`\`\`

**Step 2: Check history to see what to rollback to**:
\`\`\`bash
flask db history
\`\`\`

**Output**:
\`\`\`
jkl345mno678 -> mno678pqr901 (head), Add full_name field to users
ghi012jkl345 -> jkl345mno678, Add performance indexes to posts and users tables
def789ghi012 -> ghi012jkl345, Create categories table and add category_id to posts
abc123def456 -> def789ghi012, Add user profile fields: avatar_url, bio, is_verified
<base> -> abc123def456, Initial migration
\`\`\`

**Step 3: Rollback to previous version**:
\`\`\`bash
flask db downgrade
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade mno678pqr901 -> jkl345mno678, Add full_name field to users
\`\`\`

**Step 4: Verify rollback**:
\`\`\`bash
flask db current
\`\`\`

**Output**:
\`\`\`
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
jkl345mno678 (head)
\`\`\`

### Example 6: Handling Migration Conflicts

**Scenario**: Multiple developers created migrations, causing conflicts

**Step 1: Identify the conflict**:
\`\`\`bash
flask db upgrade
\`\`\`

**Output**:
\`\`\`
FAILED: Multiple head revisions are present for given argument "head"; please specify a specific target revision, or use --resolve-dependencies to resolve all heads
\`\`\`

**Step 2: Check heads**:
\`\`\`bash
flask db heads
\`\`\`

**Output**:
\`\`\`
pqr901stu234 (branch1)
pqr901xyz789 (branch2)
\`\`\`

**Step 3: Create merge migration**:
\`\`\`bash
flask db merge -m "Merge branch migrations"
\`\`\`

**Output**:
\`\`\`
  Generating /path/to/migrations/versions/006_merge_branch_migrations.py ... done
\`\`\`

**Step 4: Apply merge migration**:
\`\`\`bash
flask db upgrade
\`\`\`

### Example 7: Complete Development Cycle

**Real scenario**: Adding a complete commenting system

**Step 1: Add Comment model** in `api/index.py`:
\`\`\`python
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)  # For replies
    
    # Relationships
    author = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
\`\`\`

**Step 2: Generate migration**:
\`\`\`bash
flask db migrate -m "Create comments table with nested replies support"
\`\`\`

**Step 3: Review generated migration**:
\`\`\`bash
cat migrations/versions/007_create_comments_table.py
\`\`\`

**Generated content**:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
\`\`\`

**Step 4: Apply migration**:
\`\`\`bash
flask db upgrade
\`\`\`

**Step 5: Add performance indexes**:
\`\`\`bash
flask db revision -m "Add indexes for comments performance"
\`\`\`

**Edit the migration**:
\`\`\`python
def upgrade():
    op.create_index('idx_comments_post_id_created_at', 'comments', ['post_id', 'created_at'])
    op.create_index('idx_comments_user_id', 'comments', ['user_id'])
    op.create_index('idx_comments_parent_id', 'comments', ['parent_id'])

def downgrade():
    op.drop_index('idx_comments_parent_id', table_name='comments')
    op.drop_index('idx_comments_user_id', table_name='comments')
    op.drop_index('idx_comments_post_id_created_at', table_name='comments')
\`\`\`

**Step 6: Apply and deploy**:
\`\`\`bash
flask db upgrade
git add migrations/versions/
git commit -m "Add comments system with performance indexes"
vercel --prod
\`\`\`

**Step 7: Monitor deployment**:
\`\`\`bash
vercel logs --follow
\`\`\`

### Example 8: Environment-Specific Migrations

**Scenario**: Different behavior for development vs production

**Step 1: Create migration with environment checks**:
\`\`\`bash
flask db revision -m "Add sample data for development"
\`\`\`

**Step 2: Edit migration with environment logic**:
\`\`\`python
import os

def upgrade():
    # Only run in development
    if os.getenv('FLASK_ENV') == 'development':
        connection = op.get_bind()
        
        # Add sample categories
        connection.execute(sa.text("""
            INSERT INTO categories (name, slug, description, color) VALUES 
            ('Technology', 'technology', 'Tech-related posts', '#3B82F6'),
            ('Lifestyle', 'lifestyle', 'Life and culture posts', '#10B981'),
            ('Business', 'business', 'Business and finance', '#F59E0B')
            ON CONFLICT (slug) DO NOTHING
        """))

def downgrade():
    if os.getenv('FLASK_ENV') == 'development':
        connection = op.get_bind()
        connection.execute(sa.text(
            "DELETE FROM categories WHERE slug IN ('technology', 'lifestyle', 'business')"
        ))
\`\`\`

These examples demonstrate real-world scenarios with actual Flask CLI commands, outputs, and migration files that developers will encounter when using the standard Flask-Migrate approach.

## 🔄 Development Workflow

### Local Development
\`\`\`bash
# 1. Set environment
export FLASK_APP=app.py
export DATABASE_URL="your-database-url"

# 2. Make model changes in api/index.py

# 3. Generate migration
flask db migrate -m "Description of changes"

# 4. Review migration file
cat migrations/versions/latest_migration.py

# 5. Apply migration
flask db upgrade

# 6. Test your application
python app.py
\`\`\`

### Production Deployment
\`\`\`bash
# 1. Commit migration files
git add migrations/versions/
git commit -m "Add migration: description"

# 2. Push to repository
git push origin main

# 3. Deploy to Vercel
vercel --prod

# 4. Auto-migration runs automatically
# 5. Check deployment logs
vercel logs
\`\`\`

## 🚨 Troubleshooting

### "No such command 'db'"
\`\`\`bash
# Make sure Flask-Migrate is installed
pip install Flask-Migrate

# Ensure FLASK_APP is set correctly
export FLASK_APP=app.py

# Check if app.py imports migrate
# Should have: migrate = Migrate(app, db)
\`\`\`

### "Target database is not up to date"
\`\`\`bash
# Check current status
flask db current
flask db heads

# Apply pending migrations
flask db upgrade
\`\`\`

### "Can't locate revision identified by"
\`\`\`bash
# Check migration files exist
ls migrations/versions/

# If migrations are corrupted, reinitialize
rm -rf migrations/
flask db init
flask db migrate -m "Recreate initial migration"
\`\`\`

### Migration Conflicts
\`\`\`bash
# If you have merge conflicts in migrations
# 1. Resolve conflicts in migration files manually
# 2. Or create a merge migration
flask db merge -m "Merge migrations"
\`\`\`

### FLASK_APP Not Set
\`\`\`bash
# Error: Could not locate a Flask application
export FLASK_APP=app.py

# Or set it permanently in your shell profile
echo 'export FLASK_APP=app.py' >> ~/.bashrc
source ~/.bashrc
\`\`\`

## 🎯 Best Practices

### Environment Setup
\`\`\`bash
# Create a .env file for local development
echo "FLASK_APP=app.py" >> .env
echo "DATABASE_URL=postgresql://..." >> .env
echo "SECRET_KEY=your-secret-key" >> .env

# Use python-dotenv to load automatically
pip install python-dotenv
\`\`\`

### Migration Messages
\`\`\`bash
# Good: Descriptive messages
flask db migrate -m "Add user email verification field"
flask db migrate -m "Create posts table with foreign key to users"
flask db migrate -m "Add index to posts.created_at for performance"

# Avoid: Vague messages
flask db migrate -m "Update"
flask db migrate -m "Changes"
\`\`\`

### Review Before Applying
\`\`\`bash
# Always review generated migrations
cat migrations/versions/latest_migration.py

# Test migrations on development data first
flask db upgrade

# Check current status
flask db current
\`\`\`

### Backup Before Major Changes
\`\`\`bash
# Create backup before destructive migrations
python scripts/backup_database.py backup

# Then apply migration
flask db upgrade
\`\`\`

## 🔄 Integration with Auto-Migration

### How They Work Together

1. **Local Development**: Use Flask CLI commands
   \`\`\`bash
   flask db migrate -m "Add new feature"
   flask db upgrade
   \`\`\`

2. **Version Control**: Commit migration files
   \`\`\`bash
   git add migrations/versions/
   git commit -m "Add migration for new feature"
   \`\`\`

3. **Vercel Deployment**: Auto-migration runs
   - Detects new migration files
   - Runs `upgrade()` automatically
   - Falls back to table creation if needed

### Environment Variables

For both Flask CLI and auto-migration:
\`\`\`bash
# Required for both
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_APP=app.py

# Optional
SECRET_KEY=your-secret-key
FLASK_ENV=development
\`\`\`

## 📚 Additional Resources

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Flask CLI Documentation](https://flask.palletsprojects.com/en/2.3.x/cli/)
- [SQLAlchemy Migration Patterns](https://docs.sqlalchemy.org/en/14/core/metadata.html)

## 🎯 Summary

The Flask CLI provides a standard, well-documented approach to database migrations:

1. **Set** `FLASK_APP=app.py`
2. **Use** standard commands like `flask db migrate` and `flask db upgrade`
3. **Deploy** to Vercel where auto-migration handles the rest
4. **Monitor** with `flask db current` and migration logs

This approach combines the simplicity of standard Flask commands with the convenience of automatic deployment migrations, making it ideal for developers familiar with Flask best practices.
