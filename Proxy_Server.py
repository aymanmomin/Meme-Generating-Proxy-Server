"""
Ayman Momin
UCID: 30192494
Assignment 2
CPSC 441
"""

import socket
import threading
import random
import os
import base64
from mimetypes import guess_type
from urllib.parse import urlparse

# Configuration
HOST = '127.0.0.1' # Localhost
PORT = 8080 # Port to listen on
MEME_DIR = 'memes' # Directory containing meme images
MEMES = [] # List for meme file paths
EASTER_EGG_HOST = 'google.ca'  # Hostname to trigger Easter egg

# Meme Management
def load_memes():
    """Load meme images from the memes directory into MEMES list"""
    global MEMES
    try:
        # Get all image files in meme directory
        MEMES = [os.path.join(MEME_DIR, f) for f in os.listdir(MEME_DIR)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        # Warn if no memes found
        if not MEMES:
            print("Warning: No meme images found in memes directory")
    except Exception as e:
        print(f"Error loading memes: {str(e)}")
        
# Easter Egg Handling
def handle_easter_egg(client_socket):
    """Handle special case for google.ca requests"""
    try:
        if not MEMES:
            return False
        
        # Select random meme
        meme_path = random.choice(MEMES)
        
        # Handle corrupted meme files
        try:
            with open(meme_path, 'rb') as f:
                meme_data = f.read()
        except IOError as e:
            print(f"Corrupted meme: {meme_path}")
            return False
        
        # Simple HTML with centered image
        html_content = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n
            <html><body>
            <div style="text-align:center; margin:20px;">
                <img src="data:image/jpeg;base64,{base64.b64encode(meme_data).decode('latin-1')}" 
                style="max-width:100%; height:75%;">
                <h1>MEME SURPRISE!</h1>
            </div>
            </body></html>\r\n\r\n"""
        
        # Send HTML response
        client_socket.send(html_content.encode('latin-1'))
        return True
    
    except Exception as e:
        print(f"Easter egg error: {str(e)}")
        return False
    
# Request Handling
def handle_client(client_socket):
    """Main client connection handler"""
    try:
        # Receive request
        request = client_socket.recv(4096)
        if not request:
            return

        # Block HTTPS CONNECT requests
        if request.startswith(b'CONNECT'):
            client_socket.send(b'HTTP/1.1 501 Not Implemented\r\n\r\n')
            client_socket.close()
            return

        # Parse request
        first_line = request.split(b'\r\n')[0]
        url = first_line.split(b' ')[1]
        parsed_url = urlparse(url.decode('utf-8'))
        
        # Check for Easter egg
        if parsed_url.hostname == EASTER_EGG_HOST:
            if handle_easter_egg(client_socket):
                return
            else:
                client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
                return

        # Forward request to target server
        target_host = parsed_url.hostname
        target_port = parsed_url.port or 80
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_sock:
            # Connect to target server and forward request
            target_sock.connect((target_host, target_port))
            target_sock.send(request)
            
            # Receive full response
            response = b''
            while True:
                data = target_sock.recv(4096)
                if not data:
                    break
                response += data

        # Process response - split headers and body
        header_end = response.find(b'\r\n\r\n')
        if header_end == -1:
            client_socket.send(response)
            return

        headers, body = response[:header_end], response[header_end+4:]
        
        # Replace images 50% of the time
        if b'Content-Type: image/' in headers and MEMES:
            if random.random() < 0.5:
                # Select random meme
                meme_path = random.choice(MEMES)
                with open(meme_path, 'rb') as f:
                    meme_data = f.read()
                
                # Update headers
                content_type = guess_type(meme_path)[0] or 'image/jpeg'
                headers = (
                    headers.split(b'\r\nContent-Type: ')[0] +
                    f"\r\nContent-Type: {content_type}".encode() +
                    f"\r\nContent-Length: {len(meme_data)}".encode()
                )
                body = meme_data

        # Send modified response to client
        client_socket.send(headers + b'\r\n\r\n' + body)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

# Server Initialization
def start_proxy():
    """Start and run the proxy server"""
    load_memes()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Meme Proxy running on {HOST}:{PORT}")

    try:
        # Main server loop
        while True:
            client_sock, addr = server_socket.accept()
            # Handle client in separate thread
            thread = threading.Thread(target=handle_client, args=(client_sock,))
            thread.start()
    except KeyboardInterrupt:
        server_socket.close()

if __name__ == "__main__":
    start_proxy()
