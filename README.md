# FashionGPT Studio 👗

> **An end-to-end AI-powered fashion trend intelligence platform** — scrapes live data from Pinterest, Zara, Uniqlo & Vogue, runs LLM analysis via Groq (Llama 3.3 70B), and delivers brand-specific strategic recommendations for Gap Inc. brands through a polished Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=flat-square&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What This Project Does

FashionGPT Studio is a **full-stack AI application** that acts as an automated market intelligence analyst for fashion retail. Given a product keyword (e.g. "denim jacket", "summer dress"), it:

1. **Scrapes live data in parallel** from four sources simultaneously:
   - **Pinterest** — 12 high-resolution visual inspiration images via headless Selenium
   - **Zara** — 10 real product listings (name, color, material, price) via Crawl4AI + BeautifulSoup
   - **Uniqlo** — 10 real product listings via Crawl4AI + BeautifulSoup
   - **Vogue** — 5 editorial articles via RSS feed + Crawl4AI fallback

2. **Runs AI trend analysis** (Groq / Llama 3.3 70B) on the scraped market data to extract:
   - Dominant color palettes
   - Key materials trending in the market
   - Aesthetic vibes & positioning
   - Market confidence score

3. **Generates brand-specific strategies** for three distinct retail tiers:
   - **Old Navy** — value/family positioning
   - **Banana Republic** — premium/professional positioning
   - **GAP** — classic American/mainstream positioning

4. **Renders a live dashboard** with moodboard imagery, trend pills, brand cards, and one-click CSV report downloads for each brand.

5. **Auto-saves reports** to timestamped output directories: JSON, CSV, and plain-text summary files.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Frontend (app.py)            │
│          Dashboard  │  Moodboard  │  Brand Reports       │
└──────────────────────────┬──────────────────────────────┘
                           │  HTTP (port 5000)
┌──────────────────────────▼──────────────────────────────┐
│                 Flask REST API (server.py)                │
│                POST /api/analyze                         │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│            Orchestrator (backend/orchestrator.py)        │
│     asyncio.gather() — all 4 scrapers run in parallel    │
└───────┬──────────┬──────────┬──────────┬────────────────┘
        │          │          │          │
   Pinterest    Zara      Uniqlo      Vogue
   (Selenium  (Crawl4AI  (Crawl4AI  (feedparser
   +thread    +BS4)      +BS4)      +Crawl4AI)
   pool)
        │          │          │          │
┌───────▼──────────▼──────────▼──────────▼────────────────┐
│           AI Analyzer (backend/ai_analyzer.py)           │
│    Trend Analysis  →  Brand Strategies  →  Exec Summary  │
│           All three powered by Groq LLM                  │
└─────────────────────────────────────────────────────────┘
```

---

## Skills Demonstrated

| Skill Area | Details |
|---|---|
| **LLM / AI Integration** | Groq API (Llama 3.3 70B), structured JSON prompt engineering, async LLM calls, graceful fallback handling |
| **Web Scraping** | Selenium headless Chrome, Crawl4AI, BeautifulSoup, RSS feedparser, multi-source parallel scraping |
| **Async Programming** | `asyncio.gather()` for parallel execution, `run_in_executor()` to offload blocking I/O, `get_running_loop()` best practices |
| **REST API Design** | Flask backend with CORS, JSON request/response, error handling, health-check endpoint |
| **Full-Stack Dev** | Streamlit reactive frontend calling a Flask backend — two-process architecture |
| **Data Engineering** | pandas DataFrames, CSV/JSON report generation, timestamped output directories |
| **Prompt Engineering** | Data-grounded prompts feeding real scraped market data into the LLM for analysis |
| **Python Best Practices** | Environment-variable config, `.env` + `python-dotenv`, modular package layout, type hints |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | Flask + Flask-CORS |
| AI / LLM | Groq (Llama 3.3 70B) — free tier |
| Web Scraping | Selenium, Crawl4AI, BeautifulSoup4, feedparser |
| Data | pandas, JSON, CSV |
| Async | asyncio, concurrent.futures thread pool |
| Config | python-dotenv |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Google Chrome installed (for Pinterest Selenium scraper)
- Free API keys (see below)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fashiongpt-studio.git
cd fashiongpt-studio
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
# .env
GROQ_API_KEY=your_groq_key_here       # free at console.groq.com
FIRECRAWL_API_KEY=your_firecrawl_key  # free tier at firecrawl.dev
```

**Getting your Groq key (free, 2 minutes):**
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with email — no credit card required
3. Click **Create API Key** and copy it

### 5. Run the application

Open two terminals:

```bash
# Terminal 1 — Flask backend
python server.py

# Terminal 2 — Streamlit frontend
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. Type a fashion keyword in the search box — e.g. `denim jacket`, `summer dress`, `oversized hoodie`
2. Click **Analyze**
3. The app scrapes all four sources in parallel (~2–3 minutes)
4. Results appear with:
   - Visual moodboard (Pinterest imagery)
   - Trend pills (colors, materials, vibes)
   - Brand-specific strategy cards (Old Navy / Banana Republic / GAP)
   - Download buttons for per-brand CSV reports

---

## Project Structure

```
fashiongpt-studio/
├── app.py                    # Streamlit frontend
├── server.py                 # Flask REST API
├── requirements.txt
├── .env.example              # API key template
│
├── backend/
│   ├── orchestrator.py       # Async pipeline coordinator
│   ├── ai_analyzer.py        # Groq LLM analysis engine
│   └── llm_config.py         # LLM configuration
│
├── scrapers/
│   ├── pinterest_scraper.py  # Selenium headless scraper
│   ├── zara_scraper.py       # Crawl4AI + BeautifulSoup
│   ├── uniqlo_scraper.py     # Crawl4AI + BeautifulSoup
│   ├── vogue_scraper.py      # feedparser + Crawl4AI
│   └── firecrawl_config.py   # Firecrawl API config
│
└── outputs/                  # Auto-generated reports (git-ignored)
    └── {query}_{timestamp}/
        ├── full_report.json
        ├── summary.txt
        ├── trend_analysis.csv
        ├── Old_Navy_report.csv
        ├── Banana_Republic_report.csv
        └── GAP_report.csv
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Run full analysis for a query. Body: `{"query": "denim jacket"}` |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/outputs` | List all saved output directories |

---

## Sample Output

```json
{
  "query": "denim jacket",
  "trend_analysis": {
    "dominant_palette": ["indigo blue", "stone wash", "black", "white", "ecru"],
    "materials": ["premium denim", "stretch cotton", "twill"],
    "aesthetic_vibes": ["casual-cool", "effortless", "versatile"],
    "key_trends": ["oversized silhouettes", "vintage wash", "patch detailing"],
    "market_confidence": "high"
  },
  "old_navy": {
    "summary": "Accessible denim jacket with bold wash options...",
    "colors": ["medium wash", "black", "white"],
    "target": "Value-conscious families and young adults 18–35"
  }
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

Built as a portfolio project demonstrating applied AI, full-stack Python development, and real-world web scraping in a fashion retail context.
