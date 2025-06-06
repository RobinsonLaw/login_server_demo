-- Insert sample users (passwords are hashed versions of 'password123')
INSERT INTO users (username, email, password_hash) VALUES 
('alice', 'alice@example.com', 'scrypt:32768:8:1$YourHashedPasswordHere'),
('bob', 'bob@example.com', 'scrypt:32768:8:1$YourHashedPasswordHere'),
('charlie', 'charlie@example.com', 'scrypt:32768:8:1$YourHashedPasswordHere');

-- Insert sample posts
INSERT INTO posts (title, content, user_id) VALUES 
('Welcome to PostgreSQL', 'This is my first post using PostgreSQL with Flask!', 1),
('Database Performance', 'PostgreSQL offers excellent performance for web applications.', 2),
('Flask Integration', 'Integrating Flask with PostgreSQL is straightforward and powerful.', 1),
('Advanced Queries', 'PostgreSQL supports complex queries and JSON operations.', 3),
('Scaling Applications', 'PostgreSQL scales well for growing applications.', 2);

-- Verify the data
SELECT 
    p.id, 
    p.title, 
    u.username as author,
    p.created_at
FROM posts p 
JOIN users u ON p.user_id = u.id 
ORDER BY p.created_at DESC;
