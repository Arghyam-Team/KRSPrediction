# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "..", ""))
from db import appdb

nlu_fall_back = "Please ask me a valid question. Default response"
all_in_one_intents = [
    "features",
    "model",
    "contact"
]



"""Load data from JSON"""
with open("data.json") as json_file:
    data = json.load(json_file)


class WeatherConnector:
    """
    Gets the weather data from the database
    """
    pass


class StorageConnector:
    """
    Gets the storage data from the database
    """
    pass



class ActionAllInOne(Action):
    """
    One Action for all stand alone responses
    """

    def name(self) -> Text:
        return "action_all_in_one"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        intent_of_user = tracker.get_intent_of_latest_message()
        if intent_of_user in all_in_one_intents:
            data_to_send_to_user_from_json = data.get(intent_of_user, nlu_fall_back)
            data_to_send_to_user_from_json = data_to_send_to_user_from_json if data_to_send_to_user_from_json is not None else nlu_fall_back
            dispatcher.utter_message(text = data_to_send_to_user_from_json)
            return []
        dispatcher.utter_message(text = nlu_fall_back)
        return []


class ActionAskWeather(Action):
    """
    Class to respond for Weather 
    """
    def name(self) -> Text:
        return "action_ask_weather"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text = "Dummy weather")
        return []


class ActionAskStorage(Action):
    """
    Class to respond for Storage
    """
    def name(self) -> Text:
        return "action_ask_storage"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text = "Dummy storage")
        return []
