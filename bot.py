import subprocess, time, requests, platform as pf, os, pyautogui as pag, cfg, pyrogram, logging
from sound import Sound

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message as msg, CallbackQuery as cq
from pyrogram import enums
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen

logging.basicConfig(level=logging.INFO)

curs = ''
sound_msgid = ""
power_msgid = ""
power_message = "Выберите кнопку:\n\n"



app = Client("bot", api_id=cfg.api_id, api_hash=cfg.api_hash, bot_token=cfg.TOKEN)





try:
    with app:
        start_start = ReplyKeyboardMarkup(
                    [
                        ["/start"],  # First row
                    ],
                    resize_keyboard=True  # Make the keyboard smaller
                )
        app.send_message(cfg.developer_id, f"{cfg.start_text}", reply_markup=start_start)
except:
    print("Ошибка, не удалось отправить сообщение о запуске ПК.")

Sound.volume_set(20)

@app.on_message(filters.command("start", prefixes="/"))
async def app_start(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Выберите действие:", reply_markup=menu_keyboard)   
    else:
        alert = f'Кто-то пытался задать команду: {message.text}\n'
        alert += f'ID: {message.from_user.id}\n'
        alert += f'Username: @{message.from_user.username}'
        await app.send_message(cfg.developer_id, alert)

#----------------------------  Action with screen  ---------------------------------------------------------

@app.on_message(filters.command("Screen", prefixes=""))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            pag.screenshot('s.png')
            await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
            await message.reply_photo("s.png")
        except Exception as e:
            await message.edit_text(f"Произошла ошибка: {str(e)}")

@app.on_message(filters.command("chat", prefixes=""))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введите текст для отображения на экран.")
        text = asking.text
        await app.send_message(message.from_user.id, f"Текст  '{text}'  отображён.")
        result = pag.prompt(f"{text}")
        await app.send_message(message.from_user.id, f"Ответ: {result}")

@app.on_message(filters.command("msg", prefixes=""))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введите текст для отображения на экран.")
        text = asking.text
        await app.send_message(message.from_user.id, f"Текст  '{text}'  отображён.")
        pag.alert(f"{text}")

#----------------------------  Power and CMD  ---------------------------------------------------------

@app.on_message(filters.command("выключение через:", prefixes="@RC_Fire_Bot "))
async def power_off(client, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            countdown = int(message.text.split(": ", 1)[1])
            subprocess.run(f"shutdown -s -t {countdown}", shell=True)
            await app.edit_message_text(message.chat.id, power_msgid, power_message+f"Выключение через: {countdown} сек.", reply_markup=power_keyboard)
        except Exception as e:
            await message.reply(f"Произошла ошибка:\n{str(e)}")

@app.on_message(filters.command("перезагрузка через:", prefixes="@RC_Fire_Bot "))
async def power_restart(client, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            countdown = int(message.text.split(": ", 1)[1])
            subprocess.run(f"shutdown -r -t {countdown}", shell=True)
            await app.edit_message_text(message.chat.id, power_msgid, power_message+f"Перезагрузка через: {countdown} сек.", reply_markup=power_keyboard)
        except Exception as e:
            await message.reply(f"Произошла ошибка:\n{str(e)}")

@app.on_message(filters.command("инъекция команды:", prefixes="@RC_Fire_Bot "))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            execute_cmd = message.text.split(": ", 1)[1]
            subprocess.run(f"{execute_cmd}", shell=True)
            await app.edit_message_text(message.chat.id, power_msgid, power_message+f"Введена команда: {execute_cmd}", reply_markup=power_keyboard)
        except Exception as e:
            await message.reply(f"Произошла ошибка:\n{str(e)}")

@app.on_message(filters.command("power and cmd", prefixes=""))
async def power_control(client, message: msg):
    if message.from_user.id == cfg.developer_id:
        global power_msgid
        power_msgid = message.id + 1
        await message.reply(power_message, reply_markup=power_keyboard)

#----------------------------  Mouse  ---------------------------------------------------------

@app.on_message(filters.command("mouse", prefixes=""))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        await message.reply('Выберите действие:', reply_markup=mouse_keyboard)
            
@app.on_message(filters.command("шаг курсора:", prefixes="@RC_Fire_Bot "))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            global curs
            curs = int(message.text.split(": ", 1)[1])
        except Exception as e:
            await message.reply(f"Произошла ошибка:\n{str(e)}")

#----------------------------  Sound  ---------------------------------------------------------
            
@app.on_message(filters.command("sound", prefixes=""))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        global sound_msgid
        sound_msgid = message.id + 1
        await app.send_message(message.from_user.id, f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
        print(sound_msgid)
            
@app.on_message(filters.command("установить громкость:", prefixes="@RC_Fire_Bot "))
async def command(_, message: msg):
    if message.from_user.id == cfg.developer_id:
        try:
            vol = int(message.text.split(": ", 1)[1])
            Sound.volume_set(vol)
            await app.edit_message_text(message.chat.id, int(sound_msgid), f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
        except Exception as e:
            await message.reply(f"Произошла ошибка:\n{str(e)}")
            


@app.on_callback_query()
async def callback(client, cq: cq):
    try:
#----------------------------  Mouse  ---------------------------------------------------------
        x, y = pag.position()  # Текущие координаты курсора

        if cq.data == "lbm":
            pag.leftClick()
            await cq.answer()

        elif cq.data == "rbm":
            pag.rightClick()
            await cq.answer()

        elif cq.data == "up":
            pag.moveTo(x, int(y - curs), duration=0.2)
            new_x, new_y = pag.position()
            await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse1_keyboard)

        elif cq.data == "down":
            pag.moveTo(x, int(y + curs), duration=0.2)
            new_x, new_y = pag.position()
            await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse1_keyboard)

        elif cq.data == "left":
            pag.moveTo(int(x - curs), y, duration=0.2)
            new_x, new_y = pag.position()
            await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse1_keyboard)

        elif cq.data == "right":
            pag.moveTo(int(x + curs), y, duration=0.2)
            new_x, new_y = pag.position()
            await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse1_keyboard)
        
        elif cq.data == "mouse_c":
            await cq.message.edit_text(f"Координаты курсора: X={x}, Y ={y}", reply_markup=mouse1_keyboard)

#----------------------------  Sound  ---------------------------------------------------------
        if cq.data == "sound_mute":
            Sound.mute()
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
        
        elif cq.data == "vol_minus":
            current_vol = int(Sound.current_volume())
            Sound.volume_set(current_vol - 10)
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)

        elif cq.data == "vol_plus":
            current_vol = int(Sound.current_volume())
            Sound.volume_set(current_vol + 10)
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)

