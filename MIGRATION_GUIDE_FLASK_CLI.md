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
