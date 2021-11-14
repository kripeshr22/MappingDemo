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
    user: "techequity",
    host: "localhost",
    database: "parceldatabase",
    password: "clinic",
    port: 5432
    // user: "ub5debmb55aodh",
    // host: "ec2-52-201-66-148.compute-1.amazonaws.com",
    // database: "d44ns4ruujn4nq",
    // password: "pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163",
    // port: 5432

    // connectionString: process.env.DATABASE_URI
});

async function testFunction (request, response) {
    console.log('Request for data received by testFunction');
    response.status(200).json("Request for data received by testFunction");
}

async function testGet (request, response) {
    console.log('Request for data received by testGet');

    try{
        // const dbase = await pool.connect();
        const dbase = await client.connect();
        console.log('Succesfully connected')
        const rowList = await client.query('SELECT * FROM rawParcelTable');
        const results = { 'results': (rowList) ? rowList.rows : null};
        response.status(200).send(results);
        // await response.json(rowList);
        // await response.status(200).send(rowList);
    } catch (error){
        response.status(400).json('SERVER RESP: Error retrieving userrecords. Log:'+error)
        console.log('Error retrieving userrecords. Log:')
        console.log(error);
    }
}

async function testHerokuPg (request, response) {
    console.log('Request for data received by testHerokuPg');

    try{
        const dbase = await client.connect();
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