# RedditToxicityDataset

## Instanciate MongoDB docker container

`sudo docker run --name mongodb -d -p 27017:27017 -v $(pwd)/mongo:/data/db mongodb/mongodb-community-server:latest`