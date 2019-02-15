const handler = require('../index.js').handler;

let callCount = 0;

function callback(error, count) {
    console.log("***** END REQUEST", callCount, "*****");
    if (! error)
        return;

    console.log(error);
}

process.stdin.setEncoding('utf8');

process.stdin.on('readable', () => {
  const chunk = process.stdin.read();

  if (chunk !== null) {
    callCount++;
    console.log("===== BEGIN REQUEST", callCount, " =====");
    const parsed = JSON.parse(chunk.toString('ascii'));
    // console.log(JSON.stringify(parsed, null, 2));
    handler(parsed.event, parsed.context, callback);
  }
});
