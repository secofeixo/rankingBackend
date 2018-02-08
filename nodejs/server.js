var url = require('url');
var http = require('http');
var net = require('net');

var sendMessage = function(message, callback){
  var client = new net.Socket();
  var bReceivedData = false;
  var fullData = "";
  var iPortBase = 4550;

  var bErrorConnection = false;
  client.setTimeout(30000, function(){
    console.log((new Date()).toString() + " - " +"server.js. sendMessage. Timeout event.");
    client.end();
    callback("Timeout");
  });

  iPort = iPortBase;
  var connectfunction = function(port){
    client.connect(port,'localhost', function(){
      console.log((new Date()).toString() + " - " +"server.js. sendMessage. Connected to search server.");
      start = Date.now();
      client.write(message);
    });
  };

  connectfunction(iPort);

  client.on('data', function(data) {
    bReceivedData = true;
    fullData = fullData + data;
  });

  client.on('close', function() {
    console.log((new Date()).toString() + " - " +"server.js. sendMessage. Connection closed.");
    var bSendError = false;
    if (bErrorConnection === false)
    {
      if (bReceivedData)
      {
        var end = Date.now();
        var dif = (end - start) / 1000;
        console.log((new Date()).toString() + " - " +"console. Time : " + dif);
        callback(undefined, fullData);
      }
      else
      {
        bSendError = true;
      }
    }
    else
    {
      bSendError = true;
    }
    client.end();
    client.destroy();
    if (bSendError)
    {
      callback("Error");
    }
  });

  client.on('error', function(error) {
    bErrorConnection = true;
    console.log((new Date()).toString() + " - " +"console. Error Event."+error);
    callback(error);
  });
}


http.createServer(function(req, res){
  var myUrl = url.parse(req.url);
  var pathname = myUrl.pathname;

  if (pathname === '/'){
    res.writeHead(200, {"Content-Type": "text/plain"});
    res.end("HomePage");
  }
  else if (pathname === '/addscore'){
    if (req.method == 'POST') {
      console.log("POST");
      var body = '';
      req.on('data', function (data) {
        body += data;
        console.log("Partial body: " + body);
      });
      req.on('end', function () {
        console.log("Body: " + body);
        // send the query to the python server
        sendMessage(body, function(err, data){
          if (err){
              res.writeHead(500, {"Content-Type": "text/plain"});
              res.end(err);
              return;
          }

          res.writeHead(200, {"Content-Type": "application/json"});
          res.end(data);
        })
      });
    }
    else if (req.method == 'GET'){
      res.writeHead(200, {"Content-Type": "text/plain"});
      res.end("Add Score");
    }
  }
  else if (pathname === '/getranking'){
    if (req.method == 'GET') {
      // res.writeHead(200, {"Content-Type": "text/plain"});
      // res.end("Get Ranking");
      var parameters = myUrl.query;
      console.log("Parameters: " + parameters);
      // remove query string
      parameters = parameters.replace("query=", "")
      // send the query to the python server
      sendMessage(parameters, function(err, data){
        if (err){
            res.writeHead(500, {"Content-Type": "text/plain"});
            res.end(err);
            return;
        }
        res.writeHead(200, {"Content-Type": "application/json"});
        res.end(data);
      })
    }
    else{
      res.writeHead(200, {"Content-Type": "text/plain"});
      res.end("POST query not allowed");
    }

  }
  else{
    res.writeHead(404, {"Content-Type": "text/plain"});
    res.end("Page not found");
  }
}).listen(8080);
console.log("Server running at port 8080");
