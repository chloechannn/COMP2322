import socket
import datetime
import threading
import os
import email.utils

if os.path.exists("server.log"):
    os.remove("server.log") 

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

# log
def log_request(client_addr, filename, status):
    ip = client_addr[0]
    now_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    try:

    #     if not os.path.exists("server.log"):
    #         mode = "w"
    #     else:
    #         mode = "a"

        with open("server.log", "a", encoding="utf-8") as f:
            f.write(f"{ip} | {now_time} | {filename} | {status} \n")
        print(f"Logged: {ip} | {now_time} | {filename} | {status}")
    except Exception as e:
        print ("Log error: ", e) # if log fails, dun crush server
#stage 1
'''# Handle the HTTP request
def handle_request(request):
    # Just print the request (this is what Stage 1 asks)
    print('\n--- HTTP REQUEST RECEIVED ---')
    print(request)
    print('--- END OF REQUEST ---\n')
    
    # For now, send a simple reply so browser doesn't freeze
    response = 'HTTP/1.1 200 OK\n\nHello from Stage 1 - Request received!'
    return response
'''
# stage 2 http txt image 403
# Handle HTTP request - Stage 3 (fixed version)
def handle_request(request, client_addr):
    headers = request.split('\n')
    fields = headers[0].split()
    request_type = fields[0]  
    filename = fields[1]

    if request_type == 'GET' or request_type == 'HEAD':
        # Security check FIRST
        if '..' in filename or filename.startswith('/..') or filename.startswith('../') or filename.startswith('/secret'):
            status = '403 Forbidden'
            log_request(client_addr, filename, status )
            return 'HTTP/1.1 403 Forbidden\r\n\r\n403 Forbidden', status

        # ←←← PASTE THE 304 BLOCK HERE
        if request_type in ['GET', 'HEAD']:
            if_mod = None
            for line in headers:
                if line.lower().startswith('if-modified-since:'):
                    if_mod = line.split(':',1)[1].strip()
                    break
            if if_mod:
                try:
                    file_path = filename.lstrip('/')
                    last_mod_time = os.path.getmtime(file_path)
                    last_mod_str = email.utils.formatdate(last_mod_time, usegmt=True)
                    
                    if email.utils.parsedate_to_datetime(if_mod) >= email.utils.parsedate_to_datetime(last_mod_str):
                        status = "304 Not Modified"
                        log_request(client_addr, filename, status)
                        return f'HTTP/1.1 304 Not Modified\r\nLast-Modified: {last_mod_str}\r\nConnection: close\r\n\r\n', status
                except:
                    pass

        # Default file
        if filename == '/':
            filename = '/2322.html'

        # Choose content type and mode
        if filename.endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
            mode = 'rb'
        elif filename.endswith('.html'):
            content_type = 'text/html'
            mode = 'r'
        elif filename.endswith('.txt'):
            content_type = 'text/plain'
            mode = 'r'
        else:
            content_type = 'application/octet-stream'
            mode = 'rb'

        try:
            fin = open(filename.lstrip('/'), mode)
            content = fin.read()
            fin.close()

            # Build header
            status = "200 OK"
            last_modified = email.utils.formatdate(os.path.getmtime(filename.lstrip('/')), usegmt=True)
            
            connect_header = "close"
            for line in headers:
                if line.lower().startswith('connection:'):
                    connect_value = line.split(':',1)[1].strip().lower()
                    if connect_value == "keep-alive":
                        connect_header = "keep-alive"
                    break
            header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nLast-Modified: {last_modified}\r\nConnection: {connect_header}\r\n\r\n'
            
            if request_type == 'HEAD':
                response = header # only shows header no bodyyy
            elif mode == 'r':
                # For text files (html, txt)
                response = header + content
            else:
                # For images (jpg)
                response = header.encode() + content

        except FileNotFoundError:
            status = "404 Not Found"
            response = 'HTTP/1.1 404 Not Found\r\n\r\nFile Not Found'
            log_request(client_addr, filename, status)
            return response, status

        log_request(client_addr, filename, status)
        return response, status

    else:
        status = "400 Bad Request"
        response = 'HTTP/1.1 400 Bad Request\r\n\r\nRequest Not Supported'
        log_request(client_addr, filename, status)
        return response, status

# for multi-threading
'''
def work_client(client_connection, client_addr):
    try:
        request = client_connection.recv(1024).decode()
        response, status = handle_request(request, client_addr)

        if isinstance(response, str):
            client_connection.sendall(response.encode())
        else: 
            client_connection.sendall(response)
        # if "close" in response.lower():
        #     client_connection.close()
        
    except:
        pass
    finally:
        try:
            client_connection.close()
        except:
            pass
'''
def work_client(client_connection, client_addr):
    try:
        request = client_connection.recv(1024).decode()
        response, status = handle_request(request, client_addr)

        if isinstance(response, str):
            client_connection.sendall(response.encode())
        else:
            client_connection.sendall(response)
    except:
        pass
    finally:
        try:
            client_connection.close()
        except:
            pass
'''single thread
while True:
    client_connection, client_addr = server_socket.accept()
    print('New connection from ', client_addr)
    request = client_connection.recv(1024).decode()
    response, status = handle_request(request, client_addr)

    if isinstance(response, str):
        client_connection.sendall(response.encode())
    else:
        client_connection.sendall(response)
    
    client_connection.close()
    '''

    #start a new thread

while True:
    client_connection, client_addr = server_socket.accept()
    print('New connection from ', client_addr)
    
    thread = threading.Thread(target=work_client, args=(client_connection, client_addr))
    thread.start()

