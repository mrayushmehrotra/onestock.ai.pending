from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from agents.orchestrator import OrchestratorAgent
from utils.logger import logger
from utils.alerts import send_telegram_alert
import pytz

IST = pytz.timezone("Asia/Kolkata")

async def run_prediction_job():
    logger.info("Starting scheduled prediction job...")
    # Normally fetch from DB/CSV
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TATAPOWER", "IRFC", "ZOMATO"]
    
    orchestrator = OrchestratorAgent(symbols)
    results = await orchestrator.run()
    
    if results:
        top_picks_str = "\n".join([f"🚀 {p['symbol']} - Score: {p['boom_score']}" for p in results[:5]])
        message = f"<b>OneStock.ai Morning Report</b>\n\nTop Momentum Picks:\n{top_picks_str}"
        await send_telegram_alert(message)
    
    logger.info("Scheduled prediction job completed.")

def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone=IST)
    
    # Run at 9:30 AM IST on weekdays
    scheduler.add_job(
        run_prediction_job,
        CronTrigger(day_of_week="mon-fri", hour=9, minute=30, timezone=IST),
        id="morning_prediction_run",
        name="Morning Prediction Run"
    )

    # Run at 1:00 PM IST on weekdays
    scheduler.add_job(
        run_prediction_job,
        CronTrigger(day_of_week="mon-fri", hour=13, minute=0, timezone=IST),
        id="midday_prediction_run",
        name="Midday Prediction Run"
    )

    return scheduler

if __name__ == "__main__":
    import asyncio
    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started successfully (IST).")
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
