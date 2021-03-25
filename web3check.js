const readline = require('readline');
const fs = require('fs');

const readInterface = readline.createInterface({
    input: fs.createReadStream('./test/report.txt'),
    output: process.stdout,
    console: false
});

var arguments = []

readInterface.on('line', (line) => {
    //console.log(line);
    arguments.push(line);
}).on('close', () => {
    console.log(arguments);
    console.log(arguments.length);
    process.exit(0);
});
