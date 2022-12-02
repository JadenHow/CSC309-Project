The following assumes your current working directory is PB.

To setup the project (build your venv), run:
```
 ./startup.sh
```

To run the project, run:
```
 ./run.sh
```

An automatic admin account will be created for you. The credentials are:
username: admin
password: 123

API documentation is at docs.html and in the Postman collection. Unfortunately, there's a compatibility issue with the docs package we used, drf-yasg, so this is a simplified version of it. Should suffice though. If it's unclear, you can upload the docs.json file to https://editor-next.swagger.io.