import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- SOZLAMALAR ---
API_TOKEN = '8594100359:AAHvSdp_KBpQeLPLcwBa5iyzkHwZGyS_i-g' 
ADMIN_ID = '790466388'
KARTA_RAQAM = "9860 1201 7907 3834 (Jumaniyazov Murodjon.)"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- TUGMALAR ---
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("✍️ Buyurtma berish"))
main_menu.add(KeyboardButton("📣 Kanalimiz"), KeyboardButton("📞 Admin"))

contact_btn = ReplyKeyboardMarkup(resize_keyboard=True)
contact_btn.add(KeyboardButton("📱 Raqamimni yuborish", request_contact=True))

cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_btn.add(KeyboardButton("🔙 Bekor qilish"))

# --- BOSQICHLAR ---
class Muloqot(StatesGroup):
    ism = State()     # 1. Ismi
    xabar = State()   # 2. Buyurtma matni/rasmi
    chek = State()    # 3. To'lov cheki (MAJBURIY)
    aloqa = State()   # 4. Telefon raqam

# --- START ---
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        f"Assalomu alaykum! **@Biznes_Dizayn** botiga xush kelibsiz.\n"
        "Buyurtma berish uchun tugmani bosing 👇",
        reply_markup=main_menu, parse_mode="Markdown"
    )

# BEKOR QILISH
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(lambda message: message.text == "🔙 Bekor qilish", state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Buyurtma bekor qilindi.", reply_markup=main_menu)

# 1. ISM
@dp.message_handler(lambda message: message.text == "✍️ Buyurtma berish")
async def start_chat(message: types.Message):
    await Muloqot.ism.set()
    await message.answer("Ismingiz nima?", reply_markup=cancel_btn)

# 2. BUYURTMA
@dp.message_handler(state=Muloqot.ism)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Muloqot.next()
    await message.answer(
        "Qanday poster kerak? (Matn yoki rasm yuboring):",
        reply_markup=cancel_btn
    )

# 3. TO'LOV SO'ROVI (MAJBURIY)
@dp.message_handler(content_types=['text', 'photo'], state=Muloqot.xabar)
async def process_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.photo:
            data['type'] = 'photo'
            data['content'] = message.photo[-1].file_id
            data['caption'] = message.caption or ""
        else:
            data['type'] = 'text'
            data['content'] = message.text
            
    await Muloqot.next()
    # Faqat "Bekor qilish" tugmasi chiqadi, o'tkazib yuborish yo'q
    await message.answer(
        f"💰 **To'lov bosqichi**\n\n"
        f"Buyurtma qabul qilinishi uchun to'lov qiling:\n💳 `{KARTA_RAQAM}`\n\n"
        "📸 **Chek rasm (skrinshot)ini yuboring.** (Cheksiz qabul qilinmaydi)",
        reply_markup=cancel_btn, parse_mode="Markdown"
    )

# 4. CHEKNI TEKSHIRISH (Faqat rasm o'tadi)
@dp.message_handler(content_types=['any'], state=Muloqot.chek)
async def process_chek(message: types.Message, state: FSMContext):
    # Agar rasm bo'lmasa, qaytarib yuboramiz
    if not message.photo:
        await message.answer("❌ Bu rasm emas. Iltimos, to'lov chekini rasm (skrinshot) qilib yuboring.")
        return

    # Rasm bo'lsa saqlaymiz
    chek_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['chek_id'] = chek_id

    await Muloqot.next()
    await message.answer("Bog'lanish uchun telefon raqamingizni yuboring:", reply_markup=contact_btn)

# 5. YAKUNIY (Adminga yuborish)
@dp.message_handler(content_types=['contact', 'text'], state=Muloqot.aloqa)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    
    async with state.proxy() as data:
        ism = data['name']
        msg_type = data['type']
        content = data['content']
        caption = data.get('caption', '')
        chek_id = data['chek_id']

    # --- ADMINGA ---
    admin_header = f"🔔 **YANGI BUYURTMA!**\n👤 Mijoz: {ism}\n📞 Tel: {phone}\n👇 Buyurtma:"
    
    try:
        # 1. Buyurtmani yuborish
        if msg_type == 'photo':
            await bot.send_photo(chat_id=ADMIN_ID, photo=content, caption=f"{admin_header}\nIzoh: {caption}", parse_mode="Markdown")
        else:
            await bot.send_message(chat_id=ADMIN_ID, text=f"{admin_header}\n📝 {content}", parse_mode="Markdown")
        
        # 2. Chekni yuborish
        await bot.send_photo(chat_id=ADMIN_ID, photo=chek_id, caption=f"💸 **{ism}** dan to'lov cheki (Tasdiqlandi) ✅", parse_mode="Markdown")
            
        await message.answer("✅ Buyurtmangiz va to'lov qabul qilindi! Tez orada aloqaga chiqamiz.", reply_markup=main_menu)
    
    except Exception as e:
        await message.answer("Xatolik bo'ldi, lekin ma'lumotlar saqlandi.")
    
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
