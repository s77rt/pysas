#!/usr/bin/env python
# coding: utf-8

################################################
## CONFIG FILE
import pysas_conf
################################################
import sys
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
		if random.randrange(num + 2):
			continue
		line = aline
	return line

def remove_empty_lines(filename):
	"""Overwrite the file, removing empty lines and lines that contain only whitespace."""
	with open(filename) as in_file, open(filename, 'r+') as out_file:
		out_file.writelines(line for line in in_file if line.strip())
		out_file.truncate()

def searchinfile(filename, string):
	with open(filename) as f:
		datafile = f.readlines()
		for line in datafile:
			if string == line.strip():
				return True

def main():
	print("Python Simple Auto Surfer: by abdelhafidh.com\n");
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
	batch = int(input("Loop for ? times: "))
	if batch<=0:
		sys.exit("\n[*] Nothing to do")
	print("============================SETTINGS============================")
	print("Browser: "+browser)
	print("Open x site at the same time: "+(str(pysas_conf.open_x_site_at_the_same_time) if pysas_conf.open_x_site_at_the_same_time!=0 else "none"))
	print("Open sites each ? seconds: "+str(pysas_conf.open_sites_each_x_seconds))
	print("Wait ? seconds before closing x sites: "+(str(pysas_conf.wait_y_seconds_before_closing_x_sites) if pysas_conf.wait_y_seconds_before_closing_x_sites!=0 else "no"))
	print("Loop ? times: "+str(batch))
	print("Init time: "+str(pysas_conf.init_time))
	print("================================================================")
	if batch == 1:
		if os.path.isfile(pysas_conf.urls_tmp):
			print("[i] Warning an existing tmp file ({}) has been found.\nPresume Multiprocessing...".format(pysas_conf.urls_tmp))
		else:
			u = open(pysas_conf.urls_tmp, "w")
			u.close()
			if os.path.exists(pysas_conf.tmp_dir):
				shutil.rmtree(pysas_conf.tmp_dir)
	else:
		print("[i] Warning Multiprocessing is not supported while loops>1")
		if os.path.isfile(pysas_conf.urls_tmp):
			print("[i] Warning an existing tmp file has been found.")
			check = input("[?] Remove it and start over? (y/n): ")
			while (check!="y" and check!="n"):
				check = input("[?] Remove it and start over? (y/n): ")
			if check == "y":
				os.remove(pysas_conf.urls_tmp)
			else:
				sys.exit("\n[*] Operation Cancelled By User")
		if os.path.exists(pysas_conf.tmp_dir):
			shutil.rmtree(pysas_conf.tmp_dir)
	if not os.path.exists(pysas_conf.tmp_dir):
		os.makedirs(pysas_conf.tmp_dir)
	print("[+] Starting Process")
	FNULL = open(os.devnull, 'w')
	remove_empty_lines(pysas_conf.urls)
	num_lines = sum(1 for line in open(pysas_conf.urls))
	needed=pysas_conf.open_x_site_at_the_same_time
	if needed == 0:
		sys.exit("\n[*] Nothing to do")
	try:
		while True and c<=batch:
			done=0
			have=0
			togo=[]
			filecount = uuid.uuid4().hex
			k=open(os.path.join(pysas_conf.tmp_dir, filecount), 'a+')
			k.close()
			while have<needed:
				url = None
				b=0;
				while not url or searchinfile(pysas_conf.urls_tmp, url) is True:
					f=open(pysas_conf.urls,"r")
					url=(random_line(f)).rstrip('/\r\n')+"/"
					f.close()
					b+=1
					if b>100:
						done=1
						break
				if done == 1: break
				with open(pysas_conf.urls_tmp, "a+") as tmpfile:
					tmpfile.write(url+"\n")
				b=0;
				t=len([name for name in os.listdir(pysas_conf.tmp_dir) if os.path.isfile(os.path.join(pysas_conf.tmp_dir, name))])

				if browser == "native":
					pysas_conf.open_x_site_at_the_same_time=1
					headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
					}
					response = requests.get(url, headers=headers, verify=True)
				else:
					if browser == "Firefox":
						bin=pysas_conf.firefox_bin
						params=pysas_conf.firefox_params
					elif browser == "Chrome":
						bin=pysas_conf.chrome_bin
						params=pysas_conf.chrome_params

					if have==0 and pysas_conf.open_x_site_at_the_same_time !=0 :
						if pysas_conf.wait_y_seconds_before_closing_x_sites !=0 or c == 0:
							#os.system(path+" &> /dev/null &")
							process = subprocess.Popen([bin, params, "--window-size=50,100"], shell=False, stdin=FNULL, stdout=FNULL, stderr=FNULL)
							time.sleep(pysas_conf.init_time)

					togo.append(url)
				print("[+] Adding to queue: "+url+"                      ")
				print("[i] Surfing now: {}\tBatch: {}/{}\tElapsed Time: {}\r".format(
					str(t*pysas_conf.open_x_site_at_the_same_time),
					str(c), str(batch),
					str(Runtime(time.time() - start_time)),
				), end="")
				have+=1
			for (go) in togo:
				subprocess.Popen([bin, params, "--window-size=50,100", go], shell=False, stdin=FNULL, stdout=FNULL, stderr=FNULL)

			time.sleep(pysas_conf.open_sites_each_x_seconds)
			if pysas_conf.wait_y_seconds_before_closing_x_sites !=0:
				if browser != "native": time.sleep(pysas_conf.wait_y_seconds_before_closing_x_sites)
				if os.path.isfile(pysas_conf.tmp_dir+filecount):
					os.remove(pysas_conf.tmp_dir+filecount)
				if browser !="native":
					try:
						kill(process.pid)
					except:
						#print("\n[!] Failed to kill process")
						pass
			if done == 1:
				if batch>1: os.remove(pysas_conf.urls_tmp)
				c+=1
		sys.exit("\n[*] We are done.") if batch>1 else sys.exit("\n[*] We are done. Please remove the "+pysas_conf.urls_tmp+" file to start again")

	except KeyboardInterrupt:
		print("")
		if os.path.isfile(pysas_conf.tmp_dir+filecount):
			os.remove(pysas_conf.tmp_dir+filecount)
		exit(0)

if __name__ == '__main__':
	main()