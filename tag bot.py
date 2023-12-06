import psycopg2
from threading import Thread
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
import logging
from flask import Flask, request, jsonify

LOG = logging.getLogger(__name__)


if __name__ == "__main__":

    app = Flask(__name__)

    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w")

    connection = psycopg2.connect(user="postgres",
                                  password="Akadem53",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="telegram_bot")

    cursor = connection.cursor()
    connection.commit()
    API_TOKEN = 'token'

    bot = telebot.TeleBot(API_TOKEN)

    def keyboard():
        markup = ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(KeyboardButton("Мои вакансии"), KeyboardButton("Добавить вакансию"), KeyboardButton("Мой профиль"))
        return markup
    
    
    
    def inline_keyboard_profile_edit():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 1
        inline_markup.add(InlineKeyboardButton("Отредактировать данные", callback_data="data_edit"))
        return inline_markup
    

    def inline_keyboard_vac_edit():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 2
        inline_markup.add(InlineKeyboardButton("Изменить", callback_data="vac_edit"),
                             InlineKeyboardButton("Удалить", callback_data="vac_del"))
        return inline_markup
    
    def inline_keyboard_vac_del_confirm():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 2
        inline_markup.add(InlineKeyboardButton("Да", callback_data="vac_del_yes"),
                             InlineKeyboardButton("Нет", callback_data="vac_del_no"))
        return inline_markup
    
    def inline_keyboard_vac_edit_what():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 2
        inline_markup.add(InlineKeyboardButton("Название", callback_data="vac_edit_name"),
                             InlineKeyboardButton("З.П.", callback_data="vac_edit_pay"),
                             InlineKeyboardButton("Описание", callback_data="vac_edit_desc"),
                             InlineKeyboardButton("Адрес", callback_data="vac_edit_adress"))
        return inline_markup

    def inline_keyboard_profile_edit_what():
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 2
        inline_markup.add(InlineKeyboardButton("ФИО", callback_data="prof_edit_fio"),
                             InlineKeyboardButton("Телефон", callback_data="prof_edit_phone"),
                             InlineKeyboardButton("E-mail", callback_data="prof_edit_email"),
                             InlineKeyboardButton("Организацию", callback_data="prof_edit_org"))
        return inline_markup


    
    def setphone(id, phone):
        update_destination = """UPDATE employers set ask = 0, phone = %s where id = %s"""
        cursor.execute(update_destination, (phone, id))
        connection.commit()
    
    def askstage(id, stage):
        update_destination = """UPDATE employers set ask = %s where id = %s"""
        cursor.execute(update_destination, (stage, id))
        connection.commit()
        LOG.debug(f"Using DB, Method = UPDATE. Set ask stage, id = {id}, stage = {stage}")
    
    def set_vacancy_stage(id, user_id, stage):
        vac_stage = """UPDATE vacancies SET stage = %s WHERE id = %s AND employer = %s"""
        cursor.execute(vac_stage, (stage, id, user_id))
        connection.commit()
    
    def get_vacancy_stage(id, user_id):
        select_stage = """SELECT stage from vacancies where id = %s AND employer = %s"""
        cursor.execute(select_stage, (id, user_id))
        stage = cursor.fetchall()
        connection.commit()
        if not stage or stage[0][0] == None:
            return 0
        else:
            return stage[0][0]
    
    def get_vacancy_id(user_id):
        select_id = """SELECT id FROM vacancies WHERE employer = %s AND stage != 0"""
        cursor.execute(select_id, [user_id])
        vacancy_id = cursor.fetchall()
        connection.commit()
        if vacancy_id:
            return vacancy_id[0][0]
        else:
            return ()

    def check_not_finished_vacancies(user_id):
        select_id = """SELECT id FROM vacancies WHERE employer = %s AND stage != 0"""
        cursor.execute(select_id, [user_id])
        unfinished_ids = cursor.fetchall()
        if len(unfinished_ids) == 1:
            deleting_id = """DELETE FROM vacancies WHERE id = %s AND employer = %s"""
            cursor.execute(deleting_id, (unfinished_ids[0][0], user_id))
        elif unfinished_ids:
            for id in unfinished_ids[0]:
                deleting_id = """DELETE FROM vacancies WHERE id = %s AND employer = %s"""
                cursor.execute(deleting_id, (id, user_id))
        connection.commit()

    def getstage(id):
        select_stage = """SELECT ask from employers where id = %s"""
        cursor.execute(select_stage, [id])
        stage = cursor.fetchall()
        connection.commit()
        if not stage or stage[0][0] == None:
            return 0
        else:
            return stage[0][0]
        
    def fiocheck(id):
        select_fio = """SELECT fio FROM employers WHERE id = %s"""
        cursor.execute(select_fio, [id])
        fio = cursor.fetchall()
        connection.commit()
        if fio[0][0] == None:
            askstage(id, 2)
            return True
        else:
            return False

    def select_vacancies_by_employer(user_id):
        select_vacancies_amount = """SELECT id FROM vacancies WHERE employer = %s"""
        cursor.execute(select_vacancies_amount, [user_id])
        vacancy_amount = cursor.fetchall()
        if not vacancy_amount:
            return list()
        else:
            vacancy_list = list()
            for id in vacancy_amount:
                vacancy_list.append(int(id[0]))
            return(vacancy_list)
        
    def split_list(lst):
        return tuple(tuple(lst[i:i+5]) for i in range(0, len(lst), 5))

    
    def setfio(id, fio):
        set_fio = """UPDATE employers SET fio = %s, ask = 3 WHERE id = %s"""
        cursor.execute(set_fio, (fio, id))
        connection.commit()

    def set_email(id, email):
        set_mail = """UPDATE employers SET email = %s, ask = 4 WHERE id = %s"""
        cursor.execute(set_mail, (email, id))
        connection.commit()
    
    def update_email(id, email):
        set_mail = """UPDATE employers SET email = %s, ask = 0 WHERE id = %s"""
        cursor.execute(set_mail, (email, id))
        connection.commit()

    def get_user_data(id):
        select_fio = """SELECT fio FROM employers WHERE id = %s"""
        cursor.execute(select_fio, [id])
        fio = cursor.fetchall()
        if fio:
            fio = fio[0][0]
        else:
            fio = None
        select_phone = """SELECT phone FROM employers WHERE id = %s"""
        cursor.execute(select_phone, [id])
        phone = cursor.fetchall()
        if phone:
            phone = phone[0][0]
        else:
            phone = None
        select_email = """SELECT email FROM employers WHERE id = %s"""
        cursor.execute(select_email, [id])
        email = cursor.fetchall()
        if email:
            email = email[0][0]
        else:
            email = None
        select_org = """SELECT organisation FROM employers WHERE id = %s"""
        cursor.execute(select_org, [id])
        org = cursor.fetchall()
        if org:
            org = org[0][0]
        else:
            org = None
        return fio, phone, email, org
    
    def vac_set_edit(vac_id, user_id, type):
        vac_upd = """UPDATE vacancies SET to_edit = %s WHERE id = %s AND employer = %s"""
        cursor.execute(vac_upd, (type, vac_id, user_id))



    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        insert_destination = """INSERT INTO employers (id) VALUES (%s) """
        select_destination_id = """SELECT id from employers"""
        cursor.execute(select_destination_id)
        destination_id_tuple = cursor.fetchall()
        destination_id = list()
        for item in destination_id_tuple:
            destination_id.append(int(item[0]))
        if message.from_user.id not in destination_id:
            cursor.execute(insert_destination, [message.from_user.id])
            connection.commit()
        stage = getstage(message.from_user.id)
        try:
            stage = int(stage)
            if stage != 0:
                askstage(message.chat.id, 0)
        except TypeError:
            pass
        check_not_finished_vacancies(message.from_user.id)
        user_data = get_user_data(message.from_user.id)
        cursor.execute(f"UPDATE vacancies SET to_edit = 0, to_del = False WHERE employer = {message.from_user.id}")
        connection.commit()
        
        if None in user_data:
            bot.send_message(message.chat.id, "Приветствую Вас!\nЯ чат-бот ТАГ (Трудовой агрегатор).\nС радостью помогу Вашей компании в подборе сотрудников.\nДля идентификации и обратной связи пожалуйста введите номер вашего сотового в формате 7ХХХХХХХХХХ.", parse_mode='HTML')
            askstage(message.from_user.id, 1)
        else:
            fio = user_data[0]
            bot.send_message(message.chat.id, f"Здравствуйте, {fio}")
            bot.send_message(message.chat.id, "Я чат-бот ТАГ (Трудовой агрегатор).\nС радостью помогу Вашей компании в подборе сотрудников.", parse_mode='HTML', reply_markup=keyboard())
            
            

    
    @bot.message_handler(commands=['help'])
    def commands_help(message):
        bot.reply_to(message, "Для перезапуска работы бота введите /start. Если вдруг перестало работать меню то введите /menu")


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "data_edit":
            bot.send_message(call.message.chat.id, "Что вы хотите отредактировать?", reply_markup=inline_keyboard_profile_edit_what())
        elif call.data == "prof_edit_fio":
            bot.edit_message_text("Напишите новое ФИО", call.message.chat.id, call.message.message_id)
            askstage(call.message.chat.id, 10)
        elif call.data == "prof_edit_phone":
            bot.edit_message_text("Напишите новый телефон", call.message.chat.id, call.message.message_id)
            askstage(call.message.chat.id, 11)
        elif call.data == "prof_edit_email":
            bot.edit_message_text("Напишите новый e-mail", call.message.chat.id, call.message.message_id)
            askstage(call.message.chat.id, 12)
        elif call.data == "prof_edit_org":
            bot.edit_message_text("Напишите новое название организации", call.message.chat.id, call.message.message_id)
            askstage(call.message.chat.id, 13)


        elif call.data == "vac_del":
            to_del_vac_id = call.message.text.split(".")[0]
            set_vac_to_del = """UPDATE vacancies SET to_del = %s WHERE id = %s AND employer = %s"""
            cursor.execute(set_vac_to_del, (True, to_del_vac_id, call.message.chat.id))
            connection.commit()
            bot.send_message(call.message.chat.id, "Вы точно хотите удалить данную вакансию?", reply_markup=inline_keyboard_vac_del_confirm())
        elif call.data == "vac_del_yes":
            cursor.execute(f"DELETE FROM vacancies WHERE employer = {call.message.chat.id} AND to_del = {True}")
            connection.commit()
            bot.edit_message_text("Вакансия успешно удалена", call.message.chat.id, call.message.message_id)
        elif call.data == "vac_del_no":
            cursor.execute(f"UPDATE vacancies SET to_del = {False} WHERE employer = {call.message.chat.id} AND to_del = {True}")
            connection.commit()
            bot.edit_message_text("Вакансия не будет удалена, можете продолжать пользоваться ботом", call.message.chat.id, call.message.message_id)


        elif call.data == "vac_edit":
            to_edit_vac_id = call.message.text.split(".")[0]
            set_vac_to_edit = """UPDATE vacancies SET to_edit = %s WHERE id = %s AND employer = %s"""
            cursor.execute(set_vac_to_edit, (1, to_edit_vac_id, call.message.chat.id))
            connection.commit()
            bot.send_message(call.message.chat.id, "Что вы хотите изменить?", reply_markup=inline_keyboard_vac_edit_what())
        elif call.data == "vac_edit_name":
            bot.edit_message_text("Напишите новое название вакансии", call.message.chat.id, call.message.message_id)
            select_vac_to_edit = """SELECT id FROM vacancies WHERE employer = %s AND to_edit = 1"""
            cursor.execute(select_vac_to_edit, (call.message.chat.id, ))
            vac_id = cursor.fetchall()[0][0]
            vac_set_edit(vac_id, call.message.chat.id, 2)
        elif call.data == "vac_edit_pay":
            bot.edit_message_text("Напишите новую з.п.", call.message.chat.id, call.message.message_id)
            select_vac_to_edit = """SELECT id FROM vacancies WHERE employer = %s AND to_edit = 1"""
            cursor.execute(select_vac_to_edit, (call.message.chat.id, ))
            vac_id = cursor.fetchall()[0][0]
            vac_set_edit(vac_id, call.message.chat.id, 3)
        elif call.data == "vac_edit_desc":
            bot.edit_message_text("Напишите новое описание", call.message.chat.id, call.message.message_id)
            select_vac_to_edit = """SELECT id FROM vacancies WHERE employer = %s AND to_edit = 1"""
            cursor.execute(select_vac_to_edit, (call.message.chat.id, ))
            vac_id = cursor.fetchall()[0][0]
            vac_set_edit(vac_id, call.message.chat.id, 4)
        elif call.data == "vac_edit_adress":
            bot.edit_message_text("Напишите новый адрес", call.message.chat.id, call.message.message_id)
            select_vac_to_edit = """SELECT id FROM vacancies WHERE employer = %s AND to_edit = 1"""
            cursor.execute(select_vac_to_edit, (call.message.chat.id, ))
            vac_id = cursor.fetchall()[0][0]
            vac_set_edit(vac_id, call.message.chat.id, 5)




    @bot.message_handler(func=lambda message: True)
    def all_messages(message):
        connection.commit()
        stage = int(getstage(message.from_user.id))
        cursor.execute(f"SELECT to_edit FROM vacancies WHERE employer = {message.from_user.id} AND to_edit != 0")
        vac_edit_tmp = cursor.fetchall()
        if vac_edit_tmp:
            vac_edit = vac_edit_tmp[0][0]
        else:
            vac_edit = 0
    
        if get_vacancy_id(message.from_user.id):
            vacancy_stage = get_vacancy_stage((get_vacancy_id(message.from_user.id)), message.from_user.id)
        else: 
            vacancy_stage = 0

        insert_destination = """INSERT INTO employers (id) VALUES (%s) """
        select_destination_id = """SELECT id from employers"""
        cursor.execute(select_destination_id)
        destination_id_tuple = cursor.fetchall()
        destination_id = list()
        for item in destination_id_tuple:
            destination_id.append(int(item[0]))
        if message.from_user.id not in destination_id:
            cursor.execute(insert_destination, [message.from_user.id])
            connection.commit()

        if stage == 1:
            try:
                our_message = message.text.strip()
                our_message = our_message.replace(' ', '').replace('-', '').replace('+', '')
                if our_message[0] == '8':
                    our_message = '7' + our_message[1:]
                if our_message[0] != "7":
                    int("SuS")
                if len(our_message) < 8 or len(our_message) > 13:
                    int("SuS")
                phone_check = """SELECT id FROM employers WHERE phone = %s"""
                cursor.execute(phone_check, [our_message])
                id = cursor.fetchall()
                if id:
                    id = id[0][0]
                    if id != message.from_user.id:
                        bot.send_message(message.chat.id, "Введённый телефон уже зарегестрирован, пожалуйста используйте другой номер")
                    else:
                        phone = int(our_message)
                        setphone(message.chat.id, phone)
                        bot.send_message(message.chat.id, "Спасибо! Сотовый сохранен в системе")
                        bot.send_message(message.chat.id, "Напишите пожалуйства своё ФИО ")
                        askstage(message.from_user.id, 2)
                else:
                    phone = int(our_message)
                    setphone(message.chat.id, phone)
                    bot.send_message(message.chat.id, "Спасибо! Сотовый сохранен в системе")
                    bot.send_message(message.chat.id, "Напишите пожалуйства своё ФИО ")
                    askstage(message.from_user.id, 2)
            except ValueError:
                wrong_message = message.text.strip()
                bot.send_message(message.chat.id, "Введённый телефон не корректен, напишите пожалуйста ещё раз")
                LOG.debug(f"Telephone incorrect, message: {wrong_message}")

        elif stage == 2:
            our_message_fio = message.text.strip()
            our_fio = our_message_fio.split(' ')
            if len(our_fio) != 3:
                bot.send_message(message.chat.id, "Введённое ФИО не корректно, напишите пожалуйста ещё раз")
            else:
                setfio(message.from_user.id, ' '.join(our_fio))
                bot.send_message(message.chat.id, "Напишите пожалуйста email для связи")

        elif stage == 3:
            our_message_email = message.text.strip()
            if "@" and "." not in our_message_email:
                bot.send_message(message.chat.id, "Введённый email не корректен, напишите пожалуйста ещё раз")
            else:
                set_email(message.from_user.id, our_message_email)
                bot.send_message(message.chat.id, "Напишите пожалуйста название организации, которую Вы представляете")

        elif stage == 4:
            our_message_org = message.text.strip()
            insert_org = """UPDATE employers SET ask = 0, organisation = %s WHERE id = %s"""
            cursor.execute(insert_org, (our_message_org, message.from_user.id))
            connection.commit()
            bot.send_message(message.chat.id, "Спасибо!", reply_markup=keyboard())
        
        elif stage == 10:
            our_message_fio = message.text.strip()
            our_fio = our_message_fio.split(' ')
            if len(our_fio) != 3:
                bot.send_message(message.chat.id, "Введённое ФИО не корректно, напишите пожалуйста ещё раз")
            else:
                setfio(message.from_user.id, ' '.join(our_fio))
                askstage(message.from_user.id, 0)
                bot.send_message(message.chat.id, "ФИО успешно обновленно")

        elif stage == 11:
            try:
                our_message = message.text.strip()
                our_message = our_message.replace(' ', '').replace('-', '').replace('+', '')
                if our_message[0] == '8':
                    our_message = '7' + our_message[1:]
                if our_message[0] != "7":
                    int("SuS")
                if len(our_message) < 8 or len(our_message) > 13:
                    int("SuS")
                phone_check = """SELECT id FROM employers WHERE phone = %s"""
                cursor.execute(phone_check, [our_message])
                id = cursor.fetchall()
                if id:
                    id = id[0][0]
                    if id != message.from_user.id:
                        bot.send_message(message.chat.id, "Введённый телефон уже зарегестрирован, пожалуйста используйте другой номер")
                    else:
                        phone = int(our_message)
                        setphone(message.chat.id, phone)
                        bot.send_message(message.chat.id, "Сотовый успешно обновлённ")
                else:
                    phone = int(our_message)
                    setphone(message.chat.id, phone)
                    bot.send_message(message.chat.id, "Сотовый успешно обновлённ")
            except ValueError:
                wrong_message = message.text.strip()
                bot.send_message(message.chat.id, "Введённый телефон не корректен, напишите пожалуйста ещё раз")
                LOG.debug(f"Telephone incorrect, message: {wrong_message}")
        
        elif stage == 12:
            our_message_email = message.text.strip()
            if "@" and "." not in our_message_email:
                bot.send_message(message.chat.id, "Введённый email не корректен, напишите пожалуйста ещё раз")
            else:
                update_email(message.from_user.id, our_message_email)
                bot.send_message(message.chat.id, "E-mail успешно обновлённ")

        elif stage == 13:
            our_message_org = message.text.strip()
            insert_org = """UPDATE employers SET ask = 0, organisation = %s WHERE id = %s"""
            cursor.execute(insert_org, (our_message_org, message.from_user.id))
            connection.commit()
            bot.send_message(message.chat.id, "Организация успешно обновленна")

        elif vacancy_stage == 1:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Название не было записано, напишите пожалуйста ещё раз")
                pass
            else:
                vacancy_id = get_vacancy_id(message.from_user.id)
                set_vacancy_name = """UPDATE vacancies SET name = %s WHERE id = %s AND employer = %s"""
                cursor.execute(set_vacancy_name, (message.text, vacancy_id, message.from_user.id))
                connection.commit()
                bot.send_message(message.chat.id, "Напишите з. п.")
                set_vacancy_stage(vacancy_id, message.from_user.id, 2)

        elif vacancy_stage == 2:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "З.п. не была записана, напишите пожалуйста ещё раз")
                pass
            else:
                vacancy_id = get_vacancy_id(message.from_user.id)
                set_vacancy_pay = """UPDATE vacancies SET pay = %s WHERE id = %s AND employer = %s"""
                cursor.execute(set_vacancy_pay, (message.text, vacancy_id, message.from_user.id))
                connection.commit()
                bot.send_message(message.chat.id, "Напишите место работы")
                set_vacancy_stage(vacancy_id, message.from_user.id, 3)
        
        elif vacancy_stage == 3:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Адрес не был записан, напишите пожалуйста ещё раз")
                pass
            else:
                vacancy_id = get_vacancy_id(message.from_user.id)
                set_vacancy_adress = """UPDATE vacancies SET adress = %s WHERE id = %s AND employer = %s"""
                cursor.execute(set_vacancy_adress, (message.text, vacancy_id, message.from_user.id))
                connection.commit()
                bot.send_message(message.chat.id, "Напишите описание вакансии")
                set_vacancy_stage(vacancy_id, message.from_user.id, 4)
        
        elif vacancy_stage == 4:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Описание не было записано, напишите пожалуйста ещё раз")
                pass
            else:
                vacancy_id = get_vacancy_id(message.from_user.id)
                set_vacancy_description = """UPDATE vacancies SET description = %s WHERE id = %s AND employer = %s"""
                cursor.execute(set_vacancy_description, (message.text, vacancy_id, message.from_user.id))
                connection.commit()
                bot.send_message(message.chat.id, "Вакансия успешно сохранена.")
                set_vacancy_stage(vacancy_id, message.from_user.id, 0)
        
        elif vac_edit == 2:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Название не было обновленно, напишите пожалуйста ещё раз")
                pass
            else:
                bot.send_message(message.chat.id, "Название успешно обновлено")
                name = message.text.strip()
                vac_name_upd = """UPDATE vacancies SET name = %s, to_edit = 0 WHERE to_edit = 2 AND employer = %s"""
                cursor.execute(vac_name_upd, (name, message.from_user.id))
                connection.commit()
        
        elif vac_edit == 3:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "З.п. не была обновлена, напишите пожалуйста ещё раз")
                pass
            else:
                bot.send_message(message.chat.id, "З.п. успешно обновлена")
                pay = message.text.strip()
                vac_pay_upd = """UPDATE vacancies SET pay = %s, to_edit = 0 WHERE to_edit = 3 AND employer = %s"""
                cursor.execute(vac_pay_upd, (pay, message.from_user.id))
                connection.commit()
            
        elif vac_edit == 4:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Описание не было обновлено, напишите пожалуйста ещё раз")
                pass
            else:
                bot.send_message(message.chat.id, "Описание успешно обновлено")
                desc = message.text.strip()
                vac_desc_upd = """UPDATE vacancies SET description = %s, to_edit = 0 WHERE to_edit = 4 AND employer = %s"""
                cursor.execute(vac_desc_upd, (desc, message.from_user.id))
                connection.commit()
                            
        elif vac_edit == 5:
            if message.text.lower() == "мой профиль" or message.text.lower() == "добавить вакансию" or message.text.lower() == "мои вакансии":
                bot.send_message(message.chat.id, "Адрес не был обновлён, напишите пожалуйста ещё раз")
                pass
            else:
                bot.send_message(message.chat.id, "Адрес успешно обновлён")
                adress = message.text.strip()
                vac_adress_upd = """UPDATE vacancies SET adress = %s, to_edit = 0 WHERE to_edit = 5 AND employer = %s"""
                cursor.execute(vac_adress_upd, (adress, message.from_user.id))
                connection.commit()
            
        elif message.text.lower() == "мои вакансии":
            vacancy_list = select_vacancies_by_employer(message.from_user.id)
            if not vacancy_list:
                bot.send_message(message.chat.id, "У Вас нет вакансий")
            else:
                vacancy_list.sort()
                for vac_id in vacancy_list:
                    select_vacancy_data = """SELECT name, pay, adress, description FROM vacancies WHERE id = %s AND employer = %s"""
                    cursor.execute(select_vacancy_data, (vac_id, message.from_user.id))
                    vac_data = cursor.fetchall()
                    vac_name = vac_data[0][0]
                    vac_pay = vac_data[0][1]
                    vac_adress = vac_data[0][2]
                    vac_desc = vac_data[0][3]
                    bot.send_message(message.chat.id, f"{vac_id}. Название: {vac_name}\nЗар. плата: {vac_pay}\nАдрес: {vac_adress}\nОписание: {vac_desc}", reply_markup=inline_keyboard_vac_edit())

        elif message.text.lower() == "мой профиль":
            user_data = get_user_data(message.from_user.id)
            bot.send_message(message.chat.id, f"Ваш профиль:\nФИО: {user_data[0]}\nТелефон: {user_data[1]}\ne-mail: {user_data[2]}\nНазвание организации: {user_data[3]}", reply_markup=inline_keyboard_profile_edit())
        
        elif message.text.lower() == "добавить вакансию":
            bot.send_message(message.chat.id, "Напишите название вакансии")
            vacancy_list = select_vacancies_by_employer(message.from_user.id)
            insert_vacancy = """INSERT INTO vacancies (id, employer, stage) VALUES (%s, %s, 1)"""
            if not vacancy_list:
                cursor.execute(insert_vacancy, (1, message.from_user.id))
            else:
                cursor.execute(insert_vacancy, (max(vacancy_list)+1, message.from_user.id))
            connection.commit()
        
        else:
            pass

    def tuple_to_assocarray(tuple):
        array = []
        for row in tuple:
            record = {}
            col = 0
            for d in cursor.description:
                if d[0] == "finishdate":
                    record[d[0]] = row[col].strftime("%Y-%m-%d")
                else:
                    record[d[0]] = row[col]
                col = col + 1
            array.append(record)
        return array    
            
    @app.route('/GetEmployers', methods=['GET'])
    def getemployers():
        cursor.execute("""SELECT id, fio, phone, email, organisation FROM employers""")
        return_tuple = cursor.fetchall()
        return_array = tuple_to_assocarray(return_tuple)
        LOG.debug("Using DB, Method = SELECT. Selecting id, phone and fio, endpoint /GetUIDSAndPhonesAndNames")
        return jsonify(return_array)
    
    @app.route('/GetVacancies', methods=['GET'])
    def getvacancies():
        cursor.execute("""SELECT employer, name, pay, adress, description FROM vacancies""")
        return_tuple = cursor.fetchall()
        return_array = tuple_to_assocarray(return_tuple)
        LOG.debug("Using DB, Method = SELECT. Selecting id, phone and fio, endpoint /GetUIDSAndPhonesAndNames")
        return jsonify(return_array)    
    
    botThread = Thread(target=bot.infinity_polling)
    botThread.daemon = True
    botThread.start()
#    bot.infinity_polling()
    app.run(host='0.0.0.0', port=80, debug=True)

 
    





