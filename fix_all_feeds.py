import feedparser
import requests
from datetime import datetime
import pytz
import time

# Multiple RSS feed URLs to try for each source
RSS_FEEDS = {
    'Economic Times': [
        'https://economictimes.indiatimes.com/rssfeedstopstories.cms',
        'https://economictimes.indiatimes.com/rssfeedbusiness.cms',
        'https://economictimes.indiatimes.com/rssfeedmarkets.cms',
        'https://economictimes.indiatimes.com/rssfeedcompanies.cms',
    ],
    'Business Standard': [
        'https://www.business-standard.com/rss/current/rss.xml',
        'https://www.business-standard.com/rss/companies-101.rss',
        'https://www.business-standard.com/rss/markets-102.rss',
        'https://www.business-standard.com/rss/economy-policy-103.rss',
    ],
    'Financial Express': [
        'https://www.financialexpress.com/feed/',
        'https://www.financialexpress.com/feed/rss',
        'https://www.financialexpress.com/feed/xml',
    ],
    'Money Control': [
        'https://www.moneycontrol.com/rss/business.xml',
        'https://www.moneycontrol.com/rss/companies.xml',
        'https://www.moneycontrol.com/rss/markets.xml',
    ],
    'Livemint': [
        'https://www.livemint.com/rss/companies',
        'https://www.livemint.com/rss/markets',
        'https://www.livemint.com/rss/technology',
    ],
    'IndianChemicalNews': [
        'https://www.indianchemicalnews.com/feed',
        'https://www.indianchemicalnews.com/rss',
        'https://www.indianchemicalnews.com/rss.xml',
        'http://www.indianchemicalnews.com/feed',  # HTTP version
    ],
    'Chemindigest': [
        'https://chemindigest.com/feed',
        'https://chemindigest.com/rss',
        'https://chemindigest.com/rss.xml',
        'http://chemindigest.com/feed',  # HTTP version
    ],
    'Chemical Weekly': [
        'https://chemicalweekly.com/feed/',
        'https://chemicalweekly.com/rss',
        'https://chemicalweekly.com/rss.xml',
    ],
    'ICIS News': [
        'https://www.icis.com/explore/resources/news/feed/',
        'https://www.icis.com/explore/resources/news/rss',
    ],
    'Chemical & Engineering News': [
        'https://cen.acs.org/rss.xml',
        'https://cen.acs.org/feed',
    ],
    'Platts': [
        'https://www.spglobal.com/platts/en/feed',
        'https://www.spglobal.com/platts/en/rss',
    ],
    'Reuters': [
        'https://feeds.reuters.com/reuters/businessNews',
        'https://feeds.reuters.com/reuters/technologyNews',
        'https://feeds.reuters.com/reuters/scienceNews',
        'http://feeds.reuters.com/reuters/businessNews',  # HTTP version
    ],
    'ChemistryWorld': [
        'https://www.chemistryworld.com/rss/feed',
        'https://www.chemistryworld.com/feed',
        'https://www.chemistryworld.com/rss.xml',
        'http://www.chemistryworld.com/rss/feed',  # HTTP version
    ]
}

# Enhanced keywords for chemical industry news including pricing
CHEMICAL_KEYWORDS = {
    'Chemical Pricing': [
        'price', 'pricing', 'cost', 'rate', 'per kg', 'per ton', 'per litre',
        'price hike', 'price increase', 'price rise', 'price surge',
        'price drop', 'price fall', 'price decline', 'price reduction',
        'market price', 'spot price', 'contract price', 'export price',
        'import price', 'domestic price', 'international price'
    ],
    'Supply & Demand': [
        'shortage', 'supply constraint', 'supply chain', 'demand surge',
        'high demand', 'demand increase', 'supply shortage', 'supply gap',
        'inventory', 'stock', 'production capacity', 'capacity expansion',
        'production increase', 'production decrease'
    ],
    'Chemical Products': [
        'acetic acid', 'methanol', 'aniline', 'ethylene', 'propylene',
        'benzene', 'toluene', 'xylene', 'ammonia', 'urea', 'fertilizer',
        'polymer', 'plastic', 'petrochemical', 'specialty chemical',
        'agrochemical', 'pharmaceutical', 'dye', 'paint', 'coating',
        'solvent', 'catalyst', 'additive', 'surfactant'
    ],
    'Business News': [
        'acquisition', 'merger', 'joint venture', 'investment', 'expansion',
        'plant', 'facility', 'manufacturing', 'production', 'capacity',
        'shutdown', 'layoff', 'job cut', 'restructuring', 'bankruptcy'
    ],
    'Innovation & Discovery': [
        'discovery', 'innovation', 'breakthrough', 'new technology',
        'patent', 'research', 'development', 'R&D', 'new product',
        'green chemistry', 'sustainable', 'bio-based', 'renewable'
    ],
    'Events & Conferences': [
        'seminar', 'conference', 'exhibition', 'event', 'summit',
        'workshop', 'symposium', 'trade show', 'expo'
    ],
    'Regulatory': [
        'regulation', 'compliance', 'QCO', 'BIS', 'certification',
        'standard', 'policy', 'government', 'ministry', 'authority'
    ]
}

