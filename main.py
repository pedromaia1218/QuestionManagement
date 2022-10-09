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

url = "https://www.ufc.br/restaurante/cardapio/1-restaurante-universitario-de-fortaleza"
response = requests.get(url)
content_cardapio = response.content
site = bs(content_cardapio,'html.parser') # passando html

# Pegando os elementos do cardapio
desjejum = site.find('table',attrs={'class':'refeicao desjejum'})
almoco = site.find('table',attrs={'class':'refeicao almoco'})
jantar = site.find('table',attrs={'class':'refeicao jantar'})

# Retornando cardapio em formato dicionário
def cardapio_do_dia():
    dia = site.find('table').findAll('th')[1].text.split() # Dia da semana
    cardapio_json = {"restaurante_menu":[{"Dia": "{0}{1}".format(dia[0],dia[1])},{"Campi":"Pici"}]}
    desjejum_list= [i.text for i in desjejum('span')] 
    almoco_list = [i.text for i in almoco('span')] 
    jantar_list = [i.text for i in jantar('span')] 
    cardapio_json["restaurante_menu"].append({"Desjejum": json.dumps((desjejum_list),ensure_ascii=False)})
    cardapio_json["restaurante_menu"].append({"Almoco":  json.dumps(almoco_list,ensure_ascii=False)})
    cardapio_json["restaurante_menu"].append({"Jantar": json.dumps((jantar_list),ensure_ascii=False)})
    return json.dumps(cardapio_json,ensure_ascii = False)

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
# Rota GET ...get_ru/<string:campi>"
class get_ru(Resource):
    def get(self,campi):
        return menu_ru_fort
class home(Resource):
  def get(self):
    return "Hey there! This is a simple demo for making an API server made by Ali Mustufa Shaikh;"
    
api.add_resource(get_ru, "/get_ru/<string:campi>")
api.add_resource(home,"/")

if __name__ == '__main__':
    app.run(debug=True)