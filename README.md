# FinTech-Finance - A Stock Investment Website

## Video Demo
https://github.com/Progpr/FinTech-Finance/assets/95381092/387af641-a587-4cf7-9c8a-bcfc3237c2e1



This is a

+ [TechStack](#TechStack)
+ [Features](#Features)
+ [Run Locally](#Run-Locally)
+ [Future Scope](#Scope)


## TechStack

+ [Flask](https://flask.palletsprojects.com/en/3.0.x/): The website is created on a flask web application.

+ [Bootstrap 5.3.1](https://getbootstrap.com/docs/5.3/getting-started/introduction/): Front end framework used for creating the OTT-like UI
  
+ [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli): To deploy the flask application to azure app service

+ [Azure CICD](https://learn.microsoft.com/en-us/azure/app-service/deploy-azure-pipelines?tabs=yaml): To setup automated deployment from github actions itself. On commiting to the github branch, changes are automatically reflected on the deployed website.

+ [Google Forms](https://www.google.com/forms/about/): To create Registration Forms for each event.
  
## Features
- **Interfaces:** Separate interfaces for different OTT themes (Adds to the look and feel of the website). Primary UI for netflix with the navbar feature appearing on scrolling. This feature is done using JavaScript using the "ready" function and "scroll" object and also by controlling CSS in JavaScript.
- **Event Registration:** Comprehensive and simple event registration with the help of netflix-like event cards.
- **Comprehensive look:** The overall UI design with the theme provides a comprehensive introduction to the techfest and its essence.


## Files
Important Files of the directory

- **templates:** Folder contains the main html template that defines the entire webpage and all sections
- **static:** Contains all the important media related to the techfest along with landing and responsive CSS. Landing CSS defines the appearance of the website in desktop or any other wide screen mode whereas the responsive CSS attributes are applied when the screen resolution changes to mobile phones.
- **app.py:** The flask application used to host the website.
- **requirements.txt:** Contains the dependancies required to run the website on production environment smoothly.
- **venv:** To simulate a production environment.
- **github/workflows:** Contains deployment jobs that are set up in Azure CICD.
  
## Run Locally

Clone the project

```bash
  git clone https://github.com/Progpr/FinTech-Finance
```

Go to the project directory

```bash
  cd FinTech-Finance
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

First Run the streamlit app in one terminal
```bash
  streamlit run dashboard.py
```
Then run the website in another terminal
```bash
  python -m flask run
```

##Scope

