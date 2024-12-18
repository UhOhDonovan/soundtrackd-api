# Designed to be built during the first initialization of the database on the system

FROM mysql:latest AS builder

# That file does the DB initialization but also runs mysql daemon, by removing the last line it will only init
RUN ["sed", "-i", "s/exec \"$@\"/echo \"not running $@\"/", "/usr/local/bin/docker-entrypoint.sh"]

# needed for intialization

ARG MYSQL_ROOT_PASSWORD

ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

COPY initialize.sql /docker-entrypoint-initdb.d/

# Need to change the datadir to something else that /var/lib/mysql because the parent docker file defines it as a volume.
# https://docs.docker.com/engine/reference/builder/#volume :
#       Changing the volume from within the Dockerfile: If any build steps change the data within the volume after
#       it has been declared, those changes will be discarded.
RUN ["/usr/local/bin/docker-entrypoint.sh", "mysqld", "--datadir", "/initialized-db"]

FROM mysql:latest

COPY --from=builder /initialized-db /var/lib/mysql

# run `docker build --build-arg MYSQL_ROOT_PASSWORD=$(cat .env | grep DB_PASSWORD | cut -d '=' -f2) -t soundtrackd-db .` to build the image 
# run `docker run -d --rm --name <container-name> soundtrackd-db` or use docker-compose to start container