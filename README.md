# Chemical Industry RSS Monitor

A comprehensive RSS monitoring system for Indian chemical industry news with automated daily updates and REST API.

## 🚀 Features

- **6 RSS Sources**: Economic Times, Business Standard, Money Control, Livemint, Indian Chemical News, Chemindigest
- **Smart Categorization**: Chemical pricing, supply & demand, business news, innovations, events, regulatory updates
- **Daily Automation**: Automatic scraping at 09:00 and 18:00 IST
- **REST API**: Query news by category, source, or get summaries
- **JSON Data**: Structured data output for easy integration

## 📊 Current Coverage

- **Total Articles**: ~200 daily
- **Chemical Industry Relevant**: ~100 articles (51% hit rate)
- **Categories**: Chemical Pricing, Supply & Demand, Chemical Products, Business News, Innovation & Discovery, Events & Conferences, Regulatory

## 🛠️ Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the System**:
```bash
python start_api.py
```

## 📡 API Endpoints

### Base URL: `http://localhost:5000`

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/` | API help page | `GET /` |
| `/api/news` | Get all articles | `GET /api/news` |
| `/api/news?category=pricing` | Filter by category | `GET /api/news?category=Chemical Pricing` |
| `/api/news?source=Economic Times` | Filter by source | `GET /api/news?source=Economic Times` |
| `/api/news?limit=10` | Limit results | `GET /api/news?limit=10` |
| `/api/summary` | Get statistics | `GET /api/summary` |
| `/api/categories` | Available categories | `GET /api/categories` |
| `/api/sources` | Available sources | `GET /api/sources` |
| `/api/refresh` | Force refresh data | `GET /api/refresh` |

## 🔧 Usage Examples

### 1. Get All News
```bash
curl http://localhost:5000/api/news
```

### 2. Get Chemical Pricing News
```bash
curl "http://localhost:5000/api/news?category=Chemical Pricing"
```

### 3. Get Business News from Economic Times
```bash
curl "http://localhost:5000/api/news?source=Economic Times&category=Business News"
```

### 4. Get Summary Statistics
```bash
curl http://localhost:5000/api/summary
```

### 5. Python Integration
```python
import requests

# Get all articles
response = requests.get('http://localhost:5000/api/news')
articles = response.json()['articles']

# Get pricing news
response = requests.get('http://localhost:5000/api/news?category=Chemical Pricing')
pricing_news = response.json()['articles']

# Get summary
response = requests.get('http://localhost:5000/api/summary')
summary = response.json()
```

## 📁 File Structure

```
Weekly_Reports/
├── fix_all_feeds.py          # Main RSS scraper
├── api_server.py             # Flask API server
├── daily_scheduler.py        # Daily automation
├── start_api.py              # Startup script
├── requirements.txt          # Dependencies
├── latest.json              # Latest data (auto-generated)
├── daily_data_YYYY-MM-DD.json # Daily snapshots
└── all_sources_data.txt     # Raw scraped data
```

## ⏰ Automation

The system runs automatically:
- **09:00 IST**: Morning scrape
- **18:00 IST**: Evening scrape
- **Manual**: Run `python daily_scheduler.py --manual`

## 📊 Data Format

### Article Structure
```json
{
  "title": "Article Title",
  "link": "https://example.com/article",
  "published": "Mon, 28 Jul 2025 06:30:00 +0530",
  "source": "Economic Times",
  "categories": ["Chemical Pricing", "Business News"],
  "summary": "Article summary..."
}
```

### Summary Structure
```json
{
  "total_articles": 196,
  "category_breakdown": {
    "Chemical Pricing": 15,
    "Business News": 25,
    "Innovation & Discovery": 8
  },
  "source_breakdown": {
    "Economic Times": 51,
    "Indian Chemical News": 50
  },
  "last_updated": "2025-07-28T13:25:32.458067+05:30"
}
```

## 🎯 Categories

- **Chemical Pricing**: Price updates, market rates, cost changes
- **Supply & Demand**: Shortages, capacity expansions, production changes
- **Chemical Products**: Specific chemicals (acetic acid, methanol, etc.)
- **Business News**: Acquisitions, investments, expansions, layoffs
- **Innovation & Discovery**: Patents, R&D, new technologies
- **Events & Conferences**: Seminars, exhibitions, trade shows
- **Regulatory**: QCOs, BIS, government policies

## 🔍 Sources

- **Economic Times**: Business & financial news
- **Business Standard**: Indian business news
- **Money Control**: Markets & companies
- **Livemint**: Companies & technology
- **Indian Chemical News**: Chemical industry specific
- **Chemindigest**: Chemical industry news

## 🚀 Deployment

### Local Development
```bash
python start_api.py
```

### Production (with gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

### Docker (optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "start_api.py"]
```

## 📈 Monitoring

- Check `latest.json` for current data
- Monitor daily files for historical data
- API health check: `GET /api/summary`

## 🔧 Troubleshooting

1. **API not responding**: Check if port 5000 is free
2. **No data**: Run manual scrape with `python daily_scheduler.py --manual`
3. **RSS errors**: Check network connectivity and feed URLs
4. **Memory issues**: Reduce article limit in API calls

## 📝 License

This project is open source and available under the MIT License. 