import schedule
import time
import json
from datetime import datetime, timedelta
import pytz
from fix_all_feeds import scrape_all_sources, CHEMICAL_KEYWORDS
import os

def daily_rss_job():
    """Daily job to scrape RSS feeds and save data"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    print(f"🕐 [{now.strftime('%Y-%m-%d %H:%M:%S')}] Starting daily RSS scrape...")
    
    try:
        # Run the RSS scrape
        scrape_all_sources()
        
        # Read the scraped data and convert to JSON
        with open('all_sources_data.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse articles
        articles = []
        lines = content.split('\n')
        current_article = {}
        current_source = "Unknown"
        
        for line in lines:
            if line.startswith('SOURCE: '):
                current_source = line.replace('SOURCE: ', '')
            elif line.startswith('ARTICLE '):
                if current_article and 'title' in current_article:
                    current_article['source'] = current_source
                    articles.append(current_article)
                current_article = {}
            elif line.startswith('Title: '):
                current_article['title'] = line.replace('Title: ', '')
            elif line.startswith('Link: '):
                current_article['link'] = line.replace('Link: ', '')
            elif line.startswith('Published: '):
                current_article['published'] = line.replace('Published: ', '')
            elif line.startswith('🏷️ Categories: '):
                current_article['categories'] = line.replace('🏷️ Categories: ', '').split(', ')
            elif line.startswith('Summary: '):
                current_article['summary'] = line.replace('Summary: ', '')
        
        # Add the last article
        if current_article and 'title' in current_article:
            current_article['source'] = current_source
            articles.append(current_article)
        
        # Filter out articles without titles
        articles = [a for a in articles if 'title' in a and a['title'] != 'No title']
        
        # Create daily data structure
        daily_data = {
            'date': now.strftime('%Y-%m-%d'),
            'timestamp': now.isoformat(),
            'articles': articles,
            'summary': {
                'total_articles': len(articles),
                'sources': list(set([a.get('source', 'Unknown') for a in articles])),
                'categories_found': list(set([cat for a in articles if 'categories' in a for cat in a['categories']]))
            }
        }
        
        # Save to daily JSON file
        filename = f"daily_data_{now.strftime('%Y-%m-%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, indent=2, ensure_ascii=False)
        
        # Save to latest.json (always updated)
        with open('latest.json', 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ [{now.strftime('%H:%M:%S')}] Daily scrape completed!")
        print(f"📊 Articles found: {len(articles)}")
        print(f"📁 Saved to: {filename} and latest.json")
        
        # Clean up old files (keep last 30 days)
        cleanup_old_files()
        
    except Exception as e:
        print(f"❌ [{now.strftime('%H:%M:%S')}] Error in daily job: {e}")

def cleanup_old_files():
    """Clean up old daily files (keep last 30 days)"""
    try:
        files = [f for f in os.listdir('.') if f.startswith('daily_data_') and f.endswith('.json')]
        files.sort()
        
        # Keep only last 30 files
        if len(files) > 30:
            files_to_delete = files[:-30]
            for file in files_to_delete:
                os.remove(file)
                print(f"🗑️ Deleted old file: {file}")
    except Exception as e:
        print(f"⚠️ Error cleaning up files: {e}")

def run_manual_scrape():
    """Manual function to run scrape immediately"""
    print("🔄 Running manual scrape...")
    daily_rss_job()

def start_scheduler():
    """Start the daily scheduler"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    print("🚀 Starting Chemical Industry RSS Monitor Scheduler...")
    print(f"📅 Current time (IST): {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("⏰ Scheduled jobs:")
    print("   - Daily scrape at 09:00 IST")
    print("   - Daily scrape at 18:00 IST")
    print("   - Manual refresh available")
    
    # Schedule daily jobs
    schedule.every().day.at("09:00").do(daily_rss_job)  # Morning scrape
    schedule.every().day.at("18:00").do(daily_rss_job)  # Evening scrape
    
    # Run initial scrape
    print("🔄 Running initial scrape...")
    daily_rss_job()
    
    print("⏳ Waiting for scheduled jobs...")
    print("💡 Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--manual':
        run_manual_scrape()
    else:
        start_scheduler() 