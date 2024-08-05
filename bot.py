import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from dbrequests import add_dish, get_dishes
from initialize_db import init_db

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

# Helper function to create the main menu keyboard
def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Завтраки 🍳", callback_data='show_zavtrak'),
            InlineKeyboardButton("Обеды 🥩", callback_data='show_obed'),
            InlineKeyboardButton("Ужины 🥗", callback_data='show_dinner')
        ],
        [
            InlineKeyboardButton("➕ Добавить блюдо", callback_data='add_dish')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Please choose an option:',
        reply_markup=main_menu_keyboard()
    )

async def show_dishes(update: Update, context: ContextTypes.DEFAULT_TYPE, meal_type: str) -> None:
    dishes = get_dishes(meal_type)
    if dishes:
        await update.callback_query.message.reply_text('\n'.join(dishes), reply_markup=main_menu_keyboard())
    else:
        await update.callback_query.message.reply_text(f'No {meal_type} dishes found.', reply_markup=main_menu_keyboard())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'show_zavtrak':
        await show_dishes(update, context, 'zavtrak')
    elif query.data == 'show_obed':
        await show_dishes(update, context, 'obed')
    elif query.data == 'show_dinner':
        await show_dishes(update, context, 'dinner')
    elif query.data == 'add_dish':
        context.user_data['adding_dish'] = True
        keyboard = [
            [
                InlineKeyboardButton("Zavtrak", callback_data='zavtrak'),
                InlineKeyboardButton("Obed", callback_data='obed'),
                InlineKeyboardButton("Dinner", callback_data='dinner')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Please choose the meal type for the new dish:", reply_markup=reply_markup)
    else:
        # Assume it's a meal type for adding a dish
        context.user_data['meal_type'] = query.data
        await query.edit_message_text(text=f"Selected meal type: {query.data}\nPlease send the dish name.")

async def add_dish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('adding_dish'):
        await update.message.reply_text("Please use the main menu to add a dish.")
        return
    
    meal_type = context.user_data.get('meal_type')
    if not meal_type:
        await update.message.reply_text("Please start by selecting a meal type.")
        return
    
    dish = update.message.text
    add_dish(meal_type, dish)
    await update.message.reply_text(f"{meal_type.capitalize()} dish added: {dish}", reply_markup=main_menu_keyboard())
    context.user_data.clear()

def main() -> None:
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_dish_handler))

    app.run_polling()

if __name__ == '__main__':
    main()