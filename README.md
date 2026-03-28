# Jackbox bot

## Конфигурация

Для конфигурации приложения используется файл `settings.local.yaml`, скопируйте файл [`settings.local.example.yaml`](config/settings.local.example.yaml) и переименуете его в `settings.local.yaml`, укажите в нем ключ для доступа к *OpenAI API* или любому другому провайдеру, поддерживающему работу с библиотекой `openai`, в поле `api_key`.

## Запуск

> [!WARNING]
> *Python* версии не ниже 3.13 должен быть установлен на вашем устройстве!  
> Предпочтительно использовать *uv* для управления зависимостями и запуска.

### Установка зависимостей

Если вы используете *uv*, введите следующую команды:
```sh
uv sync --locked
source .venv/bin/activate
``` 
Если вы используете *poetry*, введите следующие команды:
```sh
poetry install --no-root
eval $(poetry env activate)
``` 
Иначе используйте *pip*:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Далее установите зависимости *playwright*:
```sh
playwright install chromium
```

### Запуск

Запустите приложение локально с помощью следующей команды:
```sh
uv run task start --room-code <код комнаты>
```
Или:
```sh
python -m cmd.jackbox_bot.main --room-code <код комнаты>
```

## Поддерживаемые игры

Сейчас бот поддерживает только *Survive The Internet*, в будущем также планируется поддержка *Joke boat* и *Quiplash*.
