import requests
import pygal
import webbrowser
from lxml import html
from datetime import datetime

#API Info
api_key = "QGB4RG9L7AWT1713"
url = f'https://www.alphavantage.co/query?function={T_series}&symbol={stk_symbl}&apikey={api_key}'
response = requests.get(url)
data = response.json()
tree = html.fromstring(response.text)


#Getting Stock Symbol
stk_symbl = input("Enter the stock symbol: ")

#Getting Chart Type
while True;
  print("\n----------Chart Type----------\n")
  chrt_type = input("Enter Chart Type\n1) Line chart \n2) Bar chart")
  if chrt_type in ["1", "2"]:
      break
  else:
    print("\nInvalid Input\n")

#Getting Time Series
while True:
    print("\n-----------Time Series-----------\n")
    usr_T_series = input("Enter time series:\n1) Intraday\n 2) Daily\n 3) Weekly\n 4) Monthly\n Selection: ")
    if usr_T_series in ["1","2","3","4"]:
        break
    else: 
        print("\nInvalid Input\n")

if usr_T_series == "1":
    T_series = "Time_Series_Intraday"
    T_series_output = "Time Series (5min)"
if usr_T_series == "2":
    T_series = "Time_Series_Daily"
    T_series_output = "Time Series (Daily)"
if usr_T_series == "3":
    T_series = "Time_Series_Weekly"
    T_series_output = "Weekly Time Series"
if usr_T_series == "4":
    T_series = "Time_Series_Monthly"
    T_series_output = "Monthly Time Series"
  
# Start Date
while True:
    print("-------------Start Date-------------\n")
    start_date = input("\nEnter Start Date (YYYY-MM-DD): ")
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        break
    except ValueError:
          print("\nInvalid format. Please use YYYY-MM-DD format.")
        
# End Date
while True:
    print("-------------End Date-------------\n")
    end_date = input("\nEnter End Date (YYYY-MM-DD): ")
        try:
            datetime.strptime(end_date, '%Y,%m,%d')
            if end_date >= start_date:
                break
            else:
                print("The end date shound't be before the start date")
        except ValueError:
            print("\nInvalid format. Please use YYYY-MM-DD format")

closing_prices = []
for date, values in data[T_series_output].items():
    closing_prices.append(float(values['4. close']))

#Creating Line Graph
if chrt_type == 1:
    line_chart = pygal.Line()
    line_chart.title = f'{stk_symbl} Stock Prices'
    chart.x_labels = reversed([str(i) for i in range(1, len(closing_prices) + 1)])
    chart.add('Closing Price', [float(price) for price in closing_prices])
    chart.render_to_file('stock_chart.svg')
    webbrowser.open('stock_chart.svg')

#Creating Bar Graph
if chrt_type == 2:  
    bar_chart = pygal.Bar()
    bar_chart.title = f'{stk_symbl} Stock Prices'
    chart.x_labels = reversed([str(i) for i in range(1, len(closing_prices) + 1)])
    chart.add('Closing Price', [float(price) for price in closing_prices])
    chart.render_to_file('stock_chart.svg')
    webbrowser.open('stock_chart.svg')

