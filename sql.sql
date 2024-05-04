CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL
);

INSERT INTO users VALUES
(1,'admin','admin', 'admin'),
(2,'test','test', 'manager');

SELECT * FROM users