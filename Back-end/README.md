
Run docker container

# build docker container if dev

1st - ```cd D:\L_pipe\vessel_app_celery\Vessel-app\Back-end```

check the ip address of docker container of database  then check flask-backend ip address in .env 
line environmental varaible DATABASE_URL
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgresql-server-work

2nd step - ```docker build -t flask-openvessel ./```

before your run docker container make sure network was set up prior by database step

# run docker container according to app-tier network

3rd step -  docker run --name flask-openvessel-app -p 5000:5000 --network app-tier flask-openvessel

mounted volume hot reload
```docker run -it --rm --name flask-openvessel-app -p 5000:5000 --network vessel-app-tier -v D:\L_pipe\vessel_app_celery\Vessel-app\Back-end\vessel_app:/vessel_app flask-openvessel
```

When you run docker run it execs a dockfiler linked to shell script that will automatically 
flask db init, flask db migrate, 

if you connect flask app to docker container of postgres expect 
```sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "172.20.0.2", port 5432 failed: Connection timed out (0x0000274C/10060)
        Is the server running on that host and accepting TCP/IP connections? ```

how to interact with database
https://dev.to/steadylearner/how-to-set-up-postgresql-and-pgadmin-with-docker-51h

# Need to do code 
automation updating 
https://stackoverflow.com/questions/44342741/auto-reloading-flask-server-on-docker

# inspect network 