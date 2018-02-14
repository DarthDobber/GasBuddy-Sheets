import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

def sanitizeString(input):
    try:
        if input is not None:
            rValue = input.strip()
            return rValue
        else:
            rValue = "Empty"
            return rValue
    except TypeError:
        pass

def clearCells():
    row = 4
    col = 1
    currCell = worksheet.cell(row, col).value
    while currCell != "":
        worksheet.update_cell(row, col, "")
        row = row + 1
        currCell = worksheet.cell(row, col).value
    row = 4
    col = 2
    currCell = worksheet.cell(row, col).value
    while currCell != "":
        worksheet.update_cell(row, col, "")
        row = row + 1
        currCell = worksheet.cell(row, col).value
    row = 4
    col = 3
    currCell = worksheet.cell(row, col).value
    while currCell != "":
        worksheet.update_cell(row, col, "")
        row = row + 1
        currCell = worksheet.cell(row, col).value
    

def getAverageGasPrices(state):
    url = "http://www.gasbuddy.com/USA/" + str(state)
    r = requests.get(url)
    if r.status_code == 200:
        html = r.content
        soup = BeautifulSoup(html, "lxml")
        city = soup.find_all("div", {"class": "siteName"})
        avg = soup.find_all("div", {"class": "col-xs-3"})
        change = soup.find_all("span", {"class": "falling"})

        cityRow = 4
        for c in city:
            c = sanitizeString(c.string)
            if c != "Empty":
                worksheet.update_cell(cityRow, 1, str(c))
                cityRow = cityRow + 1
        avgRow = 4
        for a in avg:
            a = sanitizeString(a.string)
            if a != "Empty":
                worksheet.update_cell(avgRow, 2, str(a))
                avgRow = avgRow + 1
        changeRow = 4
        for ch in change:
            ch = sanitizeString(ch.string)
            if ch != "Empty":
                worksheet.update_cell(changeRow, 3, str(ch))
                changeRow = changeRow + 1

#Authorizing connection to google sheets, you need to create a project on Google's 
#API Manager
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#Open a worksheet
book = client.open_by_url('https://docs.google.com/spreadsheets/d/1m0MQHHhMJJVDDesJYAGzsXa85pvSzhm_V-s6csdu4y8')

#Get the State
worksheet = book.get_worksheet(0)
state = worksheet.acell('B1').value

#Get the data and put it in the worksheet
clearCells()
getAverageGasPrices(state)