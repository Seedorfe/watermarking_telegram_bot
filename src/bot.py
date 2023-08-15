"""
Written by Seedorfe
"""


import telethon
from moviepy import editor
import os
import asyncio


import config
import init
import databace


# we also use bot token
client = telethon.TelegramClient(
    config.ROOT_PATH +"watermarkBot",
    config.API_ID,
    config.API_HASH
)


main_menu = [
    [
        telethon.Button.text(config.message_commands["process"], resize = True), 
        telethon.Button.text(config.message_commands["status"], resize = True)
    ],
    [
        telethon.Button.text(config.message_commands["options"], resize = True), 
        telethon.Button.text(config.message_commands["help"], resize = True)
    ]
]


watermark_options_menu = [
    [
        telethon.Button.text(config.message_commands["watermark_text"], resize = True),
        telethon.Button.text(config.options_text_commands["position"], resize = True)
    ],
    [
        telethon.Button.text(config.options_text_commands["fontsize"], resize = True), 
        telethon.Button.text(config.options_text_commands["color"], resize = True)
    ],
    [
        telethon.Button.text(config.message_commands["cancel"], resize = True), 
        telethon.Button.text(config.options_text_commands["opacity"], resize = True)
    ]
]





def _set_bot_mode(mode):
    config.get_bot_mode = config.bot_modes[mode]

def _get_bot_mode():
    return config.get_bot_mode





async def start_command(event):

    # _key_board = [
    #     telethon.Button.text(config.message_commands["set_admin"])
    # ]    
      
    await client.send_message(
        entity = event.chat_id,
        message = "برای شروع کار بر روی دکمه کلیل کنید",
        buttons = telethon.Button.text(text = config.message_commands["set_admin"], resize = True)  
    )





async def file_recived_handler(event):

    if len(init.get_files("/file")) < config.PROCESS_UPLOAD_FILE_LIMIT:
        await client.download_media(
            message = event.message,
            file = config.ROOT_PATH + "/file"
        )
        await client.send_message(
            entity = event.chat_id,
            message = "فایل دانلود شد"
        )

        if len(init.get_files("/file")) >= config.PROCESS_UPLOAD_FILE_LIMIT:
            await client.send_message(
                entity = event.chat_id,
                message = "شما صد ویدعو آپلود کردید و بامحدودیت صد ویدعو مواجه شدید لطفا پردازش را شروع کنید"
            )

    else: # if admin touch file uploading limitation
        await client.send_message(
            entity = event.chat_id,
            message = "شما بامحدودیت آپلود ویدعو مواجه شدید لطفا پردازش را شروع کنید"
        )
    





async def process_watermark_command(event):

    os.chdir(config.ROOT_PATH + "/temp")

    await client.send_message(
        entity = event.chat_id,
        message = config.bot_messages["starting_process"],
        buttons = telethon.Button.clear()
    )

    await client.send_message(
        entity = event.chat_id,
        message = config.bot_messages["starting_process_warning"]
    )

    _watermark_position = config.options_values["watermark_position"][databace.get_options("position")]
    _watermark_color = config.options_values["watermark_color"][databace.get_options("color")]
        

    for _ in init.get_files("/file"):

        try:
            _temp_bot_1 = editor.VideoFileClip(config.ROOT_PATH + "/file/" + _)
            _video_duration = _temp_bot_1.duration

            _temp_bot_2 = editor.TextClip(
                txt = databace.get_watermark_text(),
                fontsize=databace.get_options("fontsize"),
                color=_watermark_color,
                font="LMU-Vazir"
            )

            _temp_bot_2 = _temp_bot_2.set_position(_watermark_position)
            _temp_bot_2 = _temp_bot_2.set_opacity(databace.get_options("opacity"))
            _temp_bot_2 = _temp_bot_2.set_duration(databace.get_options("duration")).set_start(
                (_video_duration/2) - (databace.get_options("duration")/2))


            _temp_bot_video = editor.CompositeVideoClip([_temp_bot_1, _temp_bot_2]).set_duration(_temp_bot_1.duration)
            _temp_bot_video.write_videofile(config.ROOT_PATH + "/export/" + _)

    
            await client.send_message(
                entity = event.chat_id,
                file = config.ROOT_PATH + "/export/" + _
            )
        
        except: # if bot cant watermark file( maybe it is not a video)
            await client.send_message(
                entity = event.chat_id,
                message = "در واتر مارک کردن یکی از فایل ها مشکلی پیش آمد"
            )

        init.clear_files("/temp")
        init.clear_files("/export")
        init.delete_file("/file", _)


    init.clear_files("/file")
    init.clear_files("/temp")
    init.clear_files("/export")

    _set_bot_mode("standby")

    await client.send_message(
        entity = event.chat_id,
        message = config.bot_messages["end_process"],
        buttons = main_menu
    )
    


