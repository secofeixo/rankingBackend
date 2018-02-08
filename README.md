Check the next link for a short description of the exercise
https://docs.google.com/document/d/1gmS7WyLqf9K4UVi7tgCwSuL9S_GPSt9JnfXcjHjfmUE/edit?usp=sharing

# Environment
For running the service, you must have python3 installed, and also nodejs.
My development environment has been:
Mac, with OSX 10.11.6
NodeJS v 6.9.5
Python 3.6.1

# Directories description
The zip file has three directories:
python: here is the code for the service.
client: some node script in order to populate with users and scores
nodejs: a nodeJS http server in order to create a very simple api rest for adding scores, and asking for ranking

# Service 
The service is a TCP server that accepts queries from a client. In this case the client can be any of the scripts in the client folder, or the nodejs http server.

Instead of using standard sockets, it must use some message queue management service, like ZeroMQ (for a simple and non persistent mode) or RabbitMQ (for non-persistent mode and persistent mode). There are other solutions like Kafka, ActiveMQ, ...

The main idea of this service is:
The service has a thread that is checking a variable (ranking.addedScore) in order to know if it has to update the ranking. For other environments instead of this variable will be necessary to use a queue of operations.
When the service accepts a connection it creates a new thread to run the query.
The main idea is to answer to the client as soon as possible. So when the client add a new score, it only updates a dictionary of users and scores and then the service send the response to the client with the new score of the user. It also sets to True the variable ranking.addedScore). Then the thread that calculates the ranking checks the variable to know that if it needs to update the ranking.
In this way when a client ask for the ranking, the service only needs to collect the positions of the ranking without calculating the ranking.
The service has a config file (config.json) with some parameters to configure the tcp server. For instance the port of the server (by default is 4550), the connections allowed by the listen function of the sockets, the maxdatasize of the packets, etc.

Like the service uses threads and the data is shared among all of the threads created, the service needs to access the data shared in a mutex zone. In python I have used a mutex that locks for writing but nor for reading.

# Client
In order to test the service there are three scripts developed in nodejs.
addScore.js: it adds random scores to the users. The variable iNumUsers, set the number of users to add. This script is accumulative, so you can run it many times as you want in order to adding new scores to the users.
queryRanking.js: a script with some query test of ranking.
randomQueryRanking.js: it creates n requests for getting the ranking.The variable iNumRequests specify the number of requests to test.

# NodeJS
Here you can run the http server in order to test the api rest.
The server listens at port 8080.

## API: addScore
entryPoint: http://localhost:8080/addscore
type: POST
body: {“user”:”user”,”total”:1000} or {“user”:”user”,”score”:”+1000”}
return: json object with the new score of the user


## API: getRanking
entryPoint:http://localhost:8080/getranking?query=Top10
type: GET
parameter: ?query=Top10 or ?query=At40/5
return value: an array with json objects with the user, the score and the position in the ranking.


