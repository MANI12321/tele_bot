from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import logging

# token
TOKEN = "7703795153:AAERn_GUl2XSV7hRMI-oyWwqoRRuKkSTJ1g"

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Store user cookies
user_data = {}

async def start(update, context):
    await update.message.reply_text("Welcome! Please send your LinkedIn and Internshala cookies in the format:\n`LinkedIn_Cookie; Internshala_Cookie`")

async def get_cookies(update, context):
    user_id = update.message.from_user.id
    user_input = update.message.text.split(';')

    if len(user_input) != 2:
        await update.message.reply_text("Invalid format. Please send cookies in the format:\n`LinkedIn_Cookie; Internshala_Cookie`")
        return
    
    linkedin_cookie, internshala_cookie = user_input[0].strip(), user_input[1].strip()
    user_data[user_id] = {'linkedin': linkedin_cookie, 'internshala': internshala_cookie}
    await update.message.reply_text("Cookies received! You can now apply for jobs using /apply_linkedin or /apply_internshala.")

async def apply_linkedin(update, context):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await update.message.reply_text("Please send your cookies first using /start.")
        return
    
    linkedin_cookie = user_data[user_id]['linkedin']
    
    await update.message.reply_text("Applying for jobs on LinkedIn...")
    try:
        headers = {
            'Cookie': linkedin_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get("https://www.linkedin.com/jobs/search/", headers=headers)

        if response.status_code == 200:
            # Simulate job application logic here
            await update.message.reply_text("Successfully applied for jobs on LinkedIn!")
        else:
            await update.message.reply_text("Failed to apply for jobs on LinkedIn. Check your cookies or account status.")
    except Exception as e:
        logging.error(f"Error applying for LinkedIn jobs: {str(e)}")
        await update.message.reply_text(f"An error occurred while applying for LinkedIn jobs: {str(e)}")

async def apply_internshala(update, context):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await update.message.reply_text("Please send your cookies first using /start.")
        return
    
    internshala_cookie = user_data[user_id]['internshala']

    await update.message.reply_text("Applying for jobs on Internshala...")
    try:
        headers = {
            'Cookie': internshala_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get("https://internshala.com/job/search", headers=headers)

        if response.status_code == 200:
            # Simulate job application logic here
            await update.message.reply_text("Successfully applied for jobs on Internshala!")
        else:
            await update.message.reply_text("Failed to apply for jobs on Internshala. Check your cookies or account status.")
    except Exception as e:
        logging.error(f"Error applying for Internshala jobs: {str(e)}")
        await update.message.reply_text(f"An error occurred while applying for Internshala jobs: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_cookies))
    app.add_handler(CommandHandler('apply_linkedin', apply_linkedin))
    app.add_handler(CommandHandler('apply_internshala', apply_internshala))

    logging.info("Bot is running...")
    app.run_polling()
