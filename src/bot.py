
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


main_menu = [
        [telegram.KeyboardButton(config.message_commands["process"]), telegram.KeyboardButton(config.message_commands["status"])],
        [telegram.KeyboardButton(config.message_commands["options"]), telegram.KeyboardButton(config.message_commands["help"])]
]



watermark_options_menu = [
    [telegram.KeyboardButton(config.message_commands["watermark_text"]),telegram.KeyboardButton(config.options_text_commands["position"])],
    [telegram.KeyboardButton(config.message_commands["cancel"])]
]





def _set_bot_mode(mode):
    config.get_bot_mode = config.bot_modes[mode]

def _get_bot_mode():
    return config.get_bot_mode




async def start_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == 0:

        # _key_board = [[telegram.InlineKeyboardButton(text="شروع به عنوان ادمین", callback_data="set_admin")]]
        # await bot.send_message(inp.effective_message.chat_id, "برای شروع کار بر روی دکمه زیر کلیک کنید", 
        #     reply_markup=telegram.InlineKeyboardMarkup(_key_board))

        _key_board = [[telegram.KeyboardButton(config.message_commands["set_admin"])]]

        await bot.send_message(inp.effective_message.chat_id, "برای شروع کار بر روی دکمه کلیک کنید",
            reply_markup = telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
        )
            

    elif databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:


        # _key_board = [
        #     [telegram.KeyboardButton(config.message_commands["process"]), telegram.KeyboardButton(config.message_commands["status"])],
        #     [telegram.KeyboardButton(config.message_commands["options"]), telegram.KeyboardButton(config.message_commands["help"])]
        # ]


        # await bot.send_message(inp.effective_message.chat_id, "سلام ادمین جون",
        # reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
        # )

        await bot.send_message(inp.effective_message.chat_id, config.bot_messages["main_menu"],
        reply_markup=telegram.ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        
        
 
    else:
        pass # do nothing






async def button_quary_handler(inp : telegram.Update, context : ext.CallbackContext):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        if inp.callback_query.data == config.message_commands["cancel"]:

            if _get_bot_mode() == config.bot_modes["set_watermark_text"]:
                _set_bot_mode("standby")
                    
            # _key_board = [
            #     [telegram.KeyboardButton(config.message_commands["watermark_text"])],
            #     [telegram.KeyboardButton(config.message_commands["cancel"])]
            # ]

            
            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["watermark_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )

        
        pass
    else:
        pass # do nothing
            


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
        if len(init.get_files("/file")) < config.PROCESS_UPLOAD_FILE_LIMIT:
            # await bot.send_message(inp.effective_message.chat_id, "فایل در حان دانلود")
            # await bot.send_message(inp.effective_message.chat_id, inp.message.effective_attachment.address)
            _file = await inp.message.effective_attachment.get_file()

            _file_name = _file.file_path.split("/")
            _file_name = _file_name[-1]
            await _file.download_to_drive(config.ROOT_PATH + "/file/" + _file_name)
            # await bot.send_message(inp.effective_message.chat_id, _file_name)
            await bot.send_message(inp.effective_message.chat_id, "فایل دانلود شد")

            if len(init.get_files("/file")) >= config.PROCESS_UPLOAD_FILE_LIMIT:
                await bot.send_message(inp.effective_message.chat_id,"شما صد ویدعو آپلود کردید و بامحدودیت صد ویدعو مواجه شدید لطفا پردازش را شروع کنید")

        else:
            await bot.send_message(inp.effective_message.chat_id, "شما بامحدودیت آپلود ویدعو مواجه شدید لطفا پردازش را شروع کنید")
    else:
        pass # do nothing







async def process_watermark_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        os.chdir(config.ROOT_PATH + "/temp")

        await bot.send_message(inp.effective_message.chat_id, config.bot_messages["starting_process"])
        await bot.send_message(inp.effective_message.chat_id, config.bot_messages["starting_process_warning"])

        _watermark_position = config.options_values["watermark_position"][databace.get_options("position")]
        print("##########")
        print(_watermark_position)
        print(databace.get_watermark_text())
        for _ in init.get_files("/file"):

            _temp_bot_1 = editor.VideoFileClip(config.ROOT_PATH + "/file/" + _)

            _temp_bot_2 = editor.TextClip(
                txt = databace.get_watermark_text(),
                fontsize=50,
                color="white"
            )

            _temp_bot_2 = _temp_bot_2.set_position(_watermark_position)
            _temp_bot_2 = _temp_bot_2.set_opacity(databace.get_options("opacity"))
            _temp_bot_2 = _temp_bot_2.set_duration(databace.get_options("duration"))


            _temp_bot_video = editor.CompositeVideoClip([_temp_bot_1, _temp_bot_2]).set_duration(_temp_bot_1.duration)
            _temp_bot_video.write_videofile(config.ROOT_PATH + "/export/" + _)

            await bot.send_video(inp.effective_message.chat_id, config.ROOT_PATH + "/export/" + _)
            # await bot.send_message(inp.effective_message.chat_id, "فایل مارک آپ شده آپلود شد")

            init.clear_files("/export")
            init.delete_file("/file", _)


        init.clear_files("/file")
        init.clear_files("/temp")
        init.clear_files("/export")

        _set_bot_mode("standby")
        await bot.send_message(inp.effective_message.chat_id, config.bot_messages["end_process"])
        
    else:
        pass # do nothing
    

async def text_message_handler(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):
    

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        if inp.message.text == config.message_commands["process"]:
            await process_watermark_command(inp= inp, context= context)

        elif inp.message.text == config.message_commands["options"]:

            _key_board = [
                [telegram.KeyboardButton(config.message_commands["watermark_options"])],
                [telegram.KeyboardButton(config.message_commands["delete_videos"])],
                [telegram.KeyboardButton(config.message_commands["cancel"])]
            ]

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["options_menu"],
            reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard= True)
            )

        elif inp.message.text == config.message_commands["watermark_options"]:

            # _key_board = [
            #     [telegram.KeyboardButton(config.message_commands["watermark_text"])],
            #     [telegram.KeyboardButton(config.message_commands["cancel"])]
            # ]

            

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["watermark_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )
        
        elif inp.message.text == config.message_commands["watermark_text"]:
            _set_bot_mode("set_watermark_text")

            _key_board = [
                [telegram.KeyboardButton(config.message_commands["cancel"])]
            ]

            
            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["set_watermark_text"],
            reply_markup=telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
            )

            if databace.get_watermark_text() != "None":
                await bot.send_message(inp.effective_message.chat_id, databace.get_watermark_text())
            else:
                pass
        
        
        
        elif inp.message.text == config.message_commands["cancel"]:
             
            if _get_bot_mode() in [
                config.bot_modes["set_watermark_text"],
                config.bot_modes["set_watermark_options"]
            ]:
                _set_bot_mode("standby")
                    
                # _key_board = [
                #     [telegram.KeyboardButton(config.message_commands["watermark_text"])],
                #     [telegram.KeyboardButton(config.message_commands["cancel"])]
                # ]

            
                await bot.send_message(inp.effective_message.chat_id, config.bot_messages["watermark_options"],
                reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
                )
            
            else: 

                # _key_board = [
                #     [telegram.KeyboardButton(config.message_commands["process"]), telegram.KeyboardButton(config.message_commands["status"])],
                #     [telegram.KeyboardButton(config.message_commands["options"]), telegram.KeyboardButton(config.message_commands["help"])]
                # ]



                await bot.send_message(inp.effective_message.chat_id, config.bot_messages["main_menu"],
                reply_markup=telegram.ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        

            

            #################################################
            #################################################
            #################################################


        elif inp.effective_message.text in [
            config.options_text_commands["position"]
        ]:
            await options_keyboard_handler(inp= inp, context= context)



        else: # if bot gets a text that wasnt in message_commands
            if _get_bot_mode() == config.bot_modes["set_watermark_text"]:
                databace.set_watermark_text(inp.message.text)
                _set_bot_mode("standby")
                await bot.send_message(inp.effective_message.chat_id, config.bot_messages["watermark_text_seted"],
                reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True),
                # reply_to_message_id= inp.effective_message.chat_id
                )
            
            elif _get_bot_mode() == config.bot_modes["set_watermark_options"]:
                await inputed_options_handler(inp= inp, context= context)



    else:
        if inp.effective_message.text == config.message_commands["set_admin"] and databace.get_admin_CHAT_ID() == 0:
            databace.set_admin_CHAT_ID(inp.effective_message.chat_id)


            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["admin_seted"],
            reply_markup= telegram.ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            )
            



         
    

