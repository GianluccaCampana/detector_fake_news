from flask import Flask, session, render_template
#Conexão ao banco
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
#import de validação de senha
from model.validacao import validacaoSenha
#iport criptogradis 
from model.criptografia import  criptografar



app = Flask(__name__)


#dados do banco
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'detectorFakeNews'


mysql = MySQL(app)


def verificaCadastro(email):
    #conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #verificando se usuário já existe
    cursor.execute('SELECT * FROM usuario WHERE email = % s', (email, ))
    account = cursor.fetchone() #guarda resultado encontrado
    if account: #caso já exista o cadastro do e-mail
        cursor.close() #fechar conexão com o banco
        return True
    cursor.close() #fechar conexão com o banco
    return False

def cadastrado(nome, email, senha):
    senhaCriptografada = criptografar(senha)
    #conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     #executando comando de inserção
    cursor.execute('INSERT INTO usuario(nome, senha, email) VALUES (% s, % s, % s)', (nome, senhaCriptografada, email, )) 
    mysql.connection.commit() #gravando a informação no banco
    cursor.close()
    
def loginBD(email,senha):
    senhaCriptografada = criptografar(senha)
    #Conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #Verificando cadastro pelo e-mail e senha
    cursor.execute('SELECT * FROM usuario WHERE email = % s AND senha = % s', (email, senhaCriptografada, )) 
    account = cursor.fetchone()  #Capturando o primeiro resultado
    if account: # se existir
        #criando sessões 
        session['loggedin'] = True
        session['id'] = account['id_usuario'] 
        session['nome'] = account['nome']
        session['email'] = account['email']
        session['senha'] = account['senha']
        cursor.close() #fechando conexão            
        return True
    cursor.close() #fechando conexão      
    return False    

def alterarEmail(emailSession, emailAtual, emailNovo):
    #Conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if emailSession == emailAtual : #verificando se o e-mail da conta em uso é o mesmo que foi digitado               
        cursor.execute('UPDATE usuario SET email = % s WHERE email= % s',(emailNovo, emailAtual))
        mysql.connection.commit() #Registra o Update
        session['email'] = emailNovo  #atualizando a sessão        
        cursor.close() #fechando conexão
        return True
    else:
        cursor.close()
        return False

def alteraSenha(emailSession,  emailSenha, senhaSession, senhaAtual, senhaNova):
    senhaCriptografada = criptografar(senhaAtual)
    senhaNovaCriptografada = criptografar(senhaAtual)
    if emailSession == emailSenha and senhaSession == senhaCriptografada: #verificando se o e-mail e a senha da conta em são os mesmos que foram digiados
       
        #Conectando ao banco
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE usuario SET senha = % s WHERE email= % s AND senha = % s',(senhaNovaCriptografada, emailSenha, senhaAtual, ))
        mysql.connection.commit() #Registra o Update
        session['senha'] = senhaNova #atualizando a sessão
        cursor.close() #fechando conexão
        return True
    return False

def esqueceuSenha(email, senhaNova):
    senhaCriptografada = criptografar(senhaNova)
     #Conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE usuario SET senha = % s WHERE email= % s',(senhaCriptografada, email, ))
    mysql.connection.commit() #Registra o Update
    session.pop('esqueceu', None) #  saindo da sessão
    session.pop('ativo', None) #  saindo da sessão
    cursor.close() #fechando conexão
    return True

def deletarConta(emailSession, email, senhaSession, senha):
    senhaCriptografada = criptografar(senha)
    id_usuario = session.get('id')
    if emailSession == email and senhaSession == senhaCriptografada: #verificando se o e-mail e a senha da conta em são os mesmos que foram digiados
        #Conectando ao banco
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #exluindo registro 
        cursor.execute('DELETE FROM noticia WHERE id_usuario = % s ',(id_usuario, ))
        cursor.execute('DELETE FROM usuario WHERE email = % s AND senha  = % s',(email, senhaCriptografada, ))
        mysql.connection.commit() #Registra o DELETE
        cursor.close() #fechando conexão
        #finalizando sessão
        session.pop('loggedin', None) 
        session.pop('id', None) 
        session.pop('nome', None)
        session.pop('email', None)
        session.pop('senha', None)
        return True
    return False

def historicoBD():
    #Conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id_usuario = session.get('id')
    cursor.execute('SELECT id_noticia,substring(noticia, 1, 50) AS "titulo", noticia, resultado, data_analise FROM noticia WHERE id_usuario = % s ORDER BY data_analise desc',(id_usuario, ))
    resultado = cursor.fetchall()
    cursor.close() #fechar conexão com o banco
    return  resultado

def salvandoNoticia(noticia, previsao):
    #Conectando ao banco
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #Salvando no banco
    cursor.execute('INSERT INTO noticia(id_usuario, noticia, resultado) VALUES (% s, % s, % s) ORDER BY data_analise desc', (session.get('id'), noticia, previsao, )) 
    mysql.connection.commit() #gravando a informação no banco     
    cursor.close() #fechar conexão com o banco

 