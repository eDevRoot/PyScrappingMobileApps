# py_scrapping_apps_ratings
A little script of python to scraping the app ratings from Google Play and App Store

## Dependencies

~~~
pip install requests
pip install beautifulsoup4
~~~

## Config.json
### Apps
~~~
"apps": [
{
    "name": "Twitter",
    "apple": "id333903271",
    "android": "com.twitter.android"
},
...
],
~~~
### Countries
~~~
"countries": [
{
    "name": "Spain",
    "code": "es"
},
...
]
~~~
### Slack integration
~~~
"slack_webhook": "https://hooks.slack.com/services/..."
~~~
