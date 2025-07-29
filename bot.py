import telebot
from telebot import types
from datetime import datetime
import uuid
import math

API_TOKEN = '8110459054:AAE-twMstc5mDLp7jeXSjtYJz6tX48Jaiik'  # ВАШ API ТОКЕН
bot = telebot.TeleBot(API_TOKEN)
admin_ids = [1453081434,331697484]  # ID Администраторов

# Хранение данных пользователя
user_data = {}
orders = []  # Все заявки будут сохраняться в этом списке
# Хранение всех сессий
all_sessions = {}  # ключ - session_id, значение - словарь сессии

# Состояния
states = {
    'start': 0,
    'agreed': 1,
    'menu': 2,
    'city': 3,
    'area': 4,
    'podium': 5,
    'floor': 6,
    'wall_height': 7,
    'meeting_rooms': 8,
    'meeting_room1': 9,
    'meeting_room2': 10,
    'utility_room': 11,
    'utility_room_area': 12,
    'doors': 13,
    'overhead': 14,
    'light_logos': 15,
    'non_light_logos': 16,
    'reception_stands': 17,
    'podmaketniki': 18,
    'kashpo': 19,
    'plants': 20,
    'tv': 21,
    'tv_size': 22,
    'tv_size2': 23,
    'tv_size3': 24,
    'tv_size4': 25,
    'led_screens': 26,
    'led_size1': 27,
    'led_size2': 28,
    'event_name': 29,
    'furniture': 30,
    'furniture_tommy': 31,
    'furniture_gydra': 32,
    'furniture_eams': 33,
    'furniture_sofa': 34,
    'furniture_coffee_table': 35,
    'furniture_meeting_table': 36,
    'furniture_samba_chairs': 37,
    'furniture_fridge': 38,
    'furniture_fridge_size': 39,
    'furniture_cooler': 40,
    'furniture_coffee': 41,
    'furniture_shelves': 42,
    'finish': 100,
    'admin_panel': 200,
    'admin_orders': 201,
    'admin_clear': 202,
    'admin_stats': 203,
}

# Обратное сопоставление для отображения названий вопросов
reverse_states = {v: k for k, v in states.items()}

# Словарь для отображения вопросов на русском языке
question_display_names = {
    'start': 'Начало',
    'agreed': 'Согласие на обработку данных',
    'menu': 'Меню',
    'city': 'Город',
    'area': 'Площадь стенда',
    'podium': 'Подиум',
    'floor': 'Напольное покрытие',
    'wall_height': 'Высота стен',
    'meeting_rooms': 'Количество переговорных комнат',
    'meeting_room1': 'Площадь переговорной 1',
    'meeting_room2': 'Площадь переговорной 2',
    'utility_room': 'Подсобное помещение',
    'utility_room_area': 'Площадь подсобки',
    'doors': 'Количество дверей',
    'overhead': 'Подвесная конструкция',
    'light_logos': 'Световых логотипов',
    'non_light_logos': 'Несветовых логотипов',
    'reception_stands': 'Стоек-ресепшен',
    'podmaketniki': 'Тумб-подмакетников',
    'kashpo': 'Кашпо с растениями',
    'plants': 'Тип растений',
    'tv': 'Количество ТВ-плазм',
    'tv_size': 'Размер ТВ 1',
    'tv_size2': 'Размер ТВ 2',
    'tv_size3': 'Размер ТВ 3',
    'tv_size4': 'Размер ТВ 4',
    'led_screens': 'Количество светодиодных экранов',
    'led_size1': 'Размер LED 1',
    'led_size2': 'Размер LED 2',
    'event_name': 'Название выставки',
    'furniture': 'Мебель',
    'furniture_tommy': 'Барные стулья Tommy',
    'furniture_gydra': 'Круглые столы GYDRA',
    'furniture_eams': 'Стулья EAMS',
    'furniture_sofa': 'Диваны',
    'furniture_coffee_table': 'Журнальные столы',
    'furniture_meeting_table': 'Переговорные столы',
    'furniture_samba_chairs': 'Кресла SAMBA',
    'furniture_fridge': 'Холодильник',
    'furniture_fridge_size': 'Размер холодильника',
    'furniture_cooler': 'Кулер',
    'furniture_coffee': 'Кофемашина',
    'furniture_shelves': 'Стеллажи',
    'finish': 'Завершение расчета',
    'admin_panel': 'Backdoor',
    'admin_orders': 'Заявки админа',
    'admin_clear': 'Очистка истории',
    'admin_stats': 'Статистика',
}

# Цены
prices = {
    'moscow': {
        'floor': {'carpet': {'with_podium': 1000, 'no_podium': 1500},
                  'laminate': {'with_podium': 2500, 'no_podium': 3000}},
        'wall': 9000,
        'overhead': {'small': 600000, 'big': 1200000},
        'tv': {'32': 10000, '50': 15000, '70': 35000, '85': 90000},
        'plants': {'live': 60000, 'fake': 45000},
        'light_logo': 45000,
        'non_light_logo': 15000,
        'podmaketnik': 50000,
        'door': 15000,
        'led_screen': 50000,
        'documentation': 2500,
        'accreditation': {'base': 1600, 'extra': 450, 'fix': 50000 + 15000},
        'electricity': {'base': 15000, 'perimeter': 3000},
        'transport': 80000,
        'mount': 0,
        'dismount': 0,
        'reception_stand': 100000,
        'podmaketnik_price': 50000,
        'podium_base_cost': 3000
    },
    'spb': {
        'floor': {'carpet': {'with_podium': 1000, 'no_podium': 1500},
                  'laminate': {'with_podium': 2500, 'no_podium': 3000}},
        'wall': 7500,
        'overhead': {'small': 500000, 'big': 1000000},
        'tv': {'32': 10000, '50': 15000, '70': 35000, '85': 90000},
        'plants': {'live': 60000, 'fake': 45000},
        'light_logo': 45000,
        'non_light_logo': 15000,
        'podmaketnik': 50000,
        'door': 15000,
        'led_screen': 50000,
        'documentation': 2500,
        'accreditation': {'base': 1600, 'extra': 450, 'fix': 50000 + 15000},
        'electricity': {'base': 15000, 'perimeter': 3000},
        'transport': 40000,
        'mount': 0,
        'dismount': 0,
        'reception_stand': 100000,
        'podmaketnik_price': 50000,
        'podium_base_cost': 2500
    },

}


