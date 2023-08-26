###:snake:Environment Setup
1. Install vscode
2. Install Python pyenv 
3. Install python 3.8.6 using pyenv (Pyevn cheat sheet added below)
   >>video link to install pyenv and python
   ```sh
   https://www.youtube.com/watch?v=HTx18uyyHw8
   ```
   ```sh
   https://k0nze.dev/posts/install-pyenv-venv-vscode/
   ```
4. Activate it in powershell(vscode)
```sh
pyenv shell 3.8.6
```
5. Install dependent extension
   ```sh
   1. DVC
2. autoDocstring-Python
3. autopep8 : formatting python official guideline
4. Bracket Pair Colorization Togglers
5. Dev Containers: can be replaced by docker
6. Docker
7. Excel Viewer
8. Flake8 : works on python code writting style issue
9. Git History : Github history details
10. IntelliCode : not mandatory
11. IntelliCode API Usage Examples: not mandatory
12. isort: python
13. Jupyter
14. Jupyter Cell Tags
15. Jupyter Keymap
16. Jupyter Notebook Renderers
17. Jupyter Slide Show
18. Markdown All in One
19. Markdown Preview Enhanced
20. Material Icon Theme: not mandatory
21. Path Autocomplete
22. Pylance
23. Pylint
24. Python
25. Rainbow CSV
26. Regex Previewer
27. Remote-SSH: connects aws server /any cloud server and make it easier
28. Remote-SSH: Editing Configuration File:
29. Remote Explorer: 
30. REST Client: unknown
31. settings Sync: not explain: This extension is deprecated
32. TODO Highlights: by Wayou Liu; add comments on code / future coarse of work
33. Trailing Spaces: remove unnecessary space in code
```

   
6. Use vscode for EDA and other project related work
7. Install wsl and run linux over windows operating system
8. Install Docker 
9.  create virtual environment for the project under powershell
>> pip install virtualenv
>> python -m venv mlops_env
To activate virtual env in powershell(vscode)
>>.\mlops_env\Scripts\activate
note: select python kernel  (View >> Command Palette >> Python(select interpreter) >> Python 3.8.6 (mlops_env: venv)
1. install requiered python libaries after activating the virtual env
a. at first, 
pip install scikit-learn
pip install xgboost
pip install catboost

then other libaries
>>pip install -r notebook_requirements.txt 

7. to upload files / project in github
>> git push


