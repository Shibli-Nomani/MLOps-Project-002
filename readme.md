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

then other libaries
>>pip install -r notebook_requirements.txt 

7. to upload files / project in github
>> git push


