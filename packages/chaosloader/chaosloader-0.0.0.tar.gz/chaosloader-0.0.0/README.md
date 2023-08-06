[![Build Status](https://travis-ci.org/albertoig/chaos-loader.svg?branch=master)](https://travis-ci.org/albertoig/chaos-loader)
# chaos-loader
Chaos loader is a mono repository organizer to make a project easy to develop under a docker based project.

# Road map
+ Detection of .env.json and create a .env if not exists with the specific configuration.
+ Detection of docker-compose.yml and alert if not exists in the root project or specific folder.
+ Detection of .chaos-loader.json configuration and load to run with a specific configuration.
+ Detection of docker compose command cli if not exists will throw an error.
