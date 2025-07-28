from api_server import app
import os
import threading
from daily_scheduler import start_scheduler

def run_scheduler():
    """Run the daily scheduler in background"""
    start_scheduler()

if __name__ == '__main__':
    # Production settings
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Production Chemical Industry RSS Monitor API...")
    print(f"📡 Port: {port}")
    print(f"🐛 Debug: {debug}")
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start API server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    ) 