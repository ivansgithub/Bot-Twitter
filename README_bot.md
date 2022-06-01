# A serverless AWS Twitter bot

Finding quality and truthful content on social networks can be difficult, imagine having a Twitter bot that posts tweets with the information you need from reliable sources? Generate your own automatic content daily, allow your entire community to see it and also run completely without servers, it is possible to do it with python, tweepy and aws.

In this container, I will show you how to create a Twitter bot that scrapes the page of the Argentine national bank to know the volume data of the daily monetary base and posts a tweet every time this data is updated, all running in a serverless environment of aww. 

![twitterbot](https://user-images.githubusercontent.com/82000274/169691262-2b4e09da-2bde-4338-8fd3-f6993c2c2abe.jpg)

## Step One: Set-up and install requeriments

### 1) Twitter API: access to twitter api and create credentials

You must first open your twitter developer account in the Twitter Developer console.
I leave you Jean-Christophe Chouinard's blog where he explains in greater detail how to access a twitter developer account and this other article to create your credentials once you have the account active. https://www.jcchouinard.com/twitter-api-credentials/

### 2) AWS: Store Parameters in AWS, Create IAM User and Install CLI.
With the twitter api credentials, we will use Parameter Store in aws Systems Manager to store the different keys and be able to link it with aws lambda. For this we enter the aws console.

![image](https://user-images.githubusercontent.com/82000274/171403178-a00631d0-f2ce-4638-9850-cf94969070d2.png)

To create a new parameter enter the name, layer "Standard" and type "SecureString" to keep the value encrypted. Then enter the value and leave everything else as default.

We create the 4 parameters

![image](https://user-images.githubusercontent.com/82000274/171403253-f292656e-9f88-4791-b25a-4f1bbc977f42.png)

### 3) IAM: create an IAM user that allows us to interact with CLI

Log in to aws IAM, choose the users option and click on create a new one.
Choose the username, access with SDKs, then add the permissions (Ideally, restrict the permissions as much as possible, but for this exercise we will use the administrator permission) and save the keys that will be generated.

![image](https://user-images.githubusercontent.com/82000274/171403576-89059191-62bb-4e56-8c16-4e5d2e1373ea.png)

### 4) Configure CLI: to control multiple AWS services from the command line and automate them through scripts.

To configure aws on your pc, Install CLI from here https://aws.amazon.com/cli/
At the Command prompt type aws configure, then enter the keys generated in the IAM step.

![cliimagen](https://user-images.githubusercontent.com/82000274/171500880-5ce501d4-6b6b-402c-bac0-744b8f301f73.png)

Clever! Now if we can start writing code!

## Second step: We create our python script

Install libraries

<img width="520" alt="raycast-untitled (2)" src="https://user-images.githubusercontent.com/82000274/171503912-cf89af41-e94e-4e75-b3b2-5cb5708f504f.png">


We are going to divide the code into three functions, the first one will call the parameters created previously to communicate with aws and the second one will do the scraping of the page and the third one will communicate with the twitter api to tweet the scraped content.

We start by creating the function with the connector to the aws Systems Manager (ssm) and obtaining the parameters created previously.

<img width="520" alt="raycast-untitled (3)" src="https://user-images.githubusercontent.com/82000274/171405516-bd8f91ce-4463-494e-a00a-694bbc46626c.png">

we convert it to a simple dictionary and return the dictionary as the result of the function.

<img width="545" alt="raycast-untitled (4)" src="https://user-images.githubusercontent.com/82000274/171405697-fae3d234-5e37-491b-b238-979faddd09c5.png">

We created the function to scrape the page of the Argentine national central bank.
The requests module allows you to send HTTP requests using Python and returns a Response Object with all the response data (content, encoding, status, etc).

<img width="920" alt="raycast-untitled (5)" src="https://user-images.githubusercontent.com/82000274/171406062-b134e83a-a2ee-46bf-8f4c-eb7f9d34df3f.png">

BeautifulSoup is the library that allows us to read the content of the response object by parsing the html

<img width="564" alt="raycast-untitled (6)" src="https://user-images.githubusercontent.com/82000274/171406253-176e6d6e-c49c-40fc-aeec-61dc08f7251c.png">

With Beautifilsoup, understanding a bit about the HTML structure, we can find the link of the report that is updated daily. We look for the <ul> tag of the 'post-interior-page' class and extract from the <a> tag the 'href' which in html is the element that contains the hyperlink.
 
 <img width="855" alt="raycast-untitled (7)" src="https://user-images.githubusercontent.com/82000274/171406505-66e31305-e32b-44ea-812f-9d96107fb016.png">

We create a new link to be called with request
 
  <img width="709" alt="raycast-untitled (8)" src="https://user-images.githubusercontent.com/82000274/171406657-29a10800-d3cd-4572-a521-144b74e85488.png">
 
When entering the link you will be able to realize that it is a pdf file, therefore Beautifulsoup stops working to search for content in this type of page, so we must use a new library called pdfplumber. io.BytesIO (r.content): It is used because r.content is a binary code and its use is necessary to interpret the bytes.
  
 <img width="520" alt="raycast-untitled (9)" src="https://user-images.githubusercontent.com/82000274/171406948-2379f058-f1bf-460e-9a3c-ba0a705b5b24.png">

We locate the pdf page and the text that we want to extract for which we need the library re the functions in this module let you check if a particular string matches a given regular expression. 

 <img width="920" alt="raycast-untitled (10)" src="https://user-images.githubusercontent.com/82000274/171407598-669e601e-fcf1-49af-b0b9-932808a7b0ef.png">

We create a small dictionary to sort the data and return it.
 
 <img width="520" alt="raycast-untitled (11)" src="https://user-images.githubusercontent.com/82000274/171407820-0534f6b8-1e92-4aa1-a67f-acfbf7b666a1.png">
  
  
Now we create the function lambda_handler method, which is what we will have our Lambda function call. Here the twitter api will also be called

We create the string that we want to post
  
  <img width="920" alt="raycast-untitled (12)" src="https://user-images.githubusercontent.com/82000274/171408485-29b0131d-548f-4bf6-882b-ef27fe3050f5.png">
 
We call the twitter api for this we pass the parameters with oauth.

 <img width="873" alt="raycast-untitled (13)" src="https://user-images.githubusercontent.com/82000274/171408653-f56f3deb-79ea-49f2-a5f9-4b9384f6552c.png">

We verify if this string exists in the timeline and thus avoid posting the same tweet twice on days when the report is not updated. If it is not the case, we post the new tweet.
  
  <img width="591" alt="raycast-untitled (14)" src="https://user-images.githubusercontent.com/82000274/171408858-1d375813-1627-4ff3-a397-3ceb59a8d85d.png">


## Third Step: We create our lambda function
 
For this we enter the aws lambda service and press create function.
We choose a name and the language in which our script is written, we leave the rest by default.
 
 ![image](https://user-images.githubusercontent.com/82000274/171409776-987a6b34-e869-4d77-b804-dc99f301ff3a.png)

Then we add the permission for our lambda function to communicate with the parameters created in system manager, for this we go to configuration and open the link the "Execution role" panel.
Click the "Attach policies" button. On the add permissions screen, search for the "AmazonSSMReadOnlyAccess" permission.  
 
 ![image](https://user-images.githubusercontent.com/82000274/171409832-dfd27ab3-54de-48a4-8b3d-c1c04875f7ea.png)

## Fourth step: We upload our python code

First we have to install all the libraries used in a directory, if you are using a virtual environment you can use pip freeze > requirements.txt
 
For windowns: 
1.In a specific directory run pip install -r requirements.txt
2.Copy to the same directory lambda_function.py (name of the python file, where we write our code) 
3.Create a zip linking everything (not including hidden or config files, such as .git, .venv, or .gitignore).

To do this in Linux/Unix:
1.pip install -t packages -r requirements.txt
2.cd packages
3.zip -r ../deployment.zip .
4.cd ..
5.zip -g deployment.zip lambda_function.py

 
![image](https://user-images.githubusercontent.com/82000274/171409984-57db91ca-8727-4033-b5d7-b8cdf58fb2a6.png)

Select the zip file you created
 
 ![image](https://user-images.githubusercontent.com/82000274/171410095-68916c99-84ea-41a6-9c03-c72ebe3ebe86.png)

In the settings tab click edit increase the timeout to 1 minute.

 ![image](https://user-images.githubusercontent.com/82000274/171470011-c0d217d4-e221-41eb-a487-165c5ef586a3.png)

Ready you can try it!
 
![image](https://user-images.githubusercontent.com/82000274/171470078-df1873b2-6b80-4516-b154-36a98a6a5fb1.png)

 ## Fifth step: create a trigger to run daily

entering Eventbridge click on create new rule.
Enter the name, it is a good practice to name it including what it does.

Select "Schedule." On the next page, place the cron that indicates how often the lambda will be activated, this function, I will use a cron expression to execute it every day at 10:00 a.m.

In the "Select Targets" section, select "Lambda Function" for the target, and then choose your Lambda function. 
 
![image](https://user-images.githubusercontent.com/82000274/171470143-d90ee8dd-84db-4c5c-9fa3-f6f8b2e425a2.png)
 
 
Done, we have our bot running in a serverless daily!

Without a doubt, with this process we can automate the posting of a lot of content for our accounts, but I invite you to read the tweepy documentation to learn about the many other functions it has.

Thank you very much for getting here, you can see all the code in the .py file of the repository


  











