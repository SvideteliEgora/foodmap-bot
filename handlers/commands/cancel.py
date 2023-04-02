from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return

    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Операция прервана',
                           reply_markup=ReplyKeyboardRemove())
