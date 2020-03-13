import telebot
from io import BytesIO
from datetime import datetime
from db_manager import DBManager
from plate_creater import PlateCreater

# use Telegram bot authorized TOKEN
bot = telebot.TeleBot('[TOKEN]')

# use PostgreSQL login option
database = DBManager("[DBNAME]", "[USER]", "[PASSWORD]")

# use OpenALPR Cloud API secret key. DEMO version secret key for example: sk_DEMODEMODEMODEMODEMODEMO
plateCreater = PlateCreater('[SECRET_KEY]')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.chat.first_name}!\n\n'
                                      f'Я телеграм-бот, созданный для анализа фотографий на наличие '
                                      f'в них автомобильных номерных знаков ЕВРОПЕЙСКОГО образца и дальнейшего '
                                      f'добавления данной фотографии в базу данных.\n\n'
                                      f'Также, есть возможность получить фотографию автомобиля по его номерному знаку, '
                                      f'при наличии фото в данной базе данных\n\n'
                                      f'Для анализа фото - отправьте его в чат\n\n'
                                      f'Для получения фото из БД - напишите в чат номер автомобиля')


@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        database.create_connection()
        print('\nTry checking licence plate...')

        with BytesIO(database.get_data(message.text.upper())) as cur_photo:
            bot.send_message(message.chat.id, f'Фото автомобиля с государственным номером {message.text.upper()} '
                                              f'найдено в базе данных')
            bot.send_photo(message.chat.id, cur_photo)

    except TypeError as tp_err:
        print(f'ERROR: {tp_err}')
        bot.send_message(message.chat.id, f'Фото автомобиля с государственным номером {message.text.upper()} '
                                          f'отсутсвует в базе данных')

    except Exception as con_err:
        print(f'ERROR: {con_err}')
        bot.send_message(message.chat.id, 'Не удолось установить соединение с базой данных.\n\n'
                                          'Попробуйте добавить позже.')

    finally:
        if database.is_connected:
            database.close_connection()


@bot.message_handler(content_types=['photo'])
def send_photo(message):
    file_id = message.photo[-1].file_id
    path_to_file = bot.get_file(file_id).file_path

    downloaded_file = bot.download_file(path_to_file)
    plate = plateCreater.get_plate(downloaded_file)
    user_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    message_date = datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d')

    if plate == '':
        bot.send_message(user_id, 'Номер на фото не соотвествует ЕВРОПЕЙСКОМУ образцу или отсутсвует.\n\n'
                                  'Попробуйте оправить другое фото.')
    else:
        bot.send_message(user_id, f'Вы отпарили фото авто с государственным номером {plate}')

        print(f'\nUser {user_id} sent a photo\nTry connect to database...')

        try:
            database.create_connection()
            print('Try insert photo to database...')

            database.insert_data(plate, bytearray(downloaded_file), user_id, first_name, last_name, message_date)
            print('Photo inserted to database successful')

            bot.send_message(user_id, f'{first_name}, Ваше фото добавленно в базу данных. Спасибо!')



        except TypeError as tp_err:
            print(f'ERROR: {tp_err}')
            bot.send_message(user_id, 'Что-то пошло не так... Попробуйте позже.')

        except Exception as con_err:
            print(f'ERROR: {con_err}')
            bot.send_message(user_id, 'Не удолось установить соединение с базой данных.\n\n'
                                      'Попробуйте добавить фото позже.')

        finally:
            if database.is_connected:
                database.close_connection()

    del downloaded_file
    del plate


bot.polling()