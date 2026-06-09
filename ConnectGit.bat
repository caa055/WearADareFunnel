@echo off

git config --global user.email "art.nas@yahoo.com"
git config --global user.name "caa055"

:: Initialize git in your local project folder
git init

:: Track all your project files
git add .

:: Save the current state
git commit -m "Initial storefront layout"

:: Point your local files to your new GitHub repository
:: (Replace the URL below with your actual GitHub repository URL)
git remote add origin https://github.com/caa055/WearADareFunnel.git

:: Push the code to the cloud
git branch -M main
git push -u origin main

:: ----- IF ERRORS THEN FORCE IT:
:: git remote set-url origin https://github.com/caa055/WearADareFunnel.git
:: git push -u origin main

:: ------ AFTER IT'S ALL WORKING THEN:
:: Go to your repository page on the GitHub website.
:: Click on Settings (the gear icon at the top menu bar.
:: On the left sidebar, click on Pages.
:: Under Build and deployment -> Source, click the dropdown and change it from "Deploy from a branch" to "GitHub Actions".

::  https://caa055.github.io/WearADareFunnel/