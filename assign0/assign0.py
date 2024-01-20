# i have taken help of internet to know about how to open google sheet  and run it etc.
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

def analyze_consecutive_days(data):
    for employee in data:
        consecutive_days = 1
        previous_date = datetime.strptime(employee['date'], '%Y-%m-%d')  
        for entry in data[1:]:
            current_date = datetime.strptime(entry['date'], '%Y-%m-%d') 
            
            if current_date - previous_date == timedelta(days=1):
                consecutive_days += 1
            else:
                consecutive_days = 1 
            if consecutive_days == 7:
                print(f"Employee: {employee['name']}, Position: {employee['position']}")
                break
            
            previous_date = current_date

def analyze_shift_time(data):
    for i in range(1, len(data)):
        previous_end_time = datetime.strptime(data[i-1]['end_time'], '%H:%M:%S')  
        current_start_time = datetime.strptime(data[i]['start_time'], '%H:%M:%S') 

        time_between_shifts = current_start_time - previous_end_time
        hours_between_shifts = time_between_shifts.total_seconds() / 3600

        if 1 < hours_between_shifts < 10:
            print(f"Employee: {data[i]['name']}, Position: {data[i]['position']}")

def analyze_long_shifts(data):
    for entry in data:
        start_time = datetime.strptime(entry['start_time'], '%H:%M:%S')  
        end_time = datetime.strptime(entry['end_time'], '%H:%M:%S') 

        shift_duration = end_time - start_time
        hours_worked = shift_duration.total_seconds() / 3600

        if hours_worked > 14:
            print(f"Employee: {entry['name']}, Position: {entry['position']}")


def analyze_spreadsheet(json_key_path, spreadsheet_url):
    credentials = Credentials.from_service_account_file(json_key_path)

    gc = gspread.authorize(credentials)

    worksheet = gc.open_by_url(spreadsheet_url).sheet1

    data = worksheet.get_all_records()

    analyze_consecutive_days(data)
    analyze_shift_time(data)
    analyze_long_shifts(data)

if __name__ == "__main__":
    json_key_path = 'assignment-411817-7a655a0b0adc.json'
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1eRujNQYov-tZ8j9yvkah6lSzJOpNweMF/edit#gid=0'

    analyze_spreadsheet(json_key_path, spreadsheet_url)
