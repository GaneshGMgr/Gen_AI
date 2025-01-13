def create_query_result(city_name: str):
    """
    Creates a queryResult-like object manually for use in the WeatherData class.
    
    Parameters:
        city_name (str): The name of the city input by the user.
    
    Returns:
        dict: A queryResult-like dictionary that mimics Dialogflow's webhook request format.
    """
    query_result = {
        "queryResult": {
            "queryText": city_name,  # User's input as text
            "parameters": {
                "city_name": city_name  # Parameter extracted from user input
            },
            "intent": {
                "displayName": "GetWeatherIntent"  # Optional: Mimic the intent name
            },
            "languageCode": "en"  # Optional: Specify the language
        }
    }
    return query_result
