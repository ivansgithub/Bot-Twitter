import requests
from bs4 import BeautifulSoup as BS
import pdfplumber
from io import BytesIO
import tweepy
import re


# include everything in a function to run in lambda aws

def lamba_handle(event,context):
        
    # make a request to the page to scrape    
    r=requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Informe_monetario_diario.asp')
        
    # get the content of the html    
    dom = BS(r.content , features = 'html.parser')
        
    #search for the element with the link we need    
    dom2=dom.find('ul',{'class':'post-pagina-interior'})
        
    dom3=dom2.find('a')
        
    dom4=dom3.get('href')
        
    dom5='http://www.bcra.gob.ar'+dom4.replace('..','')
        
    # make a second request to the page to scrape    
    rq = requests.get(dom5)
    
    #Download the text from the pdf online
    pdf = pdfplumber.load(BytesIO(rq.content))
    page = pdf.pages[3]
    page2 = pdf.pages[2]
    text=page.extract_text()
    text3=page2.extract_text()
    
    #text mining process
    text=text.split('\n')
    
    text3=text3.replace('\n','')
            
    text2=[i for i in text if 'Base monetaria' in i]
            
    amount=text2[0].split('Base monetaria')[2]       
    amount=amount.split(' ')
    amount=amount[1].strip()
           
    date=re.search(r'Informe Monetario Diario+\s+[0-9]{1,2}\s\w\w\s(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s\w\w\s[0-9]{3,4}',text3)
    date=date.group().replace('Informe Monetario Diario  ', '')
        
    #access to twitter api    
        
        
    api_key='Your_key'
    api_key_secret='Your_key_secret'
        
    access_token='Your_token'
    access_token_secret='Your_secret_token'
        
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
        
    api = tweepy.API(auth)
        
        
    #tweet format
    single_tweet='La variacion de la base moneraria el ' + fecha +'\n'+'fue de $'+ monto + ' millones '
    
    #delete a tweet with the same format if it exists
    for statuss in tweepy.Cursor(api.user_timeline).items():
      
        try:
            api.destroy_status(statuss.id)
        except:
            pass
            
    #post the twitt
    api.update_status(status=single_tweet)



