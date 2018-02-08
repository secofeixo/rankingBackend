/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

require('events').EventEmitter.prototype._maxListeners = 100;

var net = require('net');

var sendRequest = function(user, field, value){
  var iPortBase = 4550;
  var iPort = iPortBase;
  var iMaxPorts = 9;
  var start = Date.now();
  var client = new net.Socket();

  var connectfunction = function(port){
  	client.connect(port,'localhost', function(){
  		var end = Date.now();
  		var dif = (end - start) / 1000;
  		console.log('User: '+ user + '. Time : ' + dif);

      console.log('User: '+ user + '. Connected at port ' + port + '. Field: ' + field + '. Value: ' + value);
  		start = Date.now();
  		var sQuery = '{"user":"' + user + '","' + field + '":' + value + '}';
      client.write(sQuery);
  	});
  };

  connectfunction(iPort);

  client.on('error', function (data){
  	console.log('User: '+ user + '. Error : ' + data);
  	if (iPort < (iPortBase + iMaxPorts))
  	{
  		iPort = iPort + 1;
  		connectfunction(iPort);
  	}
  	else
  	{
  		var end = Date.now();
  		var dif = (end - start) / 1000;
  		console.log('User: '+ user + '. Time : ' + dif);
  	}
  });

  client.on('data', function(data) {
  	console.log('User: '+ user + '. Received : ' + data);
  	var end = Date.now();
  	var dif = (end - start) / 1000;
  	console.log('User: '+ user + '. Time : ' + dif);
  });

  client.on('close', function() {
  	console.log('User: '+ user + '. Connection closed ');
  });

}

var iNumUsers = 1000;

var asyncSendRequest = function (i){
  value = Math.floor(Math.random() * 100);
  op = Math.floor(Math.random() *10) % 3;
  console.log('user: ' + i + '. op: ' + op + '. value: ' + value);
  sUser = "user" + i.toString();
  if (op == 0){
    sendRequest(sUser, 'total', value)
  }
  else if (op == 1){
    sendRequest(sUser, 'score', value)
  }
  else if (op==2){
    sendRequest(sUser, 'score', -value)
  }
  i++;
  if (i < iNumUsers){
    setTimeout(function(){
      asyncSendRequest(i)}, 10);
  }
}

i = 0;
asyncSendRequest(i);
