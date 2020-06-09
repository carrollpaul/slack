import requests
import re
import config
from datetime import datetime
from bs4 import BeautifulSoup

def getHoliday():
    month = datetime.now().strftime('%B') # Get full month (ex. February 01)
    currentDay = datetime.now().day # Get day
    fDate = f'{month} {currentDay}' # Format date

    URL_LOOKUP = {
        'January'  : 'https://foodimentary.com/today-in-national-food-holidays/todayinfoodhistorycalenderfoodnjanuary/',
        'February' : 'https://foodimentary.com/today-in-national-food-holidays/february-food-holidays/',
        'March'    : 'https://foodimentary.com/today-in-national-food-holidays/march-food-holidays/',
        'April'    : 'https://foodimentary.com/today-in-national-food-holidays/april-food-holidays-foodimentary/',
        'May'      : 'https://foodimentary.com/today-in-national-food-holidays/may-holidays/',
        'June'     : 'https://foodimentary.com/june-holidays/',
        'July'     : 'https://foodimentary.com/july-holidays/',
        'August'   : 'https://foodimentary.com/august-holidays/',
        'September': 'https://foodimentary.com/september-holidays/',
        'October'  : 'https://foodimentary.com/october-holidays/',
        'November' : 'https://foodimentary.com/november-holidays/',
        'December' : 'https://foodimentary.com/today-in-national-food-holidays/december-national-food-holidays/'
    }

    # Get HTML from month page
    url = URL_LOOKUP.get(month) # Lookup month URL
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser') # Parse HTML with BeautifulSoup
    text = soup.select_one('section[role="main"]').text

    # Make a dictionary of dates and lists of Food Holidays 
    out = {}
    for day, names in re.findall(r'^([A-Z][^\n]+\d\s*)$(.*?)\n\n', text, flags=re.DOTALL|re.M): # Regex courtesy of Stack Overflow
        out[day.strip()] = [name.replace('\xa0', ' ') for name in names.strip().split('\n')]

    # Get holiday for current day
    currentHoliday = out.get(fDate)[0]

    return currentHoliday

def main():
    postUrl = 'https://slack.com/api/conversations.setTopic' # Slack API endpoint URL

    holiday = getHoliday() # Get name of today's holiday

    month = datetime.now().strftime('%B') # Get full month (ex. February 01)
    currentDay = datetime.now().day # Get day
    fDate = f'{month} {currentDay}' # Format date

    # POST payload
    postData = {
        'token'   : f'{config.foodieApiToken}',
        'channel' : f'{config.foodieChannelId}',
        'topic'   : f"Happy {holiday}! ({fDate})"
    }

    p = requests.post(postUrl, data = postData)

if __name__ == '__main__':
    main()