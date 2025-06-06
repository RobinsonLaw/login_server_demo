# Flask SQLAlchemy API on Vercel

A Flask API server with SQLAlchemy ORM deployed on Vercel serverless platform.

## 🚀 Vercel Deployment Changes

### Key Modifications for Vercel:

1. **File Structure**:
   - Main app moved to `api/index.py` (Vercel requirement)
   - All models inline (no separate files for serverless)
   - Added `vercel.json` configuration

2. **Database Configuration**:
   - Optimized connection pooling for serverless
   - Added connection timeout and pre-ping
   - Environment-based DATABASE_URL

3. **Route Prefixes**:
   - All routes prefixed with `/api/`
   - Root route serves API documentation

4. **Session Management**:
   - Uses Flask's built-in sessions (stored in cookies)
   - For production, consider Redis or database sessions

5. **Error Handling**:
   - Enhanced for serverless cold starts
   - Proper database rollback on errors

## 📋 Prerequisites

- Vercel account
- PostgreSQL database (Neon, Supabase, or other cloud provider)
- Python 3.8+

## 🛠️ Setup Instructions

### 1. Database Setup

Use a cloud PostgreSQL provider:

**Option A: Neon (Recommended)**
\`\`\`bash
# Sign up at neon.tech
# Create a new project
# Copy the connection string
\`\`\`

**Option B: Supabase**
\`\`\`bash
# Sign up at supabase.com
# Create a new project
# Go to Settings > Database
# Copy the connection string
\`\`\`

### 2. Local Development

\`\`\`bash
# Clone the repository
git clone <your-repo>
cd flask-vercel-app

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@host:port/database"
export SECRET_KEY="your-secret-key"

# Setup database (run once)
python scripts/setup_database.py

# Run locally
python api/index.py
\`\`\`

### 3. Deploy to Vercel

\`\`\`bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Set environment variables
vercel env add DATABASE_URL
vercel env add SECRET_KEY

# Deploy
vercel --prod
\`\`\`

### 4. Environment Variables

Set these in Vercel dashboard or CLI:

\`\`\`bash
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-super-secret-key-here
\`\`\`

## 🔧 Vercel Configuration

### vercel.json
\`\`\`json
{
  "version": 2,
  "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"src": "/(.*)", "dest": "api/index.py"}
  ]
}
\`\`\`

## 📡 API Endpoints

All endpoints are prefixed with `/api/`:

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login  
- `POST /api/logout` - User logout

### User Management
- `GET /api/profile` - Get user profile (protected)
- `PUT /api/profile` - Update user profile (protected)
- `GET /api/users` - Get all users (paginated)

### Post Management
- `POST /api/posts` - Create new post (protected)
- `GET /api/posts` - Get all posts (paginated)
- `GET /api/posts/<id>` - Get specific post
- `PUT /api/posts/<id>` - Update post (protected)
- `DELETE /api/posts/<id>` - Delete post (protected)

### System
- `GET /api` - API documentation
- `GET /api/health` - Health check

## 🧪 Testing

### Local Testing
\`\`\`bash
python test_vercel_api.py
\`\`\`

### Production Testing
\`\`\`bash
export VERCEL_URL="your-app.vercel.app"
python test_vercel_api.py
\`\`\`

## 🔍 Serverless Considerations

### Cold Starts
- First request may be slower (~1-3 seconds)
- Subsequent requests are fast
- Database connections are pooled

### Database Connections
- Connection pooling optimized for serverless
- Automatic connection cleanup
- Pre-ping to handle stale connections

### Session Storage
- Currently uses cookie-based sessions
- For high-traffic apps, consider Redis sessions

### File Storage
- No persistent file system
- Use cloud storage for file uploads

## 🚨 Limitations on Vercel

1. **Execution Time**: Max 30 seconds per request
2. **Memory**: Limited memory per function
3. **File System**: Read-only, no persistent storage
4. **Database**: Must use external database
5. **Background Tasks**: No long-running processes

## 🔧 Troubleshooting

### Common Issues

**Database Connection Errors:**
\`\`\`bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:port/db
\`\`\`

**Cold Start Timeouts:**
\`\`\`bash
# Increase timeout in vercel.json
"functions": {
  "api/index.py": {
    "maxDuration": 30
  }
}
\`\`\`

**Import Errors:**
\`\`\`bash
# Ensure all imports are in api/index.py
# Vercel serverless functions need everything in one file
\`\`\`

### Debugging

**Check Vercel Logs:**
\`\`\`bash
vercel logs your-deployment-url
\`\`\`

**Local Testing:**
\`\`\`bash
vercel dev
\`\`\`

## 🚀 Production Optimizations

1. **Use Connection Pooling**:
   ```python
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
       'pool_size': 5,
       'pool_recycle': 300,
       'pool_pre_ping': True
   }
   \`\`\`

2. **Enable Caching**:
   - Use Redis for session storage
   - Cache frequently accessed data

3. **Monitor Performance**:
   - Use Vercel Analytics
   - Monitor database connections
   - Track cold start times

## 📚 Additional Resources

- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel Guide](https://vercel.com/guides/using-flask-with-vercel)
- [Neon Database](https://neon.tech/)
- [Supabase Database](https://supabase.com/)

## 🎯 Next Steps

- [ ] Add Redis for session storage
- [ ] Implement API rate limiting
- [ ] Add comprehensive logging
- [ ] Set up monitoring and alerts
- [ ] Add API documentation with Swagger
