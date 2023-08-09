
"""
Written by Seedorfe
"""

import telegram
import telegram.ext as ext
import asyncio
from moviepy import editor
import os


import init
import config
import databace



app = ext.Application.builder().token(config.BOT_TOKEN).build()

bot = app.bot



async def start_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == 0:
        _key_board = [[telegram.InlineKeyboardButton(text="شروع به عنوان ادمین", callback_data="set_admin")]]
        await bot.send_message(inp.effective_message.chat_id, "برای شروع کار بر روی دکمه زیر کلیک کنید", 
            reply_markup=telegram.InlineKeyboardMarkup(_key_board))
    elif databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        await bot.send_message(inp.effective_message.chat_id, "سلام ادمین جون")
    else:
        pass # do nothing



async def button_quary_handler(inp : telegram.Update, context : ext.CallbackContext):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        pass
    else:
        if inp.callback_query.data == "set_admin" and databace.get_admin_CHAT_ID() == 0:
            databace.set_admin_CHAT_ID(inp.effective_message.chat_id)
            await bot.send_message(inp.effective_message.chat_id, "شما ادمین شدید")
            


async def watermark(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        await bot.send_message(inp.effective_message.chat_id, "فایل در حان دانلود")
        # await bot.send_message(inp.effective_message.chat_id, inp.message.effective_attachment.address)
        _file = await inp.message.effective_attachment.get_file()

        _file_name = _file.file_path.split("/")
        _file_name = _file_name[-1]
        await _file.download_to_drive(config.ROOT_PATH + "/file/" + _file_name)
        # await bot.send_message(inp.effective_message.chat_id, _file_name)
        await bot.send_message(inp.effective_message.chat_id, "فایل دانلود شد")


        for _ in init.get_files("/file"):

            os.chdir(config.ROOT_PATH + "/temp")

            _temp_bot_1 = editor.VideoFileClip(config.ROOT_PATH + "/file/" + _)

            _temp_bot_2 = editor.TextClip(
                txt = "watermark",
                fontsize=50,
                color="white"
            )
            _temp_bot_2 = _temp_bot_2.set_position("center", "center")
            _temp_bot_2 = _temp_bot_2.set_opacity(0.5)
            _temp_bot_2 = _temp_bot_2.set_duration(10)


            _temp_bot_video = editor.CompositeVideoClip([_temp_bot_1, _temp_bot_2]).set_duration(_temp_bot_1.duration)
            _temp_bot_video.write_videofile(config.ROOT_PATH + "/export/" + _)

            await bot.send_video(inp.effective_message.chat_id, config.ROOT_PATH + "/export/" + _)
            await bot.send_message(inp.effective_message.chat_id, "فایل مارک آپ شده آپلود شد")

    pass



async def video_handler(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        if len(init.get_files("/file")) < 3:
            await bot.send_message(inp.effective_message.chat_id, "فایل در حان دانلود")
            # await bot.send_message(inp.effective_message.chat_id, inp.message.effective_attachment.address)
            _file = await inp.message.effective_attachment.get_file()

            _file_name = _file.file_path.split("/")
            _file_name = _file_name[-1]
            await _file.download_to_drive(config.ROOT_PATH + "/file/" + _file_name)
            # await bot.send_message(inp.effective_message.chat_id, _file_name)
            await bot.send_message(inp.effective_message.chat_id, "فایل دانلود شد")

            if len(init.get_files("/file")) >= 3:
                await bot.send_message(inp.effective_message.chat_id,"شما صد ویدعو آپلود کردید و بامحدودیت صد ویدعو مواجه شدید لطفا پردازش را شروع کنید")

        else:
            await bot.send_message(inp.effective_message.chat_id, "شما بامحدودیت آپلود ویدعو مواجه شدید لطفا پردازش را شروع کنید")
    else:
        pass # do nothing







async def process_watermark(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        os.chdir(config.ROOT_PATH + "/temp")

        for _ in init.get_files("/file"):

            _temp_bot_1 = editor.VideoFileClip(config.ROOT_PATH + "/file/" + _)

            _temp_bot_2 = editor.TextClip(
                txt = "watermark",
                fontsize=50,
                color="white"
            )

            _temp_bot_2 = _temp_bot_2.set_position("center", "center")
            _temp_bot_2 = _temp_bot_2.set_opacity(0.5)
            _temp_bot_2 = _temp_bot_2.set_duration(10)


            _temp_bot_video = editor.CompositeVideoClip([_temp_bot_1, _temp_bot_2]).set_duration(_temp_bot_1.duration)
            _temp_bot_video.write_videofile(config.ROOT_PATH + "/export/" + _)

            await bot.send_video(inp.effective_message.chat_id, config.ROOT_PATH + "/export/" + _)
            await bot.send_message(inp.effective_message.chat_id, "فایل مارک آپ شده آپلود شد")

            init.clear_files("/export")
            init.delete_file("/file", _)



        pass
    else:
        pass # do nothing
    






def run_bot():
    '''run bot'''

    # app = ext.Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(ext.CommandHandler("start", start_command))
    app.add_handler(ext.CallbackQueryHandler(button_quary_handler))
    app.add_handler(ext.MessageHandler(ext.filters.VIDEO, video_handler))
    app.add_handler(ext.CommandHandler("process", process_watermark))
    

    # bot = app.bot

    app.run_polling()

