# Simple-Web-Framework
an educational purpose repo containing a simple project of creating the backbone of a functional web framework.

## Building a Simple Web Framework in Python: Understanding the Fundamentals.

### Introduction
In this post, we'll explore the creation of a simple web framework for building REST API applications. By examining the code I've included in my GitHub repo, we'll dive into the core concepts and functionalities of web frameworks like Flask or FastAPI. We will cover the basic components of these frameworks, including the server, request parsing, routing, and response generation. Let's get started!

1) 'Server.py' - Server:
The `Server.py` file serves as the foundation of our web framework. It sets up the HTTP server, built with the socket module, which allows for low level control and configuration of the server. The server handles incoming connections, and manages the event loop using asyncio (which serves as the base for our server's ability to support concurrency). It also includes the server shutdown mechanism.

2) 'Request_parser.py' - Parser:
The `RequestParser` module provides functionality for parsing incoming HTTP requests. It extracts relevant information such as request headers, request body, and cookies. It accomplishes this through regular expressions and JSON parsing. My implementation here is super basic, but it's good enough for this example.

3) 'Router_api.py' - Router:
The `RouterAPI` module represents the routing mechanism of our web framework. It allows developers to define routes and associate them with specific HTTP methods (GET, POST, PUT, DELETE etc.). By using decorators, developers can easily define functions to handle requests to specific routes and methods. The routes are stores as a hash-map(dictionary) for efficiency and speed.

4) 'app.py' - Endpoint Functions:
In the `app.py` file, I demonstrate how to define endpoint functions using decorators provided by the `RouterAPI`. These functions handle specific routes and methods, generating appropriate responses based on the request. In the example, we define endpoints for retrieving all movies and creating a movie.

5) Handling Requests and Generating Responses:
Within the server's event loop, incoming requests are processed in an infinite loop. The server extracts the request, passes it through the request parser, and generates a response by invoking the appropriate endpoint function defined in the `RouterAPI`. The response is then sent back to the client.

### Conclusion:
By examining this code, we've gained a foundational understanding of how web frameworks operate. We've covered key aspects such as the server setup, request parsing, routing, and generating responses. This simplified framework captures the essence of popular web frameworks like Flask or FastAPI and provides a starting point for building more complex web applications.

**Note**: This code is meant for educational purposes and may not provide the same level of functionality, scalability, and security as mature web frameworks. However, it serves as a valuable learning tool to grasp the core concepts of web development and REST APIs.
