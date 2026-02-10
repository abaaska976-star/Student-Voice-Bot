from aiogram import Router, F, Bot, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import get_db
import uuid, os
from dotenv import load_dotenv

router = Router()
bot: Bot = None  # будет инициализирован из main.py

load_dotenv()  # загружает переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")  # теперь точно подхватит
print("TOKEN =", BOT_TOKEN)  # временная проверка

GROUP_ID = -4941840152
ANTI_BULLYING_CHAT_ID = -5201762937

class Question(StatesGroup):
    waiting_text = State()

# --- Keyboards ---
def get_main_rep_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Русский")],
            [KeyboardButton(text="Қазақша")],
            [KeyboardButton(text="English")]
        ],
        resize_keyboard=True
    )

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мероприятия📌")],
            [KeyboardButton(text="Предложить идею или оставить отзыв о работе Парламента💡")],
            [KeyboardButton(text="Часто задаваемые вопросы❓")],
            [KeyboardButton(text="Я хочу стать частью Парламента🙌")],
            [KeyboardButton(text="О Парламенте🫶")],
            [KeyboardButton(text="Задай вопрос анонимно и мы постараемся помочь❣️")]
        ],
        resize_keyboard=True
    )

def get_main_re_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Іс-шаралар📌")],
            [KeyboardButton(text="Парламент жұмысы туралы ой ұсыну немесе пікір қалдыру💡")],
            [KeyboardButton(text="Көп қойылатын сұрақтар❓")],
            [KeyboardButton(text="Мен Парламенттің бір бөлігі болғым келеді🙌")],
            [KeyboardButton(text="Парламент туралы🫶")],
            [KeyboardButton(text="Сұрағыңызды аноним түрде қойыңыз, біз көмектесуге тырысамыз❣️")]
        ],
        resize_keyboard=True
    )

def get_main_r_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Events📌")],
            [KeyboardButton(text="Suggest an idea or leave feedback on the Council's work💡")],
            [KeyboardButton(text="Frequently Asked Questions❓")],
            [KeyboardButton(text="I want to become a part of Council🙌")],
            [KeyboardButton(text="About Council🫶")],
            [KeyboardButton(text="Ask a question anonymously and we will try to help❣️")]
        ],
        resize_keyboard=True
    )

def get_faq_keyboard_ru():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Можно ли провети ChocoDay еще раз?🍫")],
            [KeyboardButton(text="Дискотека для 8 классов будет с 7 классами или 9ми?💃")]
        ],
        resize_keyboard=True
    )

def get_faq_keyboard_kz():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ChocoDay-ды тағы бір рет өткізуге бола ма?🍫")],
            [KeyboardButton(text="8 сыныптар үшін дискотека 7 сыныптармен бе, әлде 9-дармен бе?💃")]
        ],
        resize_keyboard=True
    )

def get_faq_keyboard_en():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Is it possible to hold ChocoDay once more?🍫")],
            [KeyboardButton(text="Will the disco for 8th graders be with 7th graders or 9th graders?💃")]
        ],
        resize_keyboard=True
    )

# --- Start ---
@router.message(Command("start"))
async def start(message: Message):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (tg_id, username, first_name) VALUES (?, ?, ?)",
        (message.from_user.id, message.from_user.username, message.from_user.first_name)
    )
    db.commit()
    db.close()
    await message.answer(
        "Привет😇, это бот Парламента Гимназии №3.\nВыбери язык⬇️",
        reply_markup=get_main_rep_keyboard()
    )

# --- Language selection ---
@router.message(F.text == "Русский")
async def ru(message: Message):
    await message.answer("Вы выбрали русский язык! Что вас интересует?⬇️", reply_markup=get_main_reply_keyboard())

@router.message(F.text == "Қазақша")
async def kz(message: Message):
    await message.answer("Сіз қазақ тілін таңдадыңыз! Сізді не қызықтырады?⬇️", reply_markup=get_main_re_keyboard())

@router.message(F.text == "English")
async def en(message: Message):
    await message.answer("You have chosen English! What are you interested in?⬇️", reply_markup=get_main_r_keyboard())

# --- FAQ ---
@router.message(F.text == "Часто задаваемые вопросы❓")
async def faq_ru(message: Message):
    await message.answer("Выбери свой вопрос:", reply_markup=get_faq_keyboard_ru())

