# Problematica
Unsolved problems get solved, in style!

[![GitHub release](https://img.shields.io/github/release/Techmaz/Problematica-public.svg)](https://github.com/TechMaz/Problematica-public/releases)
[![Build Status](https://travis-ci.org/TechMaz/Problematica-public.svg?branch=master)](https://travis-ci.org/TechMaz/Problematica-public)
[![GitHub issues](https://img.shields.io/github/issues/TechMaz/Problematica-public.svg)](https://github.com/TechMaz/Problematica-public/issues)  


## Table of Contents:

###Getting Started  
[Setting up your virtual environment](#setting-up-your-virtual-environment)  
[Set up environment variables](#set-up-environment-variables)  
[Running the app](#running-the-app)  


##Getting Started  
**Note:** Development currently limited to those who have access to our Heroku account.

###Setting up your virtual environment:  

1. Install the virtualenv package by running `pip install virtualenv`.
1. Create a folder called `virtualenv` at the same level as the root folder of the cloned Problematica repo.
1. cd into the new folder and create a virtualenv called problematica by running the command: `virtualenv problematica`
1. Go back into the root of our repo and run the script that I wrote for enabling the virtualenv by running the following command: `source scripts/start-venv.sh`
1. Verify that you are in the correct venv by running: `pip -V`. It should show the project folder, not a global disk folder.
1. Make sure your new virtualenv has the packages listed in requirements.txt by running `pip install -r requirements.txt`
1. You should be all set to run the project locally!

###Set up environment variables:  

1. Create a new file named `.env` containing all the sensitive data that will be needed, in the following format:
``` 
ROOT_URL='https://problematica.herokuapp.com/'
DATABASE_URL='value'
ADMIN_PW=value
STRIPE_API_KEY=value
STRIPE_CHECKOUT_KEY=value
```
replacing the value text by the actual keys and passwords that are being used.  

###Running the app:  

For current developers with access to Heroku, run the command `heroku local web` 
