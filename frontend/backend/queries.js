require('dotenv').config(); //Allows retriving variables from the .env file

//For Heroku postgres
const { Client } = require('pg');
const client = new Client({
    connectionString: process.env.DATABASE_URI,
    ssl: { rejectUnauthorized: false }
});
client.connect();

async function testFunction (request, response) {
    console.log('Request for data received by testFunction');
    response.status(200).json("Request for data received by testFunction");
}

async function testGet (request, response) {
    console.log('Request for data received by testGet');

    try{
        console.log('Succesfully connected')
        const rowList = await client.query('SELECT * FROM cleanlacountytable2 LIMIT 10000');
        const results = { 'results': (rowList) ? rowList.rows : null};
        // console.log(results);
        response.status(200).send(results);
    } catch (error){
        response.status(400).json('SERVER RESP: Error retrieving userrecords. Log:'+error)
        console.log('Error retrieving userrecords. Log:')
        console.log(error);
    }
}

async function testHerokuPg (request, response) {
    console.log('Request for data received by testHerokuPg');

    try{
        const result = await client.query('SELECT * FROM rawParcelTable');
        const results = { 'results': (result) ? result.rows : null};
        response.status(200).send(results);
    } catch (error){
        console.error(error);
        response.send("Error " + error);
    }
}

module.exports = {
    testFunction,
    testGet,
    testHerokuPg
}