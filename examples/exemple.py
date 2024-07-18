from telegram_ubot import Bot, ReplyKeyboardMarkup, KeyboardButton
from machine import Pin

# TOKEN = 'YourTokenGoesHere'

bot = Bot("TOKEN")

led = Pin(2, Pin.OUT)
fan = Pin(15, Pin.OUT)

# CLAVIER DÉFINI COMME UN TABLEAU DE TABLEAUX DE BOUTONS
clavier = [
        [KeyboardButton('ALLUMER'), KeyboardButton('ÉTEINDRE')],
        [KeyboardButton('BASCULER')],
        [KeyboardButton('VENTILATEUR_ALLUMER'), KeyboardButton('VENTILATEUR_ÉTEINDRE')]
        ]
clavierReponse = ReplyKeyboardMarkup(clavier)

##### gestionnaire de fonction d'aide ####
@bot.add_command_handler('aide')
def aide(update):
    update.reply('Écrivez /demarrer pour obtenir un clavier personnalisé ou /statut pour obtenir l\'état actuel de la LED')

@bot.add_command_handler('demarrer')
def demarrer(update):
    update.reply('Clavier de contrôle LED activé', reply_markup=clavierReponse)

##### gestionnaire de fonction pour obtenir les valeurs de la LED ####
@bot.add_command_handler('statut')
def statut(update):
    if led.value():
        update.reply('La LED est allumée')
    else:
        update.reply('La LED est éteinte')

##### gestionnaire de fonction pour la LED ####
@bot.add_message_handler('^allumer|Allumer|ALLUMER$')
def allumer(update):
    led.on()
    
@bot.add_message_handler('^eteindre|Éteindre|ÉTEINDRE$')
def eteindre(update):
    led.off()
    
@bot.add_message_handler('^basculer|BASCULER|Basculer$')
def basculer(update):
    ancien_etat = bool(led.value())
    led.value(not ancien_etat)
    
##### gestionnaire de fonction pour le ventilateur ####
@bot.add_message_handler('^ventilateur_allumer|Ventilateur_allumer|VENTILATEUR_ALLUMER$')
def ventilateur_allumer(update):
    fan.on()
    
@bot.add_message_handler('^ventilateur_eteindre|Ventilateur_éteindre|VENTILATEUR_ÉTEINDRE$')
def ventilateur_eteindre(update):
    fan.off()

# Gestionnaire de commande pour la commande /aide
@bot.add_command_handler('aide')
def aide(update):
    update.reply('Voici les commandes disponibles:\n/demarrer - Démarrer le bot\n/aide - Obtenir de l\'aide\n/repeat - Répéter votre message')

# Gestionnaire de commande pour la commande /repeat
@bot.add_command_handler('repeat')
def repeat(update):
    # Répète le texte après la commande /repeat
    message = update.message['text'].split(' ', 1)
    if len(message) > 1:
        update.reply(message[1])
    else:
        update.reply('Utilisation: /repeat votre message')

# Exemple de clavier personnalisé pour le ventilateur
@bot.add_command_handler('ventilateur')
def clavier_ventilateur(update):
    clavier = ReplyKeyboardMarkup([
        [KeyboardButton('ventilateur_allumer')],
        [KeyboardButton('ventilateur_eteindre')]
    ], resize_keyboard=True)
    update.reply('VENTILATEUR', reply_markup=clavier)

@bot.add_event_handler()
def gerer_tous_les_evenements(update):
    print('Nouvel événement reçu:', update.message['text'])
    update.reply('Vous avez envoyé : ' + update.message['text'])

# Démarrer le bot
bot.start_loop(print('démarrer'))
