from backend_stuff.router_api import RouterAPI
from backend_stuff.server import HTTPServer

# Create a RouterAPI instance to power your app
app = RouterAPI()
# Create an http server and pass in your app, host and port
http_server = HTTPServer(app, 'localhost', 8080)

# Create your app routes
@app.get('/movies')
def get_movies():
    return '{"movies": [{"title": "Shrek1"}, {"title": "The Emporer\'s New Clothes"}]}'

@app.post('/movies')
def create_movie():
    return '{"message": "OK."}'


# Run your application using the http server event loop for async support
if __name__ == "__main__":
    try:
        http_server.event_loop.run_until_complete(http_server.server_setup())
    finally:
        http_server.event_loop.close()
        