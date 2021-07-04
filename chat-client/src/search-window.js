import React from "react";
import Messages from "./message-list";
import { getApiUrl } from "./util";

import "./App.css";

export default class SearchWindow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: [],
      query_text: "",
      noResult: false
    };
  }

  queryChangeHandler(event) {
    this.setState({ query_text: event.target.value });
  }

  async query(event) {
    event.preventDefault();
    const query = {
      query: this.state.query_text
    };
    const url = `${getApiUrl()}/${this.props.room}/search/`;
    let resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(query)
    });
    resp = await resp.json();
    let messages = resp.messages;
    this.setState({ messages, noResult: messages.length === 0 });
  }

  render() {
    let resultForm = this.state.noResult ? (
      <div> Sad </div>
    ) : (
      <Messages user={this.props.user} messages={this.state.messages} />
    );
    let render_value = this.props.openSearchBox ? (
      <div className="search_box">
        <form onSubmit={event => this.query(event)}>
          <input
            type="text"
            name="search_content"
            onChange={event => this.queryChangeHandler(event)}
          />
          <input type="submit" value="Search" />
        </form>
        {resultForm}
      </div>
    ) : null;
    return render_value;
  }
}
