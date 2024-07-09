import json
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler, MessageHandler, filters
import logging
import os
from weather_api import get_weather_forecast, format_weather_info
from dotenv import load_dotenv

load_dotenv()
TELE_TOKEN = os.getenv("TELE_TOKEN")


logging.basicConfig(format="App Started Info %(asctime)s - %(name)s - %(levelname)s- %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.full_name)

    msg = (f" Hello {update.effective_user.first_name}! \n\n"
           "This is the Weather Forecast telegram bot for testing purposes.☁️\n\n"
           "You first need to send your Location.")
    
    # Keyboard for requesting location
    location_keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    location_markup = ReplyKeyboardMarkup(location_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(msg, reply_markup=location_markup)

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location

    #float data type returned
    lat = user_location.latitude
    lon = user_location.longitude

    today_data = json.dumps({'lat': lat, 'lon': lon, 'action': 'today'})
    forecast_data = json.dumps({'lat': lat, 'lon': lon, 'action': 'forecast'})

    keyboard = [ 
        [InlineKeyboardButton("Today Weather", callback_data=today_data),
         InlineKeyboardButton("Forecast for next 7 days", callback_data=forecast_data)]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup= reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = json.loads(query.data)
    lat = data['lat']
    lon = data['lon']
    action = data['action']

    weather_info = get_weather_forecast(lat = lat, lon = lon, action = action)

    weather_msg = format_weather_info(weather_info)

    await query.edit_message_text(text=f"Selected option: {action.capitalize()}\n\nWeather Info:\n{weather_msg}")

async def help_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = "Use /start to test this bot. \nUse /help to get help information."
    await update.message.reply_text(msg)

def main() -> None:
    app = ApplicationBuilder().token(TELE_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", help_msg))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
