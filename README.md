# ⚽ FIFA 2026 World Cup Predictions Tracker Dashboard

A modern, high-fidelity tracking dashboard to monitor and update agentic predictions for the FIFA 2026 World Cup. Built with pure HTML/CSS/JS (vanilla) and a zero-dependency Python backend server.

## 🚀 How to Run

1. **Open a terminal** and navigate to this folder:
   ```bash
   cd "/Users/dip/.gemini/antigravity/scratch/worldcup-dashboard"
   ```
2. **Launch the dashboard**:
   ```bash
   ./run.sh
   ```
   This will start a local HTTP server on port 8080 and automatically open `http://localhost:8080/index.html` in your default browser.

3. **Stop the server**: Press `Ctrl+C` in the terminal when you are done.

---

## 🎨 Features & Architecture

- **Visual Dashboard**: Features an aggregate scoreboard tracking total forecasts, successes, failures, pending predictions, and live accuracy rate.
- **Glassmorphism Aesthetic**: Beautiful custom dark mode styling with radial space gradients, semi-transparent frosted panels, and glowing active states.
- **Tabs Categories**:
  - **Overview**: Highlights core tournament parameters, champion forecasts (Argentina), and notable group stage/tournament-wide upsets.
  - **Groups Stage**: A grid of Groups A through L showing the full team compositions, highlighted predicted top 2, and actual top 2 results.
  - **Dark Horses**: Custom card layouts highlighting S-Tier and A-Tier surprise package teams (Norway, Japan, Morocco, Egypt, USA), their talismans, and forecasted target runs.
  - **Knockout Bracket**: Structured bracket view displaying Quarter-Finals, Semi-Finals, and Final matchups.
  - **Match Day**: Individual fixture cards for crucial opening stage games showing dates, forecasted outcomes, and results.
- **Interactive Admin Mode**:
  - Toggle the **Admin Edit Mode** switch in the upper-right corner.
  - Interactive edit buttons will appear on all cards.
  - Click any edit icon to open a modal form. You can update prediction outcomes (Pass / Fail / Pending), actual team placements, scores, and details.
  - **Automatic Sync & Persistence**: Saving changes will automatically update `predictions.json` on the disk via the local Python server. If the server is offline or the dashboard is run as a direct static file, it safely falls back to saving edits to your browser's `localStorage`!

---

## 📂 Project Structure

- `index.html`: The HTML layout, interactive logic, and premium CSS styling.
- `predictions.json`: The central database containing predictions and matches data.
- `server.py`: A lightweight, zero-dependency Python server that serves pages and provides the `/update` POST API endpoint to save changes directly back to `predictions.json`.
- `run.sh`: Startup helper script.
