# Soundtrackd Backend

[Pip packages](requirements.txt)

Python version: 3.11

## Getting Started

Clone the repository:

```git clone https://github.com/UhOhDonovan/soundtrackd-api```

Install pip packages (It is recommended to use a virtual environment for this):

```pip install -r requirements.txt```

Create a `.env` file in the project root. Include an entry for `API_SECRET_KEY` and `DB_PASSWORD`:

```.env
API_SECRET_KEY=<your secret key>
DB_PASSWORD=<your database password>
```

These are secrets that will be read by the application to be used for user authentication and db access.

## Initializing the Database

**Make sure you have Docker and Docker Compose installed**

CD into the `/database` directory.

Run `docker build --build-arg MYSQL_ROOT_PASSWORD=$(cat .env | grep DB_PASSWORD | cut -d '=' -f2) -t soundtrackd-db .` to build the image.

Navigate back to project root.

To start a mysql container, run `docker-compose up -d db`

## Running the API

To run a local instance of the api, make sure the python version of your environment is 3.11, and you have all dependencies installed. Run:

```sh
python -m app
```

to start the api.

If you are using VSCode, you can use the provided debug configuration to run the api. This allows you to run the application with breakpoints and variable inspection, and it's *super* useful for debugging. Just go to the "Run and Debug" tab in the primary side bar and select the `Soundtrackd API: Module` configuration. Press the green play button to run it. *You may need to have an sh based terminal as your default integrated terminal for this to work by default*.

## Deploying the Backend

Soundtrackd uses docker to deploy containers for each layer of its archicture. The dockerfile for the api is found in the project root. The dockerfile for the database is found in `/database` in the project root.

Follow the steps above to build the db image. Make sure the image is named `soundtrackd-db` if you want to use docker compose.

To build the api image, in the project root run:

```sh
docker build -t soundtrackd-api .
```

The dockerfile will load the .env file, so make sure one is created first.

Once both containers are built, you can use the docker-compose.yml file to spin up containers for both the database and api services. The database service will create a volume named after the image to preserve database information if the container goes down. To spin up both containers, in the project root run:

```sh
docker-compose up -d
```

To spin up just one container, run:

```sh
docker-compose up -d <service name>
```

The api container will publish to port 5345 and the db container will publish to port 3306 by default. These services can be deployed to a web container such as a Kubernetes cluster on Azure or behind a reverse proxy such as Traefik. Use a DNS provider such as Cloudflare to point a domain name rule to your server's public ip. Voila! You have sucessfully deployed the Soundtrackd backend!

## WARNING

One thing to note is that when recreating the database with a new password, the data volume that contains all the container information needs to be removed, and the image completely rebuild with no cache. To remove the data volume, stop the container, then run:

```sh
docker volume rm <volume name>
docker system prune -a
docker build --no-cache --build-arg MYSQL_ROOT_PASSWORD=$(cat .env | grep DB_PASSWORD | cut -d '=' -f2) -t soundtrackd-db ./database
```

This will completely wipe the database and refresh it without any local caching. Do this only if you need a completely new database system with new authentication, and you are willing to permanently lose all data currently in your database.
