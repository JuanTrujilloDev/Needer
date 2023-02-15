#!/usr/bin/python

import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit,
        QTextEdit, QGridLayout, QApplication, QComboBox, QPushButton)
import PyQt6.QtCore as QtCore
from PyQt6.QtCore import QThread
import requests
import json
from datetime import datetime
from dateutil import parser
import pandas as pd
import time
import random
import string

class GetThread(QThread):
    requestResult = QtCore.pyqtSignal(object)

    def __init__(self, url, cookies, headers):
        QThread.__init__(self)
        self.url = url
        self.cookies = cookies
        self.headers = headers

    def http_request(self):
        result = response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
        self.requestResult.emit(result)

    def run(self):
        self.http_request()

class Scraper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.endpoint = "https://sportsinsights.actionnetwork.com/api/"
        self.sport_info= {
            "NFL":{
                "Seasons":{
                    "2022-23": "1384",
                    "2021-22": "708",
                    "2019-20": "166"
                }
            },
            "NBA": {
                "Seasons":{
                    "2022-23": "1681",
                    "2021-22": "1021",
                    "2019-20": "595"
                }
            },
            "MLB": {
                "Seasons":{
                    "2022": "1318",
                    "2021": "625",
                    "2020": "394"
                }
            },
            "NHL": {
                "Seasons":{
                    "2022-23": "1747",
                    "2021-22": "1022",
                    "2021": "596"
                }
            },
            "NCAAF": {
                "Seasons":{
                    "2022-23": "1351",
                    "2021-22": "707",
                    "2020-21": "493"
                }
            },
            "NCAAB": {
                "Seasons":{
                    "2022-23": "1516",
                    "2021-22": "790",
                    "2020-21": "514"
                }
            },
            "WNBA": {
                "Seasons":{
                    "2022": "1419",
                    "2021": "664",
                    "2020": "507"
                }
            }
        }
        self.cookies = {}
        self.handleCookies()
    
    def handleCookies(self):
        try:
            with open('cookies') as f:
                lines = f.readlines()
            if len(lines) == 1:
                pairs = lines[0].split('; ')
                for entry in pairs:
                    key, value = entry.split('=', 1)
                    self.cookies[key] = value

        except Exception as e:
            self.changeStatusLabel("cookies file not found. Using default cookies.")
            self.cookies = {
                'AN_SESSION_TOKEN_V1': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InU9MTE5ODkzOHQ9MTY0ODQ4OTEwNzM2OSIsInVzZXJfaWQiOjExOTg5MzgsImlzcyI6InNwb3J0c0FjdGlvbiIsImFnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4zOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTkuMC40ODQ0LjUxIFNhZmFyaS81MzcuMzYgT1BSLzg1LjAuNDM0MS4xOCIsImlzUmVzZXRUb2tlbiI6ZmFsc2UsImlzU2Vzc2lvblRva2VuIjpmYWxzZSwic2NvcGUiOltdLCJleHAiOjE2ODAwMjUxMDcsImlhdCI6MTY0ODQ4OTEwN30.wBL0aVyDoh5FXSdQdt2SP9gycywf5hBDbgkPs-uj0uw',
                'si_session': 'k45nwruwsvd44uqbucia3wii',
                'uid': '920837',
                'user_id': '920837',
                '__zlcmid': '19DkoFyiW29giUO',
                'SI_SESSION_TOKEN': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNicmVkcm9ja0BnbWFpbC5jb20iLCJ1c2VyX2lkIjoiOTIwODM3Iiwic291cmNlIjoiVEFOIiwiZGV2aWNlIjoiMSIsIm5iZiI6MTY0ODY1NDQ1MCwiZXhwIjoxNjQ5ODY0MDUwLCJpYXQiOjE2NDg2NTQ0NTAsImlzcyI6IlNwb3J0c0luc2lnaHRzIn0.o5ssXI8nTpEwuWJluE4tBlNQcxT5k5EswYnJw683wro',
                'AWSALB': '9if8OQB+dNMVahUAQrgMOlao8KLR5wC9tpKMKRNW/jpUHdvmu+Pd6yKf2uRVJ7hBtlgGvgGl+FeSvaWkvGwgAf4JERiHQmZuVTjxoxetCwp+UCgV1pdETPQU/cyS',
                'AWSALBCORS': '9if8OQB+dNMVahUAQrgMOlao8KLR5wC9tpKMKRNW/jpUHdvmu+Pd6yKf2uRVJ7hBtlgGvgGl+FeSvaWkvGwgAf4JERiHQmZuVTjxoxetCwp+UCgV1pdETPQU/cyS',
            }
    
    def changeStatusLabel(self, text):
        self.status_label.setText(text)
        self.status_label.repaint()

    def onclick_run(self):
        try:
            self.handleCookies()
            self.changeStatusLabel('Running')

            headers = {
                'authority': 'sportsinsights.actionnetwork.com',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Opera";v="85"',
                'accept': 'application/json, text/plain, */*',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 OPR/85.0.4341.18',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://sportsinsights.actionnetwork.com/bet-signals/?inLabs=true',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                # Requests sorts cookies= alphabetically
                # 'cookie': 'AN_SESSION_TOKEN_V1=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InU9MTE5ODkzOHQ9MTY0ODQ4OTEwNzM2OSIsInVzZXJfaWQiOjExOTg5MzgsImlzcyI6InNwb3J0c0FjdGlvbiIsImFnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4zOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTkuMC40ODQ0LjUxIFNhZmFyaS81MzcuMzYgT1BSLzg1LjAuNDM0MS4xOCIsImlzUmVzZXRUb2tlbiI6ZmFsc2UsImlzU2Vzc2lvblRva2VuIjpmYWxzZSwic2NvcGUiOltdLCJleHAiOjE2ODAwMjUxMDcsImlhdCI6MTY0ODQ4OTEwN30.wBL0aVyDoh5FXSdQdt2SP9gycywf5hBDbgkPs-uj0uw; si_session=k45nwruwsvd44uqbucia3wii; uid=920837; user_id=920837; __zlcmid=19DkoFyiW29giUO; SI_SESSION_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNicmVkcm9ja0BnbWFpbC5jb20iLCJ1c2VyX2lkIjoiOTIwODM3Iiwic291cmNlIjoiVEFOIiwiZGV2aWNlIjoiMSIsIm5iZiI6MTY0ODY1NDQ1MCwiZXhwIjoxNjQ5ODY0MDUwLCJpYXQiOjE2NDg2NTQ0NTAsImlzcyI6IlNwb3J0c0luc2lnaHRzIn0.o5ssXI8nTpEwuWJluE4tBlNQcxT5k5EswYnJw683wro; AWSALB=9if8OQB+dNMVahUAQrgMOlao8KLR5wC9tpKMKRNW/jpUHdvmu+Pd6yKf2uRVJ7hBtlgGvgGl+FeSvaWkvGwgAf4JERiHQmZuVTjxoxetCwp+UCgV1pdETPQU/cyS; AWSALBCORS=9if8OQB+dNMVahUAQrgMOlao8KLR5wC9tpKMKRNW/jpUHdvmu+Pd6yKf2uRVJ7hBtlgGvgGl+FeSvaWkvGwgAf4JERiHQmZuVTjxoxetCwp+UCgV1pdETPQU/cyS',
            }

            self.changeStatusLabel('Fetching Data')
            url = self.endpoint + "bet-signals/?lineTypeId={0}&seasonId={1}&sportId={2}&sportsbookId={3}&systemId={4}".format(self.bet_type_cb.currentData(), self.season_cb.currentData(), self.sports_cb.currentData(), self.sport_books_cb.currentData(),  self.sport_type_cb.currentData())
            self.thread = GetThread(url, self.cookies, headers)
            self.thread.requestResult.connect(self.handleResponse)
            self.thread.start()
            #response = requests.get(url, headers=headers, cookies=cookies)

        except Exception as e:
            self.changeStatusLabel('Error occured. Try different query. Error: {0}'.format(e))
    
    def handleResponse(self, response):
        try:
            if response.status_code != 200:
                if response.status_code == 401:
                    self.changeStatusLabel('Authentication Error. Please renew the cookies by adding them to "cookies" file near scraper')
                else:
                    self.changeStatusLabel('Please try again later. Server returned error: Code {0} - {1}'.format(response.status_code, response.reason))
                return

            events = response.json().get('Events', [])
            sorted_by_created_date = sorted(events, key=lambda x: parser.parse(x['CreatedDate']))     
            result_list = []
            for event in sorted_by_created_date:
                cr = event['PlayDisplay']
                d = cr.split(' ')
                if int(len(d)) == 4:
                    n = d[0]
                    o = d[1]
                    p = d[2]
                    q = d[3]
                elif int(len(d)) == 3:
                    n = d[0]
                    o = d[1]
                    p = ''
                    q = d[2]
                
                g= event['SportsbookName']+'('+event['SystemResultTextWithPercent']+')'
                j = event['HomeScore'],event['VisitorScore']


                object = {
                        "Trigger Time": event['CreatedDate'],
                        "Game Time": event['EventDateTime'],
                        "Signal": event['SystemNameShort'],
                        # "Play On": cr,
                        "Game number": n,
                        "Team": o,
                        "over/under": p,
                        "TOTAL": q,
                        'Bet Type': event['LineType'],
                        'Trigger Book': g,
                        'Percentage': g.split(',')[1].replace(')', ' '),
                        'Trigger Units': event['UnitsWonTotalFormatted'],
                        'Score': j,
                        'W/L': event['ResultText'],
                        'Result': event['UnitsWonFormatted'],
                    }
                result_list.append(object)

            if len(result_list) > 0 :
                name = "{0}_{1}_{2}".format(self.sports_cb.currentText(), self.season_cb.currentText(), self.sport_type_cb.currentText())
                excel_name = "{0}_{1}.xlsx".format(name, datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
                sheet_name = "{0}-{1}".format(name, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))).replace(" ", "")[0:30]
                p = pd.DataFrame(result_list)
                self.write_excel(excel_name , sheet_name, p)
                self.changeStatusLabel('Created document: {0}'.format(excel_name))
            else:
                self.changeStatusLabel('Query yield no result')
        
        except Exception as e:
            self.changeStatusLabel('Error occured. Try different query. Error: {0}'.format(e))      
    
    def write_excel(self, filename,sheetname,dataframe):
        options = {}
        options['strings_to_formulas'] = False
        options['strings_to_urls'] = False
        with pd.ExcelWriter(filename, engine='xlsxwriter', options=options, mode='w+') as writer: 
            workBook = writer.book
            try:
                workBook.remove(workBook[sheetname])
            except:
                pass
            finally:
                dataframe.to_excel(writer, sheet_name=sheetname,index=False)
                writer.save()

    def on_sport_changed(self):
        self.season_cb.clear()
        seasons = self.sport_info[self.sports_cb.currentText()]['Seasons']
        for season in seasons.keys():
            self.season_cb.addItem(season, seasons[season])

    def initUI(self):
        self.status_label = QLabel('')
        self.sport_type_label = QLabel('Sports Type')
        self.sport_label = QLabel('Sports')
        self.season_label = QLabel('Season')
        self.sport_books_label = QLabel('Sports Book')
        self.bet_type_label = QLabel('Bet Type')

        self.sport_type_cb = QComboBox(self)
        self.sport_type_cb.addItem('Steam', '8')
        self.sport_type_cb.addItem('Reverse line', '7')
        self.sport_type_cb.addItem('Contrarian', '1')

        self.sports_cb = QComboBox(self)
        self.sports_cb.addItem('')
        self.sports_cb.addItem('NFL', '1')
        self.sports_cb.addItem('NBA', '2')
        self.sports_cb.addItem('MLB', '3')
        self.sports_cb.addItem('NHL', '4')
        self.sports_cb.addItem('NCAAF', '11')
        self.sports_cb.addItem('NCAAB', '12')
        self.sports_cb.addItem('WNBA', '8')
        self.sports_cb.currentIndexChanged.connect(self.on_sport_changed)


        self.sport_books_cb = QComboBox(self)
        self.sport_books_cb.addItem('Top Books','-1')
        self.sport_books_cb.addItem('1BitVegas', '71')
        self.sport_books_cb.addItem('5Dimes', '6')
        self.sport_books_cb.addItem('5Dimes RJ', '80')
        self.sport_books_cb.addItem('888Sport NJ', '111')
        self.sport_books_cb.addItem('ABC', '19')
        self.sport_books_cb.addItem('Ace', '67')
        self.sport_books_cb.addItem('Bet365', '46')
        self.sport_books_cb.addItem('Bet365 NJ', '120')
        self.sport_books_cb.addItem('BetDSI', '54')

        self.season_cb= QComboBox(self)
        self.season_cb.addItem('')     

        self.bet_type_cb = QComboBox(self)
        self.bet_type_cb.addItem('All', '-1')
        self.bet_type_cb.addItem('Spread/ML', '0')
        self.bet_type_cb.addItem('Over/Under', '1')


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.sport_type_label, 1, 0)
        self.grid.addWidget(self.sport_type_cb, 1, 1)

        self.grid.addWidget(self.sport_label, 2, 0)
        self.grid.addWidget(self.sports_cb, 2, 1)

        self.grid.addWidget(self.sport_books_label, 3, 0)
        self.grid.addWidget(self.sport_books_cb, 3, 1)

        self.grid.addWidget(self.season_label, 4, 0)
        self.grid.addWidget(self.season_cb, 4, 1)

        self.grid.addWidget(self.bet_type_label, 5, 0)
        self.grid.addWidget(self.bet_type_cb, 5, 1)

        button = QPushButton("Run")

        self.grid.addWidget(button, 6, 0)
        button.clicked.connect(self.onclick_run)

        self.grid.addWidget(self.status_label, 6, 1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Scraper')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Scraper()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()