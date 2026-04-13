import httpx
from config.settings import settings
from utils.logger import logger

async def send_telegram_alert(message: str):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            logger.info("Telegram alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")

async def send_email_alert(subject: str, body: str):
    # Placeholder for email alert implementation
    logger.info(f"Email alert placeholder: {subject}")
