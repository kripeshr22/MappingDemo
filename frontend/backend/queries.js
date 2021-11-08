require('dotenv').config(); //Allows retriving variables from the .env file

//For Heroku postgres
const { Pool } = require('pg');
const pool = new Pool({
    connectionString: process.env.DATABASE_URI,
    ssl: true,
});

async function testFunction (request, response) {
    console.log('Request for data received by testFunction');
    response.status(200).json("Request for data received by testFunction");
}

async function testGet (request, response) {
    console.log('Request for data received by testGet');

    try{
        const dbase = await pool.connect();
        const rowList = await dbase.query('SELECT * FROM rawparceltable');
        response.status(200).send(rowList);
    } catch (error){
        response.status(400).json('SERVER RESP: Error retrieving userrecords. Log:'+error)
        console.log('Error retrieving userrecords. Log:')
        console.log(error);
    }
}

async function testHerokuPg (request, response) {
    console.log('Request for data received by testHerokuPg');

    try{
        const dbase = await pool.connect();
        const result = await dbase.query('SELECT * FROM rawparceltable');
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