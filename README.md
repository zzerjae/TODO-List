<h1 align="center">📒 TODO_List 😎</h1>

<p align="center">
	<a href="https://github.com/jaeho93/TODO-List/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
	<a href="https://travis-ci.com/jaeho93/TODO-List/"><img src="https://travis-ci.com/jaeho93/TODO-List.svg?token=uXH6DrxqNzFngpRF4bXk&branch=master"></a>	
</p>

## Overview

> Simple TODO List Project

<br>
<div align="middle">
<img src="https://github.com/jaeho93/TODO-List/blob/master/img/overview.png">
<br>
figure 1. Main Page
</div>

<br>

******

1. [Demo](#Demo)
2. [How to Run](#How__to_Run)
3. [Dev Stack](#Dev_Stack)
4. [License](#license)

******


## Demo

You can see demo [here](https://winter1.azurewebsites.net/todo/).

## How_to_Run

> ### You need Docker Environment.
>

```bash
# You need to replace "YOUR_DB_THINGS" of yours
# on docker_run.sh / docker_setup.sh
# before below procedure.

# Build Docker Image.
> docker build -t todolist .

# Run Docker for setup and run test server
> ./docker_setup.sh
> python3 manage.py makemigrations
> python3 manage.py migrate
> python3 manage.py createsuperuser
> python3 manage.py runserver 0.0.0.0:80
> exit

# Finally, you can run the App.
> ./docker_run.sh

# go and check http://127.0.0.1:8080/todo/
```


## Dev_Stack

> ### BackEnd
> - Python 3.6.7
> - Django 2.1.2
> - PostgreSQL
>
> ### DevOps
> - Docker
> - Azure Database for PostgreSQL server
> - Azure Web App for Containers
> - Travis CI
>
> ### FrontEnd
> - Bootstrap4
> - jQuery


## License

* [MIT License](LICENSE)
