const Web3 = require('web3');
const Storage = require('./build/contracts/Storage.json')


const init = async () => {
    try {
        const web3 = new Web3('http://localhost:7545');

        const id = await web3.eth.net.getId();
        const deployedNetwork = Storage.networks[id];
        const contract = new web3.eth.Contract(
            Storage.abi,
            deployedNetwork.address
            );

            const result = await contract.methods.storeData("tv3","video1","Linear","22-03","ES","cat").send({from: '0xB825B32b3aA8F1aA0AAeC1B8692172EC51a17fb6', gas:3000000});
            console.log(result);
    } catch (e) {
        console.log(e.message)
    }
}

init();