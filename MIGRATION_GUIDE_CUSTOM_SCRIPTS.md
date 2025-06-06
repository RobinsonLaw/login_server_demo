# 🔄 Custom Scripts Migration Guide

Simple guide for using **custom migration scripts** in this Flask application.

## 🚀 Quick Overview

**Custom Scripts Available:**
- `init_migrations.py` - Set up migrations (run once)
- `create_migration.py` - Make new migrations
- `migration_status.py` - Check status
- `manual_upgrade.py` - Apply migrations
- `rollback_migration.py` - Undo migrations
- `backup_database.py` - Backup/restore database

## 📋 Getting Started

### 1. First Time Setup
\`\`\`bash
python scripts/init_migrations.py
\`\`\`

### 2. Make Schema Changes
\`\`\`bash
# 1. Edit models in api/index.py
# 2. Create migration
python scripts/create_migration.py "Add user avatar field"
# 3. Deploy (auto-migration runs)
\`\`\`

### 3. Check Status
\`\`\`bash
python scripts/migration_status.py
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
python scripts/create_migration.py "Add avatar_url to users"
\`\`\`

**Step 3: Apply locally:**
\`\`\`bash
python scripts/manual_upgrade.py
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
python scripts/create_migration.py "Create categories table"
python scripts/manual_upgrade.py
\`\`\`

### Example 3: Rollback Changes

**Check what to rollback:**
\`\`\`bash
python scripts/migration_status.py
\`\`\`

**Rollback to previous:**
\`\`\`bash
python scripts/rollback_migration.py prev
\`\`\`

## 🛠️ Command Details

### Create Migration
\`\`\`bash
python scripts/create_migration.py "Description here"
\`\`\`
**What it does:** Detects model changes and creates migration file

### Apply Migration
\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`
**What it does:** Runs pending migrations on your database

### Check Status
\`\`\`bash
python scripts/migration_status.py
\`\`\`
**What it does:** Shows current migration status and database info

### Backup Database
\`\`\`bash
python scripts/backup_database.py backup
python scripts/backup_database.py restore backup_file.sql
\`\`\`

## 🔄 Development Workflow

### Local Development
\`\`\`bash
# 1. Make model changes
# 2. Create migration
python scripts/create_migration.py "Add new feature"

# 3. Test migration
python scripts/manual_upgrade.py

# 4. Check it worked
python scripts/migration_status.py
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

### Migration Fails
\`\`\`bash
# Check status
python scripts/migration_status.py

# Try manual upgrade
python scripts/manual_upgrade.py

# If still broken, rollback
python scripts/rollback_migration.py prev
\`\`\`

### Database Connection Issues
\`\`\`bash
# Check your DATABASE_URL
echo $DATABASE_URL

# Test connection
python scripts/migration_status.py
\`\`\`

## ✅ Best Practices

### Good Migration Messages
\`\`\`bash
# ✅ Good
python scripts/create_migration.py "Add user email verification"
python scripts/create_migration.py "Create posts table"

# ❌ Bad
python scripts/create_migration.py "Update"
python scripts/create_migration.py "Changes"
\`\`\`

### Safety First
\`\`\`bash
# Always backup before big changes
python scripts/backup_database.py backup

# Review migration files before applying
cat migrations/versions/latest_migration.py

# Test locally first
python scripts/manual_upgrade.py
\`\`\`

## 🎯 Why Use Custom Scripts?

- **Beginner-friendly** - Clear, simple commands
- **Built-in safety** - Confirmations and warnings
- **Project-specific** - Tailored for this app
- **Auto-migration ready** - Works with Vercel deployment

This approach makes database migrations simple and safe!
