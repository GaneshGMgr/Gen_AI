from app_logger.logger import logger
from flask import Flask, render_template, request, make_response
import json
from flask_cors import CORS, cross_origin
from weather_data import WeatherData
from app_exception.exception import AppException
import traceback

app = Flask(__name__)
weather_data = WeatherData()

def main():
    logger.info("Weather Chatbot is running...")
    app.run(host='127.0.0.1', port=8080, debug=True)  # Enable debug mode for development

@app.route('/')
def index():
    return render_template('weatherChatbot.html')

@app.route('/get_weather', methods=['POST'])
@cross_origin()
def get_weather():
    req = request.get_json(silent=True, force=True)

    # Debug logs to inspect client-side input
    logger.info(f"Received request (raw): {req}")
    logger.info(f"Received request (json dumps): {json.dumps(req, indent=4)}")

    try:
        res = weather_data.processRequest(req)
        res = json.dumps(res)
        logger.info(f"Response: {res}")
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r
    except AppException as e:
        logger.error(f"AppException occurred: {e}")
        error_response = {"error": str(e)}
        status_code = getattr(e, 'status_code', 400)  # Default to 400 if no status_code attribute
        return make_response(json.dumps(error_response), status_code)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        logger.error(f"Stack trace: {traceback.format_exc()}")  # Log full stack trace for debugging
        error_response = {"error": "Failed to get weather data"}
        return make_response(json.dumps(error_response), 500)

if __name__ == '__main__':
    app.config['DEBUG'] = True  # Debug mode enabled
    main()
