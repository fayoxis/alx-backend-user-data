# 🧮User Authentication Service

This project is designed to provide a thorough understanding of creating a user authentication service using modern Python practices and libraries. It encompasses essential concepts such as user management, secure password handling, and session management.

## 🧮 Overview

The User Authentication Service will enable users to register, log in, and manage their authentication credentials securely. The project utilizes SQLAlchemy for database interactions, ensuring a robust data management layer while adhering to best practices in code style and security.

## 🧮Requirements

To successfully run this project, ensure you have the following dependencies installed:

- **SQLAlchemy**: Version 1.3.x
  - A powerful SQL toolkit and Object Relational Mapper (ORM) for Python.
  
- **pycodestyle**: Version 2.5
  - A tool for checking compliance with PEP 8, the style guide for Python code.

- **bcrypt**: 
  - A library for hashing passwords securely to enhance user data protection.

- **Python**: Version 3.7
  - The programming language used for implementing the service.

## 🧮Tasks to Complete

- [x] **User Model**  
  The file [user.py](user.py) includes a SQLAlchemy model named `User`, which maps to a database table designated as `users`. This model is constructed using the [mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping) method provided by SQLAlchemy. The `User` model encompasses the following attributes:

  - **`id`**: 
    - Type: Integer
    - Description: Serves as the primary key for the `users` table, uniquely identifying each user.

  - **`email`**: 
    - Type: String
    - Description: A non-nullable field that stores the user's email address, which must be unique for each user. It serves as the primary identifier for user login.

  - **`hashed_password`**: 
    - Type: String
    - Description: A non-nullable field that stores the hashed version of the user's password. This field ensures that raw passwords are never stored in the database, thereby enhancing security.

  - **`session_id`**: 
    - Type: String (nullable)
    - Description: An optional field that holds the session identifier for the user. This is useful for managing user sessions and tracking active logins.

  - **`reset_token`**: 
    - Type: String (nullable)
    - Description: An optional field used for password reset functionality. This token is generated when a user requests to reset their password and is used to verify the user's identity during the reset process.

## 🧮Additional Features to Consider

As you develop the User Authentication Service, consider implementing the following additional features:

- **User Registration**: 
  - Create an endpoint for new users to register by providing their email and password. Ensure that the email is validated and that passwords are hashed before storage.

- **User Login**: 
  - Implement a login mechanism that verifies user credentials and initiates a session.

- **Password Reset**: 
  - Provide functionality for users to reset their passwords, utilizing the `reset_token` for verification.

- **Session Management**: 
  - Develop a system to manage user sessions, allowing users to log out and ensuring that sessions time out after a period of inactivity.

- **Input Validation**: 
  - Incorporate input validation to prevent common security vulnerabilities such as SQL injection and cross-site scripting (XSS).

- **Testing**: 
  - Write unit tests to ensure the reliability of the user authentication functionalities.

## 🧮Conclusion

By completing this project, you will gain valuable experience in building a secure and efficient user authentication service. You’ll learn how to work with SQLAlchemy, enforce best coding practices, and implement essential security measures, all of which are crucial skills in modern software development.


