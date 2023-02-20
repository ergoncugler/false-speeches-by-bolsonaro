# bibliotecas
import time
import requests
from bs4 import BeautifulSoup

# bibliotecas google
from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

# criar nova planilha
sh = gc.create("extraindo_aos_fatos")
worksheet = gc.open("extraindo_aos_fatos").sheet1
titulos = ["ID","Título","Data","Link","Texto","Tema","Repetições"]
campos = worksheet.range('A1:G1')
for i in range(0, len(campos)):
  campos[i].value = titulos[i]
worksheet.update_cells(campos)

# início do código
paginas = 446 # máximo 446
fatos = 15 # padrão 15

index = 1

p = 1
for i in range(paginas):
  site = "https://www.aosfatos.org/todas-as-declara%C3%A7%C3%B5es-de-bolsonaro/"
  url = f"{site}?page={p}"
  bs = BeautifulSoup(requests.get(url).text,'html.parser')

  f = 0
  for i in range(fatos):

    # título
    titulo = bs.find_all("h4")
    titulo = titulo[f+3].get_text()

    # data
    data = bs.find_all(class_="w600")
    data = data[f].get_text().replace("\n", "").replace("  ", "")

    # link
    link = bs.find_all(class_="microlink align-middle")
    link = f"https://www.aosfatos.org{link[f].get('href')}"

    # texto
    texto = bs.find_all(class_="neuton fs20 w300")
    texto = texto[f+3].get_text()

    # tags
    tags = bs.find_all(class_="metatags upper")
    tags = tags[f].get_text().replace("\n", "").replace(".", ". ")

    
    # /SE/ repetida
    controle = "7 / Em 2022: 18.set, 20.set, 21.set, 24.set, 07.out, 30.dez."
    bs_interno = BeautifulSoup(requests.get(link).text,'html.parser') 
    repetida = bs_interno.find_all(class_="date-list")
    repetida = repetida[0].get_text().replace("\n", "").replace("  ", "").replace("REPETIDA ", "").replace(" VEZES.", "").replace(",", ", ").replace("Em ", " / Em ")
    if repetida[:60] == controle:
      repete = "Sem Repetição"
    else:
      repete = repetida
    
    # planilhando
    conteudo = [index, titulo, data, link, texto, tags, repete]
    registros = worksheet.range(f"A{index+1}:G{index+1}")
    for i in range(0,len(registros)):
      registros[i].value = conteudo[i]
    worksheet.update_cells(registros)

    f=f+1
    index=index+1

  p=p+1
  print(f"Página {p-1} obteve {f} citações com sucesso: {(p-1)/paginas:.2f}% realizado. Total de {index-1} citações.")
  time.sleep(2)

print("\nConcluído!\n\n\n\n\n")
