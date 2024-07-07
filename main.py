import os
import requests
from datetime import datetime
from typing import Dict


APP_ID = os.environ.get("APP_ID")
APP_ID = os.environ.get("APP_KEY")
SHEETY_URL = os.environ.get("SHEETY_URL")
SHEET_NAME = "workout"
API_URL = "https://trackapi.nutritionix.com"
EXERCISE_ENDPOINT = "/v2/natural/exercise"


def get_workout_data_from_nutritionix(query:str) -> list:
    """uses nutrionix' natural langauge query to find workout data from a string given by the user. The data will include
    todays data and time, the type of workout, duration in minutes and calories burnt.

    Args:
        query (str): The query provided by the user.

    Returns:
        list: each element of the list is a dictionary containing the details of one workout.
    """

    ret_val = []

    # authentication
    headers = \
        {
            "Content-Type":"application/json",
            "x-app-id":APP_ID,
            "x-app-key":APP_KEY,
        }
    
    # parameters for json
    params = \
        {
            "query":query
        }

    # request from nutritionix.com
    response = requests.post(url=API_URL+EXERCISE_ENDPOINT, json=params, headers=headers)
    response.raise_for_status()
    workout_data = response.json()['exercises']

    # find todays date and time
    today = datetime.now()
    today_time = today.time().strftime("%H:%M:%S")
    today_date = today.date().strftime("%d/%m/%Y")
    
    # extract relevant data from the json provided by nutritionix
    for workout in workout_data:
        new_dict = \
            {
                'date':today_date,
                'time':today_time,
                'exercise':workout['name'].title(),
                'duration':workout['duration_min'],
                'calories':workout['nf_calories'],
            }
        ret_val.append(new_dict)

    # return the list of workouts
    return ret_val


def post_data_to_google_sheet(data:list) -> None:
    """posts data to google sheets, using the sheety API

    Args:
        data (a list of dictionaries): each dictionary is used to make a new row in the google sheet
    """

    # headers
    headers = \
        {
            'Content-Type':"application/json"
        }
    
    # post each row
    for i in data:
        new_dict = \
            {
                SHEET_NAME:i
            }
        response = requests.post(url=SHEETY_URL, json=new_dict, headers=headers)
        response.raise_for_status()


def main() -> None:
    """asks user to input their workout details. Uses natural language query (from nutritionix) to extract relevant workout details and
    updates it in a google sheet.
    """

    query = input("Enter your workout details\n")
    workout_data = get_workout_data_from_nutritionix(query)
    post_data_to_google_sheet(workout_data)


main()