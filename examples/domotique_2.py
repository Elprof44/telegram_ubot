from machine import Pin
from telegram_ubot import Bot, KeyboardButton, ReplyKeyboardMarkup

# Initialisation du Bot
bot = Bot('YOUR_BOT_TOKEN')

# Configuration des broches
light = Pin(2, Pin.OUT)
fan = Pin(4, Pin.OUT)

# Fonction pour mettre à jour l'état des appareils
def update_device_state(device, state):
    if device == 'light':
        light.value(state)
    elif device == 'fan':
        fan.value(state)

# Création des boutons pour le clavier
button_light_on = KeyboardButton('Allumer la lumière')
button_light_off = KeyboardButton('Éteindre la lumière')
button_fan_on = KeyboardButton('Allumer le ventilateur')
button_fan_off = KeyboardButton('Éteindre le ventilateur')

# Création du clavier
keyboard = ReplyKeyboardMarkup([
    [button_light_on, button_light_off],
    [button_fan_on, button_fan_off]
], resize_keyboard=True)

# Gestionnaire de commande pour démarrer la domotique
@bot.add_command_handler('start')
def start(update):
    update.reply('Contrôlez vos appareils domestiques:', reply_markup=keyboard)

# Gestionnaire de message pour les boutons
@bot.add_message_handler('Allumer la lumière')
def light_on(update):
    update_device_state('light', 1)
    update.reply('Lumière allumée')

@bot.add_message_handler('Éteindre la lumière')
def light_off(update):
    update_device_state('light', 0)
    update.reply('Lumière éteinte')

@bot.add_message_handler('Allumer le ventilateur')
def fan_on(update):
    update_device_state('fan', 1)
    update.reply('Ventilateur allumé')

@bot.add_message_handler('Éteindre le ventilateur')
def fan_off(update):
    update_device_state('fan', 0)
    update.reply('Ventilateur éteint')

# Démarrer la boucle du bot
bot.start_loop()