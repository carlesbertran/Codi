const Web3 = require('web3');
const Storage = require('browser/contracts/artifacts/Storage.json')


const init = async () => {
const web3 = new Web3(window.ethereum);

const id = await web3.eth.net.getId();
const deployedNetwork = Storage.networks[id];
const contract = new web3.eth.Contract(
    Storage.abi,
    deployedNetwork.address
    );

const result = await contract.methods.retrieveData().call();
console.log(result);
}

init();