#----------------------------  Power  ---------------------------------------------------------
        if cq.data == "power_undo":
            subprocess.run('shutdown -a')
            await cq.message.edit_text(power_message, reply_markup=power_keyboard)
            await cq.answer("Выключение/Перезагрузка отменено.")

    except Exception as e:
        await cq.message.reply(f"Произошла ошибка:\n{str(e)}")



mouse_keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("Шаг курсора",switch_inline_query_current_chat="Шаг курсора: "), InlineKeyboardButton("Управление",callback_data="mouse_c")]])
mouse1_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("ЛКМ",callback_data="lbm"), InlineKeyboardButton("ПКМ",callback_data="rbm")], #1
        [InlineKeyboardButton("⬆",callback_data="up")], #2
        [InlineKeyboardButton("⬅",callback_data="left"), InlineKeyboardButton("➡",callback_data="right")], #3
        [InlineKeyboardButton("⬇",callback_data="down")] #4
    ]
)
sound_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Mute", callback_data="sound_mute"), InlineKeyboardButton("Set Vol", switch_inline_query_current_chat="установить громкость: ")],
        [InlineKeyboardButton("-", callback_data="vol_minus"), InlineKeyboardButton("+", callback_data="vol_plus")]
    ]
)
power_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Команда", switch_inline_query_current_chat="Инъекция команды: "), InlineKeyboardButton("Отмена", callback_data="power_undo")],
        [InlineKeyboardButton("Выключение", switch_inline_query_current_chat="Выключение через: "), InlineKeyboardButton("Перезагрузка", switch_inline_query_current_chat="Перезагрузка через: ")]
    ]
)

menu_keyboard = ReplyKeyboardMarkup(
                [
                    ["MSG", "Screen", "Chat"],  # First row
                    ["Power and CMD"],  # Second row
                    ["Mouse", "Sound"]  # Thirth row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )



















































































































































































































































if __name__ == '__main__':
    while True:
        try:
            app.run()
        except:
            time.sleep(10) # Automatically start() and idle()
