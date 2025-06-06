# 🔄 Flask CLI Migration Guide

Simple guide for using **standard Flask CLI commands** for database migrations.

## 🚀 Quick Overview

**Flask CLI Commands:**
- `flask db init` - Set up migrations (run once)
- `flask db migrate` - Create new migrations
- `flask db upgrade` - Apply migrations
- `flask db current` - Show current status
- `flask db history` - Show migration history
- `flask db downgrade` - Rollback migrations

## 📋 Getting Started

### 1. Setup Environment
\`\`\`bash
export FLASK_APP=app.py
export DATABASE_URL="postgresql://user:pass@host:port/db"
\`\`\`

### 2. Initialize (First Time)
\`\`\`bash
flask db init
\`\`\`

### 3. Create Initial Migration
\`\`\`bash
flask db migrate -m "Initial migration"
flask db upgrade
\`\`\`

## 🎯 Real Examples

### Example 1: Add New Field

**Step 1: Edit model** in `api/index.py`:
\`\`\`python
class User(db.Model):
    # existing fields...
    avatar_url = db.Column(db.String(255), nullable=True)  # ADD THIS
\`\`\`

**Step 2: Create migration:**
\`\`\`bash
flask db migrate -m "Add avatar_url to users"
\`\`\`

**Step 3: Apply migration:**
\`\`\`bash
flask db upgrade
\`\`\`

**Step 4: Deploy:**
\`\`\`bash
git add migrations/
git commit -m "Add avatar field"
vercel --prod
\`\`\`

### Example 2: Add New Table

**Step 1: Add model** in `api/index.py`:
\`\`\`python
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
\`\`\`

**Step 2: Create and apply:**
\`\`\`bash
flask db migrate -m "Create categories table"
flask db upgrade
\`\`\`

### Example 3: Rollback Changes

**Check current status:**
\`\`\`bash
flask db current
flask db history
\`\`\`

**Rollback to previous:**
\`\`\`bash
flask db downgrade
\`\`\`

## 🛠️ Command Details

### Create Migration
\`\`\`bash
flask db migrate -m "Description here"
\`\`\`
**What it does:** Compares models with database and creates migration

### Apply Migration
\`\`\`bash
flask db upgrade
\`\`\`
**What it does:** Runs all pending migrations

### Check Status
\`\`\`bash
flask db current    # Show current revision
flask db history    # Show all migrations
\`\`\`

### Rollback
\`\`\`bash
flask db downgrade              # Go back one migration
flask db downgrade <revision>   # Go to specific revision
\`\`\`

## 🔄 Development Workflow

### Local Development
\`\`\`bash
# 1. Set environment
export FLASK_APP=app.py

# 2. Make model changes in api/index.py

# 3. Create migration
flask db migrate -m "Add new feature"

# 4. Apply migration
flask db upgrade

# 5. Check status
flask db current
\`\`\`

### Deploy to Production
\`\`\`bash
# 1. Commit migration files
git add migrations/versions/
git commit -m "Add migration"

# 2. Deploy
vercel --prod
# Auto-migration runs automatically
\`\`\`

## 🚨 Troubleshooting

### "No such command 'db'"
\`\`\`bash
# Make sure FLASK_APP is set
export FLASK_APP=app.py

# Check Flask-Migrate is installed
pip install Flask-Migrate
\`\`\`

### Migration Conflicts
\`\`\`bash
# If multiple heads exist
flask db merge -m "Merge migrations"
flask db upgrade
\`\`\`

### Database Not Up to Date
\`\`\`bash
# Check what's pending
flask db current
flask db heads

# Apply pending migrations
flask db upgrade
\`\`\`

## ✅ Best Practices

### Good Migration Messages
\`\`\`bash
# ✅ Good
flask db migrate -m "Add user email verification"
flask db migrate -m "Create posts table"

# ❌ Bad
flask db migrate -m "Update"
flask db migrate -m "Changes"
\`\`\`

### Safety First
\`\`\`bash
# Always review generated migrations
cat migrations/versions/latest_migration.py

# Test locally before deploying
flask db upgrade

# Check status after changes
flask db current
\`\`\`

### Environment Setup
\`\`\`bash
# Create .env file for convenience
echo "FLASK_APP=app.py" >> .env
echo "DATABASE_URL=your-database-url" >> .env

# Load with python-dotenv
pip install python-dotenv
\`\`\`

## 🎯 Why Use Flask CLI?

- **Industry standard** - Official Flask approach
- **Well documented** - Lots of tutorials available
- **Simple syntax** - Familiar `flask db` commands
- **Auto-migration ready** - Works with Vercel deployment

This approach follows Flask best practices and integrates seamlessly with the auto-migration system!
