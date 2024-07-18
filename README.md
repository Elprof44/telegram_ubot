# telegram_ubot

## Description

`telegram_ubot` est un module conçu pour créer et gérer facilement des bots Telegram en utilisant MicroPython. Il est spécialement conçu pour être exécuté sur des microcontrôleurs tels que l'ESP32. Vous pouvez l'utiliser pour des projets IoT, permettant au bot de recevoir des messages, de répondre à des commandes, de gérer des conversations complexes et de contrôler les broches de l'ESP32.

## Installation

### 1. Configuration de l'ESP32 avec Thonny IDE

1. Clonez ce dépôt ou copiez les fichiers dans votre environnement MicroPython.
2. Connectez votre ESP32 à votre ordinateur via USB.
3. Ouvrez Thonny IDE.
4. Sélectionnez l'interpréteur MicroPython (ESP32) dans les paramètres de Thonny.
5. Téléversez le fichier `telegram_ubot.py` sur l'ESP32.

### 2. Dépendances

Assurez-vous également d'avoir installé les bibliothèques nécessaires comme `urequests`.

## Configuration et Création du Bot

Pour créer une instance de votre bot, vous devez fournir un token que vous pouvez obtenir en créant un bot sur [BotFather](https://core.telegram.org/bots#botfather).

1. Remplacez `'YOUR_BOT_TOKEN'` par le jeton de votre bot Telegram.

### Démarrage du Bot

Pour démarrer le bot, vous devez créer une instance de la classe `Bot` avec votre jeton de bot Telegram et appeler la méthode `start_loop` :

```python
from telegram_ubot import Bot

bot = Bot('YOUR_BOT_TOKEN')

# Votre code ici

bot.start_loop()
```

### Ajouter des Gestionnaires de Commandes

Vous pouvez ajouter des gestionnaires de commandes pour répondre à des commandes spécifiques envoyées à votre bot. Utilisez le décorateur `@bot.add_command_handler` :

Par exemple, une fonction qui répond "Bienvenue! Comment puis-je vous aider?" lorsque **/start** est envoyé au bot :

```python
@bot.add_command_handler('start')
def start_command(update):
    update.reply("Bienvenue! Comment puis-je vous aider?")
```

### Ajouter des Gestionnaires de Messages

Vous pouvez ajouter des gestionnaires de messages pour répondre à des messages spécifiques correspondant à une expression régulière. Utilisez le décorateur `@bot.add_message_handler` :

Par exemple, une fonction qui répond "Bonjour! Comment ça va?" lorsqu'un message commençant par "Bonjour" est envoyé au bot :

```python
@bot.add_message_handler('^Bonjour')
def greet_handler(update):
    update.reply("Bonjour! Comment ça va?")
```

### Ajouter des Gestionnaires d'Événements Généraux

Vous pouvez ajouter des gestionnaires d'événements généraux pour répondre à tout message reçu par le bot. Utilisez le décorateur `@bot.add_event_handler` :

```python
@bot.add_event_handler()
def handle_all_events(update):
    update.reply('Vous avez envoyé : ' + update.message['text'])
```

### Gestion des Callbacks

Pour gérer les callbacks, utilisez le décorateur `@bot.add_callback_handler`.

```python
@bot.add_callback_handler('button_clicked')
def handle_button_click(update):
    update.reply('Le bouton a été cliqué!')
```

### Ajouter une Conversation à Étapes Multiples

Pour gérer des conversations avec plusieurs étapes, utilisez la classe `Conversation`.

```python
from telegram_ubot import Bot, Conversation

bot = Bot('YOUR_BOT_TOKEN')

conv = Conversation(steps=['STEP1', 'STEP2'])

@conv.add_command_handler('ENTRY', 'start')
def start_conversation(update):
    update.reply('Commencer la conversation.')
    return 'STEP1'

@conv.add_message_handler('STEP1', r'next')
def step1_next(update):
    update.reply('Passer à l\'étape 2.')
    return 'STEP2'

@conv.add_command_handler('STEP2', 'end')
def end_conversation(update):
    update.reply('Terminer la conversation.')
    conv.end()

bot.add_conversation_handler(conv)
bot.start_loop()
```

### Envoyer un Message avec un Clavier Personnalisé

```python
from telegram_ubot import Bot, ReplyKeyboardMarkup, KeyboardButton

bot = Bot('YOUR_BOT_TOKEN')

keyboard = [
    [KeyboardButton('Option 1')],
    [KeyboardButton('Option 2')]
]

@bot.add_command_handler('menu')
def show_menu(update):
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.reply('Choisir une option :', reply_markup=reply_markup)

bot.start_loop()
```

### Envoi et Mise à Jour des Messages

Vous pouvez envoyer des messages et mettre à jour des messages existants en utilisant les méthodes `send_message` et `update_message`.

```python
bot.send_message(chat_id=123456789, text='Message de test')

bot.update_message(chat_id=123456789, message_id=1, text='Message mis à jour')
```

## Utilisation Pratique du Module `telegram_ubot`

### Exemple : Contrôle des Broches de l'ESP32

Voici un exemple de code pour allumer et éteindre une LED connectée à la broche GPIO2.

```python
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
```

### Exemples de Projets de Domotique

Voici deux exemples de projets de domotique utilisant le module `telegram_ubot` pour un bot Telegram avec des `KeyboardButton` et `InlineKeyboardButton`. Ces projets permettent de contrôler des appareils domestiques tels qu'une lumière, un ventilateur, etc., via des boutons interactifs dans Telegram.

#### 1. `main.py` avec `KeyboardButton`

```python
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
```

#### 2. `main.py` avec `InlineKeyboardButton`

```python
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
    update_device_state('

light', 1)
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
```

Ces projets de domotique montrent comment utiliser des `KeyboardButton` et `InlineKeyboardButton` pour contrôler des appareils domestiques avec un bot Telegram en utilisant `telegram_ubot` sur un ESP32. Vous pouvez étendre ces projets pour ajouter plus de fonctionnalités et d'appareils selon vos besoins.

### Utilisation d'une Fonction en Parallèle avec votre Bot

```python
def main(text):
    while True:
        print(text)

bot.start_loop(main, (text,))
```

Si votre fonction a des arguments, passez-les sous forme de tuple.

## Dépannage

- **Problème de connexion à l'API Telegram** : Vérifiez que votre ESP32 est connecté à Internet.
- **Problème d'envoi de messages** : Assurez-vous que vous utilisez le bon jeton de bot et que votre bot n'est pas bloqué par l'utilisateur.
- **Problèmes de performance** : Utilisez `gc.collect()` pour gérer la mémoire et assurez-vous que votre code n'a pas de fuites de mémoire.

## Conclusion

Ce module fournit une interface simple et puissante pour créer des bots Telegram utilisant MicroPython. En suivant les exemples fournis, vous pouvez facilement étendre les fonctionnalités de votre bot et intégrer le contrôle matériel de votre ESP32.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
