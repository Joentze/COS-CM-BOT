message_text = {
    "start":"Hello there! Welcome to the COS CM Bot 🤖. This bot was created with the purpose of simplifying CM administrative matters. Please press the buttons below so we know your details and type /help for other queries",
    "attendance_pending": "Just a second...getting today's attendance ✌🏼",
    "attendance_submit": "Thank you for submitting the attendance. If you wish to make any changes do click the button below 🔽",
    "attendance_message": "Attendance for ",
    "attendance_caution":"\n\n ⚠️ The interface may take a while to update, depending on your internet connection. Check for the loading notification above 🔼",
    "welcome_back_start": "Hello! there welcome back to the COS CM bot! Ensure that the details listed below are correct ✅. Otherwise, type /setclass",
    "select_class":"Please select the class that you're teaching 🍎.",
    "select_session":"Please select the session that you're in 👨🏻‍🏫. ",
    "select_complete":"Session & class profile update complete! 🤩",
    "collate_loading":"Collating attendance...This will take a minute! ⏳",
    "FP":"1st Praise",
    "FJ":"1st Jam",
    'FT':"1st Praise-Tots",
    "SP":"2nd Praise",
    "SJ":"2nd Jam",
    "ST":"2nd Praise-Tots",
    "generic_error_msg":"Sorry something went wrong there! Do try again. If the problem persists contact Joen",
    "addkid_error":"/addkid command formatting is off. Please try again.",
    "added_kid_success":"🎉 Sucessfully added kid into ",
    "date_format_error":"The date format that you have entered is incorrect. Ensure that the date is in MM/YYYY format 📆",
    "attendance_reminder":"Good morning teachers 🌥 Gentle reminder to take /attendance today! Have a blessed Sunday 😇",
    "help_message":"""
    List of Commands:

Misc. Stuff:
/start - Initiates the start of bot ⚙️
/setclass - Change your session & class in your profile ✍🏼

Work Stuff:
/attendance - Sends the attendance for the class of session stated in your profile 📋
/absentee - Shows kids that have been absent for more than 2 weeks 🚩
/collate MM/YYYY - Collates attendance for the week and sends an excel file.

🤔Change to other classes (via /setclass) to change their attendance

Fun Stuff:
/verse - Sends you a random Bible verse 📙
/ilovejesus - 💕

Even more fun stuff:
/advancehelp - help option, but cooler.
    """,
    "help_advance":"""
This is where it gets a little cool, but crazy.

1st - F
2nd - S
Praise - P
Jam - J

Nursery - N1
Kindergarten - K1/2
Primary - P1/2/3/4/5/6

Profile code
"1st Praise Primary 4" = FPP4

/addkid NAME-OF-KID/PROFILE-CODE - Add kid into your class for administrative purposes.
    """

}

inline_options={
    "session_option":{"inline_keyboard":[
        [{"callback_data":"submit_user_session_data_P_FP","text":message_text["FP"]}],
        [{"callback_data":"submit_user_session_data_J_FJ","text":message_text["FJ"]}],
        [{"callback_data":"submit_user_session_data_T_FT","text":message_text["FT"]}],
        [{"callback_data":"submit_user_session_data_P_SP","text":message_text["SP"]}],
        [{"callback_data":"submit_user_session_data_J_SJ","text":message_text["SJ"]}],
        [{"callback_data":"submit_user_session_data_T_ST","text":message_text["ST"]}]
    ]},
    "P_class_option":{"inline_keyboard":[
        [{"callback_data":"submit_user_class_data_P3","text":"P3"},
        {"callback_data":"submit_user_class_data_P4","text":"P4"}],
        [{"callback_data":"submit_user_class_data_P5","text":"P5"},
        {"callback_data":"submit_user_class_data_P6","text":"P6"}]
    ]},
    "J_class_option":{"inline_keyboard":[
        [{"callback_data":"submit_user_class_data_P1","text":"P1"},
        {"callback_data":"submit_user_class_data_P2","text":"P2"}],
        [{"callback_data":"submit_user_class_data_K2","text":"K2"},
        {"callback_data":"submit_user_class_data_K1","text":"K1"}],
        [{"callback_data":"submit_user_class_data_N1","text":"N1"}]
    ]},
    "T_class_option":{"inline_keyboard":[
        [{"callback_data":"submit_user_class_data_N0","text":"Pre-N"}]
    ]
    }
    }


month_number_map = {
    "01":"Jan",
    "02":"Feb",
    "03":"Mar",
    "04":"Apr",
    "05":"May",
    "06":"Jun",
    "07":"Jul",
    "08":"Aug",
    "09":"Sep",
    "10":"Oct",    
    "11":"Nov",
    "12":"Dec"
}

all_session_codes=["FPP6","FPP5","FPP4","FPP3","FJP2","FJP1","FJK2","FJK1","FJN1","FTN0","SPP6","SPP5","SPP4","SPP3","SJP2","SJP1","SJK2","SJK1","SJN1","STN0"]