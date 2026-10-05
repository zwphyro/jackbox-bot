### Jackbox bot

#### Configuration

The application is configured via the `settings.local.yaml` file. Copy the [`settings.local.example.yaml`](config/settings.local.example.yaml) file, rename it to `settings.local.yaml`, and set the `api_key` field to your key for the *OpenAI API* or any other provider compatible with the `openai` library.

#### Running

> [!WARNING]
> *Python* 3.13 or higher must be installed on your device!  
> Using *uv* for dependency management and running the app is recommended.

##### Installing dependencies

If you are using *uv*, run the following commands:
```sh
uv sync --locked
source .venv/bin/activate
```
If you are using *poetry*, run the following commands:
```sh
poetry install --no-root
eval $(poetry env activate)
```
Otherwise, use *pip*:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Next, install the *playwright* dependencies:
```sh
playwright install chromium
```

##### Starting the app

Run the application locally with the following command:
```sh
uv run task start --room-code <room code>
```
Or:
```sh
python -m command.main --room-code <room code>
```

#### Supported games

Currently, the bot only supports *Survive The Internet*. Support for *Joke Boat* and *Quiplash* is planned for the future.
