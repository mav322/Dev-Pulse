# DevPulse — Real-Time Server Monitor

A lightweight, self-hosted system monitoring dashboard built with **Python + Flask**.  
Monitor CPU, memory, disk, network, and processes — live in your browser, updating every 2 seconds.

![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/flask-3.x-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## Features

- **CPU** — overall usage % + per-core vertical bars + frequency
- **Memory** — used / free with live sparkline chart
- **Disk** — storage breakdown with usage bar
- **Network** — cumulative sent/received + live delta sparkline
- **Top Processes** — top 5 CPU-hogging processes, live
- **System Info** — hostname, OS, uptime, Python version
- **Alert states** — color changes at WARNING (70%) and CRITICAL (90%)
- **Health endpoint** — `/health` for uptime monitors and server deployments
- Auto-refreshes every **2 seconds** via vanilla JS fetch

---

## Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Backend  | Python 3.8+, Flask      |
| Metrics  | psutil                  |
| Frontend | HTML, CSS, Vanilla JS   |
| Charts   | HTML5 Canvas (sparkline)|
| API      | REST / JSON             |

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/devpulse.git
cd devpulse

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Open **http://localhost:5000** in your browser.

---

## API Reference

### `GET /api/stats`
Returns a JSON snapshot of all system metrics.

```json
{
  "cpu":     { "percent": 23.5, "cores": [12, 8, 45, 3], "count": 4, "freq": 2400 },
  "memory":  { "percent": 61.2, "used_gb": 9.8, "total_gb": 16.0, "available_gb": 6.2 },
  "disk":    { "percent": 54.0, "used_gb": 270, "total_gb": 500, "free_gb": 230 },
  "network": { "bytes_sent_mb": 120.5, "bytes_recv_mb": 840.2 },
  "processes": [{ "pid": 1234, "name": "chrome", "cpu": 8.2, "mem": 3.1 }],
  "system":  { "hostname": "mypc", "os": "Linux 5.15", "uptime": "2:34:10", "python": "3.11.0" },
  "timestamp": "14:32:05"
}
```

### `GET /health`
Returns `{ "status": "ok" }` — useful for uptime monitors like UptimeRobot.

---

## Project Structure

```
devpulse/
├── app.py              # Flask server + API routes
├── requirements.txt    # Python dependencies
├── .gitignore
├── templates/
│   └── index.html      # Dashboard UI — HTML / CSS / JS
└── README.md
```

---

## Deployment (Linux Server)

To run DevPulse on a server and keep it alive:

```bash
# Install as a background service with screen
screen -S devpulse
python app.py
# Ctrl+A then D to detach
```

Or use **systemd** for a proper service (recommended for production).  
Access it at `http://YOUR_SERVER_IP:5000`.

> **Note:** By default Flask binds to `0.0.0.0`, so the dashboard is reachable on your local network too.

---

## Future Roadmap

- [ ] Historical data logging to SQLite
- [ ] Alert notifications (email / webhook)
- [ ] Multi-machine support over network
- [ ] Docker container
- [ ] Auth / password protection for public servers

---

## What I Learned

- Building REST APIs with **Flask** and returning structured JSON
- Reading live system metrics with **psutil**
- Real-time frontend updates using `setInterval` + `fetch`
- Drawing live **sparkline charts** with HTML5 Canvas
- Structuring a full-stack Python web project end-to-end

---

## Author

**Mayank** — BCA Student, Manipal University Jaipur  
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

## License

MIT — free to use, modify, and deploy.
