#LUIS LOSCOS FABREGAT
#TRABAJO DE FIN DE GRADO EN INGENIERÍA INFORMÁTICA DE UNIR

###ESTE PROGRAMA EJECUTA UN JUEGO CREADO CON BOTONES Y NUMEROS EN EL QUE HAY
###QUE ADIVINAR UN NUMERO ENTRE 1 Y 10, MIENTRAS NO LO ADIVINES TE VA DANDO PISTAS.
###OFRECE AYUDA CON EL COMANDO "/ayuda" Y PARA JUGAR EL COMANDO "/jugar"


from config import * #importamos el token
import telebot #para manejar la API de Telegram
from telebot.types import ReplyKeyboardMarkup  #para crear botones
from telebot.types import ReplyKeyboardRemove  #para eliminar botones
from random import randint #para generar numeros enteros aleatorios

#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#variable global donde guardaremos los datos del usuario
usuarios = {}

#responde al comando /start /ayuda /help
@bot.message_handler(commands=["ayuda"])
def cmd_start(message):
    #muestra el modo de uso del bot
    botones = ReplyKeyboardRemove()  #para eliminar los posibles botones
    bot.send_message(message.chat.id, "Usa el comando /jugar para empezar", reply_markup=botones)
    
@bot.message_handler(commands=["jugar"])
def cmd_jugar(message):
    #Inicia el juego
    numero = randint(1,10)
    cid = message.chat.id 
    usuarios[cid] = numero
    botones = ReplyKeyboardMarkup(input_field_placeholder="Pulsa un botón", row_width = 5)
    botones.add('1','2','3','4','5','6','7','8','9','10')
    msg = bot.send_message(message.chat.id, "Adivina el número entre 1 y 10", reply_markup=botones)
    #registramos la respuesta en la función indicada
    bot.register_next_step_handler(msg, comprobar_numero)
    
def comprobar_numero(message):   
    #comprobar si el numero es correcto
    cid = message.chat.id 
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "ERROR: Introduce un número")
        bot.register_next_step_handler(msg, comprobar_numero)
    
    else:
        n = int(message.text)
        if n < 1 or n > 10:
            msg = bot.send_message(message.chat.id, "ERROR: Número fuera de rango")
            bot.register_next_step_handler(msg, comprobar_numero)
            
        else:
            if n == usuarios[cid]:
                markup = ReplyKeyboardRemove()
                bot.reply_to(message, "¡¡Enhorabuena, has acertado!!", reply_markup=markup)
                return
            
            elif n > usuarios[cid]:
                msg = bot.reply_to(message, "Pista: es MENOR")
                bot.register_next_step_handler(msg, comprobar_numero)
                
            else:
                msg = bot.reply_to(message, "Pista: es MAYOR")
                bot.register_next_step_handler(msg, comprobar_numero)
                
                
                
            
# MAIN ###############################
if __name__ == '__main__':
    print("Iniciando el BOT") 
    #bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()                    
    
    
    
    
    