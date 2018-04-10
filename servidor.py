#-*- coding: utf-8 -*-

#Codificado por : Ítalo Magalhães da Silva
#E-mail : italo.ufsj@gmail.com

import socket
import os
import sys
    

class Servidor():

    #Construtor da Classe
    def __init__(self,endereco,porta):
        self.host=endereco
        self.port=porta
    
    def retornarGET(self,objeto,caminho,con):
        try:
            #Verifica se objeto solicitado é a página Raiz ou seja index.html
            if objeto == '/':
                #concatena caminho da pasta onde ta servidor com arquivo ou página solicitada
                f=open(caminho+'/index.html','r')
                aux =f.read()
                #Pega informaçoes da página solicitada
                response_headers = {
                'Content-Type': 'html; encoding=utf8',
                'Content-Length': len(aux),
                'Connection': 'close',
                }
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
                print response_headers_raw
                response_proto = '\nHTTP/1.1'
                response_status = 200
                response_status_text = ' OK'
                #retorna mensagem pro browser
                con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)
            else:
                #Se não for página raiz pega o objeto solicitado
                f=open(caminho+objeto,'r')
                aux =f.read()
                response_headers = {
                'Content-Type': 'html; encoding=utf8',
                'Content-Length': len(aux),
                'Connection': 'close',
                }
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
                response_proto = '\nHTTP/1.1'
                response_status = 200
                response_status_text = ' OK'
                #retorna mensagem pro browser
                con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)
        except IOError:
            #caso não encontre o arquivo que não existe servidor
            response_proto = '\nHTTP/1.1'
            response_status = 404
            response_status_text = ' File not Found'

            f=open(caminho+'/404ERROR.html','r')
            aux =f.read()
            response_headers = {
            'Content-Type': 'html; encoding=utf8',
            'Content-Length': len(aux),
            'Connection': 'close',
            }
            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
            con.send('%s %s %s' % (response_proto, response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)

        
    
    def iniciarServidor(self):
        #Cria um objeto socket, as duas constantes são:
        #AF_INET = Protocolo de endereço de IP
        #SOCK_STREAM = Protocolo de transferencia TCP
        #Assim cria um server TCP/IP        
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        #Vincula servidor ao Host e a porta
        servidor_socket.bind((self.host,self.port))        
        
        #limita a uma conexão
        servidor_socket.listen(10)
        while True:
            print 'Aguardando conexao\n' 
            #Aceita uma nova conexão quando encontrada 
            #e devolve um novo socket com a conexão e o endereço do cliente encontrado  
            con, cliente = servidor_socket.accept()            
            #Iniciar as threads para cada usuário conectado
            pid = os.fork()
            if pid == 0:
                servidor_socket.close()

                #Recebe dados do cliente ou seja mensagens  
                print ('Servidor conectado por: ',cliente)
                print '\n'
                #Recebe dados do cliente ou seja as mensagens
                mensagem = con.recv(1048576)
                
                if not mensagem: break
                
                #Mostra o cabeçalho da mensagem enviada pelo cliente(browser)
                print mensagem

                #Pega toda mensagem é quebra os espaços brancos para verificar se o cliente(browser) mandou um GET
                nomeArquivo=mensagem.split(' ')

                #Caso encontre o GET procura pela página ou arquivo solicitado    
                if nomeArquivo[0] == "GET":
                    self.retornarGET(nomeArquivo[1],RaizDocumento,con)
                else:
                    con.send('Comando GET nao solicitado\n')
                    print 'Finalizando conexao do cliente', cliente
                    con.close()
                    ssys.exit(0)
            else:
                con.close()

if __name__ == "__main__":

    #Define Raiz dos Documentos
    RaizDocumento = "%s/arquivos" % os.path.realpath(os.path.dirname(__file__))
    
    print 'Endereco e Porta não informados - Definidos por padrão (ENDERECO="l27.0.0.1", PORTA=8080")\n'
    endereco = '19.168.1.178'
    porta = 6500
    myServidor = Servidor(endereco, porta)

    myServidor.iniciarServidor()