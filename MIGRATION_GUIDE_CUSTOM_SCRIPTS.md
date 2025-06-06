# 🔄 Custom Scripts Migration Guide

This guide covers using the **custom migration scripts** approach for database schema management. This is the primary method built into this Flask application.

## 🚀 Overview

### ✅ Custom Scripts Features
- **Project-specific**: Tailored for this Flask application
- **Comprehensive toolkit**: Complete set of migration tools
- **Beginner-friendly**: Clear, explicit commands
- **Auto-migration integration**: Works seamlessly with Vercel deployment
- **Error handling**: Built-in safety checks and confirmations

### 🛠️ Available Scripts
- **`init_migrations.py`** - Initialize Flask-Migrate
- **`create_migration.py`** - Generate new migrations
- **`migration_status.py`** - Check migration status
- **`manual_upgrade.py`** - Apply migrations manually
- **`rollback_migration.py`** - Rollback to previous versions
- **`backup_database.py`** - Database backup and restore

## 📋 Quick Start

### 1. First-Time Setup
\`\`\`bash
# Initialize migrations (run once)
python scripts/init_migrations.py
\`\`\`

**What this does:**
- Creates `migrations/` directory
- Sets up Flask-Migrate configuration
- Generates initial migration
- Applies baseline schema

### 2. Making Schema Changes
\`\`\`bash
# 1. Modify your models in api/index.py
# 2. Create migration
python scripts/create_migration.py "Add user avatar field"
# 3. Deploy - auto-migration handles the rest!
\`\`\`

### 3. Monitoring and Control
\`\`\`bash
# Check migration status
python scripts/migration_status.py

# Manual upgrade if needed
python scripts/manual_upgrade.py

# Rollback if necessary
python scripts/rollback_migration.py prev
\`\`\`

## 🔧 How Auto-Migration Works

### Startup Process
1. **Check**: App looks for migrations directory
2. **Detect**: Identifies pending migrations
3. **Apply**: Runs migrations automatically
4. **Fallback**: Creates tables if migrations fail
5. **Continue**: App starts normally

### Development Workflow
1. **Modify**: Update SQLAlchemy models in `api/index.py`
2. **Generate**: Create migration with custom script
3. **Review**: Check generated migration file
4. **Test**: Verify locally with manual upgrade
5. **Deploy**: Push to production (auto-migration runs)

## 📚 Detailed Script Reference

### `init_migrations.py`
**Purpose**: Initialize Flask-Migrate for the first time

\`\`\`bash
python scripts/init_migrations.py
\`\`\`

**Features:**
- Creates migrations directory structure
- Generates initial migration from current models
- Applies baseline schema to database
- Provides setup confirmation

**Output Example:**
\`\`\`
🔧 Initializing Flask-Migrate...
✅ Migrations directory created
📝 Creating initial migration...
✅ Initial migration created
🚀 Applying initial migration...
✅ Initial migration applied successfully
🎉 Flask-Migrate initialization completed!
\`\`\`

### `create_migration.py`
**Purpose**: Generate new migrations for schema changes

\`\`\`bash
python scripts/create_migration.py "Description of changes"
\`\`\`

**Features:**
- Detects model changes automatically
- Creates timestamped migration file
- Validates migration syntax
- Provides clear feedback

**Example Usage:**
\`\`\`bash
# Add new field
python scripts/create_migration.py "Add user avatar URL field"

# Modify existing field
python scripts/create_migration.py "Increase username length to 100 chars"

# Add new table
python scripts/create_migration.py "Create categories table"
\`\`\`

**Output Example:**
\`\`\`
📝 Creating migration: Add user avatar URL field
✅ Migration created successfully

📋 Next steps:
  1. Review the generated migration file in migrations/versions/
  2. Test the migration locally
  3. Deploy to production (auto-migration will apply it)
\`\`\`

### `migration_status.py`
**Purpose**: Check current migration status and database information

\`\`\`bash
python scripts/migration_status.py
\`\`\`

**Features:**
- Shows current vs latest revision
- Lists database tables and columns
- Displays migration history
- Provides database summary

**Output Example:**
\`\`\`
📊 Migration Status Report
==================================================
Current revision: abc123def456
Latest revision:  abc123def456
Status: ✅ Database is up to date

📋 Database Tables:
------------------------------
📄 users (5 columns)
   - id (INTEGER)
   - username (VARCHAR(50))
   - email (VARCHAR(100))
   ... and 2 more

📄 posts (6 columns)
   - id (INTEGER)
   - title (VARCHAR(200))
   - content (TEXT)
   ... and 3 more

📁 Migration Files:
------------------------------
1. 001_initial_migration.py
2. 002_add_user_avatar.py
\`\`\`

### `manual_upgrade.py`
**Purpose**: Manually apply database migrations

\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`

