import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
import psycopg2
import datetime

if __name__ == "__main__":

    def send_message():            
        cursor.execute("SELECT username from sending_messages")
        our_message_username = cursor.fetchone()
        cursor.execute("SELECT text from sending_messages")
        our_message_text = cursor.fetchone()
        cheking_user_chat = """SELECT chat_id from private_message where destination_id=%s"""
        try:
            cursor.execute(cheking_user_chat, our_message_username)
            our_chat_id = cursor.fetchall()
            if len(our_chat_id) != 0:
                bot.send_message(our_chat_id[0][0], str(our_message_text[0]))
        except Exception:
            pass
    
    def cheking_for_updates():
        insert_private_message = """INSERT INTO private_message (id, chat_id, destination_id, date, text) VALUES (%s, %s, %s, %s, %s)"""
        insert_global_message = """INSERT INTO private_message (id, chat_id,  date, text) VALUES (%s, %s, %s, %s)"""
        select_private_message_id = """SELECT id from private_message"""
        cursor.execute(select_private_message_id)
        update_ids_tuple = cursor.fetchall()
        update_ids = list()
        for item in update_ids_tuple:
            update_ids.append(int(item[0]))
        connection.commit()
        cheking_last_update = """SELECT id FROM private_message ORDER BY id DESC LIMIT 1;"""
        cursor.execute(cheking_last_update)
        last_update = cursor.fetchone()[0]
        connection.commit()
        
        bot_updates = list(bot.get_updates(offset=last_update, limit=10, timeout=1000))
        print(len(bot_updates))
        for update in bot_updates:
            if update.update_id not in update_ids:
                try:
                    if update.message.chat.type == "private":
                        private_message_tuple = (update.update_id, update.message.chat.id, update.message.chat.username,  datetime.datetime.fromtimestamp(update.message.date), update.message.text)
                        cursor.execute(insert_private_message, private_message_tuple)
                        connection.commit()
                    else:
                        global_message_tuple = (update.update_id, update.message.chat.id, update.message.date, update.message.text)
                        cursor.execute(insert_global_message, global_message_tuple)
                        connection.commit()
                except AttributeError:
                    if update.edited_message.chat.type == "private":
                        private_message_tuple = (update.update_id, update.edited_message.chat.id, update.edited_message.chat.username, datetime.datetime.fromtimestamp(update.edited_message.date), update.edited_message.text)
                        cursor.execute(insert_private_message, private_message_tuple)
                        connection.commit()
                    else:
                        global_message_tuple = (update.update_id, update.edited_message.chat.id, update.edited_message.date, update.edited_message.text)
                        cursor.execute(insert_global_message, global_message_tuple)
                        connection.commit()
            else:
                pass
    
    def keyboard():
        markup = ReplyKeyboardMarkup(one_time_keyboard = True)
        markup.add(KeyboardButton("Инфо поступающим"), KeyboardButton("Найди мне работу"), KeyboardButton("КАМПУС"), KeyboardButton("Опрос для выпускников"))
        return markup

    def inline_keyboard_choice_ochno():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 2
        inline_markup.add(InlineKeyboardButton("Бюджетное образование", callback_data = "main_study"), InlineKeyboardButton("Дополнительное образование", callback_data = "dop_study"),
                          InlineKeyboardButton("FAQ", callback_data = "FAQ_ochno"))
        return inline_markup 

    def inline_keyboard_dop_study():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Повысить квалификацию", callback_data="qualification"), InlineKeyboardButton("Переподготовка", callback_data="restudy"),
                          InlineKeyboardButton("Профессиональное обучение", callback_data="prof_study"))
        return inline_markup
    
    def inline_keyboard_dop_study_price():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Рассрочки", callback_data="rassrochki"), InlineKeyboardButton("Студенческие кредиты", callback_data="krediti"), 
                          InlineKeyboardButton("Шаблоны документов", callback_data="get_shablons"))
        return inline_markup
    

    def inline_keyboard_info_first_choice():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Специальности", callback_data="info_specializations"), InlineKeyboardButton("Дополнительное профессиональное образование", callback_data = "info_dop_proffesion"),
                   InlineKeyboardButton("Есть ли льготы при поступлении?", callback_data = "info_privileges"), InlineKeyboardButton("Есть ли стипендия?", callback_data = "info_scholarship"), 
                   InlineKeyboardButton("Про материальную поддержку", callback_data = "info_material_support"))
        return markup
    
    def inline_keyboard_choice_specialization():
        inline_markup_3 = InlineKeyboardMarkup()
        inline_markup_3.row_width = 1
        inline_markup_3.add(InlineKeyboardButton("Архитектура. Средняя ЗП 60 тыс.", callback_data = "architecture"), InlineKeyboardButton("Мастер сухого строительства. Средняя ЗП 100 тыс.", callback_data = "builder"),
                             InlineKeyboardButton("Мастер ЖКХ. Средняя ЗП 30 тыс.", callback_data = "zhkh"), InlineKeyboardButton("Мастер декоративных работ. Средняя ЗП 90 тыс.", callback_data = "otdelka"),
                             InlineKeyboardButton("Строитель зданий. Средняя ЗП 30 тыс.", callback_data = "zdaniya"), InlineKeyboardButton("Водоснабжение и водоотведение. Средняя ЗП 140 тыс.", callback_data = "voda"),
                             InlineKeyboardButton("Дом. управление. Средняя ЗП 50 тыс.", callback_data = "domyprav"), InlineKeyboardButton("Столяр. Средняя ЗП 130 тыс.", callback_data = "stolyar"),
                             InlineKeyboardButton("Технология деревообработки. Средняя ЗП 25 тыс.", callback_data = "derevo"), InlineKeyboardButton("Сервис коммунального хозяйства. Средняя ЗП 25 тыс.", callback_data = "hozyaystvo"))
        return inline_markup_3
    
    def inline_keyboard_ochno_oformlenie():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Подготовительные курсы", callback_data="podgotov_kursi"), InlineKeyboardButton("Оформление онлайн", callback_data="oformlenie_online"), 
                          InlineKeyboardButton("Свяжитесь со мной по поступлению на подготовительные курсы", callback_data="callback_kursi"))
        return inline_markup

    def inline_keyboard_dop_kursi():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Есть ли вступительные испытания или нет?", callback_data="info_tests"), InlineKeyboardButton("Есть ли подготовительные курсы?", callback_data="tests_kursi"))    
        return inline_markup
    
    def inline_keyboard_dop_kursi_choice():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Расписание", callback_data="tests_time"), InlineKeyboardButton("Оставить заявку", callback_data="tests_zayavka"), 
                          InlineKeyboardButton("Стоимость", callback_data="info_price"))
        return inline_markup
    
    def inline_keyboard_dop_kursi_price_choice():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Оформление онлайн", callback_data="oformlenie_online"), InlineKeyboardButton("Свяжитесь со мной по поступлению на подготовительные курсы", callback_data="callback_kursi"))
        return inline_markup

    def inline_keyboard_quiz_specialization():
        inline_markup_5 = InlineKeyboardMarkup()
        inline_markup_5.row_width = 1
        inline_markup_5.add(InlineKeyboardButton("Архитектура", callback_data = "quiz_architecture"), InlineKeyboardButton("Мастер сухого строительства", callback_data = "quiz_builder"),
                             InlineKeyboardButton("Мастер ЖКХ", callback_data = "quiz_zhkh"))
        return inline_markup_5

    def inline_keyboard_quiz_callback():
        inline_markup_6 = InlineKeyboardMarkup()
        inline_markup_6.row_width = 2
        inline_markup_6.add(InlineKeyboardButton("Да", callback_data="yes_1"), InlineKeyboardButton("Нет", callback_data="no_1"))
        return inline_markup_6

    def inline_keyboard_quiz_callback_2():
        inline_markup_7 = InlineKeyboardMarkup()
        inline_markup_7.row_width = 2
        inline_markup_7.add(InlineKeyboardButton("Да", callback_data="yes_2"), InlineKeyboardButton("Нет", callback_data="no_2"))
        return inline_markup_7

    def inline_keyboard_quiz_callback_3():
        inline_markup_8 = InlineKeyboardMarkup()
        inline_markup_8.row_width = 2
        inline_markup_8.add(InlineKeyboardButton("Да", callback_data="yes_3"), InlineKeyboardButton("Нет", callback_data="no_3"))
        return inline_markup_8

    def inline_keyboard_kampus_specializtion():
        inline_markup_9 = InlineKeyboardMarkup()
        inline_markup_9.row_width = 1
        inline_markup_9.add(InlineKeyboardButton("Архитектура", callback_data= "kampus_architecture"), InlineKeyboardButton("Мастер сухого строительства", callback_data= "kampus_suhostroi"), 
                            InlineKeyboardButton("Мастер жилищно-коммунального хозяйства", callback_data= "kampus_zhkh"), InlineKeyboardButton("Мастер отделочных строительных и декоративных работ", callback_data= "kampus_otdelka"),
                            InlineKeyboardButton("Строительство и эксплуатация зданий и сооружений", callback_data= "kampus_zdaniya"), InlineKeyboardButton("Водоснабжение и водоотведение", callback_data= "kampus_voda"),
                            InlineKeyboardButton("Управление, эксплуатация и обслуживание многоквартирного дома", callback_data= "kampus_domyprav"), InlineKeyboardButton("Мастер столярного и мебельного производства", callback_data= "kampus_stolyar"),
                            InlineKeyboardButton("Технология деревообработки", callback_data= "kampus_derevo"), InlineKeyboardButton("Сервис домашнего и коммунального хозяйства", callback_data= "kampus_hozyaystvo"))
        return inline_markup_9

    def inline_keyboard_kampus_architecture_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 5
        inline_markup_10.add(InlineKeyboardButton("11-K",callback_data="kampus_architecture_group_11_k"), InlineKeyboardButton("12",callback_data="kampus_architecture_group_12"), 
                             InlineKeyboardButton("12-K",callback_data="kampus_architecture_group_12_k"), InlineKeyboardButton("20",callback_data="kampus_architecture_group_20"), 
                             InlineKeyboardButton("21-K",callback_data="kampus_architecture_group_21_k"), InlineKeyboardButton("22",callback_data="kampus_architecture_group_22"), 
                             InlineKeyboardButton("31-K",callback_data="kampus_architecture_group_31_k"), InlineKeyboardButton("32",callback_data="kampus_architecture_group_32"), 
                             InlineKeyboardButton("32-K",callback_data="kampus_architecture_group_32_k"), InlineKeyboardButton("41-K",callback_data="kampus_architecture_group_41_k"))
        return inline_markup_10
    
    def inline_keyboard_kampus_otdelka_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 5
        inline_markup_10.add(InlineKeyboardButton("10",callback_data="kampus_otdelka_group_10"), InlineKeyboardButton("11-K",callback_data="kampus_otdelka_group_11_k"), 
                             InlineKeyboardButton("12",callback_data="kampus_otdelka_group_12"), InlineKeyboardButton("12-K",callback_data="kampus_otdelka_group_12_k"), 
                             InlineKeyboardButton("13",callback_data="kampus_otdelka_group_13"), InlineKeyboardButton("14",callback_data="kampus_otdelka_group_14"), 
                             InlineKeyboardButton("15",callback_data="kampus_otdelka_group_15"), InlineKeyboardButton("16",callback_data="kampus_otdelka_group_16"), 
                             InlineKeyboardButton("17-K",callback_data="kampus_otdelka_group_17_k"), InlineKeyboardButton("18",callback_data="kampus_otdelka_group_18"),
                             InlineKeyboardButton("19",callback_data="kampus_otdelka_group_19"), InlineKeyboardButton("20",callback_data="kampus_otdelka_group_20"), 
                             InlineKeyboardButton("21-K",callback_data="kampus_otdelka_group_21_k"), InlineKeyboardButton("22",callback_data="kampus_otdelka_group_22"),
                             InlineKeyboardButton("23",callback_data="kampus_otdelka_group_23"), InlineKeyboardButton("24",callback_data="kampus_otdelka_group_24"), 
                             InlineKeyboardButton("25",callback_data="kampus_otdelka_group_25"), InlineKeyboardButton("26",callback_data="kampus_otdelka_group_26"), 
                             InlineKeyboardButton("27",callback_data="kampus_otdelka_group_27"), InlineKeyboardButton("28",callback_data="kampus_otdelka_group_28"),
                             InlineKeyboardButton("29",callback_data="kampus_otdelka_group_29"), InlineKeyboardButton("31-K",callback_data="kampus_otdelka_group_31_k"), 
                             InlineKeyboardButton("32",callback_data="kampus_otdelka_group_32"), InlineKeyboardButton("32-K",callback_data="kampus_otdelka_group_32_k"),
                             InlineKeyboardButton("33",callback_data="kampus_otdelka_group_33"), InlineKeyboardButton("34",callback_data="kampus_otdelka_group_34"), 
                             InlineKeyboardButton("35",callback_data="kampus_otdelka_group_35"), InlineKeyboardButton("36",callback_data="kampus_otdelka_group_36"), 
                             InlineKeyboardButton("37",callback_data="kampus_otdelka_group_37"), InlineKeyboardButton("38",callback_data="kampus_otdelka_group_38"), 
                             InlineKeyboardButton("39",callback_data="kampus_otdelka_group_39"), InlineKeyboardButton("41-K",callback_data="kampus_otdelka_group_41_k"), 
                             InlineKeyboardButton("44",callback_data="kampus_otdelka_group_44"), InlineKeyboardButton("48",callback_data="kampus_otdelka_group_48"), 
                             InlineKeyboardButton("СЭЗС, 1 курс",callback_data="kampus_otdelka_group_sezs_1"), InlineKeyboardButton("СЭЗС, 2 курс",callback_data="kampus_otdelka_group_sezs_2"), 
                             InlineKeyboardButton("СЭЗС, 3 курс",callback_data="kampus_otdelka_group_sezs_3"), InlineKeyboardButton("УМКД, 4 курс",callback_data="kampus_otdelka_group_ymkd_4"))
        return inline_markup_10
    
    def inline_keyboard_kampus_otdelka_group_temp():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 5
        inline_markup_10.add(InlineKeyboardButton("10",callback_data="kampus_otdelka_group_10"), InlineKeyboardButton("11-K",callback_data="kampus_otdelka_group_11_k_temp"), 
                             InlineKeyboardButton("12",callback_data="kampus_otdelka_group_12_temp"))
        return inline_markup_10
    
    def inline_keyboard_kampus_zdaniya_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 4
        inline_markup_10.add(InlineKeyboardButton("10",callback_data="kampus_zdaniya_group_10"), InlineKeyboardButton("17-K",callback_data="kampus_zdaniya_group_17_k"), 
                             InlineKeyboardButton("27",callback_data="kampus_zdaniya_group_27"), InlineKeyboardButton("37",callback_data="kampus_zdaniya_group_37"), 
                             InlineKeyboardButton("СЭЗС 1 курс",callback_data="kampus_zdaniya_group_sezs_1"), InlineKeyboardButton("СЭЗС 2 курс",callback_data="kampus_zdaniya_group_sezs_2"), 
                             InlineKeyboardButton("СЭЗС 3 курс",callback_data="kampus_zdaniya_group_sezs_3"))
        return inline_markup_10
    
    def inline_keyboard_kampus_voda_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 1
        inline_markup_10.add(InlineKeyboardButton("14",callback_data="kampus_voda_group_14"))
        return inline_markup_10
    
    def inline_keyboard_kampus_domyprav_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 3
        inline_markup_10.add(InlineKeyboardButton("19",callback_data="kampus_domyprav_group_19"), InlineKeyboardButton("29",callback_data="kampus_domyprav_group_29"), 
                             InlineKeyboardButton("39",callback_data="kampus_domyprav_group_39"), InlineKeyboardButton("УМКД 4 курс",callback_data="kampus_domyprav_group_ymkd_4"))
        return inline_markup_10
    
    def inline_keyboard_kampus_derevo_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 4
        inline_markup_10.add(InlineKeyboardButton("18",callback_data="kampus_derevo_group_18"), InlineKeyboardButton("28",callback_data="kampus_derevo_group_28"), 
                             InlineKeyboardButton("38",callback_data="kampus_derevo_group_38"), InlineKeyboardButton("48",callback_data="kampus_derevo_group_48"))
        return inline_markup_10
    
    def inline_keyboard_kampus_hozyaystvo_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 3
        inline_markup_10.add(InlineKeyboardButton("16",callback_data="kampus_hozyaystvo_group_16"), InlineKeyboardButton("26",callback_data="kampus_hozyaystvo_group_26"), 
                             InlineKeyboardButton("36",callback_data="kampus_hozyaystvo_group_36"))
        return inline_markup_10
    
    def inline_keyboard_kampus_hozyaystvo_16():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="hozyaystvo_16_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_hozyaystvo_26():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="hozyaystvo_26_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_hozyaystvo_36():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="hozyaystvo_36_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11

    
    def inline_keyboard_kampus_derevo_18():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="derevo_18_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11

    def inline_keyboard_kampus_derevo_28():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="derevo_28_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_derevo_38():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="derevo_38_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_derevo_48():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="derevo_48_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    

    def inline_keyboard_kampus_domyprav_19():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="domyprav_19_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_domyprav_29():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="domyprav_29_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_domyprav_39():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="domyprav_39_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_domyprav_ymkd_4():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="domyprav_ymkd_4_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_voda_14():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="voda_14_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11

    def inline_keyboard_kampus_zdaniya_10():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_10_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11

    def inline_keyboard_kampus_zdaniya_17_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_17_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zdaniya_27():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_27_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zdaniya_37():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_37_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zdaniya_sezs_1():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_sezs_1_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zdaniya_sezs_2():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_sezs_2_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zdaniya_sezs_3():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zdaniya_sezs_3_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_10():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_10_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_11_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_11_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_12():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_12_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_12_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_12_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_13():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_13_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_14():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_14_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_15():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_15_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_16():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_16_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_17_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_17_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_18():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_18_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_19():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_19_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_20():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_20_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_21_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_21_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_22():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_22_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_23():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_23_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_24():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_24_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_25():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_25_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_26():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_26_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_27():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_27_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_28():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_28_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_29():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_29_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_31_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_31_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_32():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_32_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_32_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_32_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_33():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_33_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_34():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_34_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_35():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_35_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_36():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_36_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_37():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_37_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_38():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_38_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_39():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_39_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_41_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_41_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_44():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_44_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_48():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_48_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_sezs_1():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_sezs_1_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_sezs_2():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_sezs_2_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_sezs_3():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_sezs_3_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_otdleka_ymkd_4():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="otdleka_ymkd_4_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    
    def inline_keyboard_kampus_suhoi_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 3
        inline_markup_10.add(InlineKeyboardButton("15",callback_data="kampus_suhoi_group_15"), InlineKeyboardButton("25",callback_data="kampus_suhoi_group_25"), 
                             InlineKeyboardButton("35",callback_data="kampus_suhoi_group_35"))
        return inline_markup_10

    def inline_keyboard_kampus_zhkh_group():
        inline_markup_10 = InlineKeyboardMarkup()
        inline_markup_10.row_width = 3
        inline_markup_10.add(InlineKeyboardButton("13",callback_data="kampus_zhkh_13"), InlineKeyboardButton("23",callback_data="kampus_zhkh_23"), 
                             InlineKeyboardButton("33",callback_data="kampus_zhkh_33"))
        return inline_markup_10
    
    def inline_keyboard_kampus_zhkh_13():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zhkh_13_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zhkh_23():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zhkh_23_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_zhkh_33():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="zhkh_33_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_suhoi_15():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="suhoi_15_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_suhoi_25():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="suhoi_25_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_suhoi_35():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="suhoi_35_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    

    def inline_keyboard_kampus_architecture_11_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_11_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_12():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_12_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_12_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_12_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_20():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_20_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_21_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_21_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_22():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_22_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_31_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_31_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_32():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_32_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_32_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_32_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_41_k():
        inline_markup_11 = InlineKeyboardMarkup()
        inline_markup_11.row_width = 3
        inline_markup_11.add(InlineKeyboardButton("Расписание", callback_data="architecture_41_k_rasp"), InlineKeyboardButton("Объявления", callback_data="architecture_11_k_attention"), 
                             InlineKeyboardButton("Вопросы", callback_data="architecture_11_k_question"))
        return inline_markup_11
    
    def inline_keyboard_kampus_architecture_11_k_faq():
        inline_markup_12 = InlineKeyboardMarkup()
        inline_markup_12.row_width = 2
        inline_markup_12.add(InlineKeyboardButton("FAQ", callback_data="architecture_11_k_question_faq"), InlineKeyboardButton("Свой вопрос", callback_data="architecture_11_k_my_question"))
        return inline_markup_12
    

    API_TOKEN = 'token'
    fio_int = 0
    oformlenie_int = 0
    tests_int = 0
    telephone_ended = 0
    telephone_int = 0
    bot = telebot.TeleBot(API_TOKEN)
    connection = psycopg2.connect(user = "postgres",
                              password = "Akadem53",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "telegram_bot")
    cursor = connection.cursor()
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Ну привет",reply_markup=keyboard())
    @bot.message_handler(commands=['help'])
    def commands_help(message):
        bot.reply_to(message, "Я пока ничего не умею :(")
    @bot.callback_query_handler(func=lambda call:True)
    def callback_query(call):
        global fio_int, oformlenie_int, tests_int
        if call.data == "nask":
            bot.send_message(call.message.chat.id, "Выберите форму обучения", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "zaochno":
            bot.answer_callback_query(call.id, "Пока недоступно")
        elif call.data == "info_specializations":
            bot.send_message(call.message.chat.id, "Выберите специальность", reply_markup=inline_keyboard_choice_specialization())
        elif call.data == "architecture":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "builder":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "zhkh":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "voda":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "zdaniya":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "domyprav":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "derevo":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "hozyaystvo":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "otdelka":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "stolyar":
            bot.send_message(call.message.chat.id, "Инфо", reply_markup=inline_keyboard_choice_ochno())
        elif call.data == "FAQ_ochno":
            bot.send_message(call.message.chat.id, "1) Предоставляете ли вы помощь в устройстве на работу?\n Да")
        elif call.data == "dop_study":
            bot.send_message(call.message.chat.id, "Какое именно дополнительно образование Вас интересует?", reply_markup=inline_keyboard_dop_study())
        elif call.data == "qualification" or call.data == "prof_study" or call.data == "restudy":
            bot.send_message(call.message.chat.id, "Цены обучения поступающих отличаются от года к году. Список на новый 2023ий учебный год будет предоставлен в первых числах июля", reply_markup=inline_keyboard_dop_study_price())
        elif call.data == "get_shablons":
            bot.send_message(call.message.chat.id, "Договор, Согласие на обработку данных", entities=[MessageEntity("text_link", 0, 7, url="https://disk.yandex.ru/i/B3-r2c1YQt0fUA"), MessageEntity("text_link", 8, 29, url="https://disk.yandex.ru/i/sDq9YY6sqtIkMw")], disable_web_page_preview = True)
        elif call.data == "rassrochki":
            bot.send_message(call.message.chat.id, "Учащимся платно могут быть предоставлены студенческие кредиты, рассрочки и другие варианты от НАСК и банков-партнеров.", entities=[MessageEntity("text_link", 101, 16, url="http://www.sberbank.ru/ru/person/credits/money/credit_na_obrazovanie")])
        elif call.data == "krediti":
            bot.send_message(call.message.chat.id, "Учащимся платно могут быть предоставлены студенческие кредиты, рассрочки и другие варианты от НАСК и банков-партнеров.", entities=[MessageEntity("text_link", 101, 16, url="http://www.sberbank.ru/ru/person/credits/money/credit_na_obrazovanie")])
        elif call.data == "main_study":
            bot.send_message(call.message.chat.id, "Про обучение", reply_markup=inline_keyboard_ochno_oformlenie())
        elif call.data == "podgotov_kursi":
            bot.send_message(call.message.chat.id, "Про дополнительные курсы", reply_markup=inline_keyboard_dop_kursi())
        elif call.data == "tests_kursi":
            bot.send_message(call.message.chat.id, "Подготовительные курсы есть", reply_markup=inline_keyboard_dop_kursi_choice())
        elif call.data == "info_price":
            bot.send_message(call.message.chat.id, "Цены обучения поступающих отличаются от года к году. Список на новый 2023ий учебный год будет предоставлен в первых числах июля", reply_markup=inline_keyboard_dop_kursi_price_choice())
        elif call.data == "tests_time":
            bot.send_message(call.message.chat.id, "Цены обучения поступающих отличаются от года к году. Список на новый 2023ий учебный год будет предоставлен в первых числах июля")
        elif call.data == "quiz_architecture":
            bot.send_message(call.message.chat.id, "Вы работаете по специальности? ", reply_markup=inline_keyboard_quiz_callback())
        elif call.data == "quiz_builder":
            bot.send_message(call.message.chat.id, "Вы работаете по специальности? ", reply_markup=inline_keyboard_quiz_callback())
        elif call.data == "quiz_zhkh":
            bot.send_message(call.message.chat.id, "Вы работаете по специальности? ", reply_markup=inline_keyboard_quiz_callback())           
        elif call.data == "yes_1" or call.data == "no_1":
            bot.send_message(call.message.chat.id, "Довольны ли вы качеством обучения в НАСК?", reply_markup=inline_keyboard_quiz_callback_2())
        elif call.data == "yes_2" or call.data == "no_2":
            bot.send_message(call.message.chat.id, "Желаете ли получить дополнительное образование? ", reply_markup=inline_keyboard_quiz_callback_3())
        elif call.data == "yes_3" or call.data == "no_3":
            bot.answer_callback_query(call.id, "Спасибо за ответы!")
            bot.send_message(call.message.chat.id, "Напишите пожалуйста в 2 следующих разных сообщения своё ФИО и телефон")
        elif call.data == "info_dop_proffesion":
            bot.send_message(call.message.chat.id, "Есть возможность получить дополнительное профессиональное образование, вся информация по ссылке: http://xn--80auhr.xn--p1ai/about/dopolnitelnoe-professionalnoe-obrazovanie.php")
        elif call.data == "info_scholarship":
            bot.send_message(call.message.chat.id, "Да, есть. Базовая стипендия начисляется тем, кто сдал сессию на хорошо и отлично. Размер базовой стипендии 647 рублей")
        elif call.data == "info_material_support":
            bot.send_message(call.message.chat.id, "Видов материальной поддержки много, вся информация по ссылке: http://xn--80auhr.xn--p1ai/about/material-support/")
        elif call.data == "info_privileges":
            bot.send_message(call.message.chat.id, "Различные льготы разным группам поступающих отличаются от года к году. Список на новый 2023-ий учебный год будет предоставлен в первых числах июля")
        elif call.data == "info_tests":
            bot.answer_callback_query(call.id, "Есть.")
        elif call.data == "kampus_architecture":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_architecture_group())
        elif call.data == "kampus_architecture_group_11_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_11_k())
        elif call.data == "kampus_architecture_group_12":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_12())
        elif call.data == "kampus_architecture_group_12_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_12_k())
        elif call.data == "kampus_architecture_group_20":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_20())
        elif call.data == "kampus_architecture_group_21_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_21_k())
        elif call.data == "kampus_architecture_group_22":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_22())
        elif call.data == "kampus_architecture_group_31_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_31_k())
        elif call.data == "kampus_architecture_group_32":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_32())
        elif call.data == "kampus_architecture_group_32_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_32_k())
        elif call.data == "kampus_architecture_group_41_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_architecture_41_k())
        elif call.data == "architecture_11_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/1k-1/")
        elif call.data == "architecture_12_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/2-k1/")
        elif call.data == "architecture_12_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/12-k/")
        elif call.data == "architecture_20_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/1e-1/")
        elif call.data == "architecture_21_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/21/")
        elif call.data == "architecture_22_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/1m-1/")
        elif call.data == "architecture_31_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/2m-1/")
        elif call.data == "architecture_32_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/2e-1/")
        elif call.data == "architecture_32_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/32-k/")
        elif call.data == "architecture_41_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/1m-16573/")
        elif call.data == "architecture_11_k_attention":
            bot.answer_callback_query(call.id, "Объявлений нет")
        elif call.data == "architecture_11_k_question":
            bot.send_message(call.message.chat.id, "Вопрос", reply_markup=inline_keyboard_kampus_architecture_11_k_faq())
        elif call.data == "architecture_11_k_question_faq":
            bot.send_message(call.message.chat.id, "1) Предоставляете ли вы помощь в устройстве на работу?\n Да")
        elif call.data == "architecture_11_k_my_question":
            bot.send_message(call.message.chat.id, "Напишите вопрос в свободной форме, ответ будет в личку от деканата")
        elif call.data == "kampus_suhoi_group_15":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_suhoi_15())
        elif call.data == "kampus_suhoi_group_25":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_suhoi_25())
        elif call.data == "kampus_suhoi_group_35":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_suhoi_35())
        elif call.data == "kampus_suhostroi":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_suhoi_group())
        elif call.data == "suhoi_15_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/15/")
        elif call.data == "suhoi_25_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/25/")
        elif call.data == "suhoi_35_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/metallurgicheskoe-otdelenie/35/")
        elif call.data == "kampus_zhkh":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_zhkh_group())
        elif call.data == "kampus_zhkh_13":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zhkh_13())
        elif call.data == "kampus_zhkh_23":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zhkh_23())
        elif call.data == "kampus_zhkh_33":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zhkh_33())
        elif call.data == "zhkh_13_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/otdelenie-ekonomiki-i-informatsionnykh-tekhnologiy/13/")
        elif call.data == "zhkh_23_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/otdelenie-ekonomiki-i-informatsionnykh-tekhnologiy/23/")
        elif call.data == "zhkh_33_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/schedule/otdelenie-ekonomiki-i-informatsionnykh-tekhnologiy/33/")
        elif call.data == "kampus_otdelka" or call.data == "kampus_stolyar":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_otdelka_group_temp())
        elif call.data == "kampus_otdelka_group_11_k_temp" or call.data == "kampus_otdelka_group_12_temp":
            bot.send_message(call.message.chat.id, "Будет добавлено позже")
        elif call.data == "kampus_otdelka_group_10":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_10())
        elif call.data == "kampus_otdelka_group_11_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_11_k())
        elif call.data == "kampus_otdelka_group_12":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_12())
        elif call.data == "kampus_otdelka_group_12_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_12_k())
        elif call.data == "kampus_otdelka_group_13":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_13())
        elif call.data == "kampus_otdelka_group_14":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_14())
        elif call.data == "kampus_otdelka_group_15":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_15())
        elif call.data == "kampus_otdelka_group_16":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_16())
        elif call.data == "kampus_otdelka_group_17_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_17_k())
        elif call.data == "kampus_otdelka_group_18":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_18())
        elif call.data == "kampus_otdelka_group_19":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_19())
        elif call.data == "kampus_otdelka_group_20":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_20())
        elif call.data == "kampus_otdelka_group_21_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_21_k())
        elif call.data == "kampus_otdelka_group_22":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_22())
        elif call.data == "kampus_otdelka_group_23":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_23())
        elif call.data == "kampus_otdelka_group_24":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_24())
        elif call.data == "kampus_otdelka_group_25":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_25())
        elif call.data == "kampus_otdelka_group_26":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_26())
        elif call.data == "kampus_otdelka_group_27":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_27())
        elif call.data == "kampus_otdelka_group_28":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_28())
        elif call.data == "kampus_otdelka_group_29":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_29())
        elif call.data == "kampus_otdelka_group_31_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_31_k())
        elif call.data == "kampus_otdelka_group_32":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_32())
        elif call.data == "kampus_otdelka_group_32_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_32_k())
        elif call.data == "kampus_otdelka_group_33":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_33())
        elif call.data == "kampus_otdelka_group_34":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_34())
        elif call.data == "kampus_otdelka_group_35":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_35())
        elif call.data == "kampus_otdelka_group_36":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_36())
        elif call.data == "kampus_otdelka_group_37":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_37())
        elif call.data == "kampus_otdelka_group_38":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_38())
        elif call.data == "kampus_otdelka_group_39":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_39())
        elif call.data == "kampus_otdelka_group_41_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_41_k())
        elif call.data == "kampus_otdelka_group_44":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_44())
        elif call.data == "kampus_otdelka_group_48":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_48())
        elif call.data == "kampus_otdelka_group_sezs_1":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_sezs_1())
        elif call.data == "kampus_otdelka_group_sezs_2":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_sezs_2())
        elif call.data == "kampus_otdelka_group_sezs_3":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_sezs_3())
        elif call.data == "kampus_otdelka_group_ymkd_4":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_otdleka_ymkd_4())
        elif call.data == "otdleka_10_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/10/")
        elif call.data == "otdleka_11_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/1k-1/")
        elif call.data == "otdleka_12_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/2-k1/")
        elif call.data == "otdleka_12_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/12-k/")
        elif call.data == "otdleka_13_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/13/")
        elif call.data == "otdleka_14_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/14/")
        elif call.data == "otdleka_15_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/15/")
        elif call.data == "otdleka_16_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/16/")
        elif call.data == "otdleka_17_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/17/")
        elif call.data == "otdleka_18_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/18/")
        elif call.data == "otdleka_19_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/19/")
        elif call.data == "otdleka_20_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/1e-1/")
        elif call.data == "otdleka_21_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/21/")
        elif call.data == "otdleka_22_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/1m-1/")
        elif call.data == "otdleka_23_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/23/")
        elif call.data == "otdleka_24_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/24/")
        elif call.data == "otdleka_25_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/25/")
        elif call.data == "otdleka_26_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/26/")
        elif call.data == "otdleka_27_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/27/")
        elif call.data == "otdleka_28_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/28/")
        elif call.data == "otdleka_29_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/29/")
        elif call.data == "otdleka_31_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/2m-1/")
        elif call.data == "otdleka_32_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/2e-1/")
        elif call.data == "otdleka_32_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/32-k/")
        elif call.data == "otdleka_33_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/33/")
        elif call.data == "otdleka_34_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/34/")
        elif call.data == "otdleka_35_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/35/")
        elif call.data == "otdleka_36_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/36/")
        elif call.data == "otdleka_37_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/37/")
        elif call.data == "otdleka_38_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/38/")
        elif call.data == "otdleka_39_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/39/")
        elif call.data == "otdleka_41_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/1m-16573/")
        elif call.data == "otdleka_44_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/44/")
        elif call.data == "otdleka_48_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/48/")
        elif call.data == "otdleka_sezs_1_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1/")
        elif call.data == "otdleka_sezs_2_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1%202%20%D0%BA%D1%83%D1%80%D1%81/")
        elif call.data == "otdleka_sezs_3_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1%203%20%D0%BA%D1%83%D1%80%D1%81/")
        elif call.data == "otdleka_ymkd_4_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/umkd-2-kurs/")
        elif call.data == "kampus_zdaniya":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_zdaniya_group())
        elif call.data == "kampus_zdaniya_group_10":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_10())
        elif call.data == "kampus_zdaniya_group_17_k":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_17_k())
        elif call.data == "kampus_zdaniya_group_27":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_27())
        elif call.data == "kampus_zdaniya_group_37":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_37())
        elif call.data == "kampus_zdaniya_group_sezs_1":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_sezs_1())
        elif call.data == "kampus_zdaniya_group_sezs_2":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_sezs_2())
        elif call.data == "kampus_zdaniya_group_sezs_3":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_zdaniya_sezs_3())
        elif call.data == "zdaniya_10_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/10/")
        elif call.data == "zdaniya_17_k_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/17/")
        elif call.data == "zdaniya_27_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/27/")
        elif call.data == "zdaniya_37_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/37/")
        elif call.data == "zdaniya_sezs_1_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1/")
        elif call.data == "zdaniya_sezs_2_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1%202%20%D0%BA%D1%83%D1%80%D1%81/")
        elif call.data == "zdaniya_sezs_3_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/%D0%A1%D0%AD%D0%97%D0%A1%203%20%D0%BA%D1%83%D1%80%D1%81/") 
        elif call.data == "kampus_voda":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_voda_group())
        elif call.data == "kampus_voda_group_14":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_voda_14())
        elif call.data == "voda_14_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/14/") 
        elif call.data == "kampus_domyprav":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_domyprav_group())
        elif call.data == "kampus_domyprav_group_19":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_domyprav_19())
        elif call.data == "kampus_domyprav_group_29":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_domyprav_29())
        elif call.data == "kampus_domyprav_group_39":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_domyprav_39())
        elif call.data == "kampus_domyprav_group_ymkd_4":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_domyprav_ymkd_4())
        elif call.data == "domyprav_19_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/19/") 
        elif call.data == "domyprav_29_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/29/") 
        elif call.data == "domyprav_39_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/39/") 
        elif call.data == "domyprav_ymkd_4_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/umkd-2-kurs/") 
 ###       elif call.data == "kampus_stolyar":
 ###           bot.send_message(call.message.chat.id, "На сайте написанны все группы, как к ""Мастер отделочных строительных и декоративных работ""")
        elif call.data == "kampus_derevo":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_derevo_group())
        elif call.data == "kampus_derevo_group_18":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_derevo_18())
        elif call.data == "kampus_derevo_group_28":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_derevo_28())
        elif call.data == "kampus_derevo_group_38":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_derevo_38())
        elif call.data == "kampus_derevo_group_48":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_derevo_48())
        elif call.data == "derevo_18_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/18/")
        elif call.data == "derevo_28_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/28/")
        elif call.data == "derevo_38_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/38/")
        elif call.data == "derevo_48_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/48/")
        elif call.data == "kampus_hozyaystvo":
            bot.send_message(call.message.chat.id, "Выберите группу", reply_markup=inline_keyboard_kampus_hozyaystvo_group())
        elif call.data == "kampus_hozyaystvo_group_16":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_hozyaystvo_16())
        elif call.data == "kampus_hozyaystvo_group_26":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_hozyaystvo_26())
        elif call.data == "kampus_hozyaystvo_group_36":
            bot.send_message(call.message.chat.id, "Что Вас интересует?", reply_markup=inline_keyboard_kampus_hozyaystvo_36())
        elif call.data == "hozyaystvo_16_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/16/")
        elif call.data == "hozyaystvo_26_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/26/")
        elif call.data == "hozyaystvo_36_rasp":
            bot.send_message(call.message.chat.id, "Расписание по ссылке: https://xn--80auhr.xn--p1ai/life/groups/36/")
        elif call.data == "tests_zayavka":
            fio_int = 1
            tests_int = 1
            bot.send_message(call.message.chat.id, "Напишите своё ФИО")
        elif call.data == "oformlenie_online":
            oformlenie_int = 1
            fio_int = 1
            bot.send_message(call.message.chat.id, "Напишите своё ФИО")
        elif call.data == "callback_kursi":
            fio_int = 1
            bot.send_message(call.message.chat.id, "Напишите своё ФИО")
            
      
    @bot.message_handler(func=lambda message:True)
    def all_messages(message):
        global fio_int, telephone_int, telephone_ended, tests_int, oformlenie_int
        connection.commit()
        insert_private_message = """INSERT INTO private_message (id, chat_id, destination_id, date, text) VALUES (%s, %s, %s, %s, %s)"""
        insert_global_message = """INSERT INTO private_message (id, chat_id,  date, text) VALUES (%s, %s, %s, %s)"""
        insert_destination = """INSERT INTO destination (id, first_name, last_name, language, username) VALUES (%s, %s, %s, %s, %s)"""
        select_destination_id = """SELECT id from destination"""
        cursor.execute(select_destination_id)
        destination_id_tuple = cursor.fetchall()
        destination_id = list()
        for item in destination_id_tuple:
            destination_id.append(int(item[0]))
        if message.from_user.id not in destination_id:
            destination_tuple = (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.language_code, message.from_user.username)
            cursor.execute(insert_destination, destination_tuple) 
            connection.commit()       
        if message.chat.type == "private":
                private_message_tuple = (message.message_id, message.chat.id, message.from_user.id,  datetime.datetime.fromtimestamp(message.date), message.text)
                cursor.execute(insert_private_message, private_message_tuple)
                connection.commit()
        else:
                global_message_tuple = (message.message_id, message.chat.id, message.date, message.text)
                cursor.execute(insert_global_message, global_message_tuple)
                connection.commit()
        if message.text == "КАМПУС":
            bot.send_message(message.chat.id, "Выберите специальность:", reply_markup=inline_keyboard_kampus_specializtion())
        elif message.text == "Найди мне работу":
            bot.send_message(message.chat.id, "В разработке")
        elif message.text == "Инфо поступающим":
            bot.send_message(message.chat.id, "Инфо", reply_markup=inline_keyboard_info_first_choice())
        elif message.text == "Опрос для выпускников":
            bot.send_message(message.chat.id, "По какой специальности вы оканчивали наш колледж?", reply_markup=inline_keyboard_quiz_specialization())
        elif fio_int == 1:
            our_message = message.text
            our_fio = our_message.split(" ")
            if len(our_fio) != 3:
                bot.send_message(message.chat.id, "Введённое ФИО не корректно, напишите пожалуйста ещё раз")
            else:
                fio_int = 0
                bot.send_message(message.chat.id, "Напишите свой телефон для связи")
                telephone_int = 1
        elif telephone_int == 1:
            try:
                phone = int(message.text)
                telephone_int = 0
                if oformlenie_int == 1:
                    bot.send_message(message.chat.id, "Договор, Согласие на обработку данных", entities=[MessageEntity("text_link", 0, 7, url="https://disk.yandex.ru/i/B3-r2c1YQt0fUA"), MessageEntity("text_link", 8, 29, url="https://disk.yandex.ru/i/sDq9YY6sqtIkMw")], disable_web_page_preview = True)
                    oformlenie_int = 0
                elif tests_int == 1:
                    bot.send_message(message.chat.id, "Напишите время, удобное для связи")
                    tests_int = 0
            except Exception:
                bot.send_message(message.chat.id, "Введённый телефон не корректен, напишите пожалуйста ещё раз")



 
 
    bot.infinity_polling()   

    

    connection.commit()
    
    cursor.execute("SELECT id from sending_messages")
    counter = cursor.fetchall()
    if len(counter) != 0:
        for item in counter:
            send_message()
            deleting_message = """DELETE from sending_messages where id = %s"""       
            cursor.execute(deleting_message, item)
            connection.commit()


    cursor.close()
    connection.close()

    
