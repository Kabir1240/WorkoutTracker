import os
import json
import requests
from datetime import datetime
from typing import Dict


APP_ID = ""
APP_KEY = ""
SHEETY_URL = ""
SHEETY_TOKEN = ""
SHEET_NAME = "workout"
API_URL = "https://trackapi.nutritionix.com"
EXERCISE_ENDPOINT = "/v2/natural/exercise"
KEYS_PATH = "keys.json"


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


def post_data_to_google_sheet(data:list[Dict]) -> None:
    """posts data to google sheets, using the sheety API

    Args:
        data (a list of dictionaries): each dictionary is used to make a new row in the google sheet
    """

    # headers
    headers = \
        {
            'Authorization':SHEETY_TOKEN,
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


def update_global_variables() -> None:
    """
    retrieves data from keys.json and updates global variables for other functions.
    """

    global APP_ID
    global APP_KEY
    global SHEETY_URL
    global SHEETY_TOKEN

    with open(KEYS_PATH, 'r') as file:
        keys = json.load(file)
    
    APP_ID = keys['APP_ID']
    APP_KEY = keys['APP_KEY']
    SHEETY_URL = keys['SHEETY_URL']
    SHEETY_TOKEN = keys['SHEETY_TOKEN']


def get_workouts() -> list[Dict]:
    """retrieves workouts from the google sheet

    Returns:
        list[Dict]: list of dictionaries, each dictionary representing one workout
    """

    update_global_variables()
    # headers
    headers = \
        {
            'Authorization':SHEETY_TOKEN,
            'Content-Type':"application/json"
        }
    
    response = requests.get(url=SHEETY_URL, headers=headers)
    response.raise_for_status()
    return response.json()


def update_workouts(query:str) -> None:
    """takes a query, runs it through nutritionix exercise natural language selection and then uploads the extracted data to a google
    sheet doc

    Args:
        query (str): a human written string, about their workouts.
    """
    
    update_global_variables()
    workout_data = get_workout_data_from_nutritionix(query)
    post_data_to_google_sheet(workout_data)