**Features:**
- Manual migration execution
- Safety confirmations
- Status verification
- Error handling with recovery tips

**Example Workflow:**
\`\`\`
🔧 Manual Database Migration
========================================
Current revision: abc123def456
Latest revision:  def789ghi012

⚠️ This will upgrade your database schema.
Continue? (y/N): y

🚀 Running database upgrade...
✅ Database upgrade completed successfully!
New current revision: def789ghi012
\`\`\`

### `rollback_migration.py`
**Purpose**: Safely rollback to previous migration

\`\`\`bash
python scripts/rollback_migration.py prev
python scripts/rollback_migration.py <revision_id>
\`\`\`

**Features:**
- Safe rollback with multiple confirmations
- Data loss warnings
- Recovery instructions
- Revision targeting

**Example Usage:**
\`\`\`bash
# Rollback to previous version
python scripts/rollback_migration.py prev

# Rollback to specific revision
python scripts/rollback_migration.py abc123def456

# Rollback to base (initial state)
python scripts/rollback_migration.py base
\`\`\`

**Safety Workflow:**
\`\`\`
⚠️ Database Migration Rollback
========================================
🚨 WARNING: This may cause data loss!

Current revision: def789ghi012
Target revision: abc123def456

Are you sure? (y/N): y
This may cause DATA LOSS. Continue? (y/N): y

🔄 Rolling back to revision: abc123def456
✅ Rollback completed successfully!
\`\`\`

### `backup_database.py`
**Purpose**: Create and restore database backups

\`\`\`bash
# Create backup
python scripts/backup_database.py backup

# Create backup with custom name
python scripts/backup_database.py backup my_backup.sql

# Restore from backup
python scripts/backup_database.py restore backup_file.sql
\`\`\`

**Features:**
- PostgreSQL database backups
- Timestamped backup files
- Restore functionality
- File size reporting

**Backup Example:**
\`\`\`
📦 Creating database backup...
Database: flask_app
Output file: backup_flask_app_20241201_143022.sql
✅ Backup created successfully!
📄 File: backup_flask_app_20241201_143022.sql
📊 Size: 2.45 MB
\`\`\`

## 🎯 Common Use Cases

### Adding New Field to Existing Table

1. **Modify the model** in `api/index.py`:
\`\`\`python
class User(db.Model):
    # ... existing fields ...
    avatar_url = db.Column(db.String(255), nullable=True)
\`\`\`

2. **Generate migration**:
\`\`\`bash
python scripts/create_migration.py "Add user avatar URL field"
\`\`\`

3. **Review generated migration**:
\`\`\`python
def upgrade():
    op.add_column('users', sa.Column('avatar_url', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('users', 'avatar_url')
\`\`\`

4. **Test locally**:
\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`

