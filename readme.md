#  Meme-Generating Proxy Server
## About
This application is a proxy server that intercepts HTTP traffic and injects humor into web browsing:
1. **Image Replacement**: Replaces 50% of images on webpages with memes from a predefined folder.
2. **Easter Egg**: Returns a custom meme page when accessing `http://google.ca`.
3. **HTTP Handling**: Manages multiple client connections and gracefully ignores HTTPS requests.


## Features  
- **Proxy Server**:  
  - TCP socket-based proxy with multithreaded client handling  
  - Image interception and replacement logic (JPEG/PNG/GIF)  
  - Custom Easter egg response for specific URLs  
  - Error handling for invalid requests and unsupported protocols  
- **Test Client**:  
  - Basic HTTP request testing  
  - Validation of Easter egg functionality  

## Installation  
1. **Prerequisites**:  
   - Python 3.6+  
   - Required packages:  
     ```bash
     pip install Pillow
     ```

2. **Setup**:  
   - Create a `memes` folder with 15+ images named `meme1.jpg`, `meme2.jpg`, etc.  
   - Files:  
     - `Proxy_Server.py`: Core proxy server  
     - `Proxy_Client.py`: Test client  
     - `memes/`: Folder containing meme images  

## Usage  
1. **Start the Proxy Server**:  
   ```bash
   python Proxy_Server.py
    ```
   - The server runs on `127.0.0.1:8080`.
  
2. **Configure Browser (Firefox)**:
    ``` bash
    python client.py
    ```
    - Go to about:preferences#general > Network Settings
    - Manual proxy: `127.0.0.1`, Port `8080`
    - **Uncheck** "Use this proxy for all protocols"
3. **Test Functionality**
    - **Image Replacement**:
      - Visit `http://httpbin.org/image/jpeg` 
      - 50% chance of meme replacement
    - **Easter Egg**
      - Visit `http://google.ca` (not HTTPS) for surprise meme page


## Outputs
- Original: http://httpbin.org/image/jpeg → Displays default/test image
- Through Proxy: 50% chance of showing meme instead
- http://google.ca → Shows centered meme with "MEME SURPRISE!" header

## Technical Details
- Image Handling:
  - Uses `mimetypes` for content-type detection
  - Base64 encoding for inline image embedding
- Protocols:
  - Explicitly blocks HTTPS CONNECT requests
  - Only processes HTTP traffic

## Disclaimer
The proxy only works for HTTP websites. HTTPS sites will either be blocked or bypass the proxy depending on browser configuration.

## Extra Credit (Optional)
Basic Encryption: Implemented basic encryption for data transmitted between the server and client using caesar cipher.

## Referred Links
- HTTP Proxy Fundamentals: https://developer.mozilla.org/en-US/docs/Web/HTTP/Proxy_servers_and_tunneling
- Python Socket Programming: https://docs.python.org/3/library/socket.html 
- Base64 Encoding: https://en.wikipedia.org/wiki/Base64