import requests
import re
import config
from datetime import date
from bs4 import BeautifulSoup

def getHoliday():
    month = date.today().strftime('%b') # Get month
    day = date.today().strftime('%d') # Get day
    fDate = f'{month.lower()}-{day}' # Format date 

    URL_LOOKUP = {
        'Jan' : 'https://foodimentary.com/today-in-national-food-holidays/todayinfoodhistorycalenderfoodnjanuary/',
        'Feb' : 'https://foodimentary.com/today-in-national-food-holidays/february-food-holidays/',
        'Mar' : 'https://foodimentary.com/today-in-national-food-holidays/march-food-holidays/',
        'Apr' : 'https://foodimentary.com/today-in-national-food-holidays/april-food-holidays-foodimentary/',
        'May' : 'https://foodimentary.com/today-in-national-food-holidays/may-holidays/',
        'June': 'https://foodimentary.com/june-holidays/',
        'July': 'https://foodimentary.com/july-holidays/',
        'Aug' : 'https://foodimentary.com/august-holidays/',
        'Sept': 'https://foodimentary.com/september-holidays/',
        'Oct' : 'https://foodimentary.com/october-holidays/',
        'Nov' : 'https://foodimentary.com/november-holidays/',
        'Dec' : 'https://foodimentary.com/today-in-national-food-holidays/december-national-food-holidays/'
    }

    # Get HTML from home page
    url = 'https://foodimentary.com/today-in-national-food-holidays/todayinfoodhistorycalenderfoodnjanuary/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') # Parse HTML with BeautifulSoup

    # Get the current month URL
    months = soup.find('ul', id='menu-months', class_='menu') # Isolate the months table
    monthUrl = months.find('a', href=True, string=month)['href'] # Get the month URL for the current month

    # Get HTML from month page, parse
    r = requests.get(monthUrl)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find tag with URL that contains formatted date
    holidayTag = soup.select_one(f'a[href*={fDate}]')
    # Navigate HTML tree to get chunk that contains National Holiday
    descendants = holidayTag.parent.parent.descendants

    for child in descendants: # Iterate through all nested tags
        try:
            if 'National' in child.string: # If tag contains a string AND the word National, grab the string
                holiday = child.string
                break
        except:
            continue
    
    return holiday

def main():
    postUrl = 'https://slack.com/api/conversations.setTopic' # Slack API endpoint URL

    holiday = getHoliday() # Get name of today's holiday
    today = date.today().strftime('%b %d') # Get formatted date

    # POST payload
    postData = {
        'token'   : f'{config.apiToken}',
        'channel' : f'{config.channelId}',
        'topic'   : f"Happy {holiday} ({today})"
    }

    p = requests.post(postUrl, data = postData)

if __name__ == '__main__':
    main()