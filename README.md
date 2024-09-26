# Projet SoftDesk

Cette application est un projet de création d'une API RESTful avec Django REST Framework.

## Installation

### Clonez le dépôt

Pour cloner le dépôt, vous devrez ouvrir le terminal et effectuer la commande suivante dans le dossier de votre choix :
```bash
git clone https://github.com/Fibuc/SoftDesk.git
```
Ensuite déplacez-vous dans le dossier créé par le clonage nommé `SoftDesk` avec la commande suivante :

```bash
cd SoftDesk
```

### Installation via `pipenv`

Dans ce projet, on va utiliser `Pipenv` afin de gérer les dépendances.
Si vous avez déjà `Pipenv`, vous pouvez directement passer à l'étape de création de l'environnement virtuel.

Sinon, voici comment installer basiquement `Pipenv` sur votre système d'exploitation :

```bash
pip install pipenv
```

Pour une installation personnalisée, vous pouvez vous référer à la [documentation de Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Créez un environnement virtuel & installation des packages

Ouvrez le terminal et rendez-vous dans le dossier du dépôt local du projet, puis tapez la commande suivante :

```bash
pipenv install
```
Lorsque vous avez effectué cette commande, les packages ont automatiquement été installés dans votre environnement virtuel `Pipenv`.

### Utilisez/activez votre environnement virtuel

Avec `Pipenv`, il existe 2 méthodes afin d'utiliser votre environnement virtuel.

#### Utilisation de Pipenv run

Grâce à cette méthode, vous pouvez exécuter directement le fichier via:

```bash
pipenv run python manage.py runserver
```

Vous n'avez pas besoin d'activer d'environnement virtuel dans le dossier du dépôt.

#### Utilisation du shell Pipenv

Vous pouvez également choisir d'activer votre environnement virtuel via le shell python qui sera activé par la commande suivante:

```bash
pipenv shell
```
Puis faite votre commande comme dans l'exemple.

```bash
# Exemple
python manage.py runserver
```

Veillez également à bien vous situer sur la branche "main" lors de l'exécution de **main.py**.

### Installation via `pip`

Si vous souhaitez utiliser un environnement virtuel classique via `pip` alors il vous suffit de créer un environnement virtuel que vous devrez nommer `env` afin d'éviter son push dans le repository. Si toutefois, vous voulez utiliser un autre nom d'environnement, ajoutez-le au fichier `.gitignore`.

Ouvrez le terminal et rendez-vous dans le dossier du dépôt local du projet, puis tapez la commande suivante :

```bash
python -m venv nom_de_l_environnement
```

#### Activez votre environnement virtuel

Pour activer votre environnement virtuel, la méthode est différente selon votre système d'exploitation.

##### Linux & MacOS :
```bash
source chemin_de_votre_env/bin/activate
```
##### Windows : 

CMD :
```bash
chemin_de_votre_env\Scripts\activate.bat
```

PowerShell :
```bash
chemin_de_votre_env\Scripts\activate.ps1
```

Veillez également à bien vous situer sur la branche "main" lors de l'exécution de **main.py**.

### Installez les packages

Lorsque vous aurez activé votre environnement virtuel, vous aurez également besoin d'installer les packages essentiels pour le lancement disponibles dans le requirements.txt.

```bash
pip install -r requirements.txt
```

### Lancer le serveur

Maintenant que les packages ont été installés, on va pouvoir lancer le serveur afin de pouvoir accéder à l'API.

On va se rendre dans le dossier `src` et lancer la commande suivante :

```bash
python manage.py runserver
```
Et voilà, maintenant que le serveur est lancé, on va pouvoir utiliser notre API.

## Utilisation de l'API

Pour utiliser l'API, on va utiliser l'application [Postman](https://www.postman.com/) qui va nous permettre d'utiliser nos endpoints facilement.

Vous retrouverez toute la documentation des `endpoints` et de l'API via la [documentation Postman](https://documenter.getpostman.com/view/34602535/2sAXjGduhA#auth-info-816b6102-7f95-4815-baf0-a2ae5f4fc558).

## Générez un rapport flake8

L'application a été contrôlée par Flake8. Vous trouverez le rapport en ouvrant le fichier `index.html` se trouvant dans le dossier `flake8_rapport`.

Pour générer un nouveau rapport flake8 de l'application en format HTML, vous devrez ouvrir votre terminal et vous rendre à la racine de l'application puis utiliser la fonction suivante:

```bash
flake8 --format=html --htmldir=flake8_rapport
```

Ce nouveau rapport sera généré dans le dossier "flake8_rapport".
