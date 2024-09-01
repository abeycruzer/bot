from flask import Flask, request, jsonify
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2
from twilio.twiml.messaging_response import MessagingResponse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Sample data for nearby museums (In a real app, this would come from a database or API)
museums = [
    {"name": "Museum A", "lat": 28.4617715 , "lon": 77.021166},
    {"name": "Museum B", "lat": 40.7580, "lon": -73.9855},
    {"name": "Museum C", "lat": 40.730610, "lon": -73.935242}
]

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    # Get the message body and the sender's phone number
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From')

    # Debug print to log the received message
    app.logger.debug(f"Received message: {incoming_msg} from {from_number}")

    # Create a response object
    resp = MessagingResponse()
    msg = resp.message()

    # Define valid inputs for options
    valid_inputs = ['english', 'hindi', 'ticket', '2024', 'adults', 'child']

    # Handle random inputs and prompt for language selection
    if not any(phrase in incoming_msg for phrase in valid_inputs):
        msg.body("It seems like I didn't understand your request. Please select your preferred language:\n1. English\n2. Hindi")
        return str(resp)

    # Language selection (Example handling)
    if 'english' in incoming_msg:
        msg.body("Hello! I'm your museum ticket booking assistant. Type 'ticket' to start.")
    elif 'hindi' in incoming_msg:
        msg.body("नमस्ते! मैं आपका संग्रहालय टिकट बुकिंग सहायक हूँ। 'टिकट' टाइप करें और शुरू करें।")
    elif 'ticket' in incoming_msg:
        msg.body("Great! Please provide the date of your visit (e.g., 2024-09-01).")
    elif '2024' in incoming_msg:
        msg.body("How many tickets do you need and for whom (e.g., 2 adults, 1 child)?")
    elif 'adults' in incoming_msg or 'child' in incoming_msg:
        msg.body("Thank you! Please complete the payment at [payment link].")
    else:
        msg.body("Hello! I'm your museum ticket booking assistant. Type 'ticket' to start.")

    # Return the Twilio response as a string
    return str(resp)

@app.route('/send-location', methods=['POST'])
def send_location():
    data = request.json
    user_lat = data.get('latitude')
    user_lon = data.get('longitude')
    

    app.logger.debug(f"User Location: Latitude {user_lat}, Longitude {user_lon}")

    if user_lat is None or user_lon is None:
        return jsonify({'error': 'Invalid location data'}), 400

    # Calculate distance and find nearby museums (this is a simplified version)
    nearby_museums = [
        museum for museum in museums
        if calculate_distance(user_lat, user_lon, museum['lat'], museum['lon']) < 50 # Radius in km
    ]
    # Log the nearby museums
    app.logger.debug(f"Nearby Museums: {nearby_museums}")
    

    return jsonify({'museums': nearby_museums})

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula to calculate distance
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    distance = r * c  # Distance in kilometers

    return distance

if __name__ == '__main__':
    # Run the app with debugging enabled, and ensure it listens on all interfaces
    app.run(debug=True, host="0.0.0.0", port=8000)
