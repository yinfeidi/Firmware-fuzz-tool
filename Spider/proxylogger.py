import mitmproxy

n = 1

def real_path(path):
  print(path)
  if path == "/":
    return False
  elif path[-3:] == "php" or path[-3:] == "cgi":
    return True
  elif path[-2:] == "js" or path[-3:] == "gif" or path[-3:] == "css":
    return False
  return True


class ProxyLogger:

  def __init__(self,request_url):
    self.request_url = request_url

  def request(self,flow):
    global n
    f = open("PROXY_MODE_FILE", 'r')
    mode = f.readline()
    #Creating template request
    print(mode)
    if mode != '0':
      print ('REQUEST CAPTURE MODE')
      headers = flow.request.headers
      request = flow.request.get_text(strict=True)
      if real_path(flow.request.path):
        string = "-*-" + str(n) + "\n"
        n = n + 1
        #print()
        # if flow.request.method == 'GET' and \
        #     '?' not in flow.request.path:
        #   return
        string += flow.request.method + ' '
        string += flow.request.path + ' '
        string += flow.request.http_version + '\n'
        print(string)
        for k,v in headers.items():
          #print(k,v)
          temp = '%s %s\n'%(k,v)
          string = string + temp
        string = string + '\n'
        with open("REQUEST_FILE"+mode, 'a') as f:
          f.write(string)
          print(request)
          if len(request) > 0:
            f.write(request + '\n')
        f.close()

  # def response(self,flow):
  #   f = open("PROXY_MODE_FILE", 'r')
  #   mode = f.readline()
  #   #Logging the response status code  
    
  #   self.forced_browsing_mode(flow)

  # def normal_log_mode(self,flow):
  #   status_code = str(flow.response.status_code)[0] #checking first digit of the error code
  #   # if status_code == '4' or status_code == '5': #4xx or 5xx error code received
  #   #   fp1 = open(ERROR_FILE, 'a+')
  #   #   fp1.write(self.request_url + ' ' + str(flow.response.status_code) + '\n')
  #   #   fp1.close()
  
  # def forced_browsing_mode(self,flow):
  #   status_code = str(flow.response.status_code)
  #   if status_code == '200':
  #     print('DISCLOSURE DETECTED')

def start():
  return ProxyLogger('placeholder') 
