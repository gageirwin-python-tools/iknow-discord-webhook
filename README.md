# iknowwhatyoudownload.com discord webhook
 A Python application that monitors a given IP address on iknowwhatyoudownload.com and send a Discord webhook if something is found.

## Usage
Install requirements
```bash
pip install -r requirements.txt
```
Run application
```bash
python iknow.py --ip "YOUR IP ADDRESS" --webhook "YOUR DISCORD WEBHOOK"
```
## Notes
 - A `downloads.txt` file will be created to store previously found downloads to not send duplicate notifications.  
 - Webhook message includes the IP address you passed in. 
 - To have the application periodically run set up cron on linux or task scheduler on windows.