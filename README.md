# Gifty

## Getting started with Docker

This project includes a Dockerfile and docker-compose.yml that will setup all the necessary services and dependencies to run this project.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop). This will also install docker-compose, which you will use to build the container.
2. From a terminal window, run `docker-compose up` to start up the docker container. This starts the following services:

#### db
Creates a MySQL database named `gifty` and starts the database server.

#### web
Starts the django webserver running at localhost:3000

#### scss
Start a scss compiler that watches scss files and compiles to css.# niftygifter
