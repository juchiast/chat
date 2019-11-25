import React from "react";
import Messages from './message-list';
import Input from './input';

import './App.css';



export default class ChatWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: this.getMessages(),
        }
    }

    // // connect to server
    // componentWillMount() {
    // }

    getMessages() {
        let TEST_MESSAGES = [
            { id: "1", timestamp: 0, user_name: "not duy", content: "Hello" },
            { id: "2", timestamp: 0, user_name: "duy", content: "Not Hello" }
        ];
        return TEST_MESSAGES;
    }

    // when has new messages, do sth
    newMessage(message) {
    }

    // send event server
    sendnewMessage(message) {
    }

    render() {
        return (
            <div className={this.props.openSearchBox ? 'app_content' : 'app_content_0'}>
                <div className="chat_window">
                    <Messages user={this.props.user} messages={this.state.messages} />
                    <Input sendMessage={this.sendnewMessage.bind(this)} />
                </div>
            </div>
        )
    }
}