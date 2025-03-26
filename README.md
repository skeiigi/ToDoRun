# To Do Run

This is an Information Security project. As a team, together with our classmates, we are making a web application in Django.

## Documentation

- [Дока на русском](./docs/README.ru.md)
- [Guides](./docs/)
  - A guide on how to use prt-commit [EN](./docs/pre-commit/PRE-COMMIT.en.md)/[RU](./docs/pre-commit/PRE-COMMIT.ru.md)
  - How to run in docker [EN](./docs/docker/DOCKER.en.md)/[RU](./docs/docker/DOCKER.ru.md)

## Installation and launch

Cloning repository project

```bash
git clone https://github.com/skeiigi/ToDoRun.git
```

Going to the project directory

```bash
cd ToDoRun
```

## Before running the scripts

You need to open  **Git Bash**, find the repository ToDoRun using **cd**.
<br><br>**IMPORTANT** (use "/")<br>
```bash
D:/one/two/three/ToDoRun
```


## Launch (automation)

```bash
chmod +x deployment-environment.sh
./deployment-environment.sh
```

In PowerShell __(recommended for Windows)__

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deployment-environment.ps1
```

## Launch and migration (manual)

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

## Start migration (manual)

```bash
cd src
python manage.py makemigrations
python manage.py migrate
cd ..
```

## Start project

Script start

```bash
chmod +x project-app.sh
./project-app.sh
```

In PowerShell __(recommended for Windows)__

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\project-app.ps1
```

Manual start

```bash
cd src
python manage.py runserver
```
