import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import calendar
import csv
import schedule
import time


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_day():
    day = date.today()
    return calendar.day_name[day.weekday()]


def get_capacity():
    url = 'https://operations.daxko.com/Online/2217/MembershipV2/Capacity.mvc'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find_all('text', class_='percentage')

    capacity = text[len(text) - 3]
    for c in capacity:
        strcapacity = str(c.encode("utf-8"))
    return int(strcapacity[-3])


def write_csv():
    with open('/Users/fardeenkhan/PycharmProjects/capacity/caps.csv', 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow([get_day(), get_time(), get_capacity()])


def add_csv():
    with open('/Users/fardeenkhan/PycharmProjects/capacity/caps.csv', 'a') as csvfile:
        write = csv.writer(csvfile)
        write.writerow([get_day(), get_time(), get_capacity()])


if __name__ == "__main__":
    add_csv()
    schedule.every(1).seconds.do(add_csv)

    while True:
        schedule.run_pending()
        time.sleep(1)
