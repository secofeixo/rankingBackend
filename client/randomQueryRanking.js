/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

require('events').EventEmitter.prototype._maxListeners = 100;

var net = require('net');

var iNumOp = 0;

var sendRequest = function(ranking){
  var iPortBase = 4550;
  var iPort = iPortBase;
  var iMaxPorts = 9;
  var start = Date.now();
  var client = new net.Socket();

  var connectfunction = function(port){
  	client.connect(port,'localhost', function(){
  		var end = Date.now();
  		var dif = (end - start) / 1000;
  		console.log('Query: '+ ranking + 'Time : ' + dif);
  		start = Date.now();
      client.write(ranking);
  	});
  };

  connectfunction(iPort);

  client.on('error', function (data){
  	console.log('Query: '+ ranking +  '. Error : ' + data);
  	if (iPort < (iPortBase + iMaxPorts))
  	{
  		iPort = iPort + 1;
  		connectfunction(iPort);
  	}
  	else
  	{
  		var end = Date.now();
  		var dif = (end - start) / 1000;
  		console.log('Query: '+ ranking +  '. Time : ' + dif);
  	}
  });

  client.on('data', function(data) {
  	console.log('Query: '+ ranking +  '. Received : ' + data);
  	var end = Date.now();
  	var dif = (end - start) / 1000;
  	console.log('Query: '+ ranking +  '. Time : ' + dif);
  });

  client.on('close', function() {
  	console.log('Query: '+ ranking +  + '. Connection closed ');
  });

}

var iNumRequests = 1000;

for(var i= 0; i < iNumRequests; i++){
  value = Math.floor(Math.random() * 100);
  value2 = Math.floor(Math.random() * 10);
  op = Math.floor(Math.random() *10) % 2;
  console.log('Op: ' + op + '. value: ' + value + '. value2: ' + value2);
  ranking = ""
  if (op == 0){
    ranking = "Top" + value.toString();
  }
  else if (op == 1){
    ranking = "At" + value.toString() + "/" + value2.toString();
  }
  sendRequest(ranking)
}
