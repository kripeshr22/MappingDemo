//Require the express module, built in bodyParser middlware, and set our app and port variables
const express = require('express');
const app = express();
cons router = express.Router();
const serverless = require('serverless-http');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config(); //Allows retriving variables from the .env file

//Defined in .env file
const port = process.env.PORT || 6000;
console.log(`PORT given to server: ${process.env.PORT}`)

//To get all the exported functions from queries.js, we'll 'require' the file and assign it to a variable.
const db = require('./backend/queries.js')

// Use bodyParser to parse JSON
app.use(bodyParser.json())
app.use('/.netlify/functions/server', router);


app.get("/server/testFunction", db.testFunction)
app.get("/server/testGet", db.testGet)
app.get("/server/testHerokuPg", db.testHerokuPg)

//Used only in local development where there is no build step.
if(process.env.NODE_ENV != "production"){
    //tell a route making a GET request on the root (/) URL to head to the HomePage
    app.get("/server/", (request, response) => {
        if (error) {
            throw error
        }
        response.sendFile(__dirname + '/mapping-demo/public/index.html');
        //response.send("Server running on Node.js, Express, and Postgres API")
        //response.json({ info: "Server running on Node.js, Express, and Postgres API" });
    })

    //Static file declaration, which is the location of the React app
    //Used in deployment by React app to access index.js
    app.use(express.static(path.join(__dirname, 'mapping-demo')));

    //Put this last among all routes. Otherwise, it will return HTML to all fetch requests and trip up CORS. They interrupt each other
    // For any request that doesn't match, this sends the index.html file from the client. This is used for all of our React code.
    //Eliminates need to set redirect in package.json at start script with concurrently
    app.get('*', (req, res) => {
        res.sendFile(path.join(__dirname+'/mapping-demo/public/index.html'));
    })
}
//Only used in production, since I do not build before running in development
if(process.env.NODE_ENV == "production"){
    //tell a route making a GET request on the root (/) URL to head to the HomePage
    app.get("/server/", (request, response) => {
        if (error) {
            throw error
        }
        response.sendFile(__dirname + '/frontend/build/index.html');
        //response.send("Server running on Node.js, Express, and Postgres API")
        //response.json({ info: "Server running on Node.js, Express, and Postgres API" });
    })

    //Static file declaration, which is the location of the React app
    //Used in deployment by React app to access index.js
    app.use(express.static(path.join(__dirname, 'frontend/build')));

    //Put this last among all routes. Otherwise, it will return HTML to all fetch requests and trip up CORS. They interrupt each other
    // For any request that doesn't match, this sends the index.html file from the client. This is used for all of our React code.
    //Eliminates need to set redirect in package.json at start script with concurrently
    app.get('*', (req, res) => {
        res.sendFile(path.join(__dirname+'/frontend/build/index.html'));
    })
}

/*set the app to listen on the port you set*/
app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})

module.exports.handler = serverless(app);