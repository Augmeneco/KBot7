## Оглавление

1. [Install](#Install)
2. [Config](#Config)
3. [Run](#Run)

# Install 
## Ubuntu 18.04
```bash
git clone https://github.com/Augmeneco/KBot7
cd KBot7
pip3 install requests untangle bs4 pillow
```

## Windows
Поддержки нет, но я верю в тебя

# Config
Создай файл "config.json" в папке "data" и заполни его нужной информацией
```json
{
"group_token":"токен группы",
"user_token":"токен юзера",
"group_id": ид,
"names":["кб","кбот","kb","кл","kbot","карина","кв","бот"],
"version":"0.1"
}

```
# Run
```bash
while true; do python3 main.py; sleep 1; done
```
