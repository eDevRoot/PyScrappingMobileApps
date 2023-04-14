import json
import os.path
import requests
import re
from bs4 import BeautifulSoup


def get_apple_ratings(country_code, app_id):
    r = requests.get('https://apps.apple.com/' + country_code + '/app/' + app_id)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('figcaption', class_='we-rating-count star-rating__count')
    if s is None:
        return "Not found"
    x = s.contents[0].split(" • ")
    return x[0]


def get_google_ratings(country_code, app_id):
    r = requests.get('https://play.google.com/store/apps/details?id=' + app_id + '&gl=' + country_code)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_='TT9eCd')
    if s is None:
        return "Not found"
    return s.contents[0]


def verify_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def post_slack(slack_webhook, data):
    headers = {"Content-Type": "application/json"}
    text = "py apps ratings:\n"

    for r in data:
        text += r['name'] + " | " + r['country'] + \
                " | Google Play: " + r['android'] + " | App Store: " + r['apple'] + "\n"

    body = json.dumps({"text": text})
    requests.request("POST", slack_webhook, headers=headers, data=body)


def read_settings():
    filename = 'config.json'
    if not os.path.exists(filename):
        print(filename + " doesn't exist")
        return None, None

    with open(filename) as f:
        d = json.load(f)
        if 'apps' not in d.keys() or 'countries' not in d.keys():
            print("Keys 'apps' or 'countries' does not match in " + filename + " file")
            return None, None

        slack_webhook = None
        if 'slack_webhook' in d.keys() and d['slack_webhook'] is not None and verify_url(d['slack_webhook']):
            slack_webhook = d['slack_webhook']

        return d['apps'], d['countries'], slack_webhook


# Main


apps, countries, webhook = read_settings()

if apps is None or countries is None:
    exit(0)

ratings = []
for app in apps:
    for country in countries:
        apple = get_apple_ratings(country['code'], app['apple'])
        google = get_google_ratings(country['code'], app['android'])
        rating = dict(name=app['name'], country=country['name'], android=google, apple=apple)
        ratings.append(rating)
        print(app['name'] + " | " + country['name'] + " | Google Play: " + rating['android'] +
              " | App Store: " + rating['apple'])


if webhook is not None:
    post_slack(webhook, ratings)
