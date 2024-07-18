from machine import Pin
from telegram_ubot import Bot, InlineKeyboardButton, InlineKeyboardMarkup

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

# Création des boutons pour le clavier inline
button_light_on = InlineKeyboardButton('Allumer la lumière', callback_data='light_on')
button_light_off = InlineKeyboardButton('Éteindre la lumière', callback_data='light_off')
button_fan_on = InlineKeyboardButton('Allumer le ventilateur', callback_data='fan_on')
button_fan_off = InlineKeyboardButton('Éteindre le ventilateur', callback_data='fan_off')

# Création du clavier inline
keyboard = InlineKeyboardMarkup([
    [button_light_on, button_light_off],
    [button_fan_on, button_fan_off]
])

# Gestionnaire de commande pour démarrer la domotique
@bot.add_command_handler('start')
def start(update):
    update.reply('Contrôlez vos appareils domestiques:', reply_markup=keyboard)

# Gestionnaire de callback pour les boutons
@bot.add_callback_handler('light_on')
def light_on(update):
    update_device_state('light', 1)
    update.reply('Lumière allumée')

@bot.add_callback_handler('light_off')
def light_off(update):
    update_device_state('light', 0)
    update.reply('Lumière éteinte')

@bot.add_callback_handler('fan_on')
def fan_on(update):
    update_device_state('fan', 1)
    update.reply('Ventilateur allumé')

@bot.add_callback_handler('fan_off')
def fan_off(update):
    update_device_state('fan', 0)
    update.reply('Ventilateur éteint')

# Démarrer la boucle du bot
bot.start_loop()