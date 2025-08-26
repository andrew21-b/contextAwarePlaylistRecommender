# Nothing.Tech | Technical Test: Context-Aware Playlist Recommender

For my submission of this task, I followed the instructions and used the provided data to deliver an AI solution that complements the lifestyle of the user in the case study.

In brief, this project is an application that recommends a playlist based on the user's mood in real time. This is simulated using their calendar events, location, and recent social media posts.

The backend is a FastAPI implementation using the OpenAI client for the LLM. Dependencies are managed with Poetry.

The frontend is a React + Vite + Tailwind solution written in TypeScript.

## How to Run

To run the application, you will need Python and Node.js installed on your machine.

1. Clone the repository:
   ```powershell
   git clone https://github.com/andrew21-b/contextAwarePlaylistRecommender.git
   ```
2. Change to the repository directory:
   ```powershell
   cd contextAwarePlaylistRecommender
   ```
3. Change to the API directory:
   ```powershell
   cd api
   ```
4. Activate the virtual environment:
   ```powershell
   poetry env activate
   ```
5. Install dependencies:
   ```powershell
   poetry install
   ```
6. Create an environment file at `api\.env` and fill out these environment variables:
   ```powershell
   SPOTIFY_CLIENT_ID=<your_spotify_api_id>
   SPOTIFY_CLIENT_SECRET=<your_spotify_secret>
   LASTFM_API_KEY=<your_lastfm_api_key>
   LASTFM_SECRET=<your_lastfm_secret>
   OPENAI_API_KEY=<your_openai_key>
   ```

### Running the API

Once you have installed the dependencies and set the environment variables, you can run the API:

```powershell
poetry run fastapi dev main.py
```

### Running the Frontend

Once the API is up and running, open a new terminal and change to the `frontend` directory:

```powershell
cd frontend
```

1. Install dependencies:
   ```powershell
   npm install
   ```
2. Run the application:
   ```powershell
   npm run dev
   ```

The site can be accessed at http://localhost:5173

## Assumptions

During this project, a few assumptions had to be made since the instructions were quite open-ended. For example, the real implementation of this project would be an app running on a device and taking data directly from the sources. That is why I did not create a database for the API, as the data would be stored on the device. Additionally, the external APIs and clients I am using would not be the same if this were deployed. For example, I could have used a local LLM for this project, but I decided to use OpenAI to develop this rapidly. However, the choice of OpenAI was also because the client supports on-device LLMs, so my implementation would not have to change to accommodate that.

My original plan was to use Spotify's API to get features from the songs and build my own mood playlist model using Nearest Neighbor. However, that endpoint for features has been deprecated, and using librosa to extract features from raw audio files would take much more time. Plus, the instructions said the solution should be small but work well.

Another assumption I made was with the UI. Ideally, this app could work in the background of the device and be granted permissions to access the user's calendar and apps to extract data directly. So, the UI is simply used to interface with the API and provide a user-friendly visualization of the data.
