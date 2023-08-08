
"""
Written by Seedorfe
"""

import telegram
import telegram.ext as ext
import asyncio



import config
import databace



app = ext.Application.builder().token(config.BOT_TOKEN).build()
bot = app.bot



async def start_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() != inp.effective_message.chat_id:
        databace.set_admin_CHAT_ID(inp.effective_message.chat_id)
        await bot.send_message(inp.effective_message.chat_id, "hi u are not admin")
    else:
        await bot.send_message(inp.effective_message.chat_id, "hi u are  admin!!!!")

    



def run_bot():
    '''run bot'''

    # app = ext.Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(ext.CommandHandler("start", start_command))

    # bot = app.bot

    app.run_polling()

