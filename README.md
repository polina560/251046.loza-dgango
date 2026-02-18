Активировация виртуальной среды
- в PowerShell
```shell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

Устаовка зависимостей
```shell
pip install -r requirements.txt
```

- в командной строке
```shell
.venv\Scripts\activate.bat
```

Обновить переводы
```shell
django-admin compilemessages 
```