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