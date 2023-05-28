import asyncio
import os
import signal
import socket
import sys


from logger import logger
from request_parser import RequestParser
from router_api import RouterAPI


class HTTPServer:
    def __init__(self, routerapi: RouterAPI, host: str = None, port: int = None) -> None:
        self.host = os.getenv('HOST', host)
        self.port = os.getenv('PORT', port)
        self.request_parser = RequestParser()
        self.routerapi = routerapi
        
        if self.host == None or self.port == None:
            raise RuntimeError("Host and port can not be None.")
        
        # Create server socket
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket option to reuse the address
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket server to address
        self.__server_socket.bind((self.host, self.port))
        # Set socket to non-blocking mode
        self.__server_socket.setblocking(False)
        # # Set socket connection timeout
        # self.__server_socket.settimeout(5)
        # Create an event loop for the server to handle connections asynchronously
        self.event_loop = asyncio.get_event_loop()
        
        # Set up signal for server shutdown
        signal.signal(signal.SIGINT, self.__server_shutdown)
        
    def __server_shutdown(self, signal, frame) -> None:
        logger.info(f'Shutdown signal received.\nShutting down...')
        self.__server_socket.close()
        sys.exit(0)
    
    async def __get_client_req(self, client_socket: socket.socket, client_address: socket.socket) -> str:
        # Receive data from client
        request_received = await self.event_loop.sock_recv(client_socket, 1024)
        decoded_req = request_received.decode("utf-8")
        logger.debug(f'Request from {client_address[0]} -\n{decoded_req}')
        return decoded_req
    
    async def __parse_req(self, c_request: str) -> dict:
        return self.request_parser.parse_request(c_request)
    
    async def __generate_response(self, c_request: str):
        parsed_req = await self.__parse_req(c_request)
        path = parsed_req.get('path')
        method = parsed_req.get('method')
        response = await self.routerapi.request_router(path, method)
        return response
    
    async def send_response(self, client_socket: socket.socket, s_response: str):    
        # Send response to client
        await self.event_loop.sock_sendall(client_socket, s_response.encode('utf-8'))
        resp_header = s_response.split('\n')[0]
        logger.debug(f"Responded with - {resp_header}")
        # Close client socket - end connection with client
        client_socket.close()
            
    async def server_setup(self) -> None:
        # Set socket to listen for new connections - argument sets the queue size for incoming connections
        self.__server_socket.listen(5)
        logger.info(f'Server is now running on http://{self.host}:{self.port}')

        while True:
            try:
                # Accept client connection
                client_socket, client_address = await self.event_loop.sock_accept(self.__server_socket)
                logger.debug(f'Received connection from {client_address[0]}:{client_address[1]}')
                # Proccess client request
                client_request = self.event_loop.create_task(self.__get_client_req(client_socket, client_address))
                await client_request
                # Generate response for client
                generate_resp = self.event_loop.create_task(self.__generate_response(client_request.result()))
                await generate_resp
                # Send response to client
                await self.event_loop.create_task(self.send_response(client_socket, generate_resp.result()))
                
            except asyncio.CancelledError:
                # Handle cancellation when shutting down the server
                break
            # except socket.timeout:
            #     break
        
    
if __name__ == "__main__":
    http_server = HTTPServer(host='localhost', port=8080)
    # Running the server with the asyncio event loop
    try:
        http_server.event_loop.run_until_complete(http_server.server_setup())
    finally:
        http_server.event_loop.close()
    