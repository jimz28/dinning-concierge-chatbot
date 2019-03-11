var AWS = require('aws-sdk');
exports.handler = (event, context, callback) => {
    AWS.config.region = 'us-east-1';
    var lexruntime = new AWS.LexRuntime();

    var params = {
        botAlias: "Prod",
        botName: "restaurant",
        inputText: event["body-json"].message,
        userId: event["body-json"].uuid,
        sessionAttributes: {}
    };
    console.log(event)
    lexruntime.postText(params, function(err, data) {
        if (err) {
            console.log(err, err.stack); // an error occurred
            //twimlResponse.message('Sorry, we ran into a problem at our end.');
            callback(err, "failed");
        } else {
            console.log(data); // got something back from Amazon Lex
            context.succeed(data);
        }
    });
};
