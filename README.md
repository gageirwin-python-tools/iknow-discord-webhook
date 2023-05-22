# iknowwhatyoudownload.com discord webhook
 A Python application that monitors a given IP address on iknowwhatyoudownload.com and send a Discord webhook if something is found.

## Usage
```bash
python iknow.py --ip "YOUR IP ADDRESS" --webhook "YOUR DISCORD WEBHOOK"
```
## Notes
 - A `downloads.txt` file will be created to store previously found downloads to not send duplicate notifications.  
 - Webhook message includes the IP address you passed in. 