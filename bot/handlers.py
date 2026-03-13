"""
Telegram bot handlers for warehouse management system
"""

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging
from django.conf import settings
from django.db.models import F
from inventory.models import Product, TelegramUser, Transaction

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


class ProductSearch(StatesGroup):
    waiting_for_product_code = State()
    waiting_for_quantity = State()


def get_main_keyboard():
    """Get main menu keyboard"""
    kb = [
        [KeyboardButton(text="📦 Mahsulot qidirish")],
        [KeyboardButton(text="📊 Qoldiq haqida ma'lumot")],
        [KeyboardButton(text="⚙️ Sozlamalar")],
        [KeyboardButton(text="❌ Chiqish")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Start command handler"""
    await state.clear()
    
    # Get or create telegram user
    telegram_user, created = TelegramUser.objects.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            'username': message.from_user.username or '',
            'first_name': message.from_user.first_name or '',
            'last_name': message.from_user.last_name or ''
        }
    )
    
    welcome_text = f"""
Assalomu alaykim! 👋 {message.from_user.first_name}

Do'kon Omborini Boshqarish v1.0 xush kelibsiz!

Men omborning mahsulotlari haqida ma'lumot berishga tayyorman:
✅ Mahsulot mavjudligini tekshirish
✅ Kam qolgan mahsulotlar haqida ogohlantirish
✅ Omborning statistikasi

Pastdan oynachilar orqali boshlab qo'ying! 👇
    """
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@dp.message(lambda message: message.text == "📦 Mahsulot qidirish")
async def search_product(message: types.Message, state: FSMContext):
    """Product search handler"""
    await message.answer("Mahsulot kodini yoki nomini kiriting:")
    await state.set_state(ProductSearch.waiting_for_product_code)


@dp.message(ProductSearch.waiting_for_product_code)
async def process_product_search(message: types.Message, state: FSMContext):
    """Process product search"""
    query = message.text.lower()
    
    products = Product.objects.filter(
        is_active=True,
        name__icontains=query
    ) | Product.objects.filter(
        is_active=True,
        code__icontains=query
    )
    
    if not products.exists():
        await message.answer("❌ Mahsulot topilmadi!")
        await state.clear()
        return
    
    response = "🔍 Topilgan mahsulotlar:\n\n"
    
    for product in products[:10]:
        status = "✅" if product.quantity > 0 else "❌"
        response += f"{status} {product.name}\n"
        response += f"   Kod: {product.code}\n"
        response += f"   Qoldiq: {product.quantity} {product.unit}\n"
        response += f"   Narx: {product.price}\n\n"
    
    await message.answer(response, reply_markup=get_main_keyboard())
    await state.clear()


@dp.message(lambda message: message.text == "📊 Qoldiq haqida ma'lumot")
async def stock_info(message: types.Message):
    """Stock information handler"""
    low_stock_products = Product.objects.filter(
        is_active=True,
        quantity__lt=F('min_stock')
    )
    
    out_of_stock = Product.objects.filter(is_active=True, quantity=0)
    
    response = "📊 Omborning statusi:\n\n"
    response += f"📦 Jami mahsulotlar: {Product.objects.filter(is_active=True).count()}\n"
    response += f"⚠️ Kam qolgan: {low_stock_products.count()}\n"
    response += f"❌ Tugagan: {out_of_stock.count()}\n\n"
    
    if out_of_stock.exists():
        response += "❌ Tugagan mahsulotlar:\n"
        for product in out_of_stock[:5]:
            response += f"  • {product.name}\n"
    
    if low_stock_products.exists():
        response += "\n⚠️ Kam qolgan mahsulotlar:\n"
        for product in low_stock_products[:5]:
            response += f"  • {product.name} (Qoldiq: {product.quantity})\n"
    
    await message.answer(response, reply_markup=get_main_keyboard())


@dp.message(lambda message: message.text == "⚙️ Sozlamalar")
async def settings(message: types.Message):
    """Settings handler"""
    telegram_user = TelegramUser.objects.get(telegram_id=message.from_user.id)
    
    status = "✅ Yoniq" if telegram_user.notifications_enabled else "❌ O'chiq"
    
    response = f"⚙️ Sizning sozlamalari:\n\n"
    response += f"Bildirishnomalar: {status}\n"
    response += f"Telegram ID: {message.from_user.id}\n"
    
    kb = [
        [InlineKeyboardButton(text="📢 Bildirishnomalarni o'zgartirish", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(response, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "toggle_notifications")
async def toggle_notifications(callback_query: types.CallbackQuery):
    """Toggle notifications"""
    telegram_user = TelegramUser.objects.get(telegram_id=callback_query.from_user.id)
    telegram_user.notifications_enabled = not telegram_user.notifications_enabled
    telegram_user.save()
    
    status = "✅ Yoniq" if telegram_user.notifications_enabled else "❌ O'chiq"
    
    await callback_query.answer(f"Bildirishnomalar {status}")
    await callback_query.message.edit_text(
        f"✅ Sozlamalar saqlandi!\nBildirishnomalar: {status}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Bosh sahifa", callback_data="back_menu")]])
    )


@dp.callback_query(lambda c: c.data == "back_menu")
async def back_menu(callback_query: types.CallbackQuery):
    """Back to main menu"""
    await callback_query.message.delete()
    await callback_query.message.answer("Bosh sahifaga qaytoldiz!", reply_markup=get_main_keyboard())


@dp.message(lambda message: message.text == "❌ Chiqish")
async def logout(message: types.Message):
    """Logout handler"""
    await message.answer("Xayr! 👋", reply_markup=types.ReplyKeyboardRemove())


async def send_low_stock_notification(product):
    """Send low stock notification to all active telegram users"""
    try:
        telegram_users = TelegramUser.objects.filter(notifications_enabled=True)
        
        message_text = f"""
⚠️ Kam qolgan mahsulot!

Mahsulot: {product.name}
Kod: {product.code}
Mavjud: {product.quantity} {product.unit}
Minimal: {product.min_stock} {product.unit}

🔴 E'tibor bering va kirim qiling!
        """
        
        for user in telegram_users:
            try:
                await bot.send_message(user.telegram_id, message_text)
            except Exception as e:
                logger.error(f"Error sending message to {user.telegram_id}: {e}")
    except Exception as e:
        logger.error(f"Error in send_low_stock_notification: {e}")


async def send_new_income_notification(transaction):
    """Send new income notification"""
    try:
        telegram_users = TelegramUser.objects.filter(notifications_enabled=True)
        
        message_text = f"""
✅ Yangi mahsulot kirim!

Mahsulot: {transaction.product.name}
Miqdori: {transaction.quantity} {transaction.product.unit}
Vaqti: {transaction.created_at.strftime('%d.%m.%Y %H:%M')}

Ombor yangilandi!
        """
        
        for user in telegram_users:
            try:
                await bot.send_message(user.telegram_id, message_text)
            except Exception as e:
                logger.error(f"Error sending message to {user.telegram_id}: {e}")
    except Exception as e:
        logger.error(f"Error in send_new_income_notification: {e}")


async def main():
    """Start polling"""
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
