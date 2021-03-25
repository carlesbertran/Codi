const Web3 = require('web3');
const Storage = require('./build/contracts/Storage.json');
const readline = require('readline');
const fs = require('fs');


const init = async () => {
    try {
        //read txt file section
        const readInterface = readline.createInterface({
            input: fs.createReadStream('./test/report.txt'),
            output: process.stdout,
            console: false
        });
            
        var arguments = []
            
        readInterface.on('line', (line) => {
            arguments.push(line);
        }).on('close', () => {
            return arguments;
            process.exit(0);
        });


        //Web3 send function section
        const web3 = new Web3('http://localhost:7545');

        const id = await web3.eth.net.getId();
        const deployedNetwork = Storage.networks[id];
        const contract = new web3.eth.Contract(
            Storage.abi,
            deployedNetwork.address
            );
     
        console.log(arguments);
        const result = await contract.methods.storeData(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4],arguments[5]).send({from: '0xB825B32b3aA8F1aA0AAeC1B8692172EC51a17fb6', gas:3000000});
        console.log(result);
    } catch (e) {
        console.log(e.message)
    }
}

init();