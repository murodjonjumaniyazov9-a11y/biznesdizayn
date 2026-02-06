import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# -----------------------------------------------------------
# SOZLAMALAR (TOKENNI SHU YERGA YOZING)
# -----------------------------------------------------------
BOT_TOKEN = "SIZNING_TOKENINGIZNI_SHU_YERGA_QUYING" 

# Loglarni yoqish (xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -----------------------------------------------------------
# TUGMALAR (MENU)
# -----------------------------------------------------------
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎨 Dizayn xizmatlari"), KeyboardButton(text="📊 Buxgalteriya")],
        [KeyboardButton(text="📞 Bog'lanish"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True, # Tugmalar chiroyli o'lchamda bo'ladi
    input_field_placeholder="Bo'limni tanlang..."
)

# -----------------------------------------------------------
# HANDLERS (JAVOBLAR)
# -----------------------------------------------------------

@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Foydalanuvchi ismini olamiz
    user_name = message.from_user.full_name
    await message.answer(
        f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
        "Biznes Dizayn va Buxgalteriya xizmatlari botiga xush kelibsiz.\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "🎨 Dizayn xizmatlari")
async def design_info(message: Message):
    await message.answer(
        "<b>🎨 Bizning Dizayn xizmatlarimiz:</b>\n\n"
        "🔹 Logotiplar yasash\n"
        "🔹 Ijtimoiy tarmoqlar uchun bannerlar (SMM)\n"
        "🔹 Flayer va vizitkalar\n\n"
        "Buyurtma berish uchun: @AdminUser", # O'z useringizni yozing
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "📊 Buxgalteriya")
async def acc_info(message: Message):
    await message.answer(
        "<b>📊 Buxgalteriya xizmatlari:</b>\n\n"
        "✅ Soliq hisobotlarini topshirish\n"
        "✅ 1C dasturida ishlash\n"
        "✅ Korxona balansini yuritish\n\n"
        "Batafsil ma'lumot uchun biz bilan bog'laning.",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "📞 Bog'lanish")
async def contact_info(message: Message):
    await message.answer(
        "📞 <b>Aloqa uchun ma'lumotlar:</b>\n\n"
        "👤 Admin: @SizningUseringiz\n" # O'zgartiring
        "📱 Tel: +998 90 123 45 67\n"   # O'zgartiring
        "📍 Manzil: O'zbekiston",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "ℹ️ Biz haqimizda")
async def about_info(message: Message):
    await message.answer(
        "Bizning jamoa tadbirkorlarga o'z biznesini rivojlantirishda yordam beradi.\n"
        "Ham dizayn, ham hisob-kitob ishlaringizni bizga ishonib topshirishingiz mumkin!",
    )

# -----------------------------------------------------------
# BOTNI ISHGA TUSHIRISH
# -----------------------------------------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