@router.message(F.text == "Көп қойылатын сұрақтар❓")
async def faq_kz(message: Message):
    await message.answer("Выбери свой вопрос:", reply_markup=get_faq_keyboard_kz())

@router.message(F.text == "Frequently Asked Questions❓")
async def faq_en(message: Message):
    await message.answer("Выбери свой вопрос:", reply_markup=get_faq_keyboard_en())

# --- FAQ answers ---
@router.message(F.text == "Можно ли провети ChocoDay еще раз?🍫")
async def answer_ru_1(message: Message):
    await message.answer("ChocoDay был уже 2 раза!!!")

@router.message(F.text == "Дискотека для 8 классов будет с 7 классами или 9ми?💃")
async def answer_ru_2(message: Message):
    await message.answer("Дискотека💃\n\n15 февраля \n6-8 классы 15:30-17:00\n9-11 классы 17:30-19:00")

@router.message(F.text == "ChocoDay-ды тағы бір рет өткізуге бола ма?🍫")
async def answer_kz_1(message: Message):
    await message.answer("ChocoDay енді екі рет болды!!!")

@router.message(F.text == "8 сыныптар үшін дискотека 7 сыныптармен бе, әлде 9-дармен бе?💃")
async def answer_kz_2(message: Message):
    await message.answer("Дискотека💃\n\n15 ақпан\n6-8 сыныптар 15:30-17:00\n9-11 сыныптар 17:30-19:00")

@router.message(F.text == "Is it possible to hold ChocoDay once more?🍫")
async def answer_en_1(message: Message):
    await message.answer("ChocoDay has already been 2 times!!")

@router.message(F.text == "Will the disco for 8th graders be with 7th graders or 9th graders?💃")
async def answer_en_2(message: Message):
    await message.answer("Disco💃\n\nFebruary 15 \nGrades 6-8 3:30 PM - 5:00 PM\nGrades 9-11 5:30 PM - 7:00 PM")

# --- Parliament info ---
@router.message(F.text == "О Парламенте🫶")
async def parlament_ru(message: Message):
    await message.answer(
        "Наш Парламент:\n"
        " •President Дарим Амир\n"
        " •VicePresident Кайрат Адлет\n"
        " •Minister of Creativity Ахмедиева Баян\n"
        " •Minister of Events Уразбаева Газиза\n"
        " •Minister of Culture Избасты Алишер\n"
        " •Minister of SMM Бакибаева Даяна\n"
        " •Minister of Adal Urpak Наржанкызы Адия"
    )

@router.message(F.text == "Парламент туралы🫶")
async def parlament_kz(message: Message):
    await message.answer(
        "Біздің Парламент:\n"
        " •President Дарим Амир\n"
        " •VicePresident Кайрат Адлет\n"
        " •Minister of Creativity Ахмедиева Баян\n"
        " •Minister of Events Уразбаева Газиза\n"
        " •Minister of Culture Избасты Алишер\n"
        " •Minister of SMM Бакибаева Даяна\n"
        " •Minister of Adal Urpak Наржанкызы Адия"
    )

@router.message(F.text == "About Council🫶")
async def parlament_en(message: Message):
    await message.answer(
        "Our Council:\n"
        " •President Darim Amir\n"
        " •VicePresident Kairat Adlet\n"
        " •Minister of Creativity Akhmediyeva Bayan\n"
        " •Minister of Events Urazbayeva Gaziza\n"
        " •Minister of Culture Izbasty Alisher\n"
        " •Minister of SMM Bakibaeva Dayana\n"
        " •Minister of Adal Urpak Narzhankyzy Adiya"
    )

# --- Events ---
@router.message(F.text == "Мероприятия📌")
async def mer_ru(message: Message):
    await message.answer(
        "Пока нет ближайших мероприятий 😢"
    )

@router.message(F.text == "Іс-шаралар📌")
async def mer_kz(message: Message):
    await message.answer(
        "Әзірге жақын іс-шаралар жоқ 😢"
    )

@router.message(F.text == "Events📌")
async def mer_en(message: Message):
    await message.answer(
        "There are no upcoming events yet 😢"
    )

