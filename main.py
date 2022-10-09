from website import create_app
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from flask_ngrok import run_with_ngrok
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import json
import requests
import random
from bs4 import BeautifulSoup as bs
from datetime import datetime

app = create_app()
api = Api(app)

def requisicao_site(url):
    response = requests.get(url)
    content = response.content
    site = bs(content,'html.parser')
    return site

url = "https://www.ufc.br/restaurante/cardapio/1-restaurante-universitario-de-fortaleza/"
response = requests.get(url)
content_cardapio = response.content
site = bs(content_cardapio,'html.parser') # passando html

# Pegando os elementos do cardapio
desjejum = site.find('table',attrs={'class':'refeicao desjejum'})
almoco = site.find('table',attrs={'class':'refeicao almoco'})
jantar = site.find('table',attrs={'class':'refeicao jantar'})

def junta_palavras(vetor_string):
    texto = ''
    for elemento in vetor_string:
      texto += elemento +','
    return texto[0:-1]

# Retornando cardapio em formato dicionário
def cardapio_do_dia():
    dia = site.find('table').findAll('th')[1].text.split() # Dia da semana
    cardapio_json = {"restaurante_menu":[{"Dia": "{0}{1}".format(dia[0],dia[1])},{"Campi":"Pici"}]}
    desjejum_list= junta_palavras([i.text for i in desjejum('span')])
    almoco_list = junta_palavras([i.text for i in almoco('span')]) 
    jantar_list = junta_palavras([i.text for i in jantar('span')]) 
    cardapio_json["restaurante_menu"].append({"Desjejum": json.dumps((desjejum_list),ensure_ascii=False)})
    cardapio_json["restaurante_menu"].append({"Almoco":  json.dumps(almoco_list,ensure_ascii=False)})
    cardapio_json["restaurante_menu"].append({"Jantar": json.dumps((jantar_list),ensure_ascii=False)})
    return json.dumps(cardapio_json,ensure_ascii = False)

def cardapio_quixada():
    try: 
      ru_quixada = requisicao_site('https://www.quixada.ufc.br/restaurante-universitario/')
      cardapio = ru_quixada.findAll('img',attrs={'loading':'lazy'})
      almoco = cardapio[0]['srcset'].split(',')
      jantar = cardapio[1]['srcset'].split(',')
      link_almoco = almoco[0].split(' ')
      link_jantar = jantar[0].split(' ')
      cardapio_quixada = [{ "cardapio":[{'almoco': link_almoco[0]},{'jantar':link_jantar[0]}]},'image']
    except ConnectionError:
       cardapio_quixada = [{ "cardapio":[{'almoco': 'Houve um erro de conexão ao tentar requisitar o almoço'},{'jantar':'Houve um erro de conexão ao tentar requisitar o almoço'}]},'text']
    return json.dumps(cardapio_quixada,ensure_ascii = False)
json_quixada = cardapio_quixada()
cardapio_quixada = json.loads(json_quixada)

def mostrar_menu():
  ##Caso nao tenha cardápio
  if desjejum == None:
        dia = site.find('table').findAll('th')[1].text.split()
        print(dia[0]+dia[1]+'\n'+site.find('td',attrs = {'colspan':'3'}).text)   # Mostra mensagem de não haver cardápio
  else:
    # transformando tipo DICIONÁRIO em formato json
    cardapio = cardapio_do_dia()
    json_menu = cardapio
      # Retornando cardapio
    print(json.loads(json_menu)['restaurante_menu'][0]['Dia']
    + '\n')
    print('Campi',':',json.loads(json_menu)['restaurante_menu'][1]['Campi'])
    print('\n')
    print('Desjejum:\n')
    print(json.loads(json_menu)['restaurante_menu'][2]['Desjejum'])
    print('\n')
    print('Almoço:\n')
    print(json.loads(json_menu)['restaurante_menu'][3]['Almoco'])
    print('\n')
    print('Jantar:\n')
    print('\n')
    print(json.loads(json_menu)['restaurante_menu'][4]['Jantar'])

def checagem_de_retorno():
  try:
    menu = json.loads(cardapio_do_dia())
    aux = 0
  except:
      dia = site.find('table').findAll('th')[1].text.split()
      menu = dia[0]+dia[1]+': '+ site.find('td',attrs = {'colspan':'3'}).text  # Mostra mensagem de não haver cardápio
      aux = 1
  return [menu,aux]

menu_ru_fort = checagem_de_retorno()
menu_ru_quixada = cardapio_quixada

# Rota GET ...get_ru/<string:campi>"
class get_ru(Resource):
    def get(self,campi):
      self.campi = campi
      if campi == 'pici':
          return menu_ru_fort
      elif campi == 'quixada':
          return menu_ru_quixada
    