async def status_command(event):

    _status_messsage = f"""
        تعداد فایل های در انتظار پردازش:  {len(init.get_files("/file"))}
        واتر مارک : {databace.get_watermark_text()} 
        مکان: {config.options["watermark_position"][databace.get_options("position")]}
        رنگ: {config.options["watermark_color"][databace.get_options("color")]}
        شفافیت: {config.options["watermark_opacity"][config.options_values["watermark_opacity"].index(databace.get_options("opacity"))]}
        اندازه: {databace.get_options("fontsize")}
            
    """

    await client.send_message(
        entity = event.chat_id,
        message = _status_messsage
    )


async def help_command(event):

    await client.send_message(
        entity = event.chat_id,
        message = config.HELP_MESSAGE
    )
    


async def clear_files_command(event):

    init.clear_files("/file")
    init.clear_files("/temp")
    init.clear_files("/export")

    await client.send_message(
        entity = event.chat_id,
        message = "فایل های آماده پردازش حذف شدند",
        buttons = main_menu 
    )



async def options_keyboard_handler(event):

    if event.message.text == config.options_text_commands["position"]:
        _set_bot_mode("set_watermark_options")
        _key_board = [
            [telethon.Button.text(config.options["watermark_position"][0], resize=True)],
            [telethon.Button.text(config.options["watermark_position"][1], resize=True)],
            [telethon.Button.text(config.options["watermark_position"][2], resize=True)],
            [telethon.Button.text(config.message_commands["cancel"], resize=True)]
        ]
        
        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["set_options"],
            buttons = _key_board
        )
    
    elif event.message.text == config.options_text_commands["opacity"]:

        _set_bot_mode("set_watermark_options")
        _key_board = [
            [
                telethon.Button.text(config.options["watermark_opacity"][0], resize=True)
            ],
            [
                telethon.Button.text(config.options["watermark_opacity"][1], resize=True),
                telethon.Button.text(config.options["watermark_opacity"][2], resize=True)
            ],
            [
                telethon.Button.text(config.options["watermark_opacity"][3], resize=True),
                telethon.Button.text(config.message_commands["cancel"], resize=True)
            ]
        ]

        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["set_options"],
            buttons = _key_board
        )
    

    elif event.message.text == config.options_text_commands["fontsize"]:


        _set_bot_mode("set_watermark_options")
        # "watermark_fontsize" : ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
        _key_board = [
            [
                telethon.Button.text(config.options["watermark_fontsize"][0], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][1], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][2], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][3], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][4], resize=True)
            ],
            [
                telethon.Button.text(config.options["watermark_fontsize"][5], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][6], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][7], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][8], resize=True),
                telethon.Button.text(config.options["watermark_fontsize"][9], resize=True),
            ],
            [
                telethon.Button.text(config.options["watermark_fontsize"][10], resize=True),
                telethon.Button.text(config.message_commands["cancel"], resize=True)
            ]
        ]


        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["set_options"],
            buttons = _key_board
        )
    
    elif event.message.text == config.options_text_commands["color"]:

        _set_bot_mode("set_watermark_options")


        # "watermark_color" : ["white", "black", "blue", "green", "red"]

        _key_board = [
            [
                telethon.Button.text(config.options["watermark_color"][0], resize=True), 
                telethon.Button.text(config.options["watermark_color"][1], resize=True)
            ],
            [
                telethon.Button.text(config.options["watermark_color"][2], resize=True),
                telethon.Button.text(config.options["watermark_color"][3], resize=True),
                telethon.Button.text(config.options["watermark_color"][4], resize=True)
            ],
            [
                telethon.Button.text(config.message_commands["cancel"], resize=True)
            ]       
        ]

        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["set_options"],
            buttons = _key_board
        )
    
            


async def inputed_options_handler(event):

    if event.message.text  in config.options["watermark_position"]:
        _set_bot_mode("standby")
        databace.update_options("position", config.options["watermark_position"].index(event.message.text))

        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["option_added"],
            buttons = watermark_options_menu
        )
        
    elif event.message.text in config.options["watermark_opacity"]:
        _set_bot_mode("standby")
        _opacity = config.options_values["watermark_opacity"][config.options["watermark_opacity"].index(event.message.text)]
        databace.update_options("opacity", _opacity)


        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["option_added"],
            buttons = watermark_options_menu
        )

    elif event.message.text in config.options["watermark_fontsize"]:    
        _set_bot_mode("standby")
        _fontsize = config.options_values["watermark_fontsize"][config.options["watermark_fontsize"].index(event.message.text)]
        databace.update_options("fontsize", _fontsize)

        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["option_added"],
            buttons = watermark_options_menu
        )

    elif event.message.text in config.options["watermark_color"]:

        _set_bot_mode("standby")

        _color = config.options["watermark_color"].index(event.message.text)
        databace.update_options("color", _color)

        await client.send_message(
            entity = event.chat_id,
            message = config.bot_messages["option_added"],
            buttons = watermark_options_menu
        )






    

    








