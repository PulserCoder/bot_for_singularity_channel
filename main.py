import random
import textwrap

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from markups import start_menu

bot = Bot(token='6802675140:AAHNY-n1Lb39GHI2TGdkRXgE_i8_NhfuUZs', parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['send_to'], state='*')
async def send_message_to_channel(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Узнать какой бы мог грант быть у тебя',
                                        url='https://t.me/sup_singularity_robot')
    markup.add(button)
    await bot.send_message(chat_id=-1002112489499, text=textwrap.dedent("""
Как ты мог заметить, у нас есть система грантов. Что это?

Система грантов на обучение в колледже
представляет собой финансовую поддержку, предоставляемую студентам для оплаты обучения. В нашем колледже грантовая система предоставляется от нашего основателя Георгия Соловьева.

Но стоит понимать, что каждый грант имеет свойство потери.

Если ты учишься очень даже хорошо, стараешься и выполняешь все задачи в срок, то тебя такие проблемы обойдут стороной.

И самый главный вопрос. А без грантовой системы возможно поступить в IT-колледж? ДА! Но тебе придется учиться на полной коммерческой основе
    """), reply_markup=markup)


@dp.message_handler(commands=['start'], state='*')
async def start_foo(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(textwrap.dedent("""
    Привет! Давай пройдем тест и узнаем какой грант на обучение ты бы мог получить по системе оценки при поступлении в колледж Singularity Hub
    В нашем колледже полное обучение стоит 140 000 рублей в год, но грантами можно покрыть от 10% до 100% платы за обучения, необязательно знать программирование или англйиский
    
    Жми на кнопку "Начать" чтобы поскорее пройтии коротенький тест)
    """)
                         , reply_markup=start_menu())


# Структура состояний для каждого пользователя
class QuizState(StatesGroup):
    question = State()  # Текущий вопрос
    score = State()  # Текущий счет


# Структура вопросов и ответов
questions = [
    {
        "question": "Ты любишь развиваться и получать уникальные знания? 😊",
        "answers": [
            ("Не вижу смысла. 🤷", 0),
            ("Иногда, но лень. 😴", 5000),
            ("Когда есть время, да. ⏳", 10000),
            ("Конечно, это жизненно важно! 🌟", 20000)
        ]
    },
    {
        "question": "Сколько видов IT-сфер ты знаешь? 💻",
        "answers": [
            ("Ни одной, не моё. 🚫", 0),
            ("Знаю про программирование. 🖥", 5000),
            ("Где-то 5 разных. 🤔", 10000),
            ("Все! Могу объяснить каждую. 👨‍💻", 20000)
        ]
    },
    {
        "question": "Определился с будущей профессией? 🚀",
        "answers": [
            ("Нет, живу настоящим. 🎲", 0),
            ("В процессе выбора, есть надежда. 🌱", 5000),
            ("Есть интересные варианты, но не уверен. 🤨", 10000),
            ("Да, уверенно шагаю к цели! 💼", 20000)
        ]
    },
    {
        "question": "Ты открыт к новому и готов преодолевать трудности? 🚧",
        "answers": [
            ("Нет, это не про меня. 😓", 0),
            ("В зависимости от ситуации. ⚖️", 5000),
            ("Готов, но могу сомневаться. 🌪", 10000),
            ("Да, ничто меня не остановит! 💥", 20000)
        ]
    },
    {
        "question": "Готов к высокой нагрузке, занимающей весь день? 🏋️‍♂️",
        "answers": [
            ("Нет, мне нужно время для отдыха. 🛌", 0),
            ("Скорее нет, но могу попробовать. 🤷‍♂️", 5000),
            ("Готов и буду находить баланс. ⚖️", 10000),
            ("Да, я готов к любым нагрузкам! 💪", 20000)
        ]
    },
    {
        "question": "Какую роль играют финансы и стабильность в твоей жизни? 💰",
        "answers": [
            ("Не главное, лишь бы хватало на базовое. 🍜", 0),
            ("Важны, но не готов усердно трудиться. 😑", 5000),
            ("Важны, ищу дополнительные способы заработка. 👍", 10000),
            ("Крайне важны, граблю каждую возможность. 📈", 20000)
        ]
    },
    {
        "question": "Есть ли у тебя профессиональные и личные цели? 🎯",
        "answers": [
            ("Живу интуитивно. 🌬", 0),
            ("Хочу достойную жизнь и гордость мамы. ❤️", 5000),
            ("Думаю о хорошем заработке. 💭", 10000),
            ("Конечно, стремлюсь быть лучшим! ⭐️", 20000)
        ]
    }
]


# Функция для старта опроса
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Начать'))
    await message.reply("Добро пожаловать! Нажмите 'Начать', чтобы начать опрос.", reply_markup=keyboard)


# Функция для начала опроса
@dp.message_handler(lambda message: message.text == "Начать🤓", state="*")
async def start_quiz(message: types.Message, state: FSMContext):
    await QuizState.question.set()
    await state.update_data(question_idx=0, total_score=0)
    await ask_question(message, state)


# Функция для задания вопроса
async def ask_question(message, state: FSMContext):
    user_data = await state.get_data()
    question_idx = user_data.get('question_idx')

    if question_idx < len(questions):
        question = questions[question_idx]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        answers = question['answers']
        random.shuffle(answers)
        for answer in answers:
            keyboard.add(KeyboardButton(answer[0]))
        await message.answer(question['question'], reply_markup=keyboard)
    else:
        total_score = user_data.get('total_score', 0)
        if total_score < 15000:
            ans = (
                f"Опрос завершен! Не расстраивайтесь, этот бот не является 100% отражением вас в глазах приемной комиссии, ведь там смотрят на человека с разных сторон.\n"
                f"Возможный грант, который вы могли бы получить в рублях: {total_score}")
        elif 15000 < total_score < 60000:
            ans = (
                f"Опрос завершен! У вас средний результат, и это круто!\n"
                f"Возможный грант, который вы могли бы получить в рублях: {total_score}")
        elif 60000 < total_score < 100000:
            ans = (
                f"Опрос завершен! У очень серьезный результат, вам стоит серьезно задуматься о карьере в IT\n"
                f"Возможный грант, который вы могли бы получить в рублях: {total_score}")
        else:
            ans = (
                f"Опрос завершен! Ты просто создан для IT, ты бы учился c огромной скидкой\n"
                f"Возможный грант, который вы могли бы получить в рублях: {total_score}")
        await message.answer(ans)

        await state.finish()


# Функция обработки ответа
@dp.message_handler(state=QuizState.question)
async def handle_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    question_idx = user_data.get('question_idx', 0)
    total_score = user_data.get('total_score', 0)

    question = questions[question_idx]
    answer = next((ans for ans in question['answers'] if ans[0] == message.text), None)

    if answer:
        total_score += answer[1]

    await state.update_data(question_idx=question_idx + 1, total_score=total_score)
    await ask_question(message, state)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
