import _thread
import gc
import time

import ujson
import ure
import urequests
from machine import Timer


class Bot():
    '''
    Classe de base pour interagir avec l'API Telegram
    '''

    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token
        self.last_update = 0
        self.command_handlers = {}
        self.callback_handlers = {}
        self.message_handlers = {}
        self.conversation_handlers = []
        self.event_handlers = []

        self._get_updates()

    def _get_updates(self):
        '''
        Récupère toutes les mises à jour de l'API Telegram et stocke
        le dernier ID pour la prochaine itération
        '''
        parameters = {
            'offset': self.last_update + 1,
            'timeout': 2,
            'allowed_updates': ['messages']
            }

        try:
            response = urequests.post(self.url + '/getUpdates', json=parameters)
            data = response.json()
            response.close()
            
            if data['result']:
                self.last_update = data['result'][-1]['update_id']  # stockage du dernier ID de mise à jour
                return [Update(self, update) for update in data['result']]

            return None

        except Exception as e:
            print('_get_updates: ', e)
            return None

    def _handle_update(self, update):
        '''
        Fonction qui choisit la bonne fonction pour gérer la mise à jour,
        en fonction des gestionnaires définis précédemment
        '''
        text = update.message['text']

        if update.is_callback:
            self.callback_handlers[update.callback_data](update)

        if text.startswith('/'):  # est une commande
            # obtenir le premier mot (utile pour la future implémentation de commandes avec arguments)
            command = text.split(' ')[0].replace('/', '')
            
            for c in self.conversation_handlers:
                if command in c.steps[c.active][0].keys():
                    next_step = c.steps[c.active][0][command](update)
                    c.go_to_step(next_step)
                    return

            if command in set(self.command_handlers.keys()):
                self.command_handlers[command](update)
                return
        else:
            for c in self.conversation_handlers:
                for expression in c.steps[c.active][1].keys():
                    if ure.match(expression, text):
                        next_step = c.steps[c.active][1][expression](update)
                        c.go_to_step(next_step)
                        return

            for expression in set(self.message_handlers.keys()):
                # gestion des messages
                if ure.match(expression, text):
                    self.message_handlers[expression](update)
                    return

        # Appel des gestionnaires d'événements génériques
        for handler in self.event_handlers:
            handler(update)

    def _read(self):
        '''
        Fonction de lecture principale du bot
        '''
        updates = self._get_updates()
        
        if updates:
            for update in updates:
                self._handle_update(update)
                
        gc.collect()  # au cas où le gc automatique est désactivé
        return

    def _loop(self, period=100):
        while True:
            self._read()

    def start_loop(self, main_function=None, args=(), period=100):
        """
        Fonction principale utilisée pour démarrer le bot dans un autre thread.
        """
        if main_function:
            _thread.start_new_thread(main_function, args)
            
        _thread.start_new_thread(self._loop(), (period,))

    def add_message_handler(self, regular_expression):
        '''
        Décorateur pour ajouter un gestionnaire de messages avec validation regex
        '''

        def decorator(function):
            self.message_handlers[regular_expression] = function

        return decorator

    def add_callback_handler(self, callback_data):
        '''
        Décorateur pour ajouter un gestionnaire de rappel 
        '''

        def decorator(function):
            self.callback_handlers[callback_data] = function

        return decorator

    def add_command_handler(self, command):
        '''
        Décorateur pour ajouter un gestionnaire de commandes, (écrire la commande sans '/' en argument)
        '''

        def decorator(function):
            self.command_handlers[command] = function

        return decorator
        
    def add_conversation_handler(self, conversation):
        '''
        Décorateur pour ajouter un gestionnaire de conversation
        '''
        
        self.conversation_handlers.append(conversation)

    def add_event_handler(self):
        '''
        Décorateur pour ajouter un gestionnaire d'événements génériques
        '''

        def decorator(function):
            self.event_handlers.append(function)

        return decorator

    def send_message(self, chat_id, text, parse_mode='MarkdownV2', reply_markup=None):
        parameters = {
            'chat_id': chat_id,
            'text': text.replace('.', '\.'),
            'parse_mode': parse_mode
        }

        if reply_markup:
            parameters['reply_markup'] = reply_markup.data

        try:
            message = urequests.post(self.url + '/sendMessage', json=parameters)
            assert message
            message.close()

        except Exception:
            print('message non envoyé')

    def update_message(self, chat_id, message_id, text, parse_mode='MarkdownV2', reply_markup=None):
        parameters = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': parse_mode,
        }

        if reply_markup:
            parameters['reply_markup'] = reply_markup.data

        try:
            message = urequests.post(self.url + '/editMessageText', json=parameters)
            print(message.text)
            assert message
            message.close()

        except Exception:
            print('mise à jour non envoyée')
            
            
