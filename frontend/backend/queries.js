require('dotenv').config(); //Allows retriving variables from the .env file

//For Heroku postgres
const { Pool, Client } = require('pg');
const pool = new Pool({
    // user: "ub5debmb55aodh",
    // host: "ec2-52-201-66-148.compute-1.amazonaws.com",
    // database: "d44ns4ruujn4nq",
    // password: "pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163",
    // port: "5432"
    connectionString: process.env.DATABASE_URI
});

const client = new Client({
    user: "ub5debmb55aodh",
    host: "ec2-52-201-66-148.compute-1.amazonaws.com",
    database: "d44ns4ruujn4nq",
    password: "pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163",
    port: "5432",
    ssl: true,
    // connectionString: process.env.DATABASE_URI
});

async function testFunction (request, response) {
    console.log('Request for data received by testFunction');
    response.status(200).json("Request for data received by testFunction");
}

async function testGet (request, response) {
    console.log('Request for data received by testGet');

    try{
        console.log('Got here')
        // const dbase = await pool.connect();
        const dbase = await client.connect();
        console.log('Succesfully connected')
        const rowList = await dbase.query('SELECT * FROM rawParcelTable LIMIT 10');
        console.log(rowList)
        await response.status(200).send(rowList);
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
        const result = await dbase.query('SELECT TOP 5 * FROM rawparceltable');
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