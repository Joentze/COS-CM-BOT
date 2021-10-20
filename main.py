from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from attendance_handler import create_inline_obj, init_name_mapped_val, update_name_mapped_val, attd_insert_new_kid,add_in_new_attd, get_attd_obj_by_id, inside_bool_db,startup_user,get_user_readable_data,insert_class_user, insert_session_user,insert_session_id_user,get_user_session_code, insert_new_kid, get_praise_jam_attendance_array
from excel_auto import init_workbook
 #attd_change_inline_button
import time
from datetime import datetime, timedelta
import logging
from msg import message_text, inline_options, month_number_map
from private import TELEGRAM_TOKEN
from random_verse import get_random_verse
from private import TELEGRAM_TOKEN
import os



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start_msg(update, context):
    chat_id = update.message.from_user["id"]
    user_name = update.message.from_user["first_name"]
    is_id_in_db = inside_bool_db(chat_id)
    if is_id_in_db == False:
        update.message.reply_text(message_text["start"])
        startup_user(chat_id, user_name)
        update_profile(update, context)
    elif is_id_in_db == True:
        update.message.reply_text(message_text["welcome_back_start"])
        name, session, user_class = get_user_readable_data(chat_id)
        data_checking_string = f"NAME: {name}\nCLASS: {user_class}\nSESSION: {message_text[session]}"
        update.message.reply_text(data_checking_string)

def attd_date_msg(update, context):
    get_chat_id = update.message.from_user["id"]
    update.message.reply_text(message_text["attendance_pending"])
    DATE_TODAY,DATE_TODAY_SLASHED = give_sun_date_if_not_sun()
    reply_markup={}
    user_session = get_user_session_code(str(get_chat_id))
    is_available = get_attd_obj_by_id(user_session + DATE_TODAY)
    if is_available == False:
        init_obj = init_name_mapped_val(user_session)
        reply_markup = create_inline_obj(init_obj)
        add_in_new_attd(user_session+DATE_TODAY, str(init_obj))
    else:
        reply_markup = create_inline_obj(get_attd_obj_by_id(user_session+DATE_TODAY))
    whole_message = message_text["attendance_message"] + DATE_TODAY_SLASHED + message_text["attendance_caution"]
    context.bot.send_message(chat_id = get_chat_id, text=whole_message, reply_markup = reply_markup)

def update_attd(update, context):
    query = update.callback_query
    get_chat_id = update.callback_query.message.chat.id
    DATE_TODAY,DATE_TODAY_SLASHED = give_sun_date_if_not_sun()
    user_session = get_user_session_code(str(get_chat_id))
    obj = get_attd_obj_by_id(user_session+DATE_TODAY)
    button_pressed =  query.data.strip()
    new_mapped_val = update_name_mapped_val(button_pressed, obj)
    new_markup = create_inline_obj(new_mapped_val)
    whole_message = message_text["attendance_message"] + DATE_TODAY_SLASHED+ message_text["attendance_caution"]
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=query.message.message_id, text=whole_message, reply_markup=new_markup)
    add_in_new_attd(user_session+DATE_TODAY, str(new_mapped_val))

def submit_attd(update, context):
    get_chat_id = update.callback_query.message.chat.id
    user_session = get_user_session_code(str(get_chat_id))
    DATE_TODAY,DATE_TODAY_SLASHED = give_sun_date_if_not_sun()
    attd_id = user_session+DATE_TODAY
    query = update.callback_query
    mapped_val = get_attd_obj_by_id(attd_id)
    add_in_new_attd(attd_id, str(mapped_val))
    new_changes_markup = {'inline_keyboard':[[{'callback_data':'change_attd', 'text':'Make Changes 📋'}]]}
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=query.message.message_id, text=message_text["attendance_submit"], reply_markup=new_changes_markup)

def change_attd(update, context):
    get_chat_id = update.callback_query.message.chat.id
    user_session = get_user_session_code(str(get_chat_id))
    DATE_TODAY,DATE_TODAY_SLASHED = give_sun_date_if_not_sun()
    attd_id = user_session+DATE_TODAY
    query = update.callback_query
    obj = get_attd_obj_by_id(attd_id)
    markup_obj = create_inline_obj(obj)
    whole_message = message_text["attendance_message"] + DATE_TODAY_SLASHED
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=query.message.message_id,text=whole_message,  reply_markup=markup_obj)
    
def P_submit_user_session_data(update, context):
    get_chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    session = update.callback_query.data.replace("submit_user_session_data_P_", "")
    insert_session_user(str(get_chat_id), session)
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=message_id, text=message_text['select_class'], reply_markup=inline_options["P_class_option"])

def J_submit_user_session_data(update, context):
    get_chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    session = update.callback_query.data.replace("submit_user_session_data_J_", "")
    insert_session_user(str(get_chat_id), session)
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=message_id, text=message_text['select_class'], reply_markup=inline_options["J_class_option"])

def T_submit_user_session_data(update, context):
    get_chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    session = update.callback_query.data.replace("submit_user_session_data_T_", "")
    insert_session_user(str(get_chat_id), session)
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=message_id, text=message_text['select_class'], reply_markup=inline_options["T_class_option"])


