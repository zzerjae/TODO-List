<h1 align="center">📷 TODO_List 😎</h1>

<p align="center">
	<a href="https://github.com/jaeho93/TODO-List/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
</p>
<p align="center">
	<a href="https://travis-ci.com/jaeho93/TODO-List/"><img src="https://travis-ci.com/jaeho93/TODO-List.svg?token=uXH6DrxqNzFngpRF4bXk&branch=master/"></a>	
</p>

## Overview

> Simple TODO_-List Project

<br>
<div align="middle">
<img src="https://github.com/jaeho93/TODO-List/blob/master/img/overview.png">
<br>
figure 1. Main Page
</div>

<br>
*****

1. [Demo](#Demo)
2. [How to Run](#How__to_Run)
3. [License](#license)

*****


## Demo

you can see demo [here](https://winter1.azurewebsites.net/todo/)

## How_to_Run

> # You need Docker Environment.
>
> ```bash
> # You need to replace "YOUR_DB_THINGS" of yours
> # on docker_run.sh / docker_setup.sh
> # before below procedure.
> 
> # Build Docker Image.
> ~/TODO_List > docker build -t todolist .
> 
> # Run Docker for setup.
> ~/TODO_List > ./docker_setup.sh
> /code > python3 manage.py makemigrations
> /code > python3 manage.py migrate
> /code > python3 manage.py createsuperuser
> /code > exit
> 
> # Finally, you can run the App.
> ~/TODO_List > ./docker_run.sh
> 
> # go and check http://127.0.0.1:8080/todo/
> ```
>


## License

* [MIT License](LICENSE)
