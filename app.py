from flask import Flask, render_template, session, request, redirect, url_for
# render_template renderizar html,
# session criar sessão
# request serve para a função saber se vai usar o método get ou post
# redirect vai verificar se a sessão é válida
# urk_for chama as funções definidas

#imports das valicações de campos
from  model.validacao import idioma
from  model.validacao import validacaoSenha
from  model.validacao import validaçãoNome
from  model.validacao import  validacaoVardadeiraOUFalsa
from  model.validacao import  validacaoVardadeiraOUFalsaParaBD

#imports para os comando do banco de dados
from model.bd import verificaCadastro
from model.bd import cadastrado
from model.bd import loginBD
from model.bd import alterarEmail
from model.bd import alteraSenha
from model.bd import deletar
from model.bd import historicoBD
from model.bd import salvandoNoticia
from model.bd import esqueceuSenha

#importe para predicao
from model.predicao import predicaoRegressãoLogistica
from model.predicao import predicaoSVM
from model.predicao import predicaoMLP
from model.predicao import tamanho

#importe de e-mail
from model.envioEmail import enviar_email

#Conexão ao banco
from flask_mysqldb import MySQL 
import MySQLdb.cursors 



app = Flask(__name__)
 

#dados do banco
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'detectorFakeNews'

app.secret_key = 'criar_Uma_Chave'




mysql = MySQL(app)

@app.route("/", methods=['POST', 'GET'])
def home():  
      
    return render_template("home.html", usuario=session.get('nome')),200

@app.route("/cadastro", methods=['POST', 'GET'])
def cadastro():
    msg=''
    if(session.get('loggedin') == True):       
       return render_template("home.html")
    elif request.method == 'POST':        
        #criando variáveis e pegando valores do for
        nome = request.form['nomeCadastro']
        senha = request.form['senhaCadastro']
        senhaNovamente = request.form['senhaCadastroNovamente'] 
        email = request.form['emailCadastro']
        #fazendo verificações dos capos digitados
        if verificaCadastro(email):
            msg="E-mail já cadastrado"
        elif validaçãoNome(nome)==False:
            msg='Nome de usuário não pode conter números'
        elif validacaoSenha(senha)==False:
            msg='Senha não atende aos requisitos mínimos'
        elif senha != senhaNovamente:
            msg = 'Senha diferentes digitadas'        
        else: 
            cadastrado(nome, email, senha)
            msg = 'Conta registrada'          
            return render_template('home.html', msg=msg)      
    return render_template('home.html', msg=msg) 
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    msg = '' 
    #verificando se há sessão
    if(session.get('loggedin') == True):
       return render_template("home.html")    
    elif request.method == 'POST':
        #criando variáveis pelo form 
        email = request.form['emailLogin'] 
        senha = request.form['senhaLogin']
        if loginBD(email, senha):
            return redirect(url_for('home'))       
        else: 
           msg = 'E-mail/Senha não encontrados!'
    return render_template('home.html', msg=msg)
    

@app.route("/alterarEmail", methods=['POST', 'GET'])
def alterar_email():
    if(session.get('loggedin') == False):
        return render_template('home.html')
    #criando variáveis pelo form
    elif request.method == 'POST':
        emailSession = session.get('email')
        emailAtual = request.form['emailAntigo']    
        emailNovo = request.form['emailNovo']
       
       
        if emailAtual and emailNovo: #verifica se os campos foram digitados           
            if alterarEmail(emailSession, emailAtual, emailNovo):
                msg = 'E-mail alterado com sucesso'
                return render_template('alterar_email.html', msg=msg, usuario=session.get('nome'))
            else:
                msg = 'E-mail não correspondente'
                return render_template('alterar_email.html', msg=msg, usuario=session.get('nome'))                
    return render_template("alterar_email.html", usuario=session.get('nome'))

