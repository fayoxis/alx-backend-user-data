# 🧮Session Authentication

This project focuses on implementing session authentication, which is a widely-used method of authenticating users in web applications. Session authentication involves creating a temporary session upon successful user authentication and storing user-related data on the server-side. This session is then used to identify the user for subsequent requests, allowing them to access authorized resources without the need to re-authenticate for each request.

## 🧮Tasks

### 🧮1. User Endpoint and Session Authentication

In this task, you'll create a new endpoint `GET /users/me` to retrieve the authenticated user object. Additionally, you'll implement session authentication to secure the existing user endpoints.

#### 🧮Steps:

1. Copy the `models` and `api` folders from the previous project [0x06. Basic authentication](../0x01-Basic_authentication/).
2. Ensure that all mandatory tasks from the previous project are completed successfully, as this project will build upon that foundation.
3. Update the `@app.before_request` decorator in [api/v1/app.py](api/v1/app.py):
   - Assign the result of `auth.current_user(request)` to `request.current_user`. This will allow access to the authenticated user object throughout the request lifecycle.
4. Create a new view function `get_current_user` in [api/v1/views/users.py](api/v1/views/users.py):
   - This function should return the authenticated user object.
   - Decorate the function with `@user.route('/me', methods=['GET'], strict_slashes=False)`.
5. Update the existing user endpoints in [api/v1/views/users.py](api/v1/views/users.py):
   - Add a new decorator `@user_by_id` to each endpoint that requires user authentication.
   - This decorator should retrieve the authenticated user object from `request.current_user` and pass it to the respective view function as an argument.
6. Implement session authentication in [auth/auth.py](auth/auth.py):
   - Create a new method `current_user(request)` that retrieves the user object from the session.
   - If the user session is not found or expired, return `None`.
   - Otherwise, return the corresponding user object.
7. Test your implementation by sending authenticated requests to the user endpoints and verifying the responses.

This task will set the foundation for session authentication in your application. By implementing the `GET /users/me` endpoint and securing the existing user endpoints with session authentication, you'll ensure that only authenticated users can access and modify user data.

### 🧮Additional Tasks

- Implement session creation and destruction mechanisms.
- Handle session expiration and renewal.
- Enhance session security by adding measures like CSRF protection and secure cookie settings.
- Implement session management best practices, such as session fixation protection and session expiration for idle sessions.

## 🧮Resources

- [Session Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Session_cookies)
- [Flask Session](https://flask.palletsprojects.com/en/2.2.x/quickstart/#sessions)
- [Flask-Session](https://flask-session.readthedocs.io/en/latest/)
- [Session Fixation Attack](https://www.owasp.org/index.php/Session_Fixation)

By completing this project, you'll gain a deeper understanding of session authentication and its implementation in web applications. Additionally, you'll learn best practices for securing user sessions and protecting against common session-related vulnerabilities.
