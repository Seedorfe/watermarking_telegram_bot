
"""
Written by Seedorfe
"""




# write your bot token here
BOT_TOKEN = ""
API_ID = 0
API_HASH = ""


# if you do not use a special port set it on 0
CONNECTION_PORT = 65501




# use init.find_root_path() to set
ROOT_PATH = ""


# upload file limitation 
PROCESS_UPLOAD_FILE_LIMIT = 100



# this messages are like commands
message_commands = {
    "set_admin" : "شروع به عنوان ادمین",
    "process" : "پردازش",
    "options" : "تنظیمات",
    "delete_videos": "حذف ویدعو های ذخیره شده",
    "cancel" : "بیخیال",
    "watermark_options": "تنظیمات واتر مارک",
    "status":"وضعیت",
    "help": "راهنما",
    "watermark_text": "متن"

}

# messages that bot can send
bot_messages = {
    "admin_seted" : "شما ادمین شدید",
    "main_menu": "منوی اصلی",
    "options_menu" : "منوی تنظیمات",
    "watermark_options" : "تنظیمان واتر مارک",
    "set_watermark_text": "لطفا واتر مارک را بنویسید و برای من ارسال کنید",
    "watermark_text_seted": "واتر مارک ذخیره شد",
    "starting_process" : "پردازش شروع شد",
    "starting_process_warning": "لطفا تا پایان پردازش از ارسال پیام و فایل خودداری کنید",
    "end_process": "پایان پردازش",
    "set_options" : "لطفا مقدار مورد نظر را انتخاب کنید",
    "option_added" : "تنظیمات بروز شد"

    
}

# we using bot_modes whene change options 
bot_modes = {
    "standby": "standby",
    "set_watermark_text" : "set_watermark_text",
    "set_watermark_options" : "set_watermark_options"
}


# bot mode
get_bot_mode = ""


# watermark options list 
options_text_commands = {
    "position" : "مکان",
    "opacity": "شفافیت",
    "fontsize": "انداره",
    "color": "رنگ"
} 


# not used
# list_options_text_commands = [
#     "مکان"
# ]

# this options inputed from key board to change watermark style
options = {
    "watermark_position": ["بالا", "وسط", "پایین"],
    "watermark_opacity": ["بدون شفافیت", "کم", "متوسط", "زیاد"],
    "watermark_fontsize" : ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
    "watermark_color" : ["سفید", "سیاه", "آبی", "سبز", "قرمز"]
}

# using to convert inputed options from key board to what data bace can store
options_values = {
    "watermark_position" : ["top", "center", "bottom"],
    "watermark_opacity" : [1, 0.75, 0.5, 0.25],
    "watermark_fontsize" : [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    "watermark_color" : ["white", "black", "blue", "green", "red"]   
}


# help message for help command
HELP_MESSAGE = """برای دسترسی به منوی اصلی عبارت های زیر را ارسال کنید
"منو","menu","/start"

برای واتر مارک کردن, ویدعو ها را اپدیت و در منوی اصلی کلید پردازش را لمس کنید
"""
