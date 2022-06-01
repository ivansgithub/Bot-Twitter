# Bot that tweets daily

Encontrar contenido de calidad y veridico en las redes sociales puede ser dificil, imagina  tener un Twitter bot que postee tweets con la infomacion que necesitas de fuentes confiables?. Generar tu propio contenido automatico diariamente, permitir que toda tu comunidad lo vea y que ademas corra totalmente sin servidores, es posible hacerlo con python, tweepy y aws. 

En este contenedor, te  mostraré cómo crear un bot de Twitter que scrapee la pagina del banco nacional argentino para conocer el dato del volumen de la base monetarea diaria y postee un tweet cada vez que se actualice este dato, todo corriendo en un ambiente serverless  de aws. 

![twitterbot](https://user-images.githubusercontent.com/82000274/169691262-2b4e09da-2bde-4338-8fd3-f6993c2c2abe.jpg)

# Step One: Set-up and install requeriments

1) API Twitter: access to twitter api and create credentials
Primero debes abrir tu cuenta de twitter developer en Twitter Developer console.
Te dejo el blog de Jean-Christophe Chouinard donde explica en mayor detalle como acceder a una cuenta twitter developer y este otro articulo para crear tus credenciales una vez tengas la cuenta activa. https://www.jcchouinard.com/twitter-api-credentials/

2) AWS:  Almacénenar parámetros en AWS, Crear Usuario IAM and Instalar CLI.
Ya con las credenciales de la api de twitter, utilizaremos Parameter Store en Systems Manager de aws para almacenar las diferentes keys y poder enlazarlo con aws lambda. Para esto entramos en la consola de aws. 

