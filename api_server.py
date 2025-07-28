from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import pytz
from fix_all_feeds import scrape_all_sources, CHEMICAL_KEYWORDS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Global variable to store latest data
latest_data = {
    'articles': [],
    'summary': {},
    'last_updated': None
}

def get_latest_data():
    """Get the latest RSS data"""
    global latest_data
    
    # Check if data is fresh (less than 1 hour old)
    if latest_data['last_updated']:
        time_diff = datetime.now() - latest_data['last_updated']
        if time_diff.total_seconds() < 3600:  # 1 hour
            return latest_data
    
    # Run fresh scrape
    try:
        scrape_all_sources()
        
        # Read the scraped data
        with open('all_sources_data.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the data (simplified version)
        articles = []
        lines = content.split('\n')
        current_article = {}
        
        for line in lines:
            if line.startswith('ARTICLE '):
                if current_article:
                    articles.append(current_article)
                current_article = {'source': 'Unknown'}
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
        
        if current_article:
            articles.append(current_article)
        
        # Filter out articles without titles
        articles = [a for a in articles if 'title' in a and a['title'] != 'No title']
        
        latest_data = {
            'articles': articles,
            'summary': {
                'total_articles': len(articles),
                'sources': ['Economic Times', 'Business Standard', 'Money Control', 'Livemint', 'Indian Chemical News', 'Chemindigest'],
                'last_updated': datetime.now().isoformat()
            },
            'last_updated': datetime.now()
        }
        
        return latest_data
        
    except Exception as e:
        return {
            'error': str(e),
            'articles': [],
            'summary': {},
            'last_updated': datetime.now().isoformat()
        }

@app.route('/')
def home():
    """API home page"""
    return jsonify({
        'message': 'Chemical Industry RSS Monitor API',
        'endpoints': {
            '/': 'This help page',
            '/api/news': 'Get all news articles',
            '/api/news?category=pricing': 'Filter by category',
            '/api/news?source=Economic Times': 'Filter by source',
            '/api/summary': 'Get summary statistics',
            '/api/categories': 'Get available categories',
            '/api/sources': 'Get available sources'
        },
        'usage': 'Add ?category=CATEGORY or ?source=SOURCE to filter results'
    })

@app.route('/api/news')
def get_news():
    """Get news articles with optional filtering"""
    data = get_latest_data()
    
    if 'error' in data:
        return jsonify(data), 500
    
    articles = data['articles']
    
    # Filter by category
    category = request.args.get('category', '').lower()
    if category:
        articles = [a for a in articles if 'categories' in a and any(cat.lower() == category for cat in a['categories'])]
    
    # Filter by source
    source = request.args.get('source', '')
    if source:
        articles = [a for a in articles if 'source' in a and source.lower() in a['source'].lower()]
    
    # Limit results
    limit = request.args.get('limit', 50, type=int)
    articles = articles[:limit]
    
    return jsonify({
        'articles': articles,
        'count': len(articles),
        'filters_applied': {
            'category': category if category else None,
            'source': source if source else None,
            'limit': limit
        },
        'last_updated': data['summary']['last_updated']
    })

@app.route('/api/summary')
def get_summary():
    """Get summary statistics"""
    data = get_latest_data()
    
    if 'error' in data:
        return jsonify(data), 500
    
    # Count articles by category
    category_counts = {}
    source_counts = {}
    
    for article in data['articles']:
        if 'categories' in article:
            for cat in article['categories']:
                category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if 'source' in article:
            source_counts[article['source']] = source_counts.get(article['source'], 0) + 1
    
    return jsonify({
        'total_articles': len(data['articles']),
        'category_breakdown': category_counts,
        'source_breakdown': source_counts,
        'last_updated': data['summary']['last_updated']
    })

@app.route('/api/categories')
def get_categories():
    """Get available categories"""
    return jsonify({
        'categories': list(CHEMICAL_KEYWORDS.keys()),
        'description': 'Available categories for filtering news articles'
    })

@app.route('/api/sources')
def get_sources():
    """Get available sources"""
    return jsonify({
        'sources': [
            'Economic Times',
            'Business Standard', 
            'Money Control',
            'Livemint',
            'Indian Chemical News',
            'Chemindigest'
        ],
        'description': 'Available news sources'
    })

@app.route('/api/refresh')
def refresh_data():
    """Manually trigger a data refresh"""
    global latest_data
    latest_data['last_updated'] = None  # Force refresh
    data = get_latest_data()
    return jsonify({
        'message': 'Data refreshed successfully',
        'articles_count': len(data['articles']),
        'last_updated': data['summary']['last_updated']
    })

if __name__ == '__main__':
    print("🚀 Starting Chemical Industry RSS Monitor API...")
    print("📡 API will be available at: http://localhost:5000")
    print("📊 Endpoints:")
    print("   - GET /api/news - Get all articles")
    print("   - GET /api/news?category=pricing - Filter by category")
    print("   - GET /api/summary - Get statistics")
    print("   - GET /api/refresh - Force refresh data")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 