# Inline-кнопки
def create_inline_keyboard(options, include_back=True, include_skip=False, include_menu=True):
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text=opt, callback_data=opt) for opt in options]
    for btn in buttons:
        markup.add(btn)
    if include_back:
        markup.add(types.InlineKeyboardButton(text='⬅ Назад', callback_data='back'))
    if include_skip:
        markup.add(types.InlineKeyboardButton(text='🚫 Не нужно', callback_data='skip'))
    if include_menu:
        markup.add(types.InlineKeyboardButton(text='🏠 Вернуться в меню', callback_data='back_to_menu'))
    return markup


# Сброс данных
def reset_user_data(chat_id):
    if chat_id not in user_data:
        user_data[chat_id] = {
            'state': states['start'],
            'current_session': None,
            'sessions': [],
            'agreed': False,
            'answers': {},
            'last_state': None
        }
    else:
        if 'answers' not in user_data[chat_id]:
            user_data[chat_id]['answers'] = {}


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id in user_data and user_data[chat_id].get('agreed', False):
        user_data[chat_id]['state'] = states['menu']
        ask_question(chat_id)
    else:
        reset_user_data(chat_id)

        bot.send_message(chat_id,
                         "Бот осуществляет расчет стоимости выставочного стенда на основании проектов-аналогов 2025 года. Смета является приблизительной, итоговая стоимость должна рассчитываться специалистом на основании утвержденного дизайна.")
        bot.send_message(chat_id,
                         "Для продолжения использования бота вы должны дать согласие на обработку ваших персональных данных, включая сбор, хранение и использование информации, необходимой для предоставления услуг и улучшения пользовательского опыта, в соответствии с нашей политикой конфиденциальности.")

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='✅ СОГЛАШАЮСЬ', callback_data='agree'))
        bot.send_message(chat_id, "Нажмите, чтобы дать согласие:", reply_markup=markup)


# Получение текущей сессии
def get_current_session(chat_id):
    if chat_id not in user_data:
        reset_user_data(chat_id)
    current_id = user_data[chat_id].get('current_session')
    for s in user_data[chat_id]['sessions']:
        if s['id'] == current_id:
            return s
    return None


