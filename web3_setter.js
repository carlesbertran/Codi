const Web3 = require('web3');
const Storage = require('./build/contracts/Storage.json')


const init = async () => {
const web3 = new Web3('http://localhost:9545');

const id = await web3.eth.net.getId();
const deployedNetwork = Storage.networks[id];
const contract = new web3.eth.Contract(
    Storage.abi,
    deployedNetwork.address
    );

contract.methods.storeData("tv3","video1","Linear","22-03","ES","cat").send();
}

init();