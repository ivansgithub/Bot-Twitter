import requests
from bs4 import BeautifulSoup as BS
import pdfplumber
from io import BytesIO
import tweepy
import re




def lamba_handle(event,context):
        
    r=requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Informe_monetario_diario.asp')
        
    dom = BS(r.content , features = 'html.parser')
        
    dom2=dom.find('ul',{'class':'post-pagina-interior'})
        
    dom3=dom2.find('a')
        
    dom4=dom3.get('href')
        
    dom5='http://www.bcra.gob.ar'+dom4.replace('..','')
        
    rq = requests.get(dom5)

    pdf = pdfplumber.load(BytesIO(rq.content))
    page = pdf.pages[3]
    page2 = pdf.pages[2]
    text=page.extract_text()
    text3=page2.extract_text()
    
    
    text=text.split('\n')
    
    text3=text3.replace('\n','')
            
    text2=[i for i in text if 'Base monetaria' in i]
            
    monto=text2[0].split('Base monetaria')[2]       
    monto=monto.split(' ')
    monto=monto[1].strip()
           
    fecha=re.search(r'Informe Monetario Diario+\s+[0-9]{1,2}\s\w\w\s(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s\w\w\s[0-9]{3,4}',text3)
    fecha=fecha.group().replace('Informe Monetario Diario  ', '')
        
    api_key='uy6CzZrOGBElppKiL9SJdqt8N'
    api_key_secret='5NzPJUYGoBb7KsPbedYvatzssd7GA1VtepPv6VXGqK86mKFbUJ'
        
    access_token='1448023730173583361-whw7nPHiGugMsHxkFKAelWs1pBwH6V'
    access_token_secret='EY4eNCYt6zy1vx1gfqqIPeAmeKxz6EsTMBlgS1VfiOWhb'
        
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
        
    api = tweepy.API(auth)
        
        
        
    single_tweet='La variacion de la base moneraria el ' + fecha +'\n'+'fue de $'+ monto + ' millones '
    
    
    for statuss in tweepy.Cursor(api.user_timeline).items():
      
        try:
            api.destroy_status(statuss.id)
        except:
            pass
            
    api.update_status(status=single_tweet)



