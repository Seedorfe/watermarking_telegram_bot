
"""
Written by Seedorfe
"""


BOT_TOKEN = ""



ROOT_PATH = ""



PROCESS_UPLOAD_FILE_LIMIT = 100




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


bot_modes = {
    "standby": "standby",
    "set_watermark_text" : "set_watermark_text",
    "set_watermark_options" : "set_watermark_options"
}


get_bot_mode = ""



options_text_commands = {
    "position" : "مکان",
    "opacity": "شفافیت",
    "fontsize": "انداره",
    "color": "رنگ"
} 

list_options_text_commands = [
    "مکان"
]

options = {
    "watermark_position": ["بالا", "وسط", "پایین"],
    "watermark_opacity": ["بدون شفافیت", "کم", "متوسط", "زیاد"],
    "watermark_fontsize" : ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
    "watermark_color" : ["سفید", "سیاه", "آبی", "سبز", "قرمز"]
}

# "center" "top" "bottom"
options_values = {
    "watermark_position" : ["top", "center", "bottom"],
    "watermark_opacity" : [1, 0.75, 0.5, 0.25],
    "watermark_fontsize" : [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    "watermark_color" : ["white", "black", "blue", "green", "red"]   
}



HELP_MESSAGE = """برای دسترسی به منوی اصلی عبارت های زیر را ارسال کنید
"منو","menu","/start"

برای واتر مارک کردن, ویدعو ها را اپدیت و در منوی اصلی کلید پردازش را لمس کنید
"""
