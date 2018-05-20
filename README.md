# pysas
Python Simple Auto Surfer

## Features
- Supports native browser(simple get requests)
- Supports Mozilla Firefox
- Supports Google Chrome
- ..(read below)

## Requirements
- Python
- psutil
- requests (only for native browser)

## Configuration
##### input/output settings
```
urls="urls.txt"
urls_tmp="urls_tmp.txt"
tmp_dir="tmp/"
```
##### browser settings
```
firefox_bin="/usr/bin/firefox"
firefox_params="--window-size=50,100"

chrome_bin="/opt/google/chrome/google-chrome"
chrome_params="--incognito"
```
##### surfing settings (firefox/chrome)
```
open_x_site_at_the_same_time=2
open_sites_each_x_seconds=15
wait_y_seconds_before_closing_x_sites=4 # 0 to keep 
init_time=10
```
## Usage
```
python pysas.py [native/firefox/chrome]
```
## Examples
### Firefox/Chrome (First run)
```
sh-4.3# python pysas.py chrome

Python Simple Auto Surfer: by abdelhafidh.com

Loop for ? times: 1
============================SETTINGS============================
Browser: Chrome
Open x site at the same time: 2
Open sites each ? seconds: 15
Wait ? seconds before closing x sites: 4
Loop ? times: 1
Init time: 10
================================================================
[+] New Process
[+] Adding to queue: http://stackoverflow.com/
[+] Adding to queue: https://github.com/dzmodest/pysas/
[i] Surfing now: 2	Batch: 1/1	Elapsed Time: 20 seconds
```
### Firefox/Chrome (Second run == Multiprocessing)
```
sh-4.3# python pysas.py chrome

Python Simple Auto Surfer: by abdelhafidh.com

Loop for ? times: 1
============================SETTINGS============================
Browser: Chrome
Open x site at the same time: 2
Open sites each ? seconds: 15
Wait ? seconds before closing x sites: 4
Loop ? times: 1
Init time: 10
================================================================
[i] Warning an existing tmp file has been found. Presume Multiprocessing
[+] Adding to queue: http://abdelhafidh.com/
[+] Adding to queue: https://instagram.com/
[i] Surfing now: 4	Batch: 1/1	Elapsed Time: 21 seconds
```
### Native (With loops)
```
sh-4.3# python pysas.py native

Python Simple Auto Surfer: by abdelhafidh.com

Loop for ? times: 2
============================SETTINGS============================
Browser: native
Open x site at the same time: 2
Open sites each ? seconds: 15
Wait ? seconds before closing x sites: 4
Loop ? times: 2
Init time: 10
================================================================
[+] New Process
[i] Warning Multiprocessing is not supported while loops>1
[+] Adding to queue: https://www.youtube.com/
[+] Adding to queue: http://stackoverflow.com/
[+] Adding to queue: https://twitter.com/
[+] Adding to queue: http://abdelhafidh.com/
[+] Adding to queue: https://github.com/dzmodest/pysas/
[+] Adding to queue: https://instagram.com/
[+] Adding to queue: https://twitter.com/
[+] Adding to queue: https://github.com/dzmodest/pysas/
[+] Adding to queue: http://stackoverflow.com/
[+] Adding to queue: https://www.youtube.com/
[+] Adding to queue: http://abdelhafidh.com/
[+] Adding to queue: https://instagram.com/
[i] Surfing now: 1	Batch: 2/2	Elapsed Time: 35 seconds
[*] We are done.
```

# Contributors
made with :heart: by [abdelhafidh.com](http://abdelhafidh.com)

# License
Python Simple Auto Surfer is released under [General Public License v3.0](https://github.com/dzmodest/pysas/blob/master/LICENSE).
