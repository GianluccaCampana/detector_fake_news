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
        return 'Nossos algoritmos indentificaram a noticia como verdedeira, verifique as fontes antes de compartilhar!'
    elif regressaoLog == 'TRUE' and  svm == 'TRUE' and mlp == 'FAKE':
        return '2 dos 3 algoritmos (Regressão logística e SVM ) indentificaram a noticia como verdedeira, verifique as fontes antes de compartilhar!'
    elif regressaoLog == 'TRUE' and  svm == 'FAKE' and mlp == 'TRUE':
        return '2 dos 3 algoritmos (Regressão Logística e MLP) indentificaram a noticia como verdedeira, verifique as fontes antes de compartilhar!'
    elif regressaoLog == 'FAKE' and  svm == 'TRUE' and mlp == 'TRUE':
        return '2 dos 3 algoritmos (MLP e SVM) indentificaram a notícia como verdadeira, verifique as fontes antes de compartilhar!'
    #Lógica para as falsas
    elif regressaoLog == 'FAKE' and  svm == 'FAKE' and mlp == 'FAKE':
        return 'Nossos algoritmos indentificaram a noticia como uma possivel fakenews, verifique as fontes antes de compartilhar!'
    elif regressaoLog == 'FAKE' and  svm == 'FAKE' and mlp == 'TRUE':
        return '2 dos 3 (Regressção logística e SVM ) algoritmos indentificarão a noticia como uma possivel fakenews, fverifique as fontes antes de compartilhar!'
    elif regressaoLog == 'FAKE' and  svm == 'TRUE' and mlp == 'FAKE':
        return '2 dos 3 (Regressão logística e MLP) algoritmos indentificarão a noticia como uma possivel fakenews, verifique as fontes antes de compartilhar!'
    else:
        return '2 dos 3 algoritmos (SVM e MLP) indentificarão a notícia como falsa, verifique as fontes antes de compartilhar!'
   

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
    
