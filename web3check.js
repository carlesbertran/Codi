const readline = require('readline');
const fs = require('fs');

const readInterface = readline.createInterface({
    input: fs.createReadStream('./test/report.txt'),
    output: process.stdout,
    console: false
});

function deleteFile (){
    fs.writeFile('./test/report.txt','', (err) => {
        console.log("file deleted");
    });

}

var arguments = []

readInterface.on('line', (line) => {
    arguments.push(line);
}).on('close', () => {
    deleteFile();
    return arguments;
});

console.log(arguments);


