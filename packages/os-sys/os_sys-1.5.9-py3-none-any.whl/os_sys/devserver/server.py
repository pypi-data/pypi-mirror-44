import socket
__all__ = ['run']
class Request(object):
	"A simple http request object"
	
	def __init__(self, raw_request):
		self._raw_request = raw_request
		
		self._method, self._path, self._protocol, self._headers = self.parse_request()
	
	def parse_request(self):
		"Turn basic request headers in something we can use"
		temp = [i.strip() for i in self._raw_request.splitlines()]
		
		if -1 == temp[0].find('HTTP'):
			raise InvalidRequest('Incorrect Protocol')
		
		# Figure out our request method, path, and which version of HTTP we're using
		method, path, protocol = [i.strip() for i in temp[0].split()]
		
		# Create the headers, but only if we have a GET reqeust
		headers = {}
		if 'GET' == method:
			for k, v in [i.split(':', 1) for i in temp[1:-1]]:
				headers[k.strip()] = v.strip()
		else:
			raise InvalidRequest('Only accepts GET requests')
		
		return method, path, protocol, headers
	
	def __repr__(self):
		return repr({'method': self._method, 'path': self._path, 'protocol': self._protocol, 'headers': self._headers})

def run(port=8082, **files):
    
    HOST,PORT = '127.0.0.1',port
     
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    my_socket.bind((HOST,PORT))
    my_socket.listen(1)
     
    print('Serving on port ',PORT)
     
    while True:
        connection,address = my_socket.accept()
        request = connection.recv(1024).decode('utf-8')
        string_list = request.split(' ')     # Split request from spaces
     
        method = string_list[0]
        requesting_file = string_list[1]
     
        print('Client request ',requesting_file)
     
        myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/')
        if(myfile == ''):
            myfile = 'index.html'    # Load index file as default
     
        try:
            file = open(myfile,'rb') # open file , r => read , b => byte format
            response = file.read()
            file.close()
     
            header = 'HTTP/1.1 200 OK\n'
     
            if(myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(myfile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
     
            header += 'Content-Type: '+str(mimetype)+'\n\n'
     
        except Exception as e:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
     
        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)
def run_(port=8082, **files):
    import pickle
    HOST,PORT = '127.0.0.1',port
     
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    my_socket.bind((HOST,PORT))
    my_socket.listen(1)
     
    print('Serving on port ',PORT)
     
    while True:
        class r():
            def __init__(self):
                self.GET = {}
                self.POST = {}
        req = r()
        connection,address = my_socket.accept()
        _request = connection.recv(4096)
        request = _request.decode('utf-8')
        start = request
        data = start.split('\n')
        print(type(data))
        string_list = request.split(' ')     # Split request from spaces
        try:
            requesting_file = string_list[1]
        except:
            continue
        print(connection)


        print(req)
        print('Client request ',requesting_file)
        try:
            _POST = data[len(data) - 1]
            POST = _POST.split('\\n')[-1]
        except Exception as ex:
            print(ex)
            print(type(data))
            POST = ''
        else:
            if POST != []:
                LIST = POST.split('&')
                for item in LIST:
                    if item != '':
                        print(item)
                        key, data = item.split('=')
                        req.POST[key] = data
            print(req.POST)
        myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
        if '?' in requesting_file:
            get = requesting_file.split('?')[1:]
            get = ''.join(get)
            get_list = get.split('&')
            for get_item in get_list:
                if get_item != '' and '=' in get_item:
                    get_key, get_data = get_item.split('=')
                    req.GET[get_key] = get_data
            print(req.GET)
        myfile = myfile.lstrip('/')
        print(string_list)
        if(myfile == ''):
            myfile = 'index'    # Load index file as default
        ex = None 
        try:
            file = files[myfile] # open file , r => read , b => byte format
            response = file(req)
            response = response.encode('utf-8')
             
            header = 'HTTP/1.1 200 OK\n'
     
            if(myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(myfile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
     
            header += 'Content-Type: '+str(mimetype)+'\n\n'
            
        except Exception as e:
            if e == KeyboardInterrupt:
                raise SystemExit
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
     
        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)
        connection.close()
if __name__ == '__main__':
    run()
    connection.close()