def try_feed_with_headers(url, source_name):
    """Try different headers and approaches to access RSS feeds"""
    headers_list = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
        {'User-Agent': 'Mozilla/5.0 (compatible; RSSReader/1.0)'},
        {'User-Agent': 'FeedParser/6.0.10'},
        {}  # No headers
    ]
    
    for headers in headers_list:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    return True, feed, response.status_code
        except Exception as e:
            continue
    
    return False, None, None

def classify_chemical_news(title, summary):
    """Classify news articles using enhanced chemical industry keywords"""
    txt = (title + ' ' + summary).lower()
    classifications = []
    
    for category, keywords in CHEMICAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in txt:
                classifications.append(category)
                break  # Found one keyword for this category
    
    return classifications

def scrape_all_sources():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    with open('all_sources_data.txt', 'w', encoding='utf-8') as f:
        f.write(f"COMPREHENSIVE RSS SCRAPE - {now}\n")
        f.write("=" * 80 + "\n\n")
        
        total_articles = 0
        classified_articles = 0
        
        for source, urls in RSS_FEEDS.items():
            f.write(f"SOURCE: {source}\n")
            f.write("=" * 50 + "\n")
            
            source_articles = 0
            working_url = None
            
            for url in urls:
                f.write(f"Trying: {url}\n")
                
                success, feed, status = try_feed_with_headers(url, source)
                
                if success and feed and feed.entries:
                    f.write(f"✅ SUCCESS! Status: {status}\n")
                    f.write(f"📰 Total Entries: {len(feed.entries)}\n\n")
                    
                    working_url = url
                    
                    # Get ALL articles (no limit)
                    for i, entry in enumerate(feed.entries, 1):
                        title = entry.get('title', 'No title')
                        summary = entry.get('summary', '')
                        
                        # Classify the article
                        classifications = classify_chemical_news(title, summary)
                        
                        f.write(f"ARTICLE {i}:\n")
                        f.write(f"Title: {title}\n")
                        f.write(f"Link: {entry.get('link', 'No link')}\n")
                        f.write(f"Published: {entry.get('published', 'No date')}\n")
                        
                        if classifications:
                            f.write(f"🏷️ Categories: {', '.join(classifications)}\n")
                            classified_articles += 1
                        
                        # Get summary if available
                        if summary:
                            f.write(f"Summary: {summary[:200]}...\n")
                        
                        f.write("\n")
                        source_articles += 1
                    
                    break  # Found working URL, stop trying others
                else:
                    f.write(f"❌ Failed (Status: {status if status else 'Error'})\n")
            
            if working_url:
                f.write(f"✅ {source}: Working URL found - {working_url}\n")
                f.write(f"📊 Articles collected: {source_articles}\n")
                total_articles += source_articles
            else:
                f.write(f"❌ {source}: No working URLs found\n")
            
            f.write("\n" + "-" * 80 + "\n\n")
        
        f.write(f"FINAL SUMMARY:\n")
        f.write(f"Total articles collected: {total_articles}\n")
        f.write(f"Chemical industry relevant articles: {classified_articles}\n")
        f.write(f"Timestamp: {now}\n")
    
    print(f"✅ Comprehensive scrape completed! Found {total_articles} articles in all_sources_data.txt")

if __name__ == '__main__':
    scrape_all_sources() 