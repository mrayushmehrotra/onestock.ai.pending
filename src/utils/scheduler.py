import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.scrapers.manager import ScraperManager
import json
import os
from datetime import datetime

class NewsScheduler:
    def __init__(self, interval_hours: int = 4):
        self.scheduler = AsyncIOScheduler()
        self.manager = ScraperManager()
        self.interval_hours = interval_hours
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    async def scrape_job(self):
        print(f"[{datetime.now()}] Starting scheduled scraping job...")
        news = await self.manager.run_all()
        
        # For now, we save to a JSON file as we haven't set up the DB fully
        filename = os.path.join(self.data_dir, "scraped_news.json")
        
        existing_data = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []

        # Merge and deduplicate
        existing_urls = {item['url'] for item in existing_data}
        new_items = [item for item in news if item['url'] not in existing_urls]
        
        all_data = existing_data + new_items
        
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
        
        print(f"[{datetime.now()}] Job complete. Added {len(new_items)} new items. Total: {len(all_data)}")

    def start(self):
        self.scheduler.add_job(self.scrape_job, 'interval', hours=self.interval_hours)
        self.scheduler.start()
        print(f"Scheduler started. Running every {self.interval_hours} hours.")

if __name__ == "__main__":
    # To test immediately
    async def run_now():
        sched = NewsScheduler()
        await sched.scrape_job()
        
    asyncio.run(run_now())