# --- Idea / Application / Antibullying ---
@router.message(F.text.in_([
    "Предложить идею или оставить отзыв о работе Парламента💡",
    "Парламент жұмысы туралы ой ұсыну немесе пікір қалдыру💡",
    "Suggest an idea or leave feedback on the Council's work💡"
]))
async def idea(message: Message, state: FSMContext):
    await state.update_data(type="idea")
    await message.answer("✍️ Напиши сообщение" if "Предложить идею или оставить отзыв о работе Парламента💡" in message.text else "✍️ Жазыңыз" if "Парламент жұмысы туралы ой ұсыну немесе пікір қалдыру💡" in message.text else "✍️ Write your message")
    await state.set_state(Question.waiting_text)

@router.message(F.text.in_([
    "Я хочу стать частью Парламента🙌",
    "Мен Парламенттің бір бөлігі болғым келеді🙌",
    "I want to become a part of Council🙌"
]))
async def application(message: Message, state: FSMContext):
    await state.update_data(type="application")
    await message.answer("🙌 Напиши номер, класс, имя и министерство(смотреть О парламенте)" if "Я хочу стать частью Парламента🙌" in message.text else "🙌 Нөмірін, сыныбын, атын және министрлігін жаз (Парламент туралы қара)" if "Мен Парламенттің бір бөлігі болғым келеді🙌" in message.text else "🙌 Write the number, class, name, and ministry (see About Council)")
    await state.set_state(Question.waiting_text)

@router.message(F.text.in_([
    "Задай вопрос анонимно и мы постараемся помочь❣️",
    "Сұрағыңызды аноним түрде қойыңыз, біз көмектесуге тырысамыз❣️",
    "Ask a question anonymously and we will try to help❣️"
]))
async def antibullying(message: Message, state: FSMContext):
    await state.update_data(type="antibullying")
    await message.answer("❣️ Напиши, что тебя беспокоит" if "Задай вопрос анонимно и мы постараемся помочь❣️" in message.text else "❣️ Сені не алаңдатып жатқанын жаз" if "Сұрағыңызды аноним түрде қойыңыз, біз көмектесуге тырысамыз❣️" in message.text else "❣️ Write what bothers you")
    await state.set_state(Question.waiting_text)

# --- Handle user messages ---
anonymous_messages = {}

@router.message(Question.waiting_text)
async def handle_all(message: Message, state: FSMContext):
    data = await state.get_data()
    t = data.get("type")
    db = get_db()
    cur = db.cursor()

    if t == "application":
        cur.execute("INSERT INTO applications (tg_id, text) VALUES (?, ?)", (message.from_user.id, message.text))
    elif t == "idea":
        cur.execute("INSERT INTO appeals (tg_id, text, type) VALUES (?, ?, ?)", (message.from_user.id, message.text, t))
    elif t == "antibullying":
        code = uuid.uuid4().hex[:5].upper()
        anonymous_messages[code] = message.from_user.id
        await bot.send_message(
            ANTI_BULLYING_CHAT_ID,
            f"анон\n🆔 Код: {code}\n\n{message.text}\n\n↩️"
        )
        await message.answer("🤗 🩵")
        await state.clear()
        db.close()
        return

    db.commit()
    sent = await bot.send_message(GROUP_ID, f"{'Заявка в Парламент 🙌' if t=='application' else 'Идея / Feedback 💡'}:\n{message.text}")
    cur.execute("INSERT INTO messages (user_id, group_message_id) VALUES (?, ?)", (message.from_user.id, sent.message_id))
    db.commit()
    db.close()
    await message.answer("✅ Okay")
    await state.clear()

# --- Reply from GROUP ---
@router.message(F.chat.id == GROUP_ID, F.reply_to_message)
async def reply_from_group(message: Message):
    replied_id = message.reply_to_message.message_id
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT user_id FROM messages WHERE group_message_id = ?", (replied_id,))
    row = cur.fetchone()
    db.close()
    if not row:
        return
    await bot.send_message(row[0], f"📩:\n\n{message.text}")

# --- Reply to ANONYMOUS ---
@router.message(F.chat.id == ANTI_BULLYING_CHAT_ID, F.reply_to_message)
async def answer_from_group(message: Message):
    original = message.reply_to_message.text
    if "🆔 Код:" not in original:
        return
    try:
        code = original.split("🆔 Код:")[1].split("\n")[0].strip()
        user_id = anonymous_messages.get(code)
    except:
        return
    if not user_id:
        await message.reply("❌ Пользователь не найден (бот перезапускался).")
        return
    await bot.send_message(user_id, f"💬:\n\n{message.text}")
    del anonymous_messages[code]
