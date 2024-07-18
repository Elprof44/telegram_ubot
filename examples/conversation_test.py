# ### RENOMMER LE FICHIER EN main.py AVANT DE LE TÉLÉVERSER SUR LA CARTE

# CET EXEMPLE SIMPLE PERMET D'ALLUMER ET D'ÉTEINDRE UNE LED CONNECTÉE À LA BROCHE 2 EN UTILISANT UN CLAVIER PERSONNALISÉ,
# IL EST ÉGALEMENT POSSIBLE DE CONNAÎTRE L'ÉTAT ACTUEL DE LA BROCHE

from telegram_ubot import Bot, Conversation, ReplyKeyboardMarkup, KeyboardButton
from machine import Pin

TOKEN = 'VotreTokenIci'

bot = Bot(TOKEN)
led = Pin(2, Pin.OUT)
c = Conversation(['NOM', 'AGE']) # conversation en 2 étapes

@c.add_command_handler('ENTRY', 'start')
def start(update):
    update.reply('Quel est votre nom ?')
    return 'NOM'

@c.add_message_handler('NOM', '(.*?)') # chaque message
def nom(update):
    update.reply('Bonjour {}, quel âge avez-vous ?'.format(update.message['text']))
    return 'AGE'

@c.add_command_handler('AGE', 'value') # utilisé pour démontrer la priorité de la conversation sur le gestionnaire global
def valeur_fausse(update):
    update.reply('Vous ne pouvez pas obtenir la valeur maintenant, veuillez me dire votre âge')
    return 'AGE'

@c.add_message_handler('AGE', '^[0-9]*$') # seulement des chiffres
def age(update):
    if int(update.message['text']) > 17:
        update.reply('Vous êtes vérifié')
        led.on()
        return c.END
    else:
        update.reply('Accès refusé, réessayez...')
        led.off()
        return 'AGE'

@bot.add_command_handler('value')
def valeur(update):
    if led.value():
        update.reply('La LED est allumée')
    else:
        update.reply('La LED est éteinte')

bot.add_conversation_handler(c)
bot.start_loop()