api.add_resource(get_ru, "/get_ru/<string:campi>")

prograd_json = [{'contatos': [[{'setor': 'Prograd'},
    {'resp': 'Pró-Reitora: Profª Ana Paula de Medeiros Ribeiro'},
    {'subsetor': 'Coordenação Prograd'},
    {'fone': 'Fone: (85) 3366 9498'},
    {'email': 'E-mail: protocolo@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Responsável: Isabel Cristina Moraes de Souza Castro'},
    {'subsetor': 'Divisão de Apoio Administrativo'},
    {'fone': 'Fone: (85) 3366 9498'},
    {'email': 'E-mail: gabinete@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Responsável: Priscilla de Araújo Gois Pinheiro Guerra'},
    {'subsetor': 'Seção de Protocolo'},
    {'fone': 'Fone: (85) 3366 9410'},
    {'email': 'E-mail: protocolo@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Responsável: Mônica Cristina de Lucena Lucas'},
    {'subsetor': 'Divisão de Comunicação (Atendimento à imprensa)'},
    {'fone': 'Fone: (85) 3366 9527 (provisório)'},
    {'email': 'E-mail: comunicacao@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Assessor: Carlos César Osório de Melo'},
    {'subsetor': 'Assessoria de Legislação'},
    {'fone': 'Fone: (85) 3366 9421'},
    {'email': 'E-mail: ale@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenador na UFC: Prof. Pedro Rogério'},
    {'subsetor': 'Programa de Residência Pedagógica'},
    {'fone': 'Fone: (85) 3366 9527'},
    {'email': 'E-mail: rp@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenadora na UFC: Profª Maria José Costa dos Santos'},
    {'subsetor': 'Programa Institucional de Iniciação à Docência – PIBID'},
    {'fone': 'Fone: (85) 3366 9527'},
    {'email': 'E-mail: pibid@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenador: Prof. Francisco Ari de Andrade'},
    {'subsetor': 'COORDENADORIA DE ACOMPANHAMENTO DISCENTE – CAD'},
    {'fone': 'Fone: (85) 3366 9519'},
    {'email': 'E-mail: cad@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenador: Profa. Simone da Silveira Sá Borges'},
    {'subsetor': 'COORDENADORIA GERAL DE PROGRAMAS ACADÊMICOS – CGPA'},
    {'fone': 'Fone/WhatsApp: (85) 3366 9496'},
    {'email': 'E-mail: cgpa@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenadora: Aline Batista de Andrade'},
    {'subsetor': 'COORDENADORIA DE PROJETOS E ACOMPANHAMENTO CURRICULAR – COPAC'},
    {'fone': 'Fone: (85) 3366 9526'},
    {'email': 'E-mail: copac@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenadora: Profª Andréa Soares Rocha da Silva'},
    {'subsetor': 'COORDENADORIA DE PLANEJAMENTO E AVALIAÇÃO DE PROGRAMAS E AÇÕES ACADÊMICAS – COPAV'},
    {'fone': 'Fone: (85) 3366 9020'},
    {'email': 'E-mail: copav@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Coordenador: Prof. Rafael Bráz Azevedo Farias'},
    {'subsetor': 'COORDENADORIA DE PLANEJAMENTO, INFORMAÇÃO E COMUNICAÇÃO – COPIC'},
    {'fone': 'Fone: (85) 3366 9036'},
    {'email': 'E-mail: copic@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Diretora: Keyla Maciel Maia'},
    {'subsetor': 'DIVISÃO DE PLANEJAMENTO E ENSINO'},
    {'fone': 'Fone: (85) 3366 9036'},
    {'email': 'sem email'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Diretora: Milena Teixeira Barbosa'},
    {'subsetor': 'DIVISÃO DE SELEÇÃO'},
    {'fone': 'E-mail: disel@prograd.ufc.br'},
    {'email': 'Fones: (85) 3366 9522 / 3366 9423'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Diretor: Daélio Feijó Rabelo'},
    {'subsetor': 'DIVISÃO DE SELEÇÃO E MATRÍCULA'},
    {'fone': 'Fone: (85) 3366 9528'},
    {'email': 'E-mail: dsm@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Chefe: Francisco Ivanildo Ferreira Fialho'},
    {'subsetor': 'DIVISÃO DE MEMÓRIA E DOCUMENTAÇÃO'},
    {'fone': '(atendimento exclusivamente por e-mail)'},
    {'email': 'E-mail: dmd@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Responsável: Michelly Linhares de Moraes'},
    {'subsetor': 'Seção de Revalidação de Diplomas'},
    {'fone': 'Fone: (85) 3366 9521'},
    {'email': 'E-mail: revalidacao@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Chefe: Maria Cristina de Figueiredo Monteiro'},
    {'subsetor': 'Seção de Registro de Diplomas de Entidades Privadas'},
    {'fone': 'Fone: (85) 3366 9523'},
    {'email': 'E-mail: registroies@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}],
   [{'setor': 'Prograd'},
    {'resp': 'Responsável: Maria de Fátima Andrade'},
    {'subsetor': 'Seção de Arquivo'},
    {'fone': 'Fone/WhatsApp: (85) 3366 9520'},
    {'email': 'E-mail: diarq@prograd.ufc.br'},
    {'site': 'https://prograd.ufc.br/pt/'},
    {'faq': 'https://prograd.ufc.br/pt/perguntas-frequentes/'},
    {'contats': 'https://prograd.ufc.br/pt/contatos/pro-reitor-e-apoio/'},
    {'whatsapp': 'https://wa.me/558533669410'}]]}]

prointer_json = [{'contatos_prointer': [[{'setor': 'Prointer'},
    {'resp': 'Augusto Albuquerque (Pró-Reitor)'},
    {'subsetor': 'Gabinete do Pró-Reitor'},
    {'fone': ' (85) 3366.7333'},
    {'email': 'augusto.albuquerque@ufc.br'},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667333'}],
   [{'setor': 'Prointer'},
    {'resp': ['Camila Gueiros(Gestora Administrativa)',
      'Fábio Nogueira(Assessor)',
      'Bruno Souza(Atendimento ao Público)']},
    {'subsetor': 'Secretaria Administrativa'},
    {'fone': ' (85) 3366.7333'},
    {'email': ['camilagueiros@ufc.br',
      'fabionogueira@ufc.br',
      'secretaria@cai.ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667333'}],
   [{'setor': 'Prointer'},
    {'resp': ['Ananda Badaró (Tradutora e Intérprete)',
      'Tadeu Azevedo(Tradutor e Intérprete)',
      'Document Verification Service']},
    {'subsetor': 'Equipe de Tradução'},
    {'fone': ' (85) 3366.7333'},
    {'email': ['traducao@cai.ufc.br',
      'tradutor@prointer.ufc.br',
      'documents@prointer.ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667333'}],
   [{'setor': 'Prointer'},
    {'resp': ['Mônica Amorim(Diretora)',
      'Su Jianhua(Diretor)',
      'Luana Leite(Assistente de Administração']},
    {'subsetor': 'Instituto Confúcio da UFC'},
    {'fone': ' (85) 3366.9031'},
    {'email': ['monica_amorim@terra.com.br',
      'institutoconfucio@ufc.br',
      'institutoconfucio@ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://institutoconfucio.ufc.br/pt/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533669031'}],
   [{'setor': 'Prointer'},
    {'resp': ['Rodrigo Rego(Coordenador)',
      'Fabiano Gadelha(Analista de Tecnologia da Informação)']},
    {'subsetor': 'Coordenadoria de Convênios Internacionais'},
    {'fone': ' (85) 3366.7336 '},
    {'email': ['convenios@prointer.ufc.br', 'fabiano.gadelha@sti.ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667336'}],
   [{'setor': 'Prointer'},
    {'resp': ['Talita Vasconcelos(Coordenadora) ',
      'Vanderleia Lucia de Souza(Assessora)']},
    {'subsetor': 'Coordenadoria de Mobilidade Acadêmica'},
    {'fone': '(85)3366.7336'},
    {'email': ['mobilidade@prointer.ufc.br', 'administrativo@cai.ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667336'}],
   [{'setor': 'Prointer'},
    {'resp': ['Abraão Saraiva(Coordenador) ',
      'Gervina Brady(Assistente em Administração)',
      'Tatieures Gomes(Analista de Tecnologia da Informação)']},
    {'subsetor': 'Coordenadoria de Empreendedorismo'},
    {'fone': '(85) 3366.7335'},
    {'email': ['abraaofsjr@gmail.com',
      'gervina.brady@ufc.br',
      'tatieures@ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667335'}],
   [{'setor': 'Prointer'},
    {'resp': ['Bruno Matos(Coordenador)',
      'Patrícia Araújo(Administradora)',
      'Laura Figueiredo(Assistente em Administração)',
      'Ciro Texeira(Administrador)']},
    {'subsetor': 'Coordenadoria de Inovação Institucional'},
    {'fone': '  (85) 3366.7335'},
    {'email': ['brunomatos@ufc.br',
      'patricia.araujo@ufc.br|inovacao@prointer.ufc.br',
      'lauracfigueiredo@ufc.br',
      'ciro.teixeira@ufc.br']},
    {'site': 'https://prointer.ufc.br/pt/seja-bem-vindo-a-prointer/'},
    {'faq': 'https://prointer.ufc.br/pt/relacoes-internacionais/perguntas-frequentes/'},
    {'contats': 'https://prointer.ufc.br/pt/sobre-a-prointer/endereco-e-telefones/'},
    {'whatsapp': 'https://wa.me/8533667335'}]]}]

prae_json = [{'contatos_prae': [[{'setor': 'Prae'},
    {'resp': 'Pró-Reitora: Profa. Dra. Geovana Maria Cartaxo de Arruda Freire'},
    {'subsetor': 'Coordenação principal'},
    {'fone': '(85) 3366 7440'},
    {'email': 'prae.secretaria@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Pró-Reitora: Profa. Dra. Geovana Maria Cartaxo de Arruda Freire'},
    {'subsetor': 'DIVISÃO DE APOIO ADMINISTRATIVO'},
    {'fone': '(85) 3366 7440'},
    {'email': 'prae.secretaria@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Pró-Reitora: Profa. Dra. Geovana Maria Cartaxo de Arruda Freire'},
    {'subsetor': 'ASSESSORIA ADMINISTRATIVA'},
    {'fone': 'Fax: (85) 3366 7442'},
    {'email': 'praap.prae@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenadora: Márcia Regina Mariano de Sousa Arão'},
    {'subsetor': 'COORDENADORIA DE ASSISTÊNCIA ESTUDANTIL'},
    {'fone': '(85) 3366-7445 / 3366-7444'},
    {'email': 'case@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenadora: Márcia Regina Mariano de Sousa Arão'},
    {'subsetor': 'DIVISÃO DE ATENÇÃO AO ESTUDANTE'},
    {'fone': ' (85) 3366 7447'},
    {'email': 'dae.case@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenadora: Márcia Regina Mariano de Sousa Arão'},
    {'subsetor': 'DIVISÃO DE BENEFÍCIOS E MORADIA'},
    {'fone': '(85)3366-7448'},
    {'email': 'digeb.case@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenador: Wildner Lins de Souza'},
    {'subsetor': 'COORDENADORIA  DE ATIVIDADES DESPORTIVAS'},
    {'fone': '(85) 3366 7871'},
    {'email': 'desportoufc@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenador: Wildner Lins de Souza'},
    {'subsetor': 'DIVISÃO DE DESPORTO DE PARTICIPAÇÃO'},
    {'fone': '(85) 3366 7871'},
    {'email': 'desportoufc@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Diretor: José Clovandi Costa Filho'},
    {'subsetor': 'DIVISÃO DE DESPORTO DE RENDIMENTO'},
    {'fone': '(85) 3366 7871'},
    {'email': 'desportoufc@ufc.br'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Coordenador: Francisco José Albuquerque Cruz'},
    {'subsetor': 'COORDENADORIA DE RESTAURANTE UNIVERSITÁRIO'},
    {'fone': '(85) 3366 7441'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Diretora: Natália Lopes Vasconcelos'},
    {'subsetor': 'DIVISÃO DE ALIMENTAÇÃO E NUTRIÇÃO'},
    {'fone': '(85) 3366 9531'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Chefe: Conceição de Maria Coelho de Carvalho'},
    {'subsetor': 'Seção do Refeitório do Benfica'},
    {'fone': '(85) 3366 7776'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Chefe: Cleonice de Castro Silva'},
    {'subsetor': 'Seção do Refeitório do Pici'},
    {'fone': '(85) 3366 9530'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'COORDENADORIA DE RESTAURANTE UNIVERSITÁRIO'},
    {'subsetor': 'Seção do Refeitório do Porangabuçu'},
    {'fone': ' (85) 3366 7447'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}],
   [{'setor': 'Prae'},
    {'resp': 'Diretor: José Pereira Duarte'},
    {'subsetor': 'DIVISÃO DE SERVIÇOS OPERACIONAIS'},
    {'fone': ' (85) 3366 9530'},
    {'email': 'praeufc@gmail.com'},
    {'site': 'https://prae.ufc.br/pt/'},
    {'faq': 'Não existente'},
    {'contats': 'https://prae.ufc.br/pt/enderecos-e-telefones/'},
    {'whatsapp': 'https://wa.me/558533667440'}]]}]

contatos_prograd = prograd_json
contatos_prointer = prointer_json
contatos_prae = prae_json

class get_contatos(Resource):
    def get(self,setor):
      self.setor = setor
      if self.setor == 'prograd':
        return contatos_prograd
      if self.setor ==  'prointer':
        return contatos_prointer
      if self.setor == 'prae':
        return contatos_prae

api.add_resource(get_contatos,"/get_contatos/<string:setor>")

if __name__ == '__main__':
    app.run(debug=True)