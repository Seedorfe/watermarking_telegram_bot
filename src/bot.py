
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
    [telegram.KeyboardButton(config.options_text_commands["fontsize"]), telegram.KeyboardButton(config.options_text_commands["color"])],
    [telegram.KeyboardButton(config.message_commands["cancel"]), telegram.KeyboardButton(config.options_text_commands["opacity"])]
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

        _set_bot_mode("standby")
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
        _watermark_color = config.options_values["watermark_color"][databace.get_options("color")]
        
        for _ in init.get_files("/file"):

            _temp_bot_1 = editor.VideoFileClip(config.ROOT_PATH + "/file/" + _)
            _video_duration = _temp_bot_1.duration

            _temp_bot_2 = editor.TextClip(
                txt = databace.get_watermark_text(),
                fontsize=databace.get_options("fontsize"),
                color=_watermark_color
            )

            _temp_bot_2 = _temp_bot_2.set_position(_watermark_position)
            _temp_bot_2 = _temp_bot_2.set_opacity(databace.get_options("opacity"))
            _temp_bot_2 = _temp_bot_2.set_duration(databace.get_options("duration")).set_start(
                (_video_duration/2) - (databace.get_options("duration")/2))


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
        

        elif inp.message.text == config.message_commands["status"]:
            
            await status_command(inp =inp, context= context)
        
        elif inp.message.text == config.message_commands["help"]:
            await help_command(inp=inp, context= context)
        
        elif inp.message.text == config.message_commands["delete_videos"]:
            await clear_files_command(inp = inp, context= context)

            #################################################
            #################################################
            #################################################


        elif inp.effective_message.text in [
            config.options_text_commands["position"],
            config.options_text_commands["opacity"],
            config.options_text_commands["fontsize"],
            config.options_text_commands["color"]
        ]:
            await options_keyboard_handler(inp= inp, context= context)


        elif inp.effective_message.text in ["منو", "menu"]:
            _set_bot_mode("standby")
            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["main_menu"],
            reply_markup=telegram.ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        
        
            #################################################33
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
        
        if inp.effective_message.text == config.options_text_commands["position"]:
            _set_bot_mode("set_watermark_options")
            _key_board = [
                [telegram.KeyboardButton(config.options["watermark_position"][0])],
                [telegram.KeyboardButton(config.options["watermark_position"][1])],
                [telegram.KeyboardButton(config.options["watermark_position"][2])],
                [telegram.KeyboardButton(config.message_commands["cancel"])]
            ]

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["set_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
            ),

        elif inp.effective_message.text == config.options_text_commands["opacity"]:
            _set_bot_mode("set_watermark_options")
            _key_board = [
                [telegram.KeyboardButton(config.options["watermark_opacity"][0])],
                [telegram.KeyboardButton(config.options["watermark_opacity"][1]),telegram.KeyboardButton(config.options["watermark_opacity"][2])],
                [telegram.KeyboardButton(config.options["watermark_opacity"][3]),telegram.KeyboardButton(config.message_commands["cancel"])]
            ]

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["set_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
            ),

        elif inp.effective_message.text == config.options_text_commands["fontsize"]:

            _set_bot_mode("set_watermark_options")
            # "watermark_fontsize" : ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
            _key_board = [
                [
                    telegram.KeyboardButton(config.options["watermark_fontsize"][0]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][1]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][2]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][3]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][4])
                ],
                [
                    telegram.KeyboardButton(config.options["watermark_fontsize"][5]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][6]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][7]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][8]),
                    telegram.KeyboardButton(config.options["watermark_fontsize"][9]),
                ],
                [
                    telegram.KeyboardButton(config.options["watermark_fontsize"][10]),
                    telegram.KeyboardButton(config.message_commands["cancel"])
                ]
            ]

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["set_options"],
            reply_markup= telegram.ReplyKeyboardMarkup(_key_board, resize_keyboard=True)
            ),

        elif inp.effective_message.text == config.options_text_commands["color"]:
            _set_bot_mode("set_watermark_options")
            ###########################################################3

            # "watermark_color" : ["white", "black", "blue", "green", "red"]

            _key_board = [
                [
                    telegram.KeyboardButton(config.options["watermark_color"][0]), 
                    telegram.KeyboardButton(config.options["watermark_color"][1])
                ],
                [
                    telegram.KeyboardButton(config.options["watermark_color"][2]),
                    telegram.KeyboardButton(config.options["watermark_color"][3]),
                    telegram.KeyboardButton(config.options["watermark_color"][4])
                ],
                [
                    telegram.KeyboardButton(config.message_commands["cancel"])
                ]
            
                
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
        
        ###########################################################################
        elif inp.effective_message.text in config.options["watermark_opacity"]:
            _set_bot_mode("standby")
            _opacity = config.options_values["watermark_opacity"][config.options["watermark_opacity"].index(inp.effective_message.text)]
            databace.update_options("opacity", _opacity)

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["option_added"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )

        elif inp.effective_message.text in config.options["watermark_fontsize"]:
            _set_bot_mode("standby")
            _fontsize = config.options_values["watermark_fontsize"][config.options["watermark_fontsize"].index(inp.effective_message.text)]
            databace.update_options("fontsize", _fontsize)

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["option_added"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )

        elif inp.effective_message.text in config.options["watermark_color"]:
            _set_bot_mode("standby")

            _color = config.options["watermark_color"].index(inp.effective_message.text)
            databace.update_options("color", _color)

            await bot.send_message(inp.effective_message.chat_id, config.bot_messages["option_added"],
            reply_markup= telegram.ReplyKeyboardMarkup(watermark_options_menu, resize_keyboard=True)
            )
            
        
    else:
        pass # do noting


async def help_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):

    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        await bot.send_message(inp.effective_message.chat_id, config.HELP_MESSAGE)



async def status_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):
    
    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:

        _status_messsage = f"""
            تعداد فایل های در انتظار پردازش:  {len(init.get_files("/file"))}
            واتر مارک : {databace.get_watermark_text()} 
            مکان: {config.options["watermark_position"][databace.get_options("position")]}
            رنگ: {config.options["watermark_color"][databace.get_options("color")]}
            شفافیت: {config.options["watermark_opacity"][config.options_values["watermark_opacity"].index(databace.get_options("opacity"))]}
            اندازه: {databace.get_options("fontsize")}
            
        """

        await bot.send_message(inp.effective_message.chat_id, _status_messsage)


async def clear_files_command(inp : telegram.Update, context : ext.ContextTypes.DEFAULT_TYPE):
    if databace.get_admin_CHAT_ID() == inp.effective_message.chat_id:
        init.clear_files("/file")
        init.clear_files("/temp")
        init.clear_files("/export")

        await bot.send_message(inp.effective_message.chat_id, "فایل های آماده پردازش حذف شدند",
        reply_markup = telegram.ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        )


def run_bot():
    '''run bot'''

    # app = ext.Application.builder().token(config.BOT_TOKEN).build()

    init.clear_files("/temp")
    init.clear_files("/export")


    app.add_handler(ext.CommandHandler("start", start_command))
    app.add_handler(ext.CallbackQueryHandler(button_quary_handler))
    app.add_handler(ext.MessageHandler(ext.filters.VIDEO, video_handler))
    app.add_handler(ext.CommandHandler("process", process_watermark_command))
    app.add_handler(ext.MessageHandler(ext.filters.TEXT & ~ext.filters.COMMAND, text_message_handler))
    app.add_handler(ext.CommandHandler("help", help_command))
    app.add_handler(ext.CommandHandler("status", status_command))
    

    # bot = app.bot

    _set_bot_mode("standby")
    app.run_polling()

