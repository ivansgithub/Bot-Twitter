import requests
from bs4 import BeautifulSoup as BS
import PyPDF2
import io
from tika import parser
import tweepy
import time

def lamba_handle(event,context):
    
    
    y=0
    def suma(y):
        y+=1
        return y
        
    
    
    
    
    y=suma(y)
    
    
    
    def do_some_work():
        
        r=requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Informe_monetario_diario.asp')
        
        dom = BS(r.content , features = 'html.parser')
        
        dom2=dom.find('ul',{'class':'post-pagina-interior'})
        
        dom3=dom2.find('a')
        
        dom4=dom3.get('href')
        
        dom5='http://www.bcra.gob.ar'+dom4.replace('..','')
        
        response = requests.get(dom5)
        pdf_file = io.BytesIO(response.content) 
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        
        pdfFile = parser.from_file(dom5)
        
        text=(pdfFile["content"])
        text=text.split('\n')
        
        text2=[i for i in text if 'Base monetaria' in i]
        text3=[i for i in text if 'Informe Monetario Diario' in i]
        
        monto=text2[2].split('Base monetaria')[2]       
        monto=monto.split(' ')
        monto=monto[1].strip()
        
        fecha=text3[1].replace('Informe Monetario Diario','').strip()
        
        
        api_key='uy6CzZrOGBElppKiL9SJdqt8N'
        api_key_secret='5NzPJUYGoBb7KsPbedYvatzssd7GA1VtepPv6VXGqK86mKFbUJ'
        
        access_token='1448023730173583361-whw7nPHiGugMsHxkFKAelWs1pBwH6V'
        access_token_secret='EY4eNCYt6zy1vx1gfqqIPeAmeKxz6EsTMBlgS1VfiOWhb'
        
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token,access_token_secret)
        
        api = tweepy.API(auth)
        
        
        
        single_tweet='La variacion de la base moneraria el ' + fecha +'\n'+'fue de $'+ monto + ' millones ' + str(y)
        api.update_status(status=single_tweet)
        
    





