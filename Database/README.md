<!-- https://github.com/docker-library/postgres -->

# Postgres development set up

1st step - ```cd D:\L_pipe\vessel_app_celery\Vessel-app\Database```

2nd step - ```docker build -t openvessel-postgres-database ./```

# network set up

3rd step - ```docker network create vessel-app-tier --driver bridge```

<!-- creating volumes is different from linux to windows https://github.com/docker/for-win/issues/497 -->
4th step - ```docker run --rm --name openvessel-postgresql-server-work -p 5432:5432 --network vessel-app-tier -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password openvessel-postgres-database```

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRESQL_DATABASE=openvessel-database

<!-- docker run bitnami/postgresql:14 -e POSTGRES_USER=postgres -e POSTGRESQL_PASSWORD=password123 -->

run client instance GUI pgadmin

how to interact with database
https://dev.to/steadylearner/how-to-set-up-postgresql-and-pgadmin-with-docker-51h

<!-- 4th step - docker run -it -p 5432:5432 --rm --network app-tier postgresql-server-work psql -h postgresql -U postgres -->