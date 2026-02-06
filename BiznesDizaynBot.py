import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# -----------------------------------------------------------
# SOZLAMALAR (SIZNING RASMINGIZDAGI O'ZGARUVCHILAR)
# -----------------------------------------------------------
API_TOKEN = '8594100359:AAHvSdp_KBpQeLPLcwBa5iyzkHwZGyS_i-g' # @BotFather'dan olgan tokenni yozing
ADMIN_ID = '790466388'       # @userinfobot'dan olgan ID'ni yozing
KARTA_RAQAM = "9860 1201 7907 3834 (Jumaniyazov M.)" # O'z kartangizni yozing

# Loglarni yoqish
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# -----------------------------------------------------------
# TUGMALAR
# -----------------------------------------------------------
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎨 Dizayn xizmatlari"), KeyboardButton(text="📊 Buxgalteriya")],
        [KeyboardButton(text="💳 To'lov qilish"), KeyboardButton(text="📞 Bog'lanish")]
    ],
    resize_keyboard=True
)

# -----------------------------------------------------------
# JAVOBLAR
# -----------------------------------------------------------

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Assalomu alaykum! Biznes Dizayn botiga xush kelibsiz.\n"
        f"Sizga qanday yordam bera olamiz?",
        reply_markup=main_menu
    )

@dp.message(F.text == "💳 To'lov qilish")
async def pay_info(message: Message):
    await message.answer(
        f"<b>To'lov ma'lumotlari:</b>\n\n"
        f"💳 Karta: <code>{KARTA_RAQAM}</code>\n"
        f"To'lovni amalga oshirgach, chekni adminga yuboring.",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "📞 Bog'lanish")
async def contact_info(message: Message):
    await message.answer(
        f"📞 <b>Admin bilan bog'lanish:</b>\n\n"
        f"Sizga yordam berishdan xursandmiz!\n"
        f"Admin ID: <code>{ADMIN_ID}</code>\n"
        f"Telegram: @Admin_User_Nomini_Yozing",
        parse_mode=ParseMode.HTML
    )

# Qolgan xizmatlar uchun umumiy javob
@dp.message(F.text.in_({"🎨 Dizayn xizmatlari", "📊 Buxgalteriya"}))
async def services(message: Message):
    await message.answer(f"Siz <b>{message.text}</b> bo'limini tanladingiz. Tez orada ma'lumot beramiz.", parse_mode=ParseMode.HTML)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
