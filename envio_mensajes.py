#LUIS LOSCOS FABREGAT
#TRABAJO DE FIN DE GRADO EN INGENIERÍA INFORMÁTICA DE UNIR

###ESTE PROGRAMA EJECUTA UNA SERIE DE ACCIONES EN EL BOT DE TELEGRAM
###SI ESCRIBIMOS EN EL BOT "/ayuda" nos muestra un mensaje
###SI ESCRIBIMOS "/(cualquier cosa)" NOS DARÁ UN ERROR DE COMANDO NO DISPONIBLE
###SI ESCRIBIMOS "mensaje" NOS MUESTRA UN MENSAJE, LO EDITA Y LO BORRA
###SI ESCRIBIMOS "imagen" NOS CARGA UN IMAGEN
###SI ESCRIBIMOS "documento" NOS SUBE UN DOCUMENTO PDF
###SI ESCRIBIMOS "video" NOS MUESTRA UN VIDEO
###SI ESCRIBIMOS "canal" ENVIA UN MENSAJE AL CANAL QUE INDICADO
###SI ESCRIBIMOS "usuario" ENVIA UN MENSAJE AL USUARIO QUE INDICADO
###SI ESCRIBIMOS "(cualquier cosa)" NOS DARÁ UN ERROR DE ACCIÓN NO DISPONIBLE


from config import * #importamos el token
import telebot #para manejar la API de Telegram
import time
import threading

#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al comando /ayuda
@bot.message_handler(commands=["ayuda"])
def cmd_start(message):
#da la bienvenida al usuario del bot
    bot.reply_to(message, "Hola, que tal estás, en que puedo ayudarte?")
    print(message.chat.id)

#responde a los mensajes de texto que no son comandos
@bot.message_handler(content_types=["text"])  
def bot_mensajes_texto(message):
        #gestiona los mensajes de texto recibidos
        if message.text.startswith("/"):
            bot.send_message(message.chat.id, "Comando no disponible")
            
        elif message.text == "mensaje":    
            #envia mensaje, lo edita y luego lo borra
            m = bot.send_message(message.chat.id, "<b>VAMOS A EDITAR Y BORRAR ESTE TEXTO</b>", parse_mode="html")
            time.sleep(3)
            bot.edit_message_text("<u>ADIOS</u>",message.chat.id, m.message_id,parse_mode="html")
            time.sleep(3)
            bot.delete_message(message.chat.id, m.message_id)
            
        elif message.text == "imagen":            
            #envia imagen
            foto = open("./imagenes/maradona.png", "rb")
            bot.send_photo(message.chat.id, foto, "LA MANO DE DIOS")

        elif message.text == "documento":
            #envia documento
            documento = open("./docs/guia.pdf", "rb")
            bot.send_document(message.chat.id, documento, caption="GUIA TFG")
        
        elif message.text == "video":          
            #envia video
            bot.send_chat_action(message.chat.id, "upload_video")
            video = open("./videos/perro.mp4", "rb")
            bot.send_document(message.chat.id, video, caption="perrito")
            
        elif message.text == "canal":          
            #envia mensaje al canal   
            bot.send_message(CANAL_CHAT_ID, "Saludos al Canal")
        
        elif message.text == "usuario":          
             #envia mensaje al usuario   
             bot.send_message(MI_CHAT_ID, "Hola Luis, ¿qué tal?")  
              
        else:  
            bot.send_message(message.chat.id, "No hay ninguna acción disponible")


def recibir_mensajes():
        #bucle infinito que comprueba si hay nuevos mensajes en el bot
        bot.infinity_polling()

            
            
# MAIN ###############################
if __name__ == '__main__':
    print("Iniciando el BOT")    
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print("Bot iniciado")


  