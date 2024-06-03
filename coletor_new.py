import sqlalchemy as sqa 
import pandas as pd
import time as tempo
from selenium import webdriver
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome()
navegador.get('https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_taxa_de_natalidade#:~:text=Nota%3A%20A%20Taxa%20de%20Natalidade,%2C%20cidade%2C%20etc.')

navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table').text

lista_natalidade = [] 

for i in range(2,102):  
# preciso montar tabela a partir da string acima.    
    lugar_por_estado_soberano = navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/tbody/tr['+str(i)+']/td[1]').text
    lugar_por_estado          = navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/tbody/tr['+str(i)+']/td[2]').text                                                         
    entidade                  = navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/tbody/tr['+str(i)+']/td[3]').text                                                   
    taxa_de_natalidade        = navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/tbody/tr['+str(i)+']/td[4]').text
    data                      = navegador.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/tbody/tr['+str(i)+']/td[5]').text

    lista_natalidade.append([lugar_por_estado_soberano, lugar_por_estado, entidade, taxa_de_natalidade, data])  

# Criar um DataFrame com os dados coletados
df = pd.DataFrame(lista_natalidade,columns=['Lugar_Estado_Soberano','Lugar_Estado','Entidade','Taxa_Natalidade','Data'])

# Ajusta daods da coluna 
df['Lugar_Estado_Soberano'] = df['Lugar_Estado_Soberano'].str.replace('—', '0').str.replace('-', '0')
df['Data'] = df['Data'].str.replace('since all the time', 'Desde sempre').str.replace('2007 est.', '2007 estimado')

# SALVANDO DADOS EM CSV E JSON
df.to_csv('../0_bases_originais/dados_originais.csv',sep=';', index=False, encoding='utf-8')
df.to_json('../0_bases_originais/dados_originais.json')

# SALVANDO DADOS NO BANCO 
engine = sqa.create_engine("sqlite:///taxa_natalidade.db", echo=True)
conn = engine.connect()

df.to_sql('taxa_natalidade.db', con=conn, if_exists='replace', index=False)

navegador.quit()