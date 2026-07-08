"""
Web server for Render.com deployment
Keeps the bot alive and provides health check endpoint
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

bot_task = None


async def run_bot_polling():
    """Run the telegram bot in polling mode in background"""
    from bot.main import build_application, init_database
    from bot.utils import setup_logging

    setup_logging()
    logger.info("Initializing database...")
    await init_database()

    logger.info("Building application...")
    application = build_application()

    logger.info("Starting bot polling...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(
        allowed_updates=["message", "callback_query"]
    )

    # Keep running until cancelled
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage bot startup and shutdown"""
    global bot_task
    logger.info("Starting bot in background...")
    bot_task = asyncio.create_task(run_bot_polling())
    yield
    logger.info("Shutting down bot...")
    if bot_task:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Game Store Bot",
    description="Telegram Bot API Server",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "status": "running",
            "service": "Game Store Telegram Bot",
            "version": "1.0.0",
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return JSONResponse(
        content={
            "status": "healthy",
            "bot_running": bot_task is not None and not bot_task.done(),
        }
    )


@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return JSONResponse(content={"message": "pong"})
