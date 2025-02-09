# next_restaurant

## Introduction
This project is focused upon the location Berlin. We have huge numbers of restaurant in Berlin and with this app, we try to use data of existing restaurants to predict best locations to open next restaurant.

## Install

Go to `https://github.com/shanudengre82/next_restaurant` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/next_restaurant.git
cd next_restaurant

poetry install
```
Functional test with a script:

```bash
cd
mkdir tmp
cd tmp
next_restaurant-run
```