5. **Deploy**:
\`\`\`bash
git add migrations/versions/
git commit -m "Add user avatar URL field"
vercel --prod
\`\`\`

### Creating New Table

1. **Add new model** in `api/index.py`:
\`\`\`python
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
\`\`\`

2. **Generate migration**:
\`\`\`bash
python scripts/create_migration.py "Create categories table"
\`\`\`

3. **Apply and deploy** following same workflow

### Modifying Existing Field

1. **Change model** in `api/index.py`:
\`\`\`python
# Change from:
username = db.Column(db.String(50), unique=True, nullable=False)
# To:
username = db.Column(db.String(100), unique=True, nullable=False)
\`\`\`

2. **Generate migration**:
\`\`\`bash
python scripts/create_migration.py "Increase username length to 100 characters"
\`\`\`

## 🔄 Integration with Auto-Migration

### Local Development
\`\`\`bash
# 1. Make model changes
# 2. Generate migration
python scripts/create_migration.py "Add new feature"

# 3. Test migration locally
python scripts/manual_upgrade.py

# 4. Verify changes
python scripts/migration_status.py
\`\`\`

### Production Deployment
\`\`\`bash
# 1. Commit migration files
git add migrations/versions/
git commit -m "Add migration for new feature"

# 2. Deploy to Vercel
vercel --prod

# 3. Auto-migration runs automatically during cold start
# 4. Check logs for migration status
vercel logs
\`\`\`

## 🚨 Troubleshooting

### Migration Creation Fails
\`\`\`bash
# Check if migrations are initialized
python scripts/migration_status.py

# Re-initialize if needed
python scripts/init_migrations.py
\`\`\`

### Migration Application Fails
\`\`\`bash
# Check current status
python scripts/migration_status.py

# Try manual upgrade with verbose output
python scripts/manual_upgrade.py

# If still failing, consider rollback
python scripts/rollback_migration.py prev
\`\`\`

### Database Connection Issues
\`\`\`bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
python scripts/migration_status.py
\`\`\`

## 🎯 Best Practices

### Migration Messages
\`\`\`bash
# Good: Descriptive messages
python scripts/create_migration.py "Add user email verification field"
python scripts/create_migration.py "Create posts table with foreign key to users"
python scripts/create_migration.py "Add index to posts.created_at for performance"

# Avoid: Vague messages
python scripts/create_migration.py "Update"
python scripts/create_migration.py "Changes"
\`\`\`

### Safety First
\`\`\`bash
# Always backup before major changes
python scripts/backup_database.py backup

# Review migrations before applying
cat migrations/versions/latest_migration.py

# Test on development data first
python scripts/manual_upgrade.py
\`\`\`

### Version Control
\`\`\`bash
# Always commit migration files
git add migrations/versions/
git commit -m "Add migration: descriptive message"

# Never edit applied migrations
# Create new migration instead
\`\`\`

## 📊 Advantages of Custom Scripts

### **Explicit and Clear**
- Each command is self-explanatory
- No need to remember Flask CLI syntax
- Built-in help and confirmations

### **Project-Specific**
- Tailored for this application's needs
- Integrated error handling
- Custom safety features

### **Beginner-Friendly**
- Clear output messages
- Step-by-step guidance
- Built-in troubleshooting

### **Production-Ready**
- Seamless Vercel integration
- Auto-migration compatibility
- Comprehensive backup system

This custom scripts approach provides a robust, user-friendly way to manage database migrations while maintaining full compatibility with the auto-migration system for production deployments.

## 🎯 Real-World Examples

### Example 1: Adding User Profile Fields

**Scenario**: Add avatar URL and bio fields to the User model

**Step 1: Modify the model** in `api/index.py`:
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

**Step 2: Generate migration**:
\`\`\`bash
python scripts/create_migration.py "Add user profile fields: avatar_url, bio, is_verified"
\`\`\`

**Output**:
\`\`\`
📝 Creating migration: Add user profile fields: avatar_url, bio, is_verified
✅ Migration created successfully

📋 Next steps:
  1. Review the generated migration file in migrations/versions/
  2. Test the migration locally
  3. Deploy to production (auto-migration will apply it)
\`\`\`

**Step 3: Review generated migration file** (`migrations/versions/002_add_user_profile_fields.py`):
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

**Step 4: Apply migration locally**:
\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`

