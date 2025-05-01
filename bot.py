import subprocess, time, pyautogui as pag, cfg, logging, pyrogram, platform as pf
from sound import Sound
from cfg import owner_id, start_text, bot_user

from PIL import ImageDraw
from pyrogram import Client, filters
from pyrogram.types import Message as msg, CallbackQuery as cq
from pyrogram import enums
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

curs = 100
sound_msgid = ""
power_msgid = ""
power_message = "Выберите кнопку:\n\n"



app = Client("bot", api_id=cfg.api_id, api_hash=cfg.api_hash, bot_token=cfg.TOKEN)



try:
    with app:
        app.send_message(owner_id, f"{start_text}", reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))
except:
    print("Ошибка, не удалось отправить сообщение о запуске ПК.")



@app.on_message(filters.command("start", prefixes="/") & filters.user(owner_id))
async def app_start(_, message: msg):
    try:
        await message.reply("Выберите действие:", reply_markup=menu_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

#----------------------------  Action with screen  ---------------------------------------------------------

@app.on_message(filters.command("Screen", prefixes="") & filters.user(owner_id))
async def screens(_, message: msg):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('С курсором', callback_data='screen_with_cursor'), InlineKeyboardButton('Без курсора', callback_data='screen_without_cursor')]])
        await message.reply('Выберите тип скриншота:', reply_markup=keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("messages", prefixes="") & filters.user(owner_id))
