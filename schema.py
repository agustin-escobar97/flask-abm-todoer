instructions = [
    "SET FOREIGN_KEY_CHECKS=0;",
    "DROP TABLE IF EXISTS todo;",
    "DROP TABLE IF EXISTS user;",
    "SET FOREIGN_KEY_CHECKS=1;",
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT, 
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
            )
    """,
    """
        CREATE TABLE todo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES user (id)
        )
    """,
    """
    ALTER TABLE prueba.todo ALTER completed SET DEFAULT "0";
    """
]

#set FLASK_DATABASE_HOST=localhost
#set FLASK_DATABASE_USER=root
#set FLASK_DATABASE_PASSWORD=root
#set FLASK_DATABASE=prueba