**Output**:
\`\`\`
🔧 Manual Database Migration
========================================
Current revision: abc123def456
Latest revision:  def789ghi012

⚠️ This will upgrade your database schema.
Continue? (y/N): y

🚀 Running database upgrade...
✅ Database upgrade completed successfully!
New current revision: def789ghi012
\`\`\`

**Step 5: Verify changes**:
\`\`\`bash
python scripts/migration_status.py
\`\`\`

**Output**:
\`\`\`
📊 Migration Status Report
==================================================
Current revision: def789ghi012
Latest revision:  def789ghi012
Status: ✅ Database is up to date

📋 Database Tables:
------------------------------
📄 users (8 columns)
   - id (INTEGER)
   - username (VARCHAR(50))
   - email (VARCHAR(100))
   - password_hash (VARCHAR(255))
   - created_at (TIMESTAMP)
   - avatar_url (VARCHAR(255))  ← NEW
   - bio (TEXT)                 ← NEW
   - is_verified (BOOLEAN)      ← NEW
\`\`\`

**Step 6: Deploy to production**:
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
python scripts/create_migration.py "Create categories table and add category_id to posts"
\`\`\`

**Step 3: Generated migration file**:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('slug', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('color', sa.String(length=7), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'category_id')
    op.drop_table('categories')
    # ### end Alembic commands ###
\`\`\`

**Step 4: Apply and verify**:
\`\`\`bash
python scripts/manual_upgrade.py
python scripts/migration_status.py
\`\`\`

### Example 3: Adding Database Indexes for Performance

**Scenario**: Add indexes to improve query performance

**Step 1: Create custom migration** (since indexes aren't auto-detected):
\`\`\`bash
python scripts/create_migration.py "Add performance indexes to posts and users tables"
\`\`\`

**Step 2: Manually edit the generated migration file**:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Add custom indexes for performance
    op.create_index('idx_posts_created_at', 'posts', ['created_at'])
    op.create_index('idx_posts_user_id_created_at', 'posts', ['user_id', 'created_at'])
    op.create_index('idx_posts_category_id', 'posts', ['category_id'])
    op.create_index('idx_users_email_active', 'users', ['email', 'is_verified'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_users_email_active', table_name='users')
    op.drop_index('idx_posts_category_id', table_name='posts')
    op.drop_index('idx_posts_user_id_created_at', table_name='posts')
    op.drop_index('idx_posts_created_at', table_name='posts')
    # ### end Alembic commands ###
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
python scripts/create_migration.py "Add full_name field and populate from username"
\`\`\`

**Step 3: Edit migration to include data migration**:
\`\`\`python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(length=100), nullable=True))
    
    # Data migration: populate full_name from username
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = username WHERE full_name IS NULL"
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###
\`\`\`

### Example 5: Rollback Scenario

**Scenario**: The last migration caused issues and needs to be rolled back

**Step 1: Check current status**:
\`\`\`bash
python scripts/migration_status.py
\`\`\`

**Output**:
\`\`\`
📊 Migration Status Report
==================================================
Current revision: ghi012jkl345
Latest revision:  ghi012jkl345
Status: ✅ Database is up to date

📁 Migration Files:
------------------------------
1. 001_initial_migration.py
2. 002_add_user_profile_fields.py
3. 003_create_categories_table.py
4. 004_add_performance_indexes.py
5. 005_add_full_name_field.py  ← Current (problematic)
\`\`\`

**Step 2: Rollback to previous version**:
\`\`\`bash
python scripts/rollback_migration.py prev
\`\`\`

**Output**:
\`\`\`
⚠️ Database Migration Rollback
========================================
🚨 WARNING: This may cause data loss!

Current revision: ghi012jkl345
Target revision: def789ghi012

🎯 Target revision: prev
⚠️ This will rollback your database schema.
💾 Make sure you have a backup!

Are you sure? (y/N): y
This may cause DATA LOSS. Continue? (y/N): y

🔄 Rolling back to revision: def789ghi012
✅ Rollback completed successfully!
New current revision: def789ghi012

📋 Next steps:
  1. Verify your application works correctly
  2. Check for any data inconsistencies
  3. Consider creating a new migration if needed
\`\`\`

**Step 3: Verify rollback**:
\`\`\`bash
python scripts/migration_status.py
\`\`\`

### Example 6: Complete Development Cycle

**Real scenario**: Adding a complete commenting system

**Step 1: Add Comment model**:
\`\`\`python
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)  # For replies
    
    # Relationships
    author = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
\`\`\`

**Step 2: Create migration**:
\`\`\`bash
python scripts/create_migration.py "Create comments table with nested replies support"
\`\`\`

**Step 3: Apply locally**:
\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`

**Step 4: Test with sample data**:
\`\`\`bash
python scripts/seed_data.py  # Add some test comments
\`\`\`

**Step 5: Deploy**:
\`\`\`bash
git add migrations/versions/006_create_comments_table.py
git commit -m "Add comments system with nested replies"
vercel --prod
\`\`\`

**Step 6: Monitor deployment**:
\`\`\`bash
vercel logs --follow
\`\`\`

These examples show real-world scenarios with actual code changes, migration files, and command outputs that users will encounter when working with the custom scripts migration system.
