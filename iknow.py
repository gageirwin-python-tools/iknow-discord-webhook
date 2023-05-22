import argparse
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord import Embed, SyncWebhook

ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "downloads.txt")

RED = 0xFF0000
GREEN = 0x00FF00


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, help="IP address to check", required=True)
    parser.add_argument("--webhook", type=str, help="Discord Webhook", required=True)
    args = parser.parse_args()
    return (args.webhook, args.ip)


def main():
    webhook_url, ip_address = parse_arguments()

    webhook = SyncWebhook.from_url(webhook_url)
    webhook.edit(name="iknowwhatyoudownload.com")

    found_downloads = []
    if os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, "r") as f:
            found_downloads = f.read().splitlines()

    url = f"https://iknowwhatyoudownload.com/en/peer/?ip={ip_address}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)

    if not response.ok:
        embed = Embed(
            title="Error Getting iknowwhatyoudownload.com",
            url=url,
            description=f"{response.status_code} {response.reason}",
            color=RED,
            timestamp=datetime.now(),
        )
        webhook.send(embed=embed)
        quit()

    soup = BeautifulSoup(response.text, "html.parser")

    downloads = soup.find_all("tr")[1:]
    for row in downloads:
        data = row.find_all("td")
        if not data:
            continue

        data_string = f"{ip_address}, {data[0].text.strip()}, {data[1].text.strip()}, {data[2].text.strip()}, {data[3].text.strip()}, {data[4].text.strip()}"
        if data_string in found_downloads:
            continue

        embed = Embed(
            title=data[3].text.strip(),
            url=f"https://iknowwhatyoudownload.com{data[3].div.a['href']}",
            color=GREEN,
            timestamp=datetime.now(),
        )
        embed.add_field(
            name="IP Address:",
            value=ip_address,
            inline=False,
        )
        embed.add_field(
            name="FIRST SEEN (UTC):",
            value=data[0].text.strip(),
            inline=False,
        )
        embed.add_field(
            name="LAST SEEN (UTC):",
            value=data[1].text.strip(),
            inline=False,
        )
        embed.add_field(
            name="CATEGORY:",
            value=data[2].text.strip(),
            inline=False,
        )
        embed.add_field(
            name="SIZE:",
            value=data[4].text.strip(),
            inline=False,
        )
        webhook.send(embed=embed)
        with open(ARCHIVE_FILE, "a") as f:
            f.write(f"{data_string}\n")


if __name__ == "__main__":
    main()
