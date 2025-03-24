"""
Ayman Momin
UCID: 30192494
Assignment 2
CPSC 441
"""

import socket
import os

def test_proxy():
    # Test regular image request
    send_request('http://httpbin.org/image/jpeg')
    
    # Test Easter egg
    send_request('http://google.ca')

def send_request(url):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    
    request = f"GET {url} HTTP/1.1\r\nHost: {url.split('/')[2]}\r\n\r\n"
    client_socket.send(request.encode())
    
    response = b""
    while True:
        part = client_socket.recv(4096)
        if not part:
            break
        response += part
    
    print(f"Response for {url}:")
    print(response[:500].decode('latin-1', errors='ignore') + "...")
    
    client_socket.close()

if __name__ == "__main__":
    test_proxy()