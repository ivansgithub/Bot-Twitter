import requests
from bs4 import BeautifulSoup as BS
import pdfplumber
from io import BytesIO
import re 
import boto3
import tweepy


def get_twitter_keys():
    
    aws_client = boto3.client('ssm')

    parameters = aws_client.get_parameters(
        Names=[
            'api.key.twitter',
            'api.key.secret.twitter',
            'access.token.twitter',
            'access.token.secret.twitter'
        ],
        WithDecryption=True
    )

    keys = {}
    for parameter in parameters['Parameters']:
        keys[parameter['Name']] = parameter['Value']

    return keys


def scrape_page():
    response=requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Informe_monetario_diario.asp') 

 
    dom = BS(response.content , features = 'html.parser') 
    find_link_report=dom.find('ul',{'class':'post-pagina-interior'}).find('a').get('href')

    link_report='http://www.bcra.gob.ar'+find_link_report.replace('..','')

    r=requests.get(link_report)

    pdf = pdfplumber.open(BytesIO(r.content))

    page = pdf.pages[3]
    page2 = pdf.pages[2]
    text=page.extract_text()
    text2=page2.extract_text()

    text=text.split('\n')
    
    text3=text2.replace('\n','')
            
    text4=[i for i in text if 'Base monetaria' in i]
            
    amount=text4[0].split('Base monetaria')[2]       
    amount=amount.split(' ')
    amount=amount[1].strip()

           
    date=re.search(r'Informe Monetario Diario+\s+[0-9]{1,2}\s\w\w\s(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s\w\w\s[0-9]{3,4}',text3)
    date=date.group().replace('Informe Monetario Diario ', '')

    content = {}
     
    content['date'] = date
    content['amount']=amount

    return content


def lambda_handler(event, context):
   

    
    content= scrape_page()
    
    single_tweet='La variacion de la base moneraria el' + content['date'] +' fue de $'+  content['amount'] + ' millones'
    
    keys = get_twitter_keys()
    auth = tweepy.OAuthHandler(keys['api.key.twitter'], keys['api.key.secret.twitter']) 
    auth.set_access_token(keys['access.token.twitter'],keys['access.token.secret.twitter']) 
    api = tweepy.API(auth) 

    
    
    
    for statuss in tweepy.Cursor(api.user_timeline).items(1):
      
        
        if single_tweet == statuss._json['text']:
            pass
            
        else:
            api.update_status(status=single_tweet)
