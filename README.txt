Project Description
This project is a multi-threaded web server written in Python using basic socket programming.
It handles HTTP requests from a browser or client program and serves text files, HTML files, and image files.
It also supports logging, error handling, the HEAD method, and conditional requests using If-Modified-Since.


Files Required
Make sure the following files are in the same folder:
	project_web_server.py
	2322.html
	2322.txt
	project_photo.jpg

Run and Test
1.	Open terminal 
2.	Run "python project_web_server.py" in the terminal
3.	The server will start and listen on http://127.0.0.1:9999
4.	Open a browser and test with URL:
	a.	http://127.0.0.1:9999/2322.txt (show “here is the text  txt file!!!!!!!! for COMP2322 project!!!!!”)
	b.	http://127.0.0.1:9999/2322.html  (show “OK for HTML”)
	c.	http://127.0.0.1:9999/project_photo.jpg (show a picture)
	d.	http://127.0.0.1:9999/notexist.html (show “404 File Not Found”)
	e.	http://127.0.0.1:9999/secret.txt (show “403 Forbidden”)
5.	Open another terminal and use curl:
	a. HEAD request: curl.exe -I http://127.0.0.1:9999/2322.txt
	b. 404 File Not Found: curl.exe -I http://127.0.0.1:9999/notexist.html
	c. 304 Not Modified: curl.exe -I -H "If-Modified-Since: Sun, 19 Apr 2026 00:00:00 GMT" http://127.0.0.1:9999/2322.txt
	d. Connection of header:
		Keep-alive: curl.exe -I -H "Connection: keep-alive" http://127.0.0.1:9999/2322.txt
		Close: curl.exe -I -H "Connection: close" http://127.0.0.1:9999/2322.txt

Log File:
The server automatically generate a log file (server.log) in the same folder as the server program
Each request is recorded in one line, including:
	client IP address
	access time
	requested file name
	response status
The old log file will delete automatically each time when a new server starts


Features Implemented:
Multi-threaded server using Python threading
Basic socket programming
GET request for text, HTML, and image files
HEAD request
Response statuses:
	200 OK
	400 Bad Request
	403 Forbidden
	404 Not Found
	304 Not Modified
Last-Modified header
If-Modified-Since header handling
Request logging


