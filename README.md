# NASA NeoWS API Asteroid Detection Radar ☄️
# Ver: 1.0 (Python Protoype)

A Python script that connects to the NASA NeoWs (Near Earth Object Web Service) API to track NEOs (Near Earth Objects) travelling 
near Earth, allowing to scan for possible threats and browse NEO data.

## Setup
1. Clone the repo.
2. Create a `.env` file and add your `NASA_API_KEY`.
3. Install requirements: `pip install requests python-dotenv`
4. Run `python main.py`

## Features
- Fetches real-time asteroid data based on date ranges.
- Parses nested JSON to extract and filter specific NEO attributes for analysis
- Provides functionality to scan NEOs, determining possible threats based off of a custom-engineered hazard scale
- Grants ability to browse NEOs within specific time frames to view attributes such as size, approach date, and approach distance
- View top 10 threats within the upcoming 7 days

