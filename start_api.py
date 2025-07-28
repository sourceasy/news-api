import threading
import time
from api_server import app
from daily_scheduler import start_scheduler

def run_api_server():
    """Run the Flask API server"""
    print("🌐 Starting API server...")
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_scheduler():
    """Run the daily scheduler"""
    print("⏰ Starting daily scheduler...")
    start_scheduler()

def main():
    """Main function to run both API and scheduler"""
    print("🚀 Starting Chemical Industry RSS Monitor System...")
    print("=" * 60)
    print("📡 API Server: http://localhost:5000")
    print("⏰ Scheduler: Daily scrapes at 09:00 and 18:00 IST")
    print("=" * 60)
    
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Wait a bit for initial scrape
    print("⏳ Waiting for initial data scrape...")
    time.sleep(10)
    
    # Start API server
    run_api_server()

if __name__ == '__main__':
    main() 