async def messages(_, message: msg):
    try:
        await message.reply("Выберите тип MessageBox'а:", reply_markup=msgbox_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("msgbox feedback:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def msgbox_feedback(_, message: msg):
    try:
        text = message.text.split(": ", 1)[1]
        await message.reply(f"Текст  '{text}'  отображён.")
        result = pag.prompt(f"{text}")
        await message.reply(f"Ответ: {result}")
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("msgbox:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def msgbox(_, message: msg):
    try:
        text = message.text.split(": ", 1)[1]
        await message.reply(f"Текст  '{text}'  отображён.")
        pag.alert(f"{text}")
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

#----------------------------  Power and CMD  ---------------------------------------------------------

@app.on_message(filters.command("выключение через:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def power_off(_, message: msg):
    try:
        countdown = int(message.text.split(": ", 1)[1])
        subprocess.run(f"shutdown -s -t {countdown}", shell=True)
        await app.edit_message_text(message.chat.id, power_msgid, power_message+f"Выключение через: {countdown} сек.", reply_markup=power_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("перезагрузка через:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def power_restart(_, message: msg):
    try:
        countdown = int(message.text.split(": ", 1)[1])
        subprocess.run(f"shutdown -r -t {countdown}", shell=True)
        await app.edit_message_text(message.chat.id, power_msgid, power_message+f"Перезагрузка через: {countdown} сек.", reply_markup=power_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("инъекция команды:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def command_injection(_, message: msg):
    try:
        execute_cmd = message.text.split(": ", 1)[1]
        encoding = "cp866" if pf.system() == "Windows" else "utf-8"
        result = subprocess.run(execute_cmd, shell=True, capture_output=True, text=True, encoding=encoding)
        output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        if not output:
            output = "Команда выполнена, но не вернула результата."
        await app.edit_message_text(message.chat.id, power_msgid, power_message + f"Введена команда: {execute_cmd}\nРезультат:\n{output}", reply_markup=power_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

@app.on_message(filters.command("power and cmd", prefixes="") & filters.user(owner_id))
async def power_control(_, message: msg):
    try:
        global power_msgid
        power_msgid = message.id + 1
        await message.reply(power_message, reply_markup=power_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

#----------------------------  Mouse  ---------------------------------------------------------

@app.on_message(filters.command("mouse", prefixes="") & filters.user(owner_id))
async def mouse_control(_, message: msg):
    try:
        x, y = pag.position()
        await message.reply(f"Координаты курсора: X={x}, Y={y}\nРазмах курсора: {curs}", reply_markup=mouse_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")
            
@app.on_message(filters.command("шаг курсора:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def cursor(_, message: msg):
    try:
        global curs
        curs = int(message.text.split(": ", 1)[1])
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")

#----------------------------  Sound  ---------------------------------------------------------
            
@app.on_message(filters.command("sound", prefixes="") & filters.user(owner_id))
async def sound_control(_, message: msg):
    try:
        global sound_msgid
        sound_msgid = message.id + 1
        await app.send_message(message.from_user.id, f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")
            
@app.on_message(filters.command("установить громкость:", prefixes=f"{bot_user} ") & filters.user(owner_id))
async def set_volume(_, message: msg):
    try:
        vol = int(message.text.split(": ", 1)[1])
        Sound.volume_set(vol)
        await app.edit_message_text(message.chat.id, int(sound_msgid), f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка")
            

#----------------------------  CQ  ---------------------------------------------------------

@app.on_callback_query()
async def callback(_, cq: cq):
    try:
#----------------------------  Mouse CQ  ---------------------------------------------------------
        if cq.data in ["up", "down", "left", "right"]:
            x, y = pag.position()

            if cq.data == "up":
                pag.moveTo(x, int(y - curs), duration=0.2)
                new_x, new_y = pag.position()
                await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse_keyboard)

            elif cq.data == "down":
                pag.moveTo(x, int(y + curs), duration=0.2)
                new_x, new_y = pag.position()
                await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse_keyboard)

            elif cq.data == "left":
                pag.moveTo(int(x - curs), y, duration=0.2)
                new_x, new_y = pag.position()
                await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse_keyboard)

            elif cq.data == "right":
                pag.moveTo(int(x + curs), y, duration=0.2)
                new_x, new_y = pag.position()
                await cq.message.edit_text(f"Координаты курсора: X={new_x}, Y={new_y}", reply_markup=mouse_keyboard)

        if cq.data == "lbm":
            pag.leftClick()
            await cq.answer()

        elif cq.data == "rbm":
            pag.rightClick()
            await cq.answer()

#----------------------------  Screen CQ  -----------------------------------------------------

        if "screen" in cq.data:
            screenshot = pag.screenshot()
            if cq.data == "screen_with_cursor":
                x, y = pag.position()
                draw = ImageDraw.Draw(screenshot)
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline="red", width=2)
            screenshot.save("s.png")
            await cq.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
            await cq.message.reply_photo("s.png")
            await cq.answer()

#----------------------------  Sound CQ  ---------------------------------------------------------
        
        if cq.data == "vol_minus":
            current_vol = int(Sound.current_volume())
            Sound.volume_set(current_vol - 10)
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)

        elif cq.data == "vol_plus":
            current_vol = int(Sound.current_volume())
            Sound.volume_set(current_vol + 10)
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)
        
        elif cq.data == "mute":
            Sound.mute()
            await cq.message.edit_text(f"Текущая громкость: {str(Sound.current_volume())}\nЗвук замьючен: {Sound.is_muted()}", reply_markup=sound_keyboard)

#----------------------------  Power CQ  ---------------------------------------------------------
        if cq.data == "power_undo":
            subprocess.run('shutdown -a')
            await cq.message.edit_text(power_message, reply_markup=power_keyboard)
            await cq.answer("Выключение/Перезагрузка отменено.")

    except Exception as e:
        logging.error(e)
        await cq.message.reply(f"Произошла ошибка")



mouse_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("ЛКМ",callback_data="lbm"), InlineKeyboardButton("ПКМ",callback_data="rbm")],
        [InlineKeyboardButton("⬆",callback_data="up")],
        [InlineKeyboardButton("⬅",callback_data="left"), InlineKeyboardButton("➡",callback_data="right")],
        [InlineKeyboardButton("⬇",callback_data="down")],
        [InlineKeyboardButton("Шаг курсора",switch_inline_query_current_chat="Шаг курсора: ")]
    ]
)
sound_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Mute", callback_data="mute"), InlineKeyboardButton("Set Vol", switch_inline_query_current_chat="установить громкость: ")],
        [InlineKeyboardButton("-", callback_data="vol_minus"), InlineKeyboardButton("+", callback_data="vol_plus")]
    ]
)
power_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Команда", switch_inline_query_current_chat="Инъекция команды: "), InlineKeyboardButton("Отмена", callback_data="power_undo")],
        [InlineKeyboardButton("Выключение", switch_inline_query_current_chat="Выключение через: "), InlineKeyboardButton("Перезагрузка", switch_inline_query_current_chat="Перезагрузка через: ")]
    ]
)

msgbox_keyboard=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Without feedback", switch_inline_query_current_chat="msgbox: ")],
        [InlineKeyboardButton("With feedback", switch_inline_query_current_chat="msgbox feedback: ")]
    ]
)

menu_keyboard = ReplyKeyboardMarkup(
                [
                    ["Messages", "Screen"],
                    ["Power and CMD"],
                    ["Mouse", "Sound"]
                ],
                resize_keyboard=True
            )



















































































































































































































































if __name__ == '__main__':
    while True:
        try:
            app.run()
        except:
            time.sleep(10)
