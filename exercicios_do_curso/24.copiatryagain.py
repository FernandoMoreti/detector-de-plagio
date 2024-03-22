import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra: "))
    ttr = float(input("Entre a relação Type-Token: "))
    hlr = float(input("Entre a Razão Hapax Legomana: "))
    sal = float(input("Entre o tamanho médio de sentença: "))
    sac = float(input("Entre a complexidade média da sentença: "))
    pal = float(input("Entre o tamanho medio de frase: "))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair): ")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) +" (aperte enter para sair): ")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]

    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'['',:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''IMPLEMENTAR. Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    soma = 0
    for i in range(0,6):
        diferença = as_a[i] - as_b[i]
        if diferença < 0:
            diferença *= -1
        soma = soma + diferença
    return soma / 6

def calcula_assinatura(texto):
    '''IMPLEMENTAR. Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    a = tamanho_medio_palavra(texto)
    b = relaçao_type(texto)
    c = hapax_legomana(texto)
    d = tamanho_medio_sentença(texto)
    e = complexidade_sentença(texto)
    f = tamanho_frase(texto)
    assinatura = [a, b, c, d, e, f]
    return assinatura
    
def avalia_textos(textos, ass_cp):
    '''IMPLEMENTAR. Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    as_a = []
    maiorsimilaridade = 100000
    i= 0
    numero_texto = -1
    for texto in textos:
        as_a.append(calcula_assinatura(texto))
    for i in range(len(as_a)):
        similaridade = compara_assinatura(as_a[i], ass_cp)
        if similaridade < maiorsimilaridade:
            maiorsimilaridade = similaridade
            numero_texto = i + 1
    return numero_texto

def pontuacao(texto):
    texto = re.sub('[!.,:@]', '', texto)
    return texto

def tamanho_medio_palavra(texto):
    somapalavras = 0
    totalpalavras = 0
    for sentenca in separa_sentencas(texto):
        for frase in separa_frases(sentenca):
            for palavra in separa_palavras(frase):
                somapalavras = somapalavras + len(palavra)
                totalpalavras = totalpalavras + 1
    return somapalavras / totalpalavras

def relaçao_type(texto):
    texto = pontuacao(texto)
    lista_palavras = separa_palavras(texto)
    return n_palavras_diferentes(lista_palavras) / len(lista_palavras)

def hapax_legomana(texto):
    texto = pontuacao(texto)
    lista_palavras = separa_palavras(texto)
    return n_palavras_unicas(lista_palavras) / len(lista_palavras)

def tamanho_medio_sentença(texto):
    sentenças = 0
    caracteresentença = 0
    for sentenca in separa_sentencas(texto):
        caracteresentença += len(sentenca)
        sentenças += 1
    return caracteresentença / sentenças

def complexidade_sentença(texto):
    sentencas = separa_sentencas(texto)
    soma = 0
    for x in sentencas:
        frases = separa_frases(x)
        soma += len(frases)
    return soma/len(sentencas)

def tamanho_frase(texto):
    sentencas = separa_sentencas(texto)
    soma = 0
    caracteres = 0
    for x in sentencas:
        frases = separa_frases(x)
        soma += len(frases)
        for frase in frases:
            caracteres += len(frase.lstrip())
    return caracteres / soma

def main():
    assinatura_padrao = le_assinatura()
    textos = le_textos()
    similaridade = avalia_textos(textos, assinatura_padrao)
    print('O autor do texto', similaridade, 'esta infectado com COH-PIAH')