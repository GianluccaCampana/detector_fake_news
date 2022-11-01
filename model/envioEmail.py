from flask import Flask, session
import smtplib
import  email.message

from datetime import timedelta 
#colocar tempo nas sessões

app = Flask(__name__)




def enviar_email(para):
    
    session['esqueceu'] = para
    session['ativo'] = True

    corpo_email = """
    <form action="http://127.0.0.1:5000/esqueceu_senha">
        <p>Para alterar a senha clique no botão:
        <input type="submit" value="ir para alterar senha" />
    </form>
    """

    msg = email.message.Message()
    msg['Subject'] = 'Assunto'
    msg['From'] = 'detectorfakenews2022@gmail.com'
    msg['To'] = para
    password = 'mwnjjbqwbeudbgni'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


    
