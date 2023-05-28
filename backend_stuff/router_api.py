from typing import Callable
from enum import Enum

# Supported status codes and methods
class StatusCode(Enum):
    GET = "200 OK"
    POST = "201 CREATED"
    PUT = "200 OK"
    DELETE = "204 DELETED"
    METHOD_NOT_ALLOWED = "405 METHOD NOT ALLOWED"
    NOT_FOUND = "404 NOT FOUND"
    

class RouterAPI:
    def __init__(self):
        self.routes = {}

    def route(self, path: str, method: str) -> Callable:
        def decorator(func: Callable):
            if path not in self.routes:
                self.routes[path] = {}
            self.routes[path][method] =  func
            return func
        return decorator

    def get(self, path: str):
        def decorator(func: Callable) -> Callable:
            if path not in self.routes:
                self.routes[path] = {}
            self.routes[path]["GET"] = func
            return func
        return decorator

    def post(self, path: str):
        def decorator(func: Callable) -> Callable:
            if path not in self.routes:
                self.routes[path] = {}
            self.routes[path]["POST"] = func
            return func
        return decorator

    def put(self, path: str):
        def decorator(func: Callable) -> Callable:
            if path not in self.routes:
                self.routes[path] = {}    
            self.routes[path]["PUT"] = func
            return func
        return decorator

    def delete(self, path: str) -> Callable:
        def decorator(func: Callable):
            if path not in self.routes:
                self.routes[path] = {}    
            self.routes[path]["DELETE"] = func
            return func
        return decorator
    
    async def request_router(self, path: str, method: str) -> dict:
        if path in self.routes and method in self.routes[path]:
            # Call and execute the function associated with the route method
            response = self.routes[path][method]()
            # set status code according to the request method
            if method == "GET":
                status = StatusCode.GET.value
            elif method == "POST":
                status = StatusCode.POST.value
            elif method == "PUT":
                status = StatusCode.PUT.value
            elif method == "DELETE":
                status = StatusCode.DELETE.value
            else:
                return f"HTTP/1.1 {StatusCode.METHOD_NOT_ALLOWED.value}\nContent-Type: text/html\n\n"
            
            return f"HTTP/1.1 {status}\nContent-Type: application/json\n\n{response}"
        
        elif path in self.routes:
            return f"HTTP/1.1 {StatusCode.METHOD_NOT_ALLOWED.value}\nContent-Type: text/html\n\n"
        return f"HTTP/1.1 {StatusCode.NOT_FOUND.value}\nContent-Type: text/html\n\n"
    
    