################################################
## CONFIG FILE
from pysas_conf import *
################################################
import sys
from sys import stdout
import os
import requests
import random
import time
import uuid
import subprocess
import psutil
import shutil
start_time = time.time()

def Runtime(seconds,finished=False):
	seconds = int(seconds)
	status = 'has been running for' if not finished else 'finished in'

	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)

	periods = [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
	time_string = ', '.join('{} {}'.format(value, name)
							for name, value in periods
							if value)

	return time_string

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename) as in_file, open(filename, 'r+') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()

def searchinfile(filename, string):
	if string in open(filename, 'a+').read():
		return True
print("\nPython Simple Auto Surfer: by abdelhafidh.com\n");
if len(sys.argv) > 1:
	if sys.argv[1] == "native":
		browser="native"
	elif sys.argv[1] == "firefox":
		browser="Firefox"
	elif sys.argv[1] == "chrome":
		browser="Chrome"
	else:
		sys.exit("[!] select browser\n--> for firefox: python "+os.path.basename(__file__)+" firefox\n--> for chrome: python "+os.path.basename(__file__)+" chrome\n--> for native: python "+os.path.basename(__file__)+" native")
else:
		sys.exit("[!] select browser\n--> for firefox: python "+os.path.basename(__file__)+" firefox\n--> for chrome: python "+os.path.basename(__file__)+" chrome\n--> for native: python "+os.path.basename(__file__)+" native")
c=1
batch = int(raw_input("Loop for ? times: "))
if batch<=0:
	sys.exit("\n[*] Nothing to do")
print("============================SETTINGS============================")
print("Browser: "+browser)
print("Open x site at the same time: "+(str(open_x_site_at_the_same_time) if open_x_site_at_the_same_time!=0 else "none"))
print("Open sites each ? seconds: "+str(open_sites_each_x_seconds))
print("Wait ? seconds before closing x sites: "+(str(wait_y_seconds_before_closing_x_sites) if wait_y_seconds_before_closing_x_sites!=0 else "no"))
print("Loop ? times: "+str(batch))
print("Init time: "+str(init_time))
print("================================================================")
if os.path.isfile(urls_tmp) and batch==1:
	print("[i] Warning an existing tmp file has been found. Presume Multiprocessing")
elif batch>1:
	if os.path.isfile(urls_tmp):
		print("[i] Warning an existing tmp file has been found.")
		check = raw_input("[?] Remove it and start over? (y/n): ")
		while(check!="y" and check!="n"):
			check = raw_input("[?] Remove it and start over? (y/n): ")
		if check == "y": os.remove(urls_tmp)
		else: sys.exit("\n[*] Operation Cancelled By User")
	if os.path.exists(tmp_dir):
		shutil.rmtree(tmp_dir)
	print("[+] New Process")
	print("[i] Warning Multiprocessing is not supported while loops>1")
else:
	if os.path.exists(tmp_dir):
		shutil.rmtree(tmp_dir)
	print("[+] New Process")
if not os.path.exists(tmp_dir):
	os.makedirs(tmp_dir)
FNULL = open(os.devnull, 'w')
remove_empty_lines(urls)
num_lines = sum(1 for line in open(urls))
needed=open_x_site_at_the_same_time
if needed == 0:
	sys.exit("\n[*] Nothing to do")
try:
	while True and c<=batch:
		done=0
		have=0
		togo=[]
		filecount = uuid.uuid4().hex
		k=open(tmp_dir+filecount, 'a+')
		k.close()
		while have<needed:
			f=open(urls,"r")
			url=(random_line(f)).rstrip('/\r\n')+"/"
			f.close()
			b=0;
			while searchinfile(urls_tmp, url) is True:
				f=open(urls,"r")
				url=(random_line(f)).rstrip('/\r\n')+"/"
				searchinfile(urls_tmp, url)
				b+=1
				if b>100:
					done=1
					break
			if done == 1: break
			with open(urls_tmp, "a+") as tmpfile:
				tmpfile.write(url+"\n")
			b=0;
			t=len([name for name in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, name))])

			if browser == "native":
				open_x_site_at_the_same_time=1
				headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
				}
				response = requests.get(url, headers=headers, verify=True)
			else:
				if browser == "Firefox":
					bin=firefox_bin
					params=firefox_params
				elif browser == "Chrome":
					bin=chrome_bin
					params=chrome_params

				if have==0 and open_x_site_at_the_same_time !=0 :
					if wait_y_seconds_before_closing_x_sites !=0 or c == 0:
						#os.system(path+" &> /dev/null &")
						process = subprocess.Popen([bin, params, "--window-size=50,100"], shell=False, stdin=FNULL, stdout=FNULL, stderr=FNULL)
						time.sleep(init_time)

				togo.append(url)
			stdout.write("[+] Adding to queue: "+url+"                                                     \n")
			stdout.write("[i] Surfing now: "+str(t*open_x_site_at_the_same_time)+"\tBatch: "+str(c)+"/"+str(batch)+"\tElapsed Time: "+Runtime(time.time() - start_time)+"\r")
			stdout.flush()
			have+=1
		for (go) in togo:
			subprocess.Popen([bin, params, "--window-size=50,100", go], shell=False, stdin=FNULL, stdout=FNULL, stderr=FNULL)

		time.sleep(open_sites_each_x_seconds)
		if wait_y_seconds_before_closing_x_sites !=0:
			if browser != "native": time.sleep(wait_y_seconds_before_closing_x_sites)
			if os.path.isfile(tmp_dir+filecount):
				os.remove(tmp_dir+filecount)
			if browser !="native":
				try:
					kill(process.pid)
				except:
					#print("\n[!] Failed to kill process")
					pass
		if done == 1:
			if batch>1: os.remove(urls_tmp)
			c+=1
	sys.exit("\n[*] We are done.") if batch>1 else sys.exit("\n[*] We are done. Please remove the "+urls_tmp+" file to start again")

except KeyboardInterrupt:
	print("")
	if os.path.isfile(tmp_dir+filecount):
		os.remove(tmp_dir+filecount)
	exit(0)
