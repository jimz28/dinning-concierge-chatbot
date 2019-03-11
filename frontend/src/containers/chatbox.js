import React, { Component } from 'react';
import {Launcher} from 'react-chat-window'
import axios from 'axios';
import AWS from 'aws-sdk';
import config from './../config';

class Chatbox extends Component {

  constructor() {
    super();
    this.state = {
      messageList: [
        {
          author: 'them',
          type: 'text',
          data: {text: "Hello, I'm your dining guide."},
        },
        {
          author: 'them',
          type: 'text',
          data: {text: "What can I help you?"},
        },
      ]
    };
  }

  _onMessageWasSent(message) {
    // push to state msgList array
    this.setState({
      messageList: [...this.state.messageList, message]
    });

    if (message.type !== 'text') {
      // this.setState({
      //   messageList: [...this.state.messageList, {
      //     author: 'them',
      //     type: 'emoji',
      //     data: message.data,
      //   }]
      // });
      return;
    }

    // Initialize the Amazon Cognito credentials provider
    // let lexRunTime = new AWS.LexRuntime();
    let lexUserId = 'user' + Date.now();
    let sessionAttributes = {};

    let params = {
      botAlias: 'Prod',
      botName: 'restaurant',
      inputText: message.data.text,
      userId: lexUserId,
      sessionAttributes: sessionAttributes
    };

    // if we want to do it with sdk:
    // AWS.config.region = config.congnito.REGION; // Region
    // AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    //     IdentityPoolId: config.congnito.IDENTITY_POOL_ID,
    // });

    // lexRunTime.postText(params, function(err, data) {
    //   if (err) {
    //   }
    //   if (data) {
    //     // capture the sessionAttributes for the next cycle
    //     sessionAttributes = data.sessionAttributes;
    //     // show response and/or error/dialog status
    //   }
    // });

    // send to lambda api
    axios.post('https://e2zx297ug0.execute-api.us-east-1.amazonaws.com/prod/chatbot', {
      message: message.data.text,
      lexUserId: 'lexUserId'
    })
    .then(response => {
      // console.log(response);
      const responseText = response.data.message;
      const responseMessage = {
        author: 'them',
        type: 'text',
        data: {text: responseText},
      };
      // push to state msgList array
      this.setState({
        messageList: [...this.state.messageList, responseMessage]
      });
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  // _sendMessage(text) {
  //   if (text.length > 0) {
  //     this.setState({
  //       messageList: [...this.state.messageList, {
  //         author: 'me',
  //         type: 'text',
  //         data: { text }
  //       }]
  //     })
  //   }
  // }

  render() {
    return (
      <div>
        <Launcher
          agentProfile={{
            teamName: 'Dining Concierge Agent',
            imageUrl: 'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png'
          }}
          onMessageWasSent={this._onMessageWasSent.bind(this)}
          messageList={this.state.messageList}
          showEmoji
        />
      </div>)
  }
}

export default Chatbox;