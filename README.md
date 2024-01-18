# TerraTrek

🗺️ TerraTrek is a voice-controlled globe that combines software and hardware components to process voice commands and provide interesting facts about a given geographic location. It fosters global awareness and promotes cultural curiosity by making geographical concepts more tangible. 

🕹️ Using the Raspberry Pi and Porcupine API, it detects the specific wake phrase, “Hey TerraTrek.” The Google Speech Recognition API converts speech to text, and the Google Maps API gathers the coordinates of the location. Next, the Arduino with stepper and servo motors rotates and tilts the globe to the specified location, and the ChatGPT API generates interesting facts about the location. 

## Getting started: 
To get dependencies:

pip install -r requirements.txt
To save dependencies:

pip freeze requirements.txt
Create .env file for storing API keys with the following format:

API Credentials
GC_KEY=YOUR_API_KEY_HERE
