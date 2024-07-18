from machine import Pin
from telegram_ubot import Bot

bot = Bot('YOUR_BOT_TOKEN')
led = Pin(2, Pin.OUT)

@bot.add_command_handler('led_on')
def led_on(update):
    led.value(1)  # Allumer la LED
    update.reply('LED allumée!')

@bot.add_command_handler('led_off')
def led_off(update):
    led.value(0)  # Éteindre la LED
    update.reply('LED éteinte!')

bot.start_loop()