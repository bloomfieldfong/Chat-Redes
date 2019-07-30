import sys
import logging
import getpass
import sleekxmpp
from optparse import OptionParser
from sleekxmpp.exceptions import IqError, IqTimeout
from opciones import*
   

class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, opcion):

        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        #Evento de login y registro
        if (opcion == '1'):
            self.add_event_handler("session_start", self.start)
        elif(opcion == '2'):
            self.add_event_handler("register", self.register)
        
        self.add_event_handler("message", self.message)

    #Procesa el evento session_start
    def start(self, event):
        print('Session start')
        self.send_presence()
        self.get_roster()
        

    #Procesa los mensajes entrantes 
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Se envio\n%(body)s" % msg).send()
            print(msg)
    

if __name__ == '__main__':

    inicio()
    x = input("Ingrese la opcion que desea realizar:\n")
    optp = OptionParser()

    #Opciones de output
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    #Opciones de JID y password .
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    #Setear el login
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    
    #Setup de mi clase EchoBot
    xmpp = EchoBot(opts.jid, opts.password, x)
    
    #plugins de registro
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration
    xmpp['xep_0077'].force_registration = False

  
            
    #Conexion con el server
    if xmpp.connect():
        
        xmpp.process(block=False)
        print("Done")
        while(True):
            menu()
            menu_opcion = input("Ingrese la opcion que desea realizar: \n")

            #Nos da los contactos que tenemos que estan en linea
            if(menu_opcion == '1'):
                print("\nContacts:")
                print(xmpp.client_roster)
                print("")

            ##Mensaje a un usuario 
            elif(menu_opcion == '2'):
                user= input("Usuario a quien desea enviar mensaje: ")
                message = input("Mensaje:")
                print("Enviando mensaje")
                xmpp.send_message(mto= user, mbody = message, mtype = 'chat')
                print("Su mensaje fue enviado exitosamente\n")

            ##Agregar usuario 
            elif(menu_opcion == '3'):
                user = input("Ingrese el nombre del usuario que desea agregar: \n")
                xmpp.send_presence(pto = user, ptype ='subscribe')

            ##Mensaje grupal
            elif(menu_opcion == '4'):
                print("Contacts:")
                print(xmpp.client_roster+'\n')

            ##Desconectarme
            elif(menu_opcion == '5'):
                print("Contacts:")
                print(xmpp.client_roster+'\n')

            ##Mostrar detalles de contacto 
            elif(menu_opcion == '6'):
                print("Contacts:")
                print(xmpp.client_roster+'\n')

            ##Definir nuestro mensaje de preferencia
            elif(menu_opcion == '7'):

                x = input("Que mensaje e gustaria mostrar?")
                y = input("Cual es su mensaje de preferencia?")
                xmpp.makePresence(pfrom = xmpp.jid, pstatus =x, pshow = y)
            
            ##Eliminar mi cuenta
            elif(menu_opcion == '8'):
                yes = input("Esta seguro de que quiere eliminar su cuenta? (si/no)")

                if(yes == 'si')
                    xmpp.remove_user()
                    xmpp.disconect()
                    break
                else:
                    menu()
                    print("")
            ##regresar al menu principal    
            elif(menu_opcion == '0'):   
                menu()
                print("")
    else:
        print("Unable to connect.")

    
