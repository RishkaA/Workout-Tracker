import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 58
HEIGHT_CM = 168
AGE = 25

nutritionix_api = os.environ.get("NUTRITIONIX_API")
nutritionix_app_id = os.environ.get("NUTRITIONIX_APP_ID")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_question = input("Tell me what exercise you did: ")

nutritionix_headers = {
    "x-app-id": nutritionix_app_id,
    "x-app-key": nutritionix_api,
}

exercise_params = {
    "query": exercise_question,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
#
response = requests.post(exercise_endpoint, json=exercise_params, headers=nutritionix_headers)
result = response.json()

today = datetime.now()
date = today.strftime("%d-%m-%Y")
time = today.strftime("%X")

sheety_user = os.environ.get("SHEETY_USER")
sheety_pass = os.environ.get("SHEETY_PASS")

sheety_endpoint = "https://api.sheety.co/fa42f62de5a8f220dff9fafa72f746e5/myWorkouts/workout"

for exercise in result["exercises"]:
    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

sheety_response = requests.post(sheety_endpoint, json=sheety_params, auth=(sheety_user, sheety_pass)) 

print(sheety_response.text)