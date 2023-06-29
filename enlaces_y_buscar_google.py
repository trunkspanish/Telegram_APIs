#LUIS LOSCOS FABREGAT
#TRABAJO DE FIN DE GRADO EN INGENIERÍA INFORMÁTICA DE UNIR

###ESTE PROGRAMA TIENE DOS COMANDOS, "/botones" QUE CREA UNOS CUANTOS BOTONES
###CON ENLACES A PAGINAS WEB DE INTERES, Y EL COMANDO "/buscar (lo que sea)"
###QUE PERMITE BUSCAR EN GOOGLE LO QUE PONGAS A CONTINUACIÓN DE "/buscar"
###MOSTRANDOTE LOS 25 PRIMEROS ENLACES DE GOOGLE 


from config import * #importamos el token
import telebot #para manejar la API de Telegram
#botones inline
from telebot.types import InlineKeyboardMarkup #para crear botonera inline
from telebot.types import InlineKeyboardButton #para definir botones inline
import requests
from bs4 import BeautifulSoup

N_RES_PAG = 25 #numero de resultados a mostrar

#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al comando /botones
@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    #muestra mensaje con botones inline (a continuacion del mensaje)
    markup = InlineKeyboardMarkup(row_width= 2) #numero de botones por fila
    b1 = InlineKeyboardButton("Amazon", url= "https://www.amazon.es/")
    b2 = InlineKeyboardButton("Xataka", url= "https://www.xataka.com/")
    b3 = InlineKeyboardButton("Ebay", url= "https://www.ebay.es/")
    b4 = InlineKeyboardButton("Unir", url= "https://www.unir.net/")
    b5 = InlineKeyboardButton("Wallapop", url= "https://es.wallapop.com/")
    b6 = InlineKeyboardButton("Wikipedia", url= "https://es.wikipedia.org/wiki/Wikipedia:Portada")
    b7 = InlineKeyboardButton("K77 Revista de coches", url= "https://www.km77.com/")
    b8 = InlineKeyboardButton("Aliexpress", url= "https://es.aliexpress.com/?gatewayAdapt=Msite2Pc")
    b9 = InlineKeyboardButton("Youtube", url= "https://www.youtube.com/")
    b10 = InlineKeyboardButton("Facebook", url= "https://es-es.facebook.com/")
    b_cerrar = InlineKeyboardButton("CERRAR", callback_data="cerrar")
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b_cerrar)
    bot.send_message(message.chat.id, "Páginas Web de Interés >>", reply_markup=markup)
    

@bot.callback_query_handler(func=lambda x: True)
def respuesta_botones_inline(call):
    #gestiona las acciones de los botones callback_data
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "cerrar":
        bot.delete_message(cid, mid)

            
#responde al comando buscar
@bot.message_handler(commands=['buscar'])
def cmd_buscar(message): 
    #realiza una busqueda en Google y devuelve una lista de resultados
    texto_buscar = " ".join(message.text.split()[1:])
    #si no se han pasado parametros
    if not texto_buscar:
        texto = 'Debes introducir una busqueda.\n'
        texto+= 'Ejemplo:\n'
        texto+= f'<code>{message.text} gatos</code>'
        bot.send_message(message.chat.id, texto, parse_mode='html')
        return 1
    
    #si se ha indicado un texto de busqueda
    else:
        print(f'Buscando en Google: {texto_buscar}"')
        url = f'https://www.google.es/search?q={texto_buscar.replace(" ","+")}&num=100'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        headers = {"user-agent": user_agent}
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code != 200:
            print(f'ERROR al buscar: {res.status_code}{res.reason}')
            bot.send_message(message.chat.id, "Se ha producido un error. Inténtalo más tarde")
            return 1
        
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            elementos = soup.find_all("div", class_='g')
            lista = []
            
            for elemento in elementos:
                try:
                    titulo=elemento.find("h3").text
                    url = elemento.find("a").attrs.get("href")
                    
                    if not url.startswith("http"):
                        url = "https://www.google.es/" + url
                        
                    if [titulo, url] in lista:
                        continue
                    lista.append([titulo, url])
                    
                except:
                    continue                    
        mostrar_pagina(lista, message.chat.id)                
            
    
def mostrar_pagina(lista, cid, pag=0, mid=None): 
#crea o edita un mensaje de la pagina
    #creamos la botonera
    markup = InlineKeyboardMarkup()
    b_cerrar = InlineKeyboardButton("❌", callback_data="cerrar")
    inicio = pag * N_RES_PAG  #numero resultado inicio de pagina en curso
    fin = inicio+N_RES_PAG #numero resultado fin de pagina en curso
    markup.row(b_cerrar)
    mensaje = f'<i>Mostrando los 25 primeros resultados en Google</i>\n\n'
    n = 1
    
    for item in lista[inicio:fin]:
        mensaje+= f'[<b>{n}</b>] <a href="{item[1]}">{item[0]}</a>\n'
        n+= 1
        
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
    else:
        bot.send_message(cid, mensaje, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
    
        
    
    
    
# MAIN ###############################
if __name__ == '__main__':
    print("Iniciando el BOT") 
    #bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()       