# Создание новой сессии
def create_new_session(chat_id):
    if chat_id not in user_data:
        reset_user_data(chat_id)
    session_id = str(uuid.uuid4())
    new_session = {
        'id': session_id,
        'user_chat_id': chat_id,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'answers': {},
        'finished': False,
        'submitted': False,
        'total': None
    }
    user_data[chat_id]['sessions'].append(new_session)
    user_data[chat_id]['current_session'] = session_id
    all_sessions[session_id] = new_session
    return new_session


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if chat_id not in user_data:
        reset_user_data(chat_id)

    current_state = user_data[chat_id]['state']
    user_data[chat_id]['last_state'] = current_state

    if data == 'agree':
        user_data[chat_id]['state'] = states['menu']
        user_data[chat_id]['agreed'] = True
        ask_question(chat_id)


    elif data == 'back':
        if current_state == states['plants']:
            user_data[chat_id]['state'] = states['kashpo']
        elif current_state == states['podmaketniki']:
            user_data[chat_id]['state'] = states['reception_stands']
        elif current_state == states['reception_stands']:
            user_data[chat_id]['state'] = states['light_logos']
        elif current_state > states['city']:
            user_data[chat_id]['state'] -= 1
        ask_question(chat_id)

    elif data == 'skip':
        current_state = user_data[chat_id]['state']
        user_data[chat_id]['answers'][current_state] = 'Не нужно'
        user_data[chat_id]['state'] += 1
        ask_question(chat_id)


    elif data == 'Посчитать стоимость стенда':
        create_new_session(chat_id)
        user_data[chat_id]['state'] = states['city']
        ask_question(chat_id)

    elif data == 'Админская панель':  # Эта ветка для первого входа в админку из главного меню
        if chat_id in admin_ids:
            user_data[chat_id]['state'] = states['admin_panel']
            ask_question(chat_id)
        else:
            bot.send_message(chat_id, "❌ У вас нет доступа к админ-панели.")
            user_data[chat_id]['state'] = states['menu']
            ask_question(chat_id)

    elif data == 'admin_panel':  # ЭТА НОВАЯ ВЕТКА ДЛЯ КНОПКИ "НАЗАД В АДМИН-ПАНЕЛЬ"
        if chat_id in admin_ids:
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("📬 Посмотреть заявки", callback_data="Посмотреть заявки"),
                types.InlineKeyboardButton("🗑 Очистить историю", callback_data="Очистить историю"),
                types.InlineKeyboardButton("📈 Статистика", callback_data="Статистика"),
                types.InlineKeyboardButton("🏠 Вернуться в меню", callback_data="back_to_menu")
            )
            # Используем edit_message_text для замены текущего сообщения
            bot.edit_message_text(
                "🔐 <b>Админ-панель</b>",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
            )
        else:
            bot.answer_callback_query(call.id, "❌ Нет доступа!")

    elif data == 'Посмотреть заявки':
        if chat_id in admin_ids:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📬 Заявки пользователей", callback_data="admin_orders"))
            markup.add(types.InlineKeyboardButton("🧮 Все расчеты", callback_data="admin_all_sessions"))
            markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data="admin_panel"))
            # Используем edit_message_text, чтобы заменить меню админ-панели
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Выберите, что хотите посмотреть:",
                reply_markup=markup
            )
        user_data[chat_id]['state'] = states['admin_panel']

    elif data == 'Очистить историю':
        if chat_id in admin_ids:
            orders.clear()
            bot.answer_callback_query(call.id, "✅ История заявок очищена.")
        user_data[chat_id]['state'] = states['admin_panel']

    elif data == 'Статистика':
        if chat_id in admin_ids:
            total_orders = len(orders)
            unique_users = len(set(order.get('chat_id', '') for order in orders if isinstance(order, dict)))
            bot.answer_callback_query(call.id,
                                      f"📊 Статистика:\nКоличество заявок: {total_orders}\nУникальных пользователей: {unique_users}")
        user_data[chat_id]['state'] = states['admin_panel']

    elif data == 'admin_orders':
        handle_admin_orders_list(call)

    elif data == 'admin_all_sessions':
        handle_admin_all_sessions(call)

    elif data.startswith('admin_view_order_'):
        handle_admin_view_order(call)

    elif data.startswith('admin_view_session_'):
        handle_admin_view_session(call)

    elif data == '⬅ В меню':
        user_data[chat_id]['state'] = states['menu']
        ask_question(chat_id)

    elif data == 'submit':
        session = get_current_session(chat_id)
        if not session:
            bot.send_message(chat_id, "❌ Ошибка: сессия не найдена")
            return

        order_data = {
            'chat_id': chat_id,
            'user_name': call.from_user.username or call.from_user.first_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total': session.get('total', 0),
            'answers': session['answers'].copy(),
            'event_name': session['answers'].get(states['event_name'], 'Не указано')
        }

        orders.append(order_data)
        session['submitted'] = True
        session['submitted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        bot.send_message(chat_id, "✅ Ваша заявка успешно отправлена!")

        for admin_id in admin_ids:
            try:
                admin_msg = f"📌 Новая заявка #{len(orders)}\n"
                admin_msg += f"👤 Пользователь: @{order_data['user_name']}\n"
                admin_msg += f"📅 Дата: {order_data['timestamp']}\n"
                admin_msg += f"🏷 Выставка: {order_data['event_name']}\n"
                admin_msg += f"💰 Сумма: {order_data['total']:,.0f} руб.\n"
                bot.send_message(admin_id, admin_msg)

            except Exception as e:
                print(f"Ошибка отправки уведомления админу {admin_id}: {e}")

        user_data[chat_id]['state'] = states['menu']
        ask_question(chat_id)


    elif data == 'cancel':
        bot.send_message(chat_id, "❌ Вы отменили отправку заявки.")
        user_data[chat_id]['state'] = states['menu']
        ask_question(chat_id)

    elif data == 'back_to_menu':
        user_data[chat_id]['state'] = states['menu']
        ask_question(chat_id)

    else:
        if current_state in [states['light_logos'], states['non_light_logos'],
                             states['reception_stands'], states['podmaketniki'],
                             states['kashpo'], states['tv'], states['led_screens'],
                             states['furniture_tommy'], states['furniture_gydra'],
                             states['furniture_eams'], states['furniture_sofa'],
                             states['furniture_coffee_table'], states['furniture_meeting_table'],
                             states['furniture_samba_chairs'], states['furniture_shelves']]:
            try:
                parsed_data = int(data)
                user_data[chat_id]['answers'][current_state] = parsed_data
            except ValueError:
                bot.send_message(chat_id, "Пожалуйста, выберите количество из предложенных вариантов.")
                return
        else:
            user_data[chat_id]['answers'][current_state] = data

        session = get_current_session(chat_id)
        if session:
            session['answers'][current_state] = user_data[chat_id]['answers'][current_state]
            session['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")

        user_data[chat_id]['last_state'] = current_state

        if current_state == states['furniture_shelves']:
            user_data[chat_id]['state'] = states['finish']
        else:
            user_data[chat_id]['state'] += 1

        ask_question(chat_id)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_data:
        reset_user_data(chat_id)
        send_welcome(message)
        return

    state = user_data[chat_id]['state']

    if 'answers' not in user_data[chat_id]:
        user_data[chat_id]['answers'] = {}

    try:
        if state in [states['area'], states['meeting_room1'], states['meeting_room2'],
                     states['utility_room_area'], states['doors']]:
            text = float(text.replace(',', '.'))
        elif state == states['event_name']:
            pass
        else:
            bot.send_message(chat_id, "Пожалуйста, используйте кнопки для ответа на этот вопрос.")
            return

    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
        return

    user_data[chat_id]['answers'][state] = text

    session = get_current_session(chat_id)
    if session:
        session['answers'][state] = text
        session['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    user_data[chat_id]['last_state'] = state

    next_state_map = {
        states['area']: states['podium'],
        states['meeting_room1']: states['meeting_room2'],
        states['meeting_room2']: states['utility_room'],
        states['utility_room_area']: states['doors'],
        states['doors']: states['overhead'],
        states['event_name']: states['furniture'],
    }

    if state in next_state_map:
        user_data[chat_id]['state'] = next_state_map[state]
    else:
        user_data[chat_id]['state'] += 1

    ask_question(chat_id)


def ask_question(chat_id):
    state = user_data[chat_id]['state']
    answers = user_data[chat_id].get('answers', {})

    if chat_id not in user_data:
        reset_user_data(chat_id)

    elif state == states['menu']:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('СДЕЛАТЬ НОВЫЙ РАСЧЕТ СТОИМОСТИ СТЕНДА', callback_data='Посчитать стоимость стенда'))
        if chat_id in admin_ids:
            markup.add(types.InlineKeyboardButton('🔐 Админская панель', callback_data='Админская панель'))
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


    elif state == states['city']:
        bot.send_message(chat_id, "Выберите город проведения выставки:",
                         reply_markup=create_inline_keyboard(['Москва', 'Санкт-Петербург'], include_menu=True,
                                                             include_back=False))

    elif state == states['area']:
        bot.send_message(chat_id, "Введите площадь стенда в м²:")

    elif state == states['podium']:
        bot.send_message(chat_id, "Нужен ли подиум?", reply_markup=create_inline_keyboard(['Да', 'Нет']))

    elif state == states['floor']:
        bot.send_message(chat_id, "Выберите тип напольного покрытия:",
                         reply_markup=create_inline_keyboard(['Ковролин', 'Ламинат (ЛДСП)']))

    elif state == states['wall_height']:
        bot.send_message(chat_id, "Выберите высоту стен:",
                         reply_markup=create_inline_keyboard(['3-4м', '4-5м', '5-6м']))

    elif state == states['meeting_rooms']:
        bot.send_message(chat_id, "Сколько переговорных комнат?", reply_markup=create_inline_keyboard(['0', '1', '2']))

    elif state == states['meeting_room1']:
        meeting_rooms_ans = answers.get(states['meeting_rooms'])
        if meeting_rooms_ans is None or int(meeting_rooms_ans) <= 0:
            user_data[chat_id]['state'] = states['utility_room']  # Пропускаем 2 комнаты
            return ask_question(chat_id)
        bot.send_message(chat_id, "Площадь первой переговорной комнаты в м²:")

    elif state == states['meeting_room2']:
        meeting_rooms_ans = answers.get(states['meeting_rooms'])
        if meeting_rooms_ans is None or int(meeting_rooms_ans) <= 1:
            user_data[chat_id]['state'] = states['utility_room']  # Пропускаем вторую
            return ask_question(chat_id)
        bot.send_message(chat_id, "Площадь второй переговорной комнаты в м²:")

    elif state == states['utility_room']:
        bot.send_message(chat_id, "Нужно ли подсобное помещение?", reply_markup=create_inline_keyboard(['Да', 'Нет']))

    elif state == states['utility_room_area']:
        utility_room = answers.get(states['utility_room'], 'Нет')
        if utility_room == 'Нет':
            user_data[chat_id]['state'] = states['doors']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Площадь подсобного помещения в м²:")

    elif state == states['doors']:
        bot.send_message(chat_id, "Введите количество дверей на стенде (0 - 100):")

    elif state == states['overhead']:
        bot.send_message(chat_id, "Подвесная конструкция над стендом:", reply_markup=create_inline_keyboard(
            ['Нет', 'Малый подвес (до 4 м²)', 'Большой подвес (от 4,5 м²)']))

    elif state == states['light_logos']:
        bot.send_message(chat_id, "Сколько световых логотипов, лайтбоксов и световых элементов?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 8)]))

    elif state == states['non_light_logos']:
        bot.send_message(chat_id, "Сколько несветовых объемных логотипов и графических элементов?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 8)]))

    elif state == states['reception_stands']:
        bot.send_message(chat_id, "Сколько стоек-ресепшен требуется?",
                         reply_markup=create_inline_keyboard([str(i) for i in [0, 1, 2, 3, 4, 6, 8, 10]]))

    elif state == states['podmaketniki']:
        bot.send_message(chat_id, "Сколько тумб-подмакетников требуется?",
                         reply_markup=create_inline_keyboard([str(i) for i in [0, 1, 2, 3, 4, 6, 8, 10]]))

    elif state == states['kashpo']:
        bot.send_message(chat_id, "Сколько кашпо с растениями трубется?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 11)]))


    elif state == states['plants']:
        kashpo_count = int(answers.get(states['kashpo'], 0))
        if kashpo_count > 0:
            bot.send_message(chat_id, "Какие растения нужны?",
                             reply_markup=create_inline_keyboard(
                                 ['Живые комнатные растения', 'Искусственные растения', 'Не нужны']))
        else:
            user_data[chat_id]['answers'][states['plants']] = 'Не нужны'
            user_data[chat_id]['state'] = states['tv']
            ask_question(chat_id)

    elif state == states['tv']:
        bot.send_message(chat_id, "Сколько ТВ-плазм?", reply_markup=create_inline_keyboard(['0', '1', '2', '3', '4']))

    elif state == states['tv_size']:
        tv_count = int(answers.get(states['tv'], 0))
        if tv_count <= 0:
            user_data[chat_id]['state'] = states['led_screens']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер ТВ-плазмы:",
                         reply_markup=create_inline_keyboard(["32", "50", "70", "85"]))

    elif state == states['tv_size2']:
        tv_count = int(answers.get(states['tv'], 0))
        if tv_count <= 1:
            user_data[chat_id]['state'] = states['led_screens']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер второй ТВ-плазмы:",
                         reply_markup=create_inline_keyboard(["32", "50", "70", "85"]))

    elif state == states['tv_size3']:
        tv_count = int(answers.get(states['tv'], 0))
        if tv_count <= 2:
            user_data[chat_id]['state'] = states['led_screens']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер третьей ТВ-плазмы:",
                         reply_markup=create_inline_keyboard(["32", "50", "70", "85"]))

    elif state == states['tv_size4']:
        tv_count = int(answers.get(states['tv'], 0))
        if tv_count <= 3:
            user_data[chat_id]['state'] = states['led_screens']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер четвёртой ТВ-плазмы:",
                         reply_markup=create_inline_keyboard(["32", "50", "70", "85"]))

    elif state == states['led_screens']:
        bot.send_message(chat_id,  "Сколько светодиодных видеоэкранов?", reply_markup=create_inline_keyboard(['0', '1', '2']))


    elif state == states['led_size1']:
        led_count = int(answers.get(states['led_screens'], 0))
        if led_count <= 0:
            user_data[chat_id]['state'] = states['event_name']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер видеоэкрана:",
                         reply_markup=create_inline_keyboard(
                             ["1x2", "1.5x2", "1.5x2.5", "1.5x3", "2x2", "2x3", "3x3", "3x4", "4x4"]))


    elif state == states['led_size2']:
        led_count = int(answers.get(states['led_screens'], 0))
        if led_count <= 1:
            user_data[chat_id]['state'] = states['event_name']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер второго видеоэкрана:",
                         reply_markup=create_inline_keyboard(
                             ["1x2", "1.5x2", "1.5x2.5", "1.5x3", "2x2", "2x3", "3x3", "3x4", "4x4"]))

    elif state == states['event_name']:
        bot.send_message(chat_id, "Введите название выставки:")


    elif state == states['furniture']:
        bot.send_message(chat_id, "Рассчитать мебель на стенде?", reply_markup=create_inline_keyboard(['Да', 'Нет']))


    elif state == states['furniture_tommy']:
        furniture_choice = answers.get(states['furniture'], 'Нет')
        if furniture_choice == 'Нет':
            user_data[chat_id]['state'] = states['finish']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Сколько барных стульев типа Tommy?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 11)]))

    elif state == states['furniture_gydra']:
        bot.send_message(chat_id, "Сколько круглых столов типа GYDRA?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 7)]))

    elif state == states['furniture_eams']:
        bot.send_message(chat_id, "Сколько стандартных стульев типа EAMS?",
                         reply_markup=create_inline_keyboard(['0', '1', '2', '4', '8', '12', '16', '20', '24']))

    elif state == states['furniture_sofa']:
        bot.send_message(chat_id, "Сколько диванов?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 5)]))

    elif state == states['furniture_coffee_table']:
        bot.send_message(chat_id, "Сколько журнальных столов?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 5)]))

    elif state == states['furniture_meeting_table']:
        bot.send_message(chat_id, "Сколько переговорных столов?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 5)]))

    elif state == states['furniture_samba_chairs']:
        bot.send_message(chat_id, "Сколько переговорных кресел типа SAMBA?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 17, 2)]))

    elif state == states['furniture_fridge']:
        bot.send_message(chat_id, "Нужен ли холодильник?", reply_markup=create_inline_keyboard(['Да', 'Нет']))

    elif state == states['furniture_fridge_size']:
        fridge_choice = answers.get(states['furniture_fridge'], 'Нет')
        if fridge_choice == 'Нет':
            user_data[chat_id]['state'] = states['furniture_cooler']
            return ask_question(chat_id)
        bot.send_message(chat_id, "Размер холодильника:", reply_markup=create_inline_keyboard(['Большой', 'Средний']))

    elif state == states['furniture_cooler']:
        bot.send_message(chat_id, "Нужен ли кулер?", reply_markup=create_inline_keyboard(['Да', 'Нет']))

    elif state == states['furniture_coffee']:
        bot.send_message(chat_id, "Нужна ли кофемашина?", reply_markup=create_inline_keyboard(['Да', 'Нет']))

    elif state == states['furniture_shelves']:
        bot.send_message(chat_id, "Сколько стеллажей требуется?",
                         reply_markup=create_inline_keyboard([str(i) for i in range(0, 6)]))

    elif state == states['admin_panel']:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("📬 Посмотреть заявки", callback_data="Посмотреть заявки"),
            types.InlineKeyboardButton("🗑 Очистить историю", callback_data="Очистить историю"),
            types.InlineKeyboardButton("📈 Статистика", callback_data="Статистика"),
            types.InlineKeyboardButton("🏠 Вернуться в меню", callback_data="back_to_menu")
        )
        bot.send_message(chat_id, "🔐 <b>Админ-панель</b>", parse_mode='HTML', reply_markup=markup)

    elif state == states['finish']:
        calculate_cost(chat_id)


# Расчёт стоимости
def calculate_cost(chat_id):
    answers = user_data[chat_id].get('answers', {})
    city_raw = answers.get(states['city'], 'Москва').lower()

    if city_raw == 'москва':
        city = 'moscow'
    elif city_raw == 'санкт-петербург':
        city = 'spb'
    else:
        city = 'moscow'  # Fallback

    area = float(answers.get(states['area'], 0))
    podium = answers.get(states['podium'], 'Нет')
    floor_type = answers.get(states['floor'], 'Ковролин')
    wall_height = answers.get(states['wall_height'], '3-4м')
    doors = int(answers.get(states['doors'], 0))
    overhead = answers.get(states['overhead'], 'Нет')
    light_logos = int(answers.get(states['light_logos'], 0))
    non_light_logos = int(answers.get(states['non_light_logos'], 0))
    reception_stands = int(answers.get(states['reception_stands'], 0))
    podmaketniki = int(answers.get(states['podmaketniki'], 0))
    kashpo = int(answers.get(states['kashpo'], 0))
    plants = answers.get(states['plants'], 'Не нужны')
    tv_count = int(answers.get(states['tv'], 0))
    led_screens = int(answers.get(states['led_screens'], 0))
    furniture_choice = answers.get(states['furniture'], 'Нет')

    meeting_room1_area = float(answers.get(states['meeting_room1'], 0)) if int(
        answers.get(states['meeting_rooms'], 0)) >= 1 else 0
    meeting_room2_area = float(answers.get(states['meeting_room2'], 0)) if int(
        answers.get(states['meeting_rooms'], 0)) >= 2 else 0
    utility_room_area_val = float(answers.get(states['utility_room_area'], 0)) if answers.get(states['utility_room'],
                                                                                              'Нет') == 'Да' else 0

    # Определяем wall_area_for_formulas: зависит от наличия переговорных комнат
    meeting_rooms_count = int(answers.get(states['meeting_rooms'], 0))

    def get_average_wall_height(wall_height_str):
        try:
            clean = wall_height_str.replace('м', '').strip()
            parts = clean.split('-')
            if len(parts) == 2:
                h1, h2 = float(parts[0]), float(parts[1])
                return (h1 + h2) / 2
            else:
                return float(parts[0])
        except:
            return 3.5

    if meeting_rooms_count == 0:
        # Нет переговорных — используем половину площади стенда
        base_area = area / 2
        side_length = base_area ** 0.5
        perimeter = 4 * side_length
        avg_wall_height = get_average_wall_height(wall_height)
        wall_area_for_formulas = perimeter * avg_wall_height
    else:
        # Есть переговорные — используем их и подсобку
        base_area = meeting_room1_area + meeting_room2_area + utility_room_area_val
        side_length = base_area ** 0.5
        perimeter = 4 * side_length
        avg_wall_height = get_average_wall_height(wall_height)
        wall_area_for_formulas = perimeter * avg_wall_height

    cost = {
        '1. Документация': 0,
        '2. Аккредитация': 0,
        '3. Изготовление стенда и прокатное оборудование': {
            '3.1 Пол': 0,
            '3.2 Стены': 0,
            '3.3 Подвесная конструкция': 0,
            '3.4 Индивидуальные конструкции': 0,
            '3.5 Мебель': 0,
            '3.6 Мультимедиа': 0,
            '3.7 Электрика и освещение': 0,
            '3.8 Брендирование': 0
        },
        '4. Монтажные работы, транспортные расходы, демонтаж': 0
    }

    cost['1. Документация'] = area * prices[city]['documentation']


    cost['2. Аккредитация'] = (
            1600 * area +
            wall_area_for_formulas * 450 * 2 +
            450 * area +
            50000 +
            15000
    )

    if podium == 'Да':
        cost['3. Изготовление стенда и прокатное оборудование']['3.1 Пол'] += area * prices[city]['podium_base_cost']
    else:
        cost['3. Изготовление стенда и прокатное оборудование']['3.1 Пол'] += area * 500

    if floor_type == 'Ковролин':
        cost['3. Изготовление стенда и прокатное оборудование']['3.1 Пол'] += area * 1000
    else:
        cost['3. Изготовление стенда и прокатное оборудование']['3.1 Пол'] += area * 2500

    wall_price = prices[city]['wall']
    cost['3. Изготовление стенда и прокатное оборудование']['3.2 Стены'] = wall_price * wall_area_for_formulas + doors * 15000

    if overhead == 'Малый подвес (до 4 м²)':
        cost['3. Изготовление стенда и прокатное оборудование']['3.3 Подвесная конструкция'] = prices[city]['overhead'][
            'small']
    elif overhead == 'Большой подвес (от 4 м²)':
        cost['3. Изготовление стенда и прокатное оборудование']['3.3 Подвесная конструкция'] = prices[city]['overhead'][
            'big']

    cost['3. Изготовление стенда и прокатное оборудование']['3.4 Индивидуальные конструкции'] = reception_stands * \
                                                                                                prices[city][
                                                                                                    'reception_stand']
    cost['3. Изготовление стенда и прокатное оборудование']['3.4 Индивидуальные конструкции'] += podmaketniki * \
                                                                                                 prices[city][
                                                                                                     'podmaketnik_price']

    if plants != 'Не нужны' and kashpo > 0:
        plant_price = prices[city]['plants']['live'] if plants == 'Живые комнатные растения' else \
        prices[city]['plants']['fake']
        cost['3. Изготовление стенда и прокатное оборудование'][
            '3.4 Индивидуальные конструкции'] += kashpo * plant_price

    if furniture_choice == 'Да':
        def safe_int(val):
            try:
                return int(val)
            except (ValueError, TypeError):
                return 0

        furniture_cost = {
            'tommy': safe_int(answers.get(states['furniture_tommy'])) * 2500,
            'gydra': safe_int(answers.get(states['furniture_gydra'])) * 4000,
            'eams': safe_int(answers.get(states['furniture_eams'])) * 1500,
            'sofa': safe_int(answers.get(states['furniture_sofa'])) * 9000,
            'coffee_table': safe_int(answers.get(states['furniture_coffee_table'])) * 4000,
            'meeting_table': safe_int(answers.get(states['furniture_meeting_table'])) * 20000,
            'samba_chairs': safe_int(answers.get(states['furniture_samba_chairs'])) * 3500,
            'shelves': safe_int(answers.get(states['furniture_shelves'])) * 2000,
        }

        fridge_choice = answers.get(states['furniture_fridge'], 'Нет')
        fridge_size = answers.get(states['furniture_fridge_size'], '')
        if fridge_choice == 'Да':
            if fridge_size == 'Большой':
                furniture_cost['fridge'] = 12000
            elif fridge_size == 'Средний':
                furniture_cost['fridge'] = 9000

        if answers.get(states['furniture_cooler'], 'Нет') == 'Да':
            furniture_cost['cooler'] = 7000
        if answers.get(states['furniture_coffee'], 'Нет') == 'Да':
            furniture_cost['coffee'] = 20000

        cost['3. Изготовление стенда и прокатное оборудование']['3.5 Мебель'] = sum(furniture_cost.values()) + 20000

    led_cost = 0
    if led_screens >= 1:
        size1 = answers.get(states['led_size1'], '1x2')
        try:
            w, h = map(float, size1.lower().replace('х', 'x').split('x'))
            led_cost += prices[city]['led_screen'] * (w * h)
        except (ValueError, AttributeError):
            pass

    if led_screens >= 2:
        size2 = answers.get(states['led_size2'], '1x2')
        try:
            w, h = map(float, size2.lower().replace('х', 'x').split('x'))
            led_cost += prices[city]['led_screen'] * (w * h)
        except (ValueError, AttributeError):
            pass

    tv_costs = 0
    tv_sizes = [
        answers.get(states['tv_size']),
        answers.get(states['tv_size2']),
        answers.get(states['tv_size3']),
        answers.get(states['tv_size4'])
    ]
    for i in range(tv_count):
        size_key = str(tv_sizes[i]).replace("'", "")
        if size_key in prices[city]['tv']:
            tv_costs += prices[city]['tv'][size_key]

    cost['3. Изготовление стенда и прокатное оборудование']['3.6 Мультимедиа'] = led_cost + tv_costs

    cost['3. Изготовление стенда и прокатное оборудование']['3.7 Электрика и освещение'] = prices[city]['electricity'][
                                                                                               'base'] + perimeter * \
                                                                                           prices[city]['electricity'][
                                                                                               'perimeter']

    cost['3. Изготовление стенда и прокатное оборудование']['3.8 Брендирование'] = (
            light_logos * prices[city]['light_logo'] +
            non_light_logos * prices[city]['non_light_logo']
    )

    mount_cost = (3000 * area + 4500 * wall_area_for_formulas)
    transport_cost = prices[city]['transport']
    cost['4. Монтажные работы, транспортные расходы, демонтаж'] = mount_cost + transport_cost

    # --- НОВЫЙ ФОРМАТ ВЫВОДА СМЕТЫ ---
    result = "🧮 <b>ПРЕДВАРИТЕЛЬНАЯ сметная стоимость стенда:</b>\n"

    # 1. Документация
    doc_value = cost.get('1. Документация', 0)
    result += f"\n1. Документация (конструкторские чертежи, электропроект, расчет нагрузок, макетирование и пр.): {doc_value:,.0f} руб.\n"

    # 2. Аккредитация
    accr_value = cost.get('2. Аккредитация', 0)
    result += f"\n2. Аккредитация (расходы ОТК, противопожарная обработка, страхование, утилизация): {accr_value:,.0f} руб.\n"

    # 3. Изготовление стенда и прокатное оборудование
    equip_cost = cost.get('3. Изготовление стенда и прокатное оборудование', {})
    if equip_cost:
        result += f"\n3. Изготовление стенда и прокатное оборудование"
        equip_total = 0

        # 3.1 Пол
        val = equip_cost.get('3.1 Пол', 0)
        if val > 0:
            result += f"\n  3.1 Пол (в случае наличия - подиум, напольное покрытие): {val:,.0f} руб."
            equip_total += val

        # 3.2 Стены
        val = equip_cost.get('3.2 Стены', 0)
        if val > 0:
            result += f"\n  3.2 Стены (стеновые короба, облицовка стен): {val:,.0f} руб."
            equip_total += val

        # 3.3 Подвесная конструкция
        val = equip_cost.get('3.3 Подвесная конструкция', 0)
        if val > 0:
            result += f"\n  3.3 Подвесная конструкция (точки подвеса, лебедки, фермы, конструктив): {val:,.0f} руб."
            equip_total += val

        # 3.4 Индивидуальные конструкции
        val = equip_cost.get('3.4 Индивидуальные конструкции', 0)
        if val > 0:
            result += f"\n  3.4 Индивидуальные конструкции (стойки ресепшен, кашпо с растениями, тумбы-подмакетники и пр.): {val:,.0f} руб."
            equip_total += val

        # 3.5 Мебель
        val = equip_cost.get('3.5 Мебель', 0)
        if val > 0:
            result += f"\n  3.5 Мебель (прокат): {val:,.0f} руб."
            equip_total += val

        # 3.6 Мультимедиа
        val = equip_cost.get('3.6 Мультимедиа', 0)
        if val > 0:
            result += f"\n  3.6 Мультимедиа (прокат): {val:,.0f} руб."
            equip_total += val

        # 3.7 Электрика и освещение
        val = equip_cost.get('3.7 Электрика и освещение', 0)
        if val > 0:
            result += f"\n  3.7 Электрика и освещение (прокат): {val:,.0f} руб."
            equip_total += val

        # 3.8 Брендирование
        val = equip_cost.get('3.8 Брендирование', 0)
        if val > 0:
            result += f"\n  3.8 Брендирование: {val:,.0f} руб."
            equip_total += val

        if equip_total > 0:
            result += f"\n  Итого по категории: {equip_total:,.0f} руб."

    # 4. Монтажные работы, транспортные расходы, демонтаж
    mount_value = cost.get('4. Монтажные работы, транспортные расходы, демонтаж', 0)
    result += f"\n\n4. Монтажные работы, транспортные расходы, демонтаж: {mount_value:,.0f} руб.\n"

    # Общая стоимость
    final_grand_total = math.ceil(mount_value + doc_value + accr_value + equip_total)
    result += f"\n\n💰 <b>ОБЩАЯ ПРЕДВАРИТЕЛЬНАЯ СТОИМОСТЬ: {final_grand_total:,.0f} руб.</b>"

    # Отправляем пользователю
    bot.send_message(chat_id, result, parse_mode='HTML')

    session = get_current_session(chat_id)
    if session:
        session['finished'] = True
        session['total'] = final_grand_total

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Оставить заявку', callback_data='submit'))
    markup.add(types.InlineKeyboardButton(text='Не оставлять', callback_data='cancel'))
    markup.add(types.InlineKeyboardButton(text='🏠 Вернуться в меню', callback_data='back_to_menu'))
    bot.send_message(chat_id, "Хотите оставить заявку?", reply_markup=markup)


def handle_admin_orders_list(call):
    chat_id = call.message.chat.id
    if chat_id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ У вас нет доступа.")
        return
    try:
        markup = types.InlineKeyboardMarkup()
        if not orders:
            markup.add(types.InlineKeyboardButton(text='⬅ Назад в админ-панель', callback_data='admin_panel'))
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="📭 Нет заявок.",
                reply_markup=markup
            )
            bot.answer_callback_query(call.id)
            return

        for idx, order in enumerate(orders):
            user_name = order.get('user_name', 'Неизвестный')
            event_name = order.get('event_name', 'Не указано')[:20]
            total = order.get('total', 0)
            button_text = f"📌 Заявка #{idx + 1} | @{user_name} | {event_name} | {total:,.0f} руб."
            markup.add(types.InlineKeyboardButton(text=button_text, callback_data=f"admin_view_order_{idx}"))

        markup.add(types.InlineKeyboardButton(text='⬅ Назад в админ-панель', callback_data='admin_panel'))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="📬 <b>Заявки пользователей:</b>",
            parse_mode='HTML',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка.")
        print(f"Ошибка в handle_admin_orders_list: {e}")


def handle_admin_view_order(call):
    chat_id = call.message.chat.id
    if chat_id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ У вас нет доступа.")
        return
    try:
        order_idx = int(call.data.split('_')[-1])
        order = orders[order_idx]

        answers = order.get('answers', {})

        details = f"🔍 <b>Детали заявки #{order_idx + 1}</b>\n"
        details += f"👤 Пользователь: @{order['user_name']}\n"
        details += f"🆔 ID чата: {order['chat_id']}\n"
        details += f"📅 Дата отправки: {order['timestamp']}\n"
        details += f"🏷 Выставка: {order['event_name']}\n"
        details += f"💰 ОБЩАЯ ПРЕДВАРИТЕЛЬНАЯ СТОИМОСТЬ: {order['total']:,} руб.\n\n"

        details += "📦 <b>Ответы пользователя:</b>\n"
        for state_key in sorted(answers.keys()):
            question_name_en = reverse_states.get(state_key, f"Вопрос {state_key}")
            display_question_name = question_display_names.get(question_name_en,
                                                               question_name_en.replace('_', ' ').capitalize())
            answer_value = answers[state_key]

            if isinstance(answer_value, (int, float)):
                formatted_answer = f"{answer_value:,.0f}"
            else:
                formatted_answer = str(answer_value)

            details += f"🔹 {display_question_name}: {formatted_answer}\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='⬅ Назад к списку заявок', callback_data='admin_orders'))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=details,
            parse_mode='HTML',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    except (IndexError, ValueError) as e:
        bot.answer_callback_query(call.id, "Ошибка: заявка не найдена")
        print(f"Ошибка просмотра заявки админом: {e}")


def get_question_text(state):
    questions = {
        states['city']: "Город",
        states['area']: "Площадь стенда",
        states['podium']: "Подиум",
    }
    return questions.get(state, f"Вопрос {state}")


def handle_admin_all_sessions(call):
    chat_id = call.message.chat.id
    if chat_id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ У вас нет доступа.")
        return
    try:
        markup = types.InlineKeyboardMarkup()
        if not all_sessions:
            markup.add(types.InlineKeyboardButton(text='⬅ Назад', callback_data='Посмотреть заявки'))
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="📭 Нет ни одного расчёта.",
                reply_markup=markup
            )
            bot.answer_callback_query(call.id)
            return

        for session in all_sessions.values():
            status = "🟢" if session['finished'] else "🟡"
            submitted = " ✅" if session.get('submitted', False) else ""
            total = f" 💰 {session.get('total', '—'):,} руб." if session.get('total') else ""
            city = session['answers'].get(states['city'], '—')
            area = session['answers'].get(states['area'], '—')

            user_info = bot.get_chat(session['user_chat_id'])
            user_name = user_info.username or user_info.first_name or "Пользователь"

            user_display = f'@{user_name}' if user_info.username else user_name

            button_text = f"{status} {user_display} | {city}, {area}м²{total}{submitted}"

            markup.add(
                types.InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"admin_view_session_{session['id']}"
                )
            )
        markup.add(types.InlineKeyboardButton(text='⬅ Назад', callback_data='admin_panel'))
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="🧮 <b>Все расчёты:</b>",
            parse_mode='HTML',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка.")
        print(f"Ошибка в handle_admin_all_sessions: {e}")


def handle_admin_view_session(call):
    chat_id = call.message.chat.id
    if chat_id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ У вас нет доступа.")
        return
    try:
        session_id = call.data[len('admin_view_session_'):]
        session = all_sessions.get(session_id)

        if not session:
            bot.answer_callback_query(call.id, "Ошибка: Расчёт не найден.")
            return

        details = f"🔍 <b>Детали расчёта #{session_id[:8]}</b>\n"

        user_info = bot.get_chat(session['user_chat_id'])
        user_name = user_info.username or user_info.first_name or "Пользователь"
        user_display = f'@{user_name}' if user_info.username else user_name

        details += f"👤 Пользователь: {user_display}\n"
        details += f"🆔 ID пользователя: {session['user_chat_id']}\n"
        city = session['answers'].get(states['city'], 'Не указано')
        area = session['answers'].get(states['area'], 'Не указано')
        event_name = session['answers'].get(states['event_name'], 'Не указано')
        total = session.get('total', 'Не завершён')
        created_at = session.get('created_at', 'Неизвестно')
        submitted_at = session.get('submitted_at', 'Не отправлена')

        details += f"📅 Создан: {created_at}\n"
        if session.get('submitted'):
            details += f"📤 Отправлена: {submitted_at}\n"
        details += f"📍 Город: {city}\n"
        details += f"📐 Площадь: {area} м²\n"
        details += f"🏷 Выставка: {event_name}\n"
        if total is not None and isinstance(total, (int, float)):
            details += f"💰 ОБЩАЯ ПРЕДВАРИТЕЛЬНАЯ СТОИМОСТЬ: {total:,.0f} руб.\n"
        else:
            details += "💰 ОБЩАЯ ПРЕДВАРИТЕЛЬНАЯ СТОИМОСТЬ: Расчёт не завершён\n"

        details += "📦 <b>Ответы пользователя:</b>\n"
        answers = session['answers']
        for state_key in sorted(answers.keys()):
            question_name_en = reverse_states.get(state_key, f"Вопрос {state_key}")
            display_question_name = question_display_names.get(question_name_en,
                                                               question_name_en.replace('_', ' ').capitalize())
            answer_value = answers[state_key]

            if isinstance(answer_value, (int, float)):
                formatted_answer = f"{answer_value:,.0f}"
            else:
                formatted_answer = str(answer_value)

            details += f"🔹 {display_question_name}: {formatted_answer}\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='⬅ Назад к списку расчётов', callback_data='admin_all_sessions'))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=details, parse_mode='HTML',
                              reply_markup=markup)
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка при загрузке расчёта.")
        print(f"Ошибка в handle_admin_view_session: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('view_session_'))
def handle_view_user_session(call):
    chat_id = call.message.chat.id
    try:
        session_id = call.data[len('view_session_'):]
        session = None
        for s in user_data.get(chat_id, {}).get('sessions', []):
            if s['id'] == session_id:
                session = s
                break

        if not session:
            bot.answer_callback_query(call.id, "Ошибка: Расчёт не найден.")
            return

        details = f"🔍 <b>Детали расчёта #{session_id[:8]}</b>\n"
        city = session['answers'].get(states['city'], 'Не указано')
        area = session['answers'].get(states['area'], 'Не указано')
        event_name = session['answers'].get(states['event_name'], 'Не указано')
        created_at = session.get('created_at', 'Неизвестно')
        submitted_at = session.get('submitted_at', 'Не отправлена')

        details += f"📅 Создан: {created_at}\n"
        if session.get('submitted'):
            details += f"📤 Отправлен: {submitted_at}\n"
        details += f"📍 Город: {city}\n"
        details += f"📐 Площадь: {area} м²\n"
        details += f"🏷 Выставка: {event_name}\n"

        if session.get('finished') and session.get('total') is not None:
            total = session.get('total', 0)
            details += f"💰 Общая стоимость: {total:,.0f} руб.\n"

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='⬅ Назад к списку', callback_data='Показать предыдущие расчеты'))
            if not session.get('submitted', False):
                markup.add(
                    types.InlineKeyboardButton(text='📤 Оставить заявку', callback_data=f'submit_session_{session_id}'))
            markup.add(types.InlineKeyboardButton(text='🏠 Вернуться в меню', callback_data='back_to_menu'))
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=details, parse_mode='HTML',
                                  reply_markup=markup)
        else:
            details += "💰 Общая стоимость: Расчёт не завершён\n"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='⬅ Назад к списку', callback_data='Показать предыдущие расчеты'))
            markup.add(types.InlineKeyboardButton(text='🏠 Вернуться в меню', callback_data='back_to_menu'))
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=details, parse_mode='HTML',
                                  reply_markup=markup)

        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка при загрузке расчёта.")
        print(f"Ошибка в handle_view_user_session: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('submit_session_'))
def handle_submit_from_history(call):
    chat_id = call.message.chat.id
    try:
        session_id = call.data[len('submit_session_'):]
        session = None
        for s in user_data.get(chat_id, {}).get('sessions', []):
            if s['id'] == session_id:
                session = s
                break
        if not session:
            bot.answer_callback_query(call.id, "Ошибка: Расчёт не найден.")
            return
        if session.get('submitted', False):
            bot.answer_callback_query(call.id, "Ошибка: Заявка уже отправлена.")
            return
        if not session.get('finished', False) or session.get('total') is None:
            bot.answer_callback_query(call.id, "Ошибка: Расчёт не завершён.")
            return

        order_data = {
            'chat_id': chat_id,
            'user_name': call.from_user.username or call.from_user.first_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total': session.get('total', 0),
            'answers': session['answers'].copy(),
            'event_name': session['answers'].get(states['event_name'], 'Не указано'),
            'session_id': session_id
        }
        orders.append(order_data)
        session['submitted'] = True
        session['submitted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        admin_msg = f"📌 Новая заявка из истории\n"
        admin_msg += f"👤 Пользователь: @{order_data['user_name']}\n"
        admin_msg += f"📅 Дата отправки: {order_data['timestamp']}\n"
        admin_msg += f"🏷 Выставка: {order_data['event_name']}\n"
        admin_msg += f"🆔 ID расчёта: {session_id[:8]}\n"
        admin_msg += "\n📦 <b>Ответы пользователя:</b>\n"

        answers = session['answers']
        for state_key in sorted(answers.keys()):
            question_name_en = reverse_states.get(state_key, f"Вопрос {state_key}")
            display_question_name = question_display_names.get(question_name_en,
                                                               question_name_en.replace('_', ' ').capitalize())
            answer_value = answers[state_key]

            if isinstance(answer_value, (int, float)):
                formatted_answer = f"{answer_value:,.0f}"
            else:
                formatted_answer = str(answer_value)

            admin_msg += f"🔹 {display_question_name}: {formatted_answer}\n"

        admin_msg += f"💰 <b>ОБЩАЯ ПРЕДВАРИТЕЛЬНАЯ СТОИМОСТЬ:</b> {order_data['total']:,.0f} руб."

        for admin_id in admin_ids:
            try:
                bot.send_message(admin_id, admin_msg, parse_mode='HTML')
            except Exception as e:
                print(f"Ошибка отправки уведомления админу {admin_id}: {e}")

        bot.answer_callback_query(call.id, "✅ Заявка успешно отправлена!")
        call.data = f"view_session_{session_id}"
        handle_view_user_session(call)

    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
        print(f"Ошибка в handle_submit_from_history: {e}")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)