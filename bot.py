import subprocess
import time
import requests
import platform as pf
import os
import pyautogui as pag
from sound import Sound

from loguru import logger

import cfg
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram import enums
from pyrogram.types import ReplyKeyboardMarkup
from pyromod import listen


curs = ''




app = Client("bot", api_id=cfg.api_id, api_hash=cfg.api_hash, bot_token=cfg.TOKEN)





with app:
    start_start = ReplyKeyboardMarkup(
                [
                    ["/start"],  # First row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )
    app.send_message(cfg.developer_id, f"{cfg.start_text}", reply_markup=start_start)




@app.on_message(filters.command("start", prefixes="/"))
async def app_start(_, message):
    print(message.from_user.id)
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Выберите действие:", reply_markup=menu_keyboard)   
    else:
        alert = f'Кто-то пытался задать команду: {message.text}\n'
        alert += f'ID: {message.from_user.id}\n'
        alert += f'Username: @{message.from_user.username}'
        await app.send_message(cfg.developer_id, alert)

@app.on_message(filters.command("PC Info", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        response = requests.get("http://jsonip.com/").json()
        msg = f"Имя ПК: {pf.node()}\nIP: {response['ip']}\nСистема: {pf.system()} {pf.release()}"
        await app.send_message(cfg.developer_id, msg)

@app.on_message(filters.command("Screen", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        try:
            pag.screenshot('s.png')
            await app.send_message(message.from_user.id, "Screenshot uploading...")
            await app.send_photo(message.from_user.id, open("s.png", 'rb'))
        except:
            await app.send_message(message.from_user.id, "Произошла ошибка.")

@app.on_message(filters.command("chat", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введите текст для отображения на экран.")
        text = asking.text
        await app.send_message(message.from_user.id, f"Текст  '{text}'  отображён.")
        result = pag.prompt(f"{text}")
        await app.send_message(message.from_user.id, f"Ответ: {result}")

@app.on_message(filters.command("msg", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введите текст для отображения на экран.")
        text = asking.text
        await app.send_message(message.from_user.id, f"Текст  '{text}'  отображён.")
        pag.alert(f"{text}")
        
@app.on_message(filters.command("shutdown", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Через сколько выключить ПК?")
        countdown_1 = asking.text
        subprocess.run(f"shutdown -s -t {countdown_1}", shell=True)
        await app.send_message(message.from_user.id, f"ПК будет выключен через {countdown_1} секунд.")

@app.on_message(filters.command("restart", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Через сколько перезагрузить ПК?")
        countdown_2 = asking.text
        subprocess.run(f"shutdown -r -t {countdown_2}", shell=True)
        await app.send_message(message.from_user.id, f"ПК будет перезагружен через {countdown_2} секунд.")

@app.on_message(filters.command("exec", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введи команду")
        in_cmd = asking.text
        subprocess.run(f'{in_cmd}', shell=True)
        await app.send_message(message.from_user.id, "Команда введена.")



@app.on_message(filters.command("Hotkeys", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Выберите горячую клавишу:", reply_markup=hotkeys)


            
@app.on_message(filters.command("отмена", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        subprocess.run('shutdown -a')
        await app.send_message(message.from_user.id, "Выключение/Перезапуск отменено.")

@app.on_message(filters.command("Open App", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Выберите действие:", reply_markup=open_app1)
            
@app.on_message(filters.command("Back", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Вы вернулись в меню")
        await app.send_message(message.from_user.id, "Выберите действие:", reply_markup=menu_keyboard)

@app.on_message(filters.command("Мышка", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, 'Выберите действие:', reply_markup=mouse_keyboard)
            
@app.on_message(filters.command("⬆", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        x, y = pag.position()
        pag.moveTo(x, int(y - curs))
            
@app.on_message(filters.command("⬇", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        x, y = pag.position()
        pag.moveTo(x, int(y+curs))
            
@app.on_message(filters.command("⬅", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        x, y = pag.position()
        pag.moveTo(int(x - curs), y)
            
@app.on_message(filters.command("➡", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        x, y = pag.position()
        pag.moveTo(int(x + curs), y)
            
@app.on_message(filters.command("ЛКМ", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        pag.leftClick()
            
@app.on_message(filters.command("ПКМ", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        pag.rightClick()
            
@app.on_message(filters.command("Размах Курсора", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Укажите размах курсора:")
        try:
            global curs
            curs = int(asking.text)
        except:
            await app.send_message(message.from_user.id, "Ошибка.")
            
@app.on_message(filters.command("Звук", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, "Выбери действие:", reply_markup=rc_volume_keyboard)
            
@app.on_message(filters.command("-", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        Sound.volume_down()
        await app.send_message(message.from_user.id, f'Выполнено.\nCurrent volume | {str(Sound.current_volume())}')
            
@app.on_message(filters.command("+", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        Sound.volume_up()
        await app.send_message(message.from_user.id, f'Выполнено.\nCurrent volume | {str(Sound.current_volume())}')
            
@app.on_message(filters.command("🔇", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        Sound.mute()
        await app.send_message(message.from_user.id, f'Выполнено.\nSound muted | {str(Sound.is_muted())}')
            
@app.on_message(filters.command("Установить", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        asking = await message.chat.ask("Введи уровень звука для установки:")
        try:
            vol = int(asking.text)
            Sound.volume_set(vol)
            await app.send_message(message.from_user.id, f"Выполнено.\nCurrent volume | {str(Sound.current_volume())}")
        except:
            await app.send_message(message.from_user.id, "Ошибка.")
            
@app.on_message(filters.command("Текущие настройки", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        await app.send_message(message.from_user.id, f'Current volume | {str(Sound.current_volume())}\nSound muted | {str(Sound.is_muted())}') 
            
@app.on_message(filters.command("Discord", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        os.startfile(r"C:\Users\zombi\AppData\Local\Discord\Discord.lnk")
            
@app.on_message(filters.command("Process Hacker 2", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        os.startfile(r"C:\Users\zombi\Desktop\Process Hacker 2.lnk")
            
@app.on_message(filters.command("Chrome", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        os.startfile(r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe")
            
@app.on_message(filters.command("Steam", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        os.startfile(r"C:\Program Files (x86)\Steam\steam.exe")
            
@app.on_message(filters.command("Soundpad", prefixes=""))
def command(_, message):
    if message.from_user.id == cfg.developer_id:
        os.startfile(r"D:\Apps\Soundpad\Soundpad.exe")
            
@app.on_message(filters.command("Alt+F4", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        pag.hotkey('alt', 'f4')
        await app.send_message(message.from_user.id, "Выполнено.")
            
@app.on_message(filters.command("Task Manager", prefixes=""))
async def command(_, message):
    if message.from_user.id == cfg.developer_id:
        pag.hotkey('ctrl', 'shift', 'esc')
        await app.send_message(message.from_user.id, "Выполнено.")
            












    



start_start = ReplyKeyboardMarkup(
                [
                    ["/start"],  # First row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

menu_keyboard = ReplyKeyboardMarkup(
                [
                    ["msg", "Screen", "chat"],  # First row
                    ["Shutdown", "Exec", "Restart"],  # Second row
                    ["Hotkeys", "Отмена", "Open App"],  # Third row
                    ["Мышка", "PC Info", "Звук"]  # Fourth row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

hotkeys = ReplyKeyboardMarkup(
                [
                    ["Alt+F4", "Task Manager"],  # First row
                    ["Back"],  # Second row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

open_app1 = ReplyKeyboardMarkup(
                [
                    ["Discord", "Process Hacker 2", "Chrome"],  # First row
                    ["Steam", "Soundpad"],  # Second row
                    ["Back"],  # Third row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

mouse_keyboard = ReplyKeyboardMarkup(
                [
                    ["⬆"],  # First row
                    ["⬅", "➡"], #Second row
                    ["⬇"], #Third row
                    ["ЛКМ", "ПКМ"],  # Fourth row
                    ["Размах Курсора"],  # Fifth row
                    ["Back"] #Sixth row
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

rc_volume_keyboard = ReplyKeyboardMarkup(
                [
                    ["-", "+"],  # First row
                    ["🔇"],  # Second row
                    ["Установить", "Текущие Настройки"],  # Third row
                    ["Back"],
                ],
                resize_keyboard=True  # Make the keyboard smaller
            )

















































































































































































































































if __name__ == '__main__':
	while True:
		try:
			logger.success("Бот успешно запущен! Ожидайте пару секунд для полного функционала.")
			app.run()
		except:
			time.sleep(10)