async def options_keyboard_handler(inp, context):
    
    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        _set_bot_mode("set_watermark_options")
        if inp.effective_message.text == config.options_text_commands["position"]:
            _key_board = [
                [telegram.KeyboardButton(config.options["watermark_position"][0])],
                [telegram.KeyboardButton(config.options["watermark_position"][1])],
                [telegram.KeyboardButton(config.options["watermark_position"][2])],
                [telegram.KeyboardButton(config.message_commands["cancel"])]
            ]

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["set_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
            ),
            
    else:
        pass # do nothing









async def inputed_options_handler(inp, context):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        

        if inp.effective_message.text  in config.options["watermark_position"]:
            _set_bot_mode("standby")
            databace.update_options("position", config.options["watermark_position"].index(inp.effective_message.text))
            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["option_added"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )
        
    else:
        pass # do noting


def run_bot():
    '''run bot'''

    # app = ext.Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(ext.CommandHandler("start", start_command))
    app.add_handler(ext.CallbackQueryHandler(button_quary_handler))
    app.add_handler(ext.MessageHandler(ext.filters.VIDEO, video_handler))
    app.add_handler(ext.CommandHandler("process", process_watermark_command))
    app.add_handler(ext.MessageHandler(ext.filters.TEXT & ~ext.filters.COMMAND, text_message_handler))
    

    # bot = app.bot

    _set_bot_mode("standby")
    app.run_polling()

