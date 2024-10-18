# Spotify Insights Web Application

This project is a web-based application developed as an undergraduate project at the Department of Electrical & Computer Engineering, University of Peloponnese for the course "Digital Sound and Image Processing." The project was performed by Kioulachoglou D. and Methenitis K., under the supervision of Associate Prof. Athanasios Koutras.

## Description

The Spotify Insights Web Application allows users to analyze and visualize their Spotify listening habits by providing insights into top tracks, artists, and genres. The application uses the Spotify Web API to fetch user data, including audio features, and presents the information in an interactive and visually appealing format.

### Key Features:
1. **User Authentication:** OAuth-based login to authenticate with Spotify and access user data.
2. **Top Tracks Analysis:** Displays the user's most played tracks along with audio feature analysis using radar charts.
3. **Top Artists and Genres:** Visualizes the most listened-to artists and genres using bar and pie charts.
4. **Track Audio Features:** Provides detailed audio features of tracks, including danceability, energy, valence, and more.
5. **Session Management:** Uses Flask-Session for managing user sessions.

## Features

- **Interactive data visualization using charts and graphs**
- **OAuth-based Spotify authentication**
- **Radar charts for visualizing track audio features**
- **Data export to CSV files**
- **Dynamic web interface built with Flask**

## Requirements

To run this project, the following dependencies must be installed:

- Python 3.7 or higher
- `Flask` and `Flask-Session` for web framework and session management
- `spotipy` for interacting with the Spotify Web API
- `matplotlib` and `seaborn` for creating visualizations
- `numpy` for numerical operations

You will also need to set up a Spotify Developer account and configure the following:

- **Client ID** and **Client Secret** for the Spotify API
- **Redirect URI** for OAuth authentication

## Setup Instructions

1. **Install Python Dependencies:**
   ```
   pip install Flask Flask-Session spotipy matplotlib seaborn numpy
   ```

2. **Configure Spotify API Credentials:**
   - Replace the placeholder values for `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` in the code with your Spotify developer account credentials.

3. **Run the Application:**
   ```
   python app.py
   ```

   - Access the application at `http://localhost:5001` in your web browser.

4. **Login and Permissions:**
   - The application will prompt for Spotify login and permission to access user data. Make sure to grant the requested permissions.

## Usage Notes

- The application requires an active Spotify account.
- Ensure that the `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` are set correctly.
- Charts will be saved in the `static` directory for display in the web interface.

## License

This project is intended for educational purposes and should not be used for commercial applications without proper licensing.

