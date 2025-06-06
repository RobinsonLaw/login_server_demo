-- Create database (run this as postgres superuser)
CREATE DATABASE flask_app;

-- Create a user for the application
CREATE USER flask_user WITH PASSWORD 'flask_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE flask_app TO flask_user;

-- Connect to the flask_app database
\c flask_app;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO flask_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flask_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO flask_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO flask_user;

-- Verify the setup
SELECT current_database(), current_user;
