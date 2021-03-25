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

        const result = await contract.methods.retrieveData().call();
        console.log(result);
    } catch (e) {
        console.log(e.message)
    }
}

init();