/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

require('events').EventEmitter.prototype._maxListeners = 100;

var net = require('net');

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

sendRequest("top10000000000?skip=30&limit=30");
sendRequest("textoaleatorio");
sendRequest("10000");
sendRequest("Top10000000000?limit=100");
sendRequest("Top10");
sendRequest("Top1000?limit=25");
sendRequest("Top500?limit=250");
sendRequest("Top-10000000000");
sendRequest("Top");
sendRequest("Top0");
sendRequest("At0/-4");
sendRequest("At-4/-4");
sendRequest("At0/4");
sendRequest("At1/4");
sendRequest("At1000000000/4");
sendRequest("At1000000000/4");
sendRequest("At15/0");
sendRequest("At1000000000/1000000000?limit=100");
sendRequest("At1000000000/-1000000000");
sendRequest("At1000000000/text/dad");
sendRequest("At/text/dad");
sendRequest("Attext/56");
sendRequest("text/dad");
