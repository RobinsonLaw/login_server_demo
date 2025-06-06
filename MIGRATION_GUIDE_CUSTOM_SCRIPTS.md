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
