import requests
from bs4 import BeautifulSoup, Comment
import re


def extractComments(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Error accessing {}".format(link))
        return
    with open('matches.txt', mode='a+', encoding='utf-8') as matchFile:
        matchFile.write(link + "\n")
        matchFile.write("-" * 50 + "\n")
        comments = []
        comments.extend(re.findall(r'/\*((.|[\r\n])*?)\*/', resp))
        print("Multiline JS/CSS Matches: {}".format(len(comments)))
        for match in comments:
            for part in match:
                if part.strip() == "":
                    continue
                matchFile.write("/*{}*/\n".format(part))
        comments = []
        comments.extend(re.findall(r'[^":\']//(.+)', resp))
        print("One Liner JS Matches: {}".format(len(comments)))
        for match in comments:
            if match.strip() == "":
                continue
            matchFile.write("//{}\n".format(match))
        comments = []
        soup = BeautifulSoup(resp, 'html.parser')
        html_comments = soup.findAll(
            text=lambda text: isinstance(text, Comment))
        print("HTML Comment Matches: {}".format(len(html_comments)))
        for match in html_comments:
            if match.strip() == "":
                continue
            matchFile.write("<!--{}-->\n".format(match))
        matchFile.write("\n")


if __name__ == "__main__":
    links = open('list.txt', mode='r', encoding='utf-8').read().split('\n')
    for link in links:
        if link == "":
            continue
        print("Current link: {}".format(link))
        extractComments(link)