@app.route("/alterarSenha", methods=['POST', 'GET'])
def alterar_senha():
    if(session.get('loggedin') == False):
        return render_template('home.html')
    #criando variáveis pelo form
    elif request.method == 'POST':
        emailSession = session.get('email')
        senhaSession = session.get('senha')
        senhaAtual = request.form['senhaAntiga']
        emailSenha = request.form['emailSenha']
        senhaNova = request.form['senhaNova']        
        if emailSenha and senhaAtual and senhaNova:  #verifica se ps campos foram digitados          
            if(alteraSenha(emailSession,  emailSenha, senhaSession, senhaAtual, senhaNova)):
                msg = 'Senha alterada com sucesso'            
                return render_template('alterar_senha.html', msg=msg, usuario=session.get('nome'))
            else:
                msg = 'Senha ou E-mail não correspondente'
                return render_template('alterar_senha.html', msg=msg, usuario=session.get('nome'))     
    return render_template("alterar_senha.html", usuario=session.get('nome')) 

@app.route("/deletar", methods=['POST', 'GET'])
def deletar():
    if(session.get('loggedin') == False):
        return render_template('home.html')
    #criando variáveis pelo form
    elif request.method == 'POST':
        emailSession = session.get('email')
        senhaSession = session.get('senha')
        email = request.form['emailDel'] 
        senha = request.form['senhaDel']
        if deletar(emailSession, email, senhaSession, senha): # se existir           
            msg = 'Conta deletada com sucesso'            
            return render_template('home.html', msg=msg, usuario=session.get('nome'))
        else:          
            msg = 'Dados incorretos'
            return render_template("deletar.html", msg=msg, usuario=session.get('nome')) 
    return render_template("deletar.html", usuario=session.get('nome'))    
   

@app.route("/historico", methods=['POST', 'GET'])
def historico():
    
    if(session.get('loggedin') == True):
                     
            return  render_template("historico.html", resultado = historicoBD(), usuario=session.get('nome'))
    return render_template("home.html")

@app.route('/sair', methods=['POST', 'GET'])
def sair_sessao():          
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('nome', None)
    session.pop('email', None)
    session.pop('senha', None)
    session.pop('idEnvio', None)
    session.pop('email', None)
    session.pop('ativo', None) #  saindo da sessão     
    return redirect(url_for('login'))

@app.route('/esqueceu_senha', methods=['POST', 'GET'])
def esqueceu_senha():     
    if(session.get('loggedin') == True):
        return redirect(url_for('home'))
    if request.method == 'POST':
        #capturando dados do form
        emailCadastrado = request.form['emailCadastrado']
        #Verifica se e-mail está cadastrado
        if verificaCadastro(emailCadastrado)== False:
            msg = 'E-email não está cadastrado'
            return render_template('esqueceu_senha.html', msg=msg)
        enviar_email(emailCadastrado)
        msg = 'Verifique seu e-mail'
        return render_template('esqueceu_senha.html', msg=msg)           
    return render_template('esqueceu_senha.html')

@app.route('/mudar_senha', methods=['POST', 'GET'])
def mudar_senha():
   if( session.get('loggedin') == True):
        return redirect(url_for('home'))   
   if request.method == 'POST':
       senhaNova = request.form['senhaNova']
       if validacaoSenha(senhaNova) == False:
            msg='Senha não atende aos requisitos mínimos'
            return render_template('mudar_senha.html', msg=msg)
       email = session.get('esqueceu')
       esqueceuSenha(email, senhaNova)
       return render_template('home.html') 
   return render_template('mudar_senha.html') 
    
@app.route('/analisando', methods=[ 'POST', 'GET'])
def analisando():

    # Pegando o texto dos forms
    noticia = request.form["areaNoticia"] 
    if tamanho(noticia) ==False:
        msg='notícia com menos de 50 caracteres'
        return render_template('home.html', msg=msg)
    if idioma(noticia):
        msg='notícia não está em língua portuguesa'
        return render_template('home.html', msg=msg)

    # Fazendo previsão do texto 
    previsaoRegressaoLogistica= predicaoRegressãoLogistica(noticia)
    previsaoSVM= predicaoSVM(noticia)
    previsaoMLP= predicaoMLP(noticia)

    #salvar resultado TRUE ou FAKE
    salvarResultado = validacaoVardadeiraOUFalsaParaBD(previsaoRegressaoLogistica, previsaoSVM, previsaoMLP )

    #variável para receber mensagem que aparecerá na tela
    msg = validacaoVardadeiraOUFalsa(previsaoRegressaoLogistica,previsaoSVM,previsaoMLP )

    #Salvando notícia no BD
    salvandoNoticia(noticia,salvarResultado )

   
   
    return render_template('home.html', msg= msg, resultado = salvarResultado,  usuario=session.get('nome'))








