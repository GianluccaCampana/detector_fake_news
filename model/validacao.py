import re #expressão regular
from langdetect import detect #import para detecção da lígua do texto


#identificando a lingua e só permitindo texto em língua portuguesa
def idioma(texto):
    analise = detect(texto)
    result = analise
    if result != 'pt':
        return True
    return False      

#Verifica se atendo todos os requisitor(letras maiúsculas e minúsculas, tenha números e pelo menos 8 caracteres)
def validacaoSenha(senha):
    if not re.match("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])", senha):    
        return False    
    elif  len(senha) <8:
       return False
    return True  

#Não permite nome que tenha números 
def validaçãoNome(nome):
    if re.match(r'[0-9]+', nome):
        return False
    return True    

def validacaoVardadeiraOUFalsa(regressaoLog, svm, mlp):
    if regressaoLog == 'TRUE' and  svm == 'TRUE' and mlp == 'TRUE':
        return 'Todos os 3 algoritmos indentificarão a notícia como verdadeira, mas faça uma pesquisa antes de divulgar ela'
    elif regressaoLog == 'TRUE' and  svm == 'TRUE' and mlp == 'FAKE':
        return '2 dos 3 (Regressão logística e SVM )algoritmos indentificarão a notícia como verdadeira, mas faça uma pesquisa antes de divulgar ela'
    elif regressaoLog == 'TRUE' and  svm == 'FAKE' and mlp == 'TRUE':
        return '2 dos 3 (Regressão Logística e MLP) algoritmos indentificarão a notícia como verdadeira, mas faça uma pesquisa antes de divulgar ela'
    elif regressaoLog == 'FAKE' and  svm == 'TRUE' and mlp == 'TRUE':
        return '2 dos 3 algoritmos (MLP e SVM) indentificarão a notícia como verdadeira, mas faça uma pesquisa antes de divulgar ela'
    #Lógica para as falsas
    elif regressaoLog == 'FAKE' and  svm == 'FAKE' and mlp == 'FAKE':
        return 'Todos os 3 algoritmos indentificarão a notícia como falsa, mas faça uma pesquisa antes de divulgar ela'
    elif regressaoLog == 'FAKE' and  svm == 'FAKE' and mlp == 'TRUE':
        return '2 dos 3 algoritmos (Regressção logística e SVM ) indentificarão a notícia como falsa, mas faça uma pesquisa antes de divulgar ela'
    elif regressaoLog == 'FAKE' and  svm == 'TRUE' and mlp == 'FAKE':
        return '2 dos 3 algoritmos (Regressão logística e MLP) indentificarão a notícia como falsa, mas faça uma pesquisa antes de divulgar ela'
    else:
        return '2 dos 3 algoritmos (SVM e MLP) indentificarão a notícia como falsa, mas faça uma pesquisa antes de divulgar ela'
   

def validacaoVardadeiraOUFalsaParaBD(regressaoLog, svm, mlp):
    if regressaoLog == 'TRUE' and  svm == 'TRUE' and mlp == 'TRUE':
        return 'TRUE'
    elif regressaoLog == 'TRUE' and  svm == 'TRUE' and mlp == 'FAKE':
        return 'TRUE'
    elif regressaoLog == 'TRUE' and  svm == 'FAKE' and mlp == 'TRUE':
        return 'TRUE'
    elif regressaoLog == 'FAKE' and  svm == 'TRUE' and mlp == 'TRUE':
        return 'TRUE'
    else:
        return 'FAKE'

def tamanho(noticia):
    if len(noticia.split()) < 100:
        return False
    return True

def senhasDiferentes(senha, senhaRepete):
    if senha == senhaRepete:
        return True
    return False
    
