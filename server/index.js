const express = require("express");
const bodyParser = require("body-parser");
const pinataHelper = require('./pinataHelper');
var logger = require('morgan');


const PORT = process.env.PORT || 3001;
const app = express();
const cors = require('cors');
const SeedAndMint = require("../image-processing/SeedAndMint");
app.use(cors())
app.use(logger('dev'));

// create application/json parser
var jsonParser = bodyParser.json()
 
// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.post('/handle', jsonParser, async (request,response) => {
    //code to perform particular action.
    //To access POST variable use req.body()methods.
    let txn = await pinataHelper(request.body.data)
    //console.log(txn)
    const urlResponse = {
      "pinata" : txn
    }
    
    response.send(JSON.stringify(urlResponse))
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