![image](https://user-images.githubusercontent.com/82000274/171403178-a00631d0-f2ce-4638-9850-cf94969070d2.png)

Para crear un nuevo parametro introduce el nombre, capa "Estándar" y tipo "SecureString" para mantener  encriptado el valor. Luego introduce el valor y todo lo demas dejalo por default. 

Creamos los 4 paramatros

![image](https://user-images.githubusercontent.com/82000274/171403253-f292656e-9f88-4791-b25a-4f1bbc977f42.png)

3) IAM: crear un usuario IAM que nos permita interactuar con CLI

Para crear un usurio iam entra en iam de aws, elige usuarios y crear uno nuevo. 
Escoge el nombre del usuario, los acceder con sdk, luego agrega los permisos y guarda las claves que ser generan. 

![image](https://user-images.githubusercontent.com/82000274/171403576-89059191-62bb-4e56-8c16-4e5d2e1373ea.png)

4) Configurar CLI:  to control multiple AWS services from the command line and automate them through scripts.

Para configurar aws en tu pc, Install CLI from here https://aws.amazon.com/cli/
En la Command prompt escribe aws configure, luego introduce las claves generadas en el paso del IAM

![image](https://user-images.githubusercontent.com/82000274/171403746-3bd5d6a1-6b86-4213-b790-8ce3a15fccf5.png)


Listo! Ahora si podemos empezar a escribir codigo! 

Segundo paso: Creamos nuestro script de python 

Instalar librerias 
 <img width="520" alt="raycast-untitled (2)" src="https://user-images.githubusercontent.com/82000274/171405070-2c70e6a7-5715-4392-838a-56449f6f28fa.png">

Vamos a dividir el codigo en tres funciones, la primera llamara los parametros creados anteriormente para comunicarnos con aws y la segunda hara el escrapeo de la pagina y la tercera se comunicara con la api de twitter para  twetteara el contenido escrapeado.  

Comenzamos creando la funcion con el conector al  Systems Manager de aws (ssm) y obteniendo los parametros creados anteriormente.

<img width="520" alt="raycast-untitled (3)" src="https://user-images.githubusercontent.com/82000274/171405516-bd8f91ce-4463-494e-a00a-694bbc46626c.png">


lo convertimos en un diccionario sencillo y devolvemos el diccionario como resultado de la funcion.

<img width="545" alt="raycast-untitled (4)" src="https://user-images.githubusercontent.com/82000274/171405697-fae3d234-5e37-491b-b238-979faddd09c5.png">

Creamos la funcion para scrapear la pagina del banco central nacional argentino. 
The requests module allows you to send HTTP requests using Python and returns a Response Object with all the response data (content, encoding, status, etc).

<img width="920" alt="raycast-untitled (5)" src="https://user-images.githubusercontent.com/82000274/171406062-b134e83a-a2ee-46bf-8f4c-eb7f9d34df3f.png">

beautifulSoup es la  libreria que nos permite leer el contenido del response object parseando el  html 

<img width="564" alt="raycast-untitled (6)" src="https://user-images.githubusercontent.com/82000274/171406253-176e6d6e-c49c-40fc-aeec-61dc08f7251c.png">

Con Beautifilsoup, entendiendo un poco sobre la estructura del HTML podemos encontrar el link del informe que se actualiza diariamente. Buscamos la etiqueta <ul>  de la clasee 'post-pagina-interior' y extraemos de la etiqueta <a> el ‘href’ que en html es el elemento que contiene el hyperlink.
  
 <img width="855" alt="raycast-untitled (7)" src="https://user-images.githubusercontent.com/82000274/171406505-66e31305-e32b-44ea-812f-9d96107fb016.png">

  creamos un nuevo link para ser llamado con request 
  
  <img width="709" alt="raycast-untitled (8)" src="https://user-images.githubusercontent.com/82000274/171406657-29a10800-d3cd-4572-a521-144b74e85488.png">
  
  Al entrar al link se podran dar cuenta que es un archivo pdf, por lo tanto Beautifulsoup deja de funcionar para buscar contendio en este tipo de paginas, por lo que debemos usar una nueva libreria llamada pdfplumber. io.BytesIO (r.content): se usa porque r.content es un código binario y para interpretar los byte es necesario su uso.
  
 <img width="520" alt="raycast-untitled (9)" src="https://user-images.githubusercontent.com/82000274/171406948-2379f058-f1bf-460e-9a3c-ba0a705b5b24.png">

  ubicamos la pagina del pdf y el texto que queremos extraer para lo cual necesitamos la libreria re the functions in this module let you check if a particular string matches a given regular expression. 
  
  <img width="920" alt="raycast-untitled (10)" src="https://user-images.githubusercontent.com/82000274/171407598-669e601e-fcf1-49af-b0b9-932808a7b0ef.png">

  Creamos un pequeno diccionario para ordenar los datos y lo devolvemos. 
  
 <img width="520" alt="raycast-untitled (11)" src="https://user-images.githubusercontent.com/82000274/171407820-0534f6b8-1e92-4aa1-a67f-acfbf7b666a1.png">
  
  
Ahora creamos la funcion  lambda_handler method, which is what we will have our Lambda function call. Aca tambien se llamara a la api de twitter

creamos el string que queremos postear 
  
  <img width="920" alt="raycast-untitled (12)" src="https://user-images.githubusercontent.com/82000274/171408485-29b0131d-548f-4bf6-882b-ef27fe3050f5.png">

  llamamos a la api de twitter para esto pasamos los parametros con oauth. 
<img width="873" alt="raycast-untitled (13)" src="https://user-images.githubusercontent.com/82000274/171408653-f56f3deb-79ea-49f2-a5f9-4b9384f6552c.png">

    Verificamos si en el timeline existe este string y asi evitar postear dos veces el mismo tweet en dias donde no se actualice el informe. Si no es el caso, postamos el nuevo tweet
  
  <img width="591" alt="raycast-untitled (14)" src="https://user-images.githubusercontent.com/82000274/171408858-1d375813-1627-4ff3-a397-3ceb59a8d85d.png">

  











