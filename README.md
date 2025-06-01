# 🌦️ Full Stack Weather Forecast App

A full stack web app that fetches and displays a 3-day weather forecast using the OpenWeatherMap API. Built with **React** (frontend), **Flask** (backend), and deployed using **Docker** and **Render**.

---

## 🚀 Features

- Search for any city and view a 3-day weather forecast
- Smart suggestions:
  - **Carry umbrella** if rain is predicted
  - **Use sunscreen lotion** if temperature exceeds 40°C
- Responsive UI with separate Home and Forecast pages

---

## 🛠️ Tech Stack

### **Frontend**
- React (with Hooks)
- React Router
- Vite
- CSS

### **Backend**
- Flask (Python)
- Flask-Cors
- Flask-Caching
- python-dotenv
- requests

---

## 🗂️ Project Structure

```
full_stack_weather_app/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   ├── components/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── ErrorMessage.jsx
│   │   │   └── WeatherTable.jsx
│   │   └── pages/
│   │       ├── Home.jsx
│   │       └── Forecast.jsx
│   └── package.json
├── Dockerfile
└── ...
```

---

## ⚙️ Backend

### `.env` file

Stores sensitive configuration and API keys:
```env
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
PORT=5000
DEBUG=True
```

### `main.py`

- Loads environment variables using `python-dotenv`
- Defines a `/api` POST endpoint that:
  - Accepts a city name
  - Fetches 3-day weather forecast from OpenWeatherMap
  - Adds suggestions:
    - `"Carry umbrella"` if rain is predicted
    - `"Use sunscreen lotion"` if temperature > 40°C
  - Returns the forecast and suggestions as JSON
- Serves the frontend static files

---

## 💻 Frontend

- Built with **React** and **React Router**
- **Pages:**  
  - Home  
  - Forecast
- **Components:**  
  - SearchBar  
  - ErrorMessage  
  - WeatherTable
- All pages are rendered in `App.jsx`, which is mounted in `index.jsx`.

---

## 🐳 Docker (Build & Deploy Overview)

- **FROM python:3.10-slim**: Use a lightweight Python image as the base.
- **WORKDIR /app**: Set the working directory for the backend.
- **Install Node.js and npm**: Required to build the React frontend.
- **COPY backend /app**: Copy backend code into the container.
- **COPY frontend /frontend**: Copy frontend code into the container.
- **Build frontend**: Install frontend dependencies and build the React app.
- **Move frontend build to backend static folder**: Serve the built frontend from Flask.
- **Install backend dependencies**: Install Python packages from `requirements.txt`.
- **EXPOSE 5000**: Expose port 5000 for Flask.
- **Set Flask environment variables**: Configure Flask for production.
- **CMD ["flask", "run"]**: Start the Flask server.

---

## ☁️ Deployment (Render)

1. **Push your code to GitHub.**
2. **Create a new Web Service on [Render](https://render.com/):**
   - Connect your GitHub repo and select the main branch.
   - Render auto-detects your Dockerfile.
   - Set environment variables (`OPENWEATHERMAP_API_KEY`, etc.) in the Render dashboard.
   - Leave build and start commands blank (Dockerfile is used).
3. **Auto Deploy:**  
   Every push to your main branch triggers an automatic build and deployment on Render.
4. **Access your app:**  
   Visit the public Render URL provided after deployment.

---

## 📝 How to Run Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📦 Environment Variables

Set these in your `.env` file (for local) or in Render dashboard (for production):

```env
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
PORT=5000
DEBUG=True
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---