async def message_handloer_core(event):
    '''this function handle all recived messages'''

    
    if event.message.is_private:

        if event.chat_id == databace.get_admin_CHAT_ID():
  

            if event.message.media: # if admin sends a media(we just want videos)
                await file_recived_handler(event=event)
            

            elif event.message.text == config.message_commands["process"]:
                await process_watermark_command(event=event)

            elif event.message.text == config.message_commands["options"]:

                _key_board = [
                    [telethon.Button.text(config.message_commands["watermark_options"], resize = True)],
                    [telethon.Button.text(config.message_commands["delete_videos"], resize = True)],
                    [telethon.Button.text(config.message_commands["cancel"], resize = True)]
                ]

                await client.send_message(
                    entity = event.chat_id,
                    message = config.bot_messages["options_menu"],
                    buttons = _key_board
                )

            elif event.message.text == config.message_commands["watermark_options"]:  
              
                await client.send_message(
                    entity = event.chat_id,
                    message = config.bot_messages["watermark_options"],
                    buttons = watermark_options_menu
                )
            
            elif event.message.text == config.message_commands["watermark_text"]:

                _set_bot_mode("set_watermark_text")
                
                _key_board = [
                    [telethon.Button.text(config.message_commands["cancel"], resize = True)]
                ]

                await client.send_message(
                    entity = event.chat_id,
                    message = config.bot_messages["set_watermark_text"],
                    buttons = _key_board
                )

                if databace.get_watermark_text() != "None": # if admin has added watermark befor, show now
                    await client.send_message(
                        entity = event.chat_id,
                        message = databace.get_watermark_text()
                    )

            elif event.message.text == config.message_commands["cancel"]:
                
                if _get_bot_mode() in [
                    config.bot_modes["set_watermark_text"],
                    config.bot_modes["set_watermark_options"]
                ]:
                    _set_bot_mode("standby")
                    await client.send_message(
                        entity = event.chat_id,
                        message = config.bot_messages["watermark_options"],
                        buttons = watermark_options_menu 
                    )

                else: # if we wasnt in watermark options menu
                    await client.send_message(
                        entity = event.chat_id,
                        message = config.bot_messages["main_menu"],
                        buttons = main_menu
                    )

            elif event.message.text == config.message_commands["status"]:
                await status_command(event=event)
            elif event.message.text == config.message_commands["help"]:
                await help_command(event=event)
            elif event.message.text == config.message_commands["delete_videos"]:
                await clear_files_command(event=event)


            elif event.message.text in [
                config.options_text_commands["position"],
                config.options_text_commands["opacity"],
                config.options_text_commands["fontsize"],
                config.options_text_commands["color"]
            ]:
                await options_keyboard_handler(event=event)
     
        


            elif event.message.text in ["منو", "menu", "/start"]:
                _set_bot_mode("standby")
                await client.send_message(
                    entity = event.chat_id,
                    message = config.bot_messages["main_menu"],
                    buttons = main_menu
                )


            else: # if bot gets a text from admin that wasnt in message_commands
                
                if _get_bot_mode() == config.bot_modes["set_watermark_text"]:
                    databace.set_watermark_text(event.message.text)
                    _set_bot_mode("standby")

                    await client.send_message(
                        entity = event.chat_id,
                        message = config.bot_messages["watermark_text_seted"],
                        buttons = watermark_options_menu
                    )

                elif _get_bot_mode() == config.bot_modes["set_watermark_options"]:
                    await inputed_options_handler(event=event)



        else: # if who sends message was not admin
            
            if event.message.text == "/start":
                if databace.get_admin_CHAT_ID() == 0: # if we didnt have admin yet
                    await start_command(event=event)
                
            if event.message.text == config.message_commands["set_admin"] and databace.get_admin_CHAT_ID() == 0:
                
                databace.set_admin_CHAT_ID(event.chat_id)
                await client.send_message(
                    entity = event.chat_id,
                    message = config.bot_messages["admin_seted"],
                    buttons = main_menu
                )
                    

            
    
    else: # if message was not private
        pass # do nothing










async def run_bot():

    init.clear_files("/temp")
    init.clear_files("/export")
    _set_bot_mode("standby")


    await client.start(bot_token=config.BOT_TOKEN) 

    client.add_event_handler(message_handloer_core, telethon.events.NewMessage)

    await client.run_until_disconnected()