def submit_user_class_data(update, context):
    get_chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    user_class = update.callback_query.data.replace("submit_user_class_data_", "")
    str_chat_id = str(get_chat_id)
    insert_class_user(str_chat_id, user_class)
    session_id = get_user_session_code(str_chat_id)
    insert_session_id_user(str_chat_id, session_id)
    context.bot.edit_message_text(chat_id=get_chat_id, message_id=message_id, text=message_text["select_complete"])

def update_profile(update, context):
    chat_id = update.message.from_user["id"]
    context.bot.send_message(chat_id = chat_id, text=message_text["select_session"], reply_markup = inline_options["session_option"])

def help_msg(update, context):
    update.message.reply_text(message_text["help_message"])
    
def getverse(update, context):
    bible_verse = get_random_verse()
    update.message.reply_text(bible_verse)

def get_time_test(update, context):
    DATE_TODAY_W_MIN_S = datetime.today().strftime("%d%m%Y-%H:%M:%S")
    update.message.reply_text(DATE_TODAY_W_MIN_S)


def give_sun_date_if_not_sun():
    DATE_TODAY = datetime.today().strftime("%d%m%Y")
    DATE_TODAY_SLASHED = datetime.today().strftime("%d/%m/%Y")
    GET_DAY_OF_WEEK = datetime.today().weekday()
    GET_DATE_OF_PREV_SUN_RAW = datetime.today()-timedelta(days=GET_DAY_OF_WEEK+1)
    GET_PREV_SUN_DATE = GET_DATE_OF_PREV_SUN_RAW.strftime("%d%m%Y")
    GET_PREV_SUN_DATE_SLASHED = GET_DATE_OF_PREV_SUN_RAW.strftime("%d/%m/%Y")
    if GET_DAY_OF_WEEK != 6:
        return GET_PREV_SUN_DATE, GET_PREV_SUN_DATE_SLASHED
    else:
        return DATE_TODAY, DATE_TODAY_SLASHED

def add_kid_into_attd(update, context):
    message_receive = update.message.text.strip()
    string_combi = message_receive.replace("/addkid","")
    name_and_session_code = string_combi.split('/')
    if len(name_and_session_code) == 2:
        name = name_and_session_code[0]
        session_code = name_and_session_code[1]
        if len(session_code) != 4:
            update.message.reply_text(message_text["addkid_error"])
        elif len(session_code) == 4:
            session = session_code[0:2]
            kid_class = session_code[2:4]
            DATE_TODAY,DATE_TODAY_SLASHED = give_sun_date_if_not_sun()
            insert_new_kid({"name":name.strip(),"session_code":session_code,"age":00,"session":session,"class":kid_class})
            attd_insert_new_kid(name.strip(), session_code + DATE_TODAY)            
            update.message.reply_text(message_text["added_kid_success"] + message_text[session] + " " + kid_class)
    else:
        update.message.reply_text(message_text["addkid_error"])

def advance_help_msg(update, context):
    update.message.reply_text(message_text["help_advance"])

def collate_attendance_month(update, context):
    chat_id = update.message.from_user["id"]
    message = update.message.text.strip()
    date_input = message.replace("/collate","").strip()
    month_year = date_input.split("/")
    if len(month_year) == 2 :
        month = month_year[0]
        year = month_year[1]
        if len(month) == 2 and len(year) == 4:
            update.message.reply_text(message_text["collate_loading"])
            get_array_sessions = get_praise_jam_attendance_array(month, year)
            filename = f"collate_{month}{year}"
            init_workbook(filename,month_number_map[month],get_array_sessions)
            with open(f"{filename}.xlsx", "rb") as excel_collate:
                context.bot.send_document(chat_id = chat_id, document=excel_collate, filename=filename+".xlsx")
            os.remove(f"./{filename}.xlsx")
        else:
            update.message.reply_text(message_text["date_format_error"]) 
    else:
        update.message.reply_text(message_text["date_format_error"]) 







def run():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start_msg))
    dp.add_handler(CommandHandler('timetest',get_time_test))
    dp.add_handler(CommandHandler('help',help_msg))
    dp.add_handler(CommandHandler('advancehelp',advance_help_msg))
    dp.add_handler(CommandHandler('setclass',update_profile))
    dp.add_handler(CommandHandler('attendance', attd_date_msg))
    dp.add_handler(CommandHandler('verse', getverse))
    dp.add_handler(CommandHandler('addkid', add_kid_into_attd))
    dp.add_handler(CommandHandler('collate', collate_attendance_month))
    dp.add_handler(CallbackQueryHandler(update_attd,pattern="attd_"))
    dp.add_handler(CallbackQueryHandler(submit_attd,pattern="submit_attd"))
    dp.add_handler(CallbackQueryHandler(change_attd,pattern="change_attd"))
    dp.add_handler(CallbackQueryHandler(P_submit_user_session_data,pattern="submit_user_session_data_P"))
    dp.add_handler(CallbackQueryHandler(J_submit_user_session_data,pattern="submit_user_session_data_J"))
    dp.add_handler(CallbackQueryHandler(T_submit_user_session_data,pattern="submit_user_session_data_T"))
    dp.add_handler(CallbackQueryHandler(submit_user_class_data,pattern="submit_user_class_data_"))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run()
