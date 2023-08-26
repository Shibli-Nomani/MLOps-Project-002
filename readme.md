1. Install Python pyenv and activate it in powershell
>>pyenv shell 3.8.6
2. Use vscode for EDA and other project related work
3. Install wsl and run linux over windows operating system
4. Install Docker 
5. create virtual environment for the project under powershell
>> pip install virtualenv
>> python -m venv mlops_env
To activate virtual env in powershell(vscode)
>>.\mlops_env\Scripts\activate
note: select python kernel  (View >> Command Palette >> Python(select interpreter) >> Python 3.8.6 (mlops_env: venv)
6. install requiered python libaries after activating the virtual env
a. at first, 
pip install scikit-learn
pip install xgboost
pip install catboost
others...
```
🎆or use and install listed libaries as per dependancy 
```sh
notebook_requirements.txt
```
powerhell command
```sh
pip install -r notebook_requirements.txt 
```
1.  Performing EDA and Model Bulding over Dataset in **notebook**
2.  👻 add .gitignore in project directory to ignore the files that you don't want to push in git
    
3.  to upload files / project in github
    >> a. Source Control >> select git repo >> commit
4.  apply git push under virtual env powershell for any new change
```sh
git push
```


