# 🔄 Auto-Migration System Guide

This Flask application includes a comprehensive auto-migration system using Flask-Migrate that automatically handles database schema changes during deployment.

## 🚀 Features

### ✅ Automatic Migration on Startup
- **Smart Detection**: Checks for migrations directory on app startup
- **Auto-Upgrade**: Runs pending migrations automatically
- **Fallback Safety**: Creates tables if no migrations exist
- **Error Handling**: Graceful fallback prevents app crashes

### 🛠️ Complete Migration Toolkit
- **Initialization**: `init_migrations.py` - Set up Flask-Migrate
- **Creation**: `create_migration.py` - Generate new migrations
- **Status**: `migration_status.py` - Check migration status
- **Manual Control**: `manual_upgrade.py` - Manual migration execution
- **Rollback**: `rollback_migration.py` - Safe rollback to previous versions
- **Backup**: `backup_database.py` - Database backup and restore

## 📋 Quick Start

### 1. First-Time Setup
\`\`\`bash
# Initialize migrations (run once)
python scripts/init_migrations.py
\`\`\`

### 2. Making Schema Changes
\`\`\`bash
# 1. Modify your models in api/index.py
# 2. Create migration
python scripts/create_migration.py "Add user avatar field"
# 3. Deploy - auto-migration handles the rest!
\`\`\`

### 3. Monitoring
\`\`\`bash
# Check migration status
python scripts/migration_status.py

# Manual upgrade if needed
python scripts/manual_upgrade.py
\`\`\`

## 🔧 How Auto-Migration Works

### Startup Process
1. **Check**: App looks for migrations directory
2. **Detect**: Identifies pending migrations
3. **Apply**: Runs `flask db upgrade` automatically
4. **Fallback**: Creates tables if migrations fail
5. **Continue**: App starts normally

### Development Workflow
1. **Modify**: Update SQLAlchemy models in `api/index.py`
2. **Generate**: Create migration with descriptive message
3. **Review**: Check generated migration file
4. **Test**: Verify locally
5. **Deploy**: Push to production (auto-migration runs)

## 📚 Script Reference

### `init_migrations.py`
**Purpose**: Initialize Flask-Migrate for the first time
\`\`\`bash
python scripts/init_migrations.py
\`\`\`
- Creates migrations directory
- Generates initial migration
- Applies baseline schema

### `create_migration.py`
**Purpose**: Generate new migrations for schema changes
\`\`\`bash
python scripts/create_migration.py "Description of changes"
\`\`\`
- Detects model changes
- Creates migration file
- Validates migration

### `migration_status.py`
**Purpose**: Check current migration status
\`\`\`bash
python scripts/migration_status.py
\`\`\`
- Shows current vs latest revision
- Lists database tables and columns
- Displays migration history

### `manual_upgrade.py`
**Purpose**: Manually run migrations
\`\`\`bash
python scripts/manual_upgrade.py
\`\`\`
- Manual migration execution
- Confirmation prompts
- Status verification

### `rollback_migration.py`
**Purpose**: Rollback to previous migration
\`\`\`bash
python scripts/rollback_migration.py prev
python scripts/rollback_migration.py <revision_id>
\`\`\`
- Safe rollback with confirmations
- Data loss warnings
- Recovery instructions

### `backup_database.py`
**Purpose**: Backup and restore database
\`\`\`bash
# Create backup
python scripts/backup_database.py backup

# Restore from backup
python scripts/backup_database.py restore backup_file.sql
\`\`\`
- PostgreSQL database backups
- Timestamped backup files
- Restore functionality

## 🎯 Common Use Cases

### Adding New Table
\`\`\`python
# In api/index.py - Add new model
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Generate migration
python scripts/create_migration.py "Add categories table"
\`\`\`

### Modifying Existing Column
\`\`\`python
# In api/index.py - Modify column
# Change: username = db.Column(db.String(50), ...)
# To:     username = db.Column(db.String(100), ...)

# Generate migration
python scripts/create_migration.py "Increase username length"
\`\`\`

### Adding New Column
\`\`\`python
# In api/index.py - Add column to existing model
class User(db.Model):
    # ... existing fields ...
    avatar_url = db.Column(db.String(255), nullable=True)

# Generate migration
python scripts/create_migration.py "Add user avatar URL"
\`\`\`

## ⚠️ Important Notes

### Auto-Migration Behavior
- **Startup**: Runs automatically when app starts
- **Vercel**: Compatible with serverless cold starts
- **Safety**: Fallback to table creation if migrations fail
- **Logging**: Clear status messages for monitoring

### Best Practices
1. **Always backup** before major schema changes
2. **Test migrations** in development first
3. **Review generated** migration files
4. **Use descriptive** migration messages
5. **Monitor logs** during deployment

### Troubleshooting
- **Migration fails**: Check `manual_upgrade.py`
- **Schema conflicts**: Review migration files
- **Data loss**: Restore from backup
- **Startup issues**: Check database connection

## 🚨 Emergency Procedures

### If Migration Fails on Startup
\`\`\`bash
# 1. Check status
python scripts/migration_status.py

# 2. Try manual upgrade
python scripts/manual_upgrade.py

# 3. If still failing, rollback
python scripts/rollback_migration.py prev

# 4. Restore from backup if needed
python scripts/backup_database.py restore <backup_file>
\`\`\`

### If Database is Corrupted
\`\`\`bash
# 1. Restore from latest backup
python scripts/backup_database.py restore <latest_backup>

# 2. Re-run migrations
python scripts/manual_upgrade.py

# 3. Verify application functionality
\`\`\`

## 📊 Monitoring

### Check Migration Status
- **Current revision**: What version is deployed
- **Latest revision**: What version is available
- **Pending migrations**: What needs to be applied
- **Database tables**: Current schema state

### Log Messages
- `🔄 Running database migrations...` - Auto-migration starting
- `✅ Database migrations completed` - Success
- `🔧 Creating database tables...` - Fallback mode
- `❌ Database initialization error` - Failure

## 🎯 Advanced Usage

### Custom Migration Scripts
\`\`\`python
# In migration file - custom data migration
def upgrade():
    # Schema changes
    op.add_column('users', sa.Column('avatar_url', sa.String(255)))
    
    # Data migration
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET avatar_url = '/default-avatar.png' WHERE avatar_url IS NULL"
    )
\`\`\`

### Environment-Specific Migrations
\`\`\`python
# Different behavior per environment
import os

def upgrade():
    if os.environ.get('FLASK_ENV') == 'production':
        # Production-specific migration
        pass
    else:
        # Development migration
        pass
\`\`\`

This migration system provides robust, automatic database schema management while maintaining safety and flexibility for both development and production environments.
