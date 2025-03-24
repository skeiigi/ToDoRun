This is an Information Security project. As a team, together with our classmates, we are making a web application in Django.

[Дока на русском](./docs/README.ru.md)

## Installation and launch

Cloning the slokaln repository project

```bash
git clone https://github.com/skeiigi/ToDoRun.git
```

Going to the project directory

```bash
cd ToDoRun
```

## Launch (automation)

```bash
chmod +x deployment-environment.sh
./deployment-environment.sh
```

## Launch (manual)

Creating the viral environment

```bash
python -m venv venv  # windows
python3 -m venv myenv  # mac/linux 
```

Activation the viral environment

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # if error
.\venv\Scripts\Activate.ps1  # windows poweshell
source myenv/bin/activate  # mac/linux
```

Downloading project dependencies

```bash
pip install -r requirements.txt
```

## Start project

Script start

```bash
chmod +x project-app.sh
./project-app.sh
```

Manual start

```bash
cd src
python manage.py runserver
```
