#LUIS LOSCOS FABREGAT
#TRABAJO DE FIN DE GRADO EN INGENIERÍA INFORMÁTICA DE UNIR

###ESTE PROGRAMA MUESTRA AYUDA CON EL COMANDO "/ayuda"
###CON EL COMANDO "/registar" TE PREGUNTA DATOS, LOS ALMACENA Y LOS MUESTRA


from config import * #importamos el token
import telebot #para manejar la API de Telegram
from telebot.types import ReplyKeyboardMarkup  #para crear botones
from telebot.types import ForceReply  #para citar un mensaje
from telebot.types import ReplyKeyboardRemove  #para eliminar botones


#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#variable global donde guardaremos los datos del usuario
usuarios = {}

#responde al comando /ayuda
@bot.message_handler(commands=["ayuda"])
def cmd_start(message):
    #muestra los comandos disponibles
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "usa el comando /registrar para introducir los datos", reply_markup=markup)
        
#responde al comando /
@bot.message_handler(commands=["registrar"])
def cmd_alta(message):
    #pregunta el nombre al usuario
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Cómo te llamas?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)
    
def preguntar_edad(message):
    #preguntar edad del usuario
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"] = message.text
    markup = ForceReply()   
    msg = bot.send_message(message.chat.id, "¿Cuántos años tienes?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)
    
def preguntar_sexo(message):  
    #preguntar sexo del usuario
    if not message.text.isdigit():
        #informamos del error y volvemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un número.\n¿Cuántos años tienes?")
        bot.register_next_step_handler(msg, preguntar_sexo)
        
    else: #si se introdujo la edad correctamente
        usuarios[message.chat.id]["edad"] = int(message.text)
        #definimos dos botones
        markup =  ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa un botón", resize_keyboard=True)  
        markup.add("Hombre", "Mujer")
        msg = bot.send_message(message.chat.id, "¿Cuál es tu sexo?", reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos_usuario)
        
def guardar_datos_usuario(message):
#guardamos datos del usuario    
    #si el sexo introducido no es válido
    if message.text != "Hombre" and message.text != "Mujer":    
        #informamos del error y volvemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Sexo no válido\nPulsa un botón")
        bot.register_next_step_handler(msg, guardar_datos_usuario)   
        
    else:
        usuarios[message.chat.id]["sexo"] = message.text        
        texto = "Datos introducidos\n"
        texto+= f"<code>NOMBRE:</code> {usuarios[message.chat.id]['nombre']}\n"
        texto+= f"<code>EDAD..:</code> {usuarios[message.chat.id]['edad']}\n"
        texto+= f"<code>SEXO..:</code> {usuarios[message.chat.id]['sexo']}\n"
        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
        print(usuarios)
        del usuarios[message.chat.id]
        
    
# MAIN ###############################
if __name__ == '__main__':
    print("Iniciando el BOT") 
    #bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()    