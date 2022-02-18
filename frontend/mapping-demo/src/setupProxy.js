const { createProxyMiddleware } = require('http-proxy-middleware')

//Use this to create a proxy to the Express server port 6000 instead of specifying proxy in package.json
module.exports = app => {
    //Sends proxy request to http://localhost:6000/*
    app.use('/server/*', createProxyMiddleware({ target: process.env.HEROKU_URL, changeOrigin: true }))
};