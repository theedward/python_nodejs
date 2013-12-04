var arguments = process.argv.splice(2);
var httpProxy = require('http-proxy');

//
// Addresses to use in the round robin proxy
//
var addresses = [
    {
        host: '130.223.42.118',
        port: 8001
    },
    {
        host: '130.223.42.118',
        port: 8002
    },
    {
        host: '130.223.42.118',
        port: 8003
    }
];

var i = 0;
httpProxy.createServer(function (req, res, proxy) {
    proxy.proxyRequest(req, res, addresses[i]);

    i = (i + 1) % addresses.length;
}).listen(arguments[0] || 8000);
