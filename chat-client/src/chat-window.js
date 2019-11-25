import React from "react";
import Messages from "./message-list";
import Input from "./input";

import "./App.css";

export default class ChatWindow extends React.Component {
  // // connect to server
  // componentWillMount() {
  // }

  render() {
    return (
      <div
        className={this.props.openSearchBox ? "app_content" : "app_content_0"}
      >
        <div className="chat_window">
          <Messages user={this.props.user} messages={this.props.messages} />
          <Input sendMessage={this.props.sendMessage} />
        </div>
      </div>
    );
  }
}
