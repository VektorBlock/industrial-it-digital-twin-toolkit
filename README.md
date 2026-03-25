# Industrial IT Monitoring & Digital Twin Toolkit

Lightweight industrial monitoring and digital twin project built in Python.

## Dashboard Preview

![Dashboard](screenshots/dashboard.png)

---

## What this project does

This project simulates a production machine and combines:

- machine state simulation
- IT metrics simulation
- industrial KPI calculation
- downtime analysis
- intelligent alerts
- interactive Streamlit dashboard

## Main technologies

- Python 3.10+
- Pandas
- Streamlit

## Project structure

```
industrial-it-digital-twin-toolkit/
├── src/
│   └── simulator.py        -> generates the simulated production data
├── data/
│   └── production_data.csv -> stores the generated dataset
├── dashboard/
│   └── app.py              -> displays KPIs, charts, alerts, and insights
├── docs/
│   └── project_manual.md   -> full project documentation
├── .streamlit/
│   └── config.toml         -> Streamlit configuration (optional)
├── requirements.txt
└── README.md
```

---

## How to run

### Prerequisites

#### Windows
1. Install **Python 3.10+** from [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - During installation, **check "Add Python to PATH"**
2. Install **Git** (optional, to clone the repo) from [https://git-scm.com/](https://git-scm.com/)

#### Linux / macOS
Python is usually pre-installed. Verify with:
```bash
python3 --version
```

---

### 1. Clone the repository

```bash
git clone https://github.com/VektorBlock/industrial-it-digital-twin-toolkit.git
cd industrial-it-digital-twin-toolkit
```

Or download the ZIP from GitHub → **Code → Download ZIP** and extract it.

---

### 2. Open a terminal inside the project folder

All the following commands must be run from inside the project folder.

**Windows:**
- Open File Explorer and navigate to the extracted folder (e.g. `industrial-it-digital-twin-toolkit-main`)
- Click on the address bar at the top, type `cmd` and press Enter
- A Command Prompt window will open already positioned in that folder

Alternatively, right-click inside the folder while holding **Shift** → **"Open PowerShell window here"**

**Linux:**
- Open the file manager, navigate to the extracted folder
- Right-click inside the folder → **"Open Terminal here"** (the option name may vary by distro)

Alternatively, open a terminal and navigate manually:
```bash
cd ~/Downloads/industrial-it-digital-twin-toolkit
```

**macOS:**
- Open Finder and navigate to the extracted folder
- Right-click the folder → **"New Terminal at Folder"** (requires macOS Monterey or later)

Alternatively, open Terminal and navigate manually:
```bash
cd ~/Downloads/industrial-it-digital-twin-toolkit
```

---

### 3. Install dependencies

**Windows (Command Prompt / PowerShell):**
```cmd
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
pip3 install -r requirements.txt
```

---

### 4. Generate simulated data

**Windows:**
```cmd
python src\simulator.py
```

**Linux / macOS:**
```bash
python3 src/simulator.py
```

This creates the file `data/production_data.csv`.

---

### 5. Run the dashboard

#### Local only (accessible only from this PC)

**Windows:**
```cmd
python -m streamlit run dashboard\app.py
```

**Linux / macOS:**
```bash
python3 -m streamlit run dashboard/app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

#### Accessible from other PCs on the local network

**Windows:**
```cmd
python -m streamlit run dashboard\app.py --server.address 0.0.0.0 --server.port 8501
```

**Linux / macOS:**
```bash
python3 -m streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```

Then find your local IP address:

- **Windows:** open cmd and run `ipconfig` → look for **IPv4 Address** (e.g. `192.168.1.42`)
- **Linux/macOS:** run `hostname -I`

From another PC on the same network, open the browser at:
```
http://<your-ip>:8501
```

> **Windows Firewall:** if the connection is blocked, add an inbound rule for TCP port 8501 in Windows Defender Firewall.

---

### Optional: Streamlit configuration

To hide the Deploy button and clean up the UI, create the file `.streamlit/config.toml`:

```toml
[server]
address = "localhost"
port = 8501

[client]
toolbarMode = "minimal"
showErrorDetails = false
```

---

## Main KPIs

| KPI | Description |
|-----|-------------|
| **Availability** | % of time the machine was operational |
| **Performance** | Actual vs theoretical production speed |
| **Quality** | % of good parts produced |
| **OEE** | Overall Equipment Effectiveness (Availability × Performance × Quality) |

---

## Purpose

This project shows how IT conditions — such as CPU load, network instability, and service availability — can affect simulated industrial performance.

---

## Documentation

Full project manual available here: [`docs/project_manual.md`](docs/project_manual.md)
