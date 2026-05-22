# NASA NeoWS API Asteroid Detection Radar ☄️

A Python script that connects to the NASA NeoWs (Near Earth Object Web Service) API to track asteroids passing near Earth and other celestial bodies.

## Setup
1. Clone the repo.
2. Create a `.env` file and add your `NASA_API_KEY`.
3. Install requirements: `pip install requests python-dotenv`
4. Run `python main.py`

## Features
- Fetches real-time asteroid data based on date ranges.
- Parses nested JSON to extract specific Asteroid IDs.