class Conversation():
    """
    Classe de conversation utilisée pour les conversations à étapes multiples
    
    LES ÉTAPES DOIVENT ÊTRE DÉFINIES À L'INITIALISATION, CHAQUE ÉTAPE PEUT AVOIR PLUSIEURS GESTIONNAIRES
    
    L'ÉTAPE ENTRY EST AJOUTÉE PAR DÉFAUT ET EST UTILISÉE POUR DÉMARRER LA CONVERSATION
    
    chaque fonction utilisée comme gestionnaire doit retourner l'étape suivante de la conversation
    """
    
    def __init__(self, steps: list = []):
        self.END = 0
        self.steps = {
            'ENTRY': [{}, {}]
        }
        self.active = 'ENTRY'
        
        for step in steps:
            self.steps[step] = [{}, {}]
            
    def add_command_handler(self, step, command):
        '''
        Décorateur pour ajouter un gestionnaire de commandes à une étape spécifique,
        (écrire la commande sans '/' en argument)
        '''

        def decorator(function):
            self.steps[step][0][command] = function

            return decorator

    def add_message_handler(self, step, regular_expression):
        '''
        Décorateur pour ajouter un gestionnaire de messages à une étape spécifique,
        avec validation regex
        '''

        def decorator(function):
            self.steps[step][1][regular_expression] = function

        return decorator
        
    def go_to_step(self, step):
        if step == 0:
            self.active = 'ENTRY'
        elif step in self.steps.keys():
            self.active = step
        else:
            print('[ERREUR] Aucune étape nommée {s} définie, restant à l\'étape actuelle'.format(step))

    def end(self):
        self.active = 'ENTRY'


class ReplyKeyboardMarkup():
    '''
    Classe utilisée pour personnaliser reply_markup afin d'envoyer des claviers personnalisés
    '''

    def __init__(self, keyboard, resize_keyboard=False, one_time_keyboard=False, selective=False):
        self.data = {
            'keyboard': [[k.data for k in row] for row in keyboard],
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            'selective': selective
        }

class InlineKeyboardMarkup():
    '''
    Classe utilisée pour personnaliser reply_markup afin d'envoyer des claviers personnalisés
    '''

    def __init__(self, keyboard):
        self.data = {
            'inline_keyboard': [[k.data for k in row] for row in keyboard]
        }


class KeyboardButton():
    '''
    Classe utilisée pour créer des objets de boutons utilisés avec ReplyKeyboardMarkup
    '''

    def __init__(self, text, request_contact=False, request_location=False):
        self.data = {
            'text': text,
            'request_contact': request_contact,
            'request_location': request_location
        }

class InlineKeyboardButton():
    '''
    Classe utilisée pour créer des objets de boutons utilisés avec ReplyKeyboardMarkup
    '''

    def __init__(self, text, url="", callback_data=""):
        self.data = {
            'text': text,
            'url': url,
            'callback_data': callback_data
        }


class Update():
    '''
    Classe avec des méthodes de base pour les mises à jour
    '''

    def __init__(self, b, update):
        self.update_id = update['update_id']
        self.bot = b
        self.is_callback = False
        self.callback_data = ""
        try:
            if update['callback_query']:
                print("EST UN CALLBACK")
                self.is_callback = True
                self.message = update['callback_query']['message']
                self.callback_data = update['callback_query']['data']
        except KeyError as e:
            print("Pas un Callback")
            self.message = update['message']

    def reply(self, text, parse_mode='MarkdownV2', reply_markup=None):
        self.bot.send_message(self.message['chat']['id'], text, parse_mode=parse_mode, reply_markup=reply_markup)

    def edit(self, text, parse_mode='MarkdownV2', reply_markup=None):
        self.bot.update_message(self.message['chat']['id'], self.message['message_id'], text, parse_mode=parse_mode, reply_markup=reply_markup)

