import os

IP='192.168.1.1'
PORT=80
script='from boofuzz import *\r\n'

name_list = []

def add_script(lines):
	global script
	for line in lines:
		script += line 


def function_name(file_dir):
	global script
	functions = os.listdir(file_dir)
	for  function in functions:		
		function = 'function/' + function
		f=open(function,'r')
		lines=f.readlines() 
		#print(lines)
		add_script(lines)
		script += '\r\n' 

def do_data(line):
	global script
	line = line[0:-1]
	t=line.split('&')
	for i in range(len(t)):
		m,n=t[i].split('=')
		script+='\t\ts_static("%s=")\r\n' %(m)
		script+='\t\ts_string("%s", max_len=1024)\r\n' %(n)
		if i!=len(t)-1:
			script+='\t\ts_static("&")\r\n'
 
def do_body(line):
	global script
	t=line.split(' ')
	print(t)
	if t[0] != "GET":	
		for i in range(len(t)):
			if '\n' in t[i]:
				tt=t[i].split('\n')
				if i!=0:
					script+='\ts_delim(" ")\r\n'
				script+='\ts_static("%s")\r\n' %(tt[0])
				script+='\ts_static("\\r\\n")\r\n'
			else:
				if i!=0:
					script+='\ts_delim(" ")\r\n'
				script+='\ts_static("%s")\r\n' %(t[i])
	else:
		print("123")


 

function_name("function")
print(script)


script+='def main():\r\n'
script+='\ttar=Target(connection=TCPSocketConnection("%s", %d))\r\n' %(IP,PORT)
script+='\tsession = Session(target=tar,receive_data_after_each_request=True,)\r\n'



f = open("1.txt", 'r')
Fscript=open('FuzzScript.py','w')
lines=f.readlines()
if_data = False
for i in range(len(lines)):
	line = lines[i]
	if line[0:3] == "-*-":
		name = line[3:-1]
		print(name)
		script+= '\ts_initialize(name="%s")\r\n' %(name)
		name_list.append(name)


	elif line == '\n':
		next_line = lines[i+1]
		if next_line[0:3] != "-*-" :
			if_data = True

	else:
		print(i)
		if if_data:
			script+= '\twith s_block("data"):\r\n'
			do_data(next_line)
			print("data")
			if_data = False
		else:

			do_body(line)
                        
 
# while line:
# 	if line=='\r\n':
# 		line=f.readline()
# 		script+='\ts_static("\\r\\n", "Request-CRLF")\r\n'
# 		script+='\twith s_block("Body-Content"):\r\n'
# 		do_body(line)
# 		script+='\tsession.connect(s_get("Post"))\r\n'
# 		script+='\tsession.fuzz()\r\n'
# 		script+='if __name__ == "__main__":\r\n'
# 		script+='\tmain()\r\n'
# 		f.seek(0)
# 		all_file=f.read()
# 		script+='\r\n\'\'\'\r\n'+all_file+'\r\n\'\'\''
		
# 	else:
		
	# 	t=line.split(' ')
	# 	for i in range(len(t)):
				
	# line=f.readline()
	# script+='\r\n' 
print(script)
Fscript.write(script)
Fscript.close()
f.close()
print(name_list)
