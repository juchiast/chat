import React from "react";
import ChatWindow from "./chat-window";
import SearchWindow from "./search-window";

function RoomList(props) {
  const rooms = props.rooms;
  const roomItems = rooms.map((room, idx) => (
    <option key={idx} value={idx}>
      {" "}
      {room}{" "}
    </option>
  ));
  return (
    <select
      className="room_selection"
      onChange={event => props.onChange(event)}
    >
      {roomItems}
    </select>
  );
}

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: "kenny",
      rooms: this.getRooms(),
      messages: [],
      idxCurrentRoom: 0,
      openSearchBox: false
    };
    this.fetchMessages();
  }

  async fetchMessages() {
    let roomId = this.state.rooms[this.state.idxCurrentRoom];
    let resp = await fetch(`http://localhost:8080/${roomId}/?limit=10`);
    resp = await resp.json();
    let messages = resp.messages;
    this.setState({ messages });
  }

  getRooms() {
    return [1, 2, 3, 4, 5, 6]; // update from API
  }

  myChangeHandler(event) {
    this.setState({ idxCurrentRoom: event.target.value }, () => {
      this.fetchMessages();
    });
  }

  toggleSearchBox() {
    this.setState({ openSearchBox: !this.state.openSearchBox });
  }

  newMessage(message) {
    let messages = this.state.messages;
    messages.push(message);
    this.state.setState({ messages });
  }

  sendMessage(inputElement) {
    const msg = {
      message: inputElement.value,
      user_name: this.state.user
    };
    inputElement.value = "";
    const roomId = this.state.rooms[this.state.idxCurrentRoom];
    const url = `http://localhost:8080/${roomId}/`;
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(msg)
    }).then(() => this.fetchMessages());
  }

  userChangeHandler(event) {
    this.setState({ user: event.target.value });
  }

  render() {
    return (
      <div>
        <div className="room_window">
          <div className="room_form">
            <form className="user_form">
              <label> Choose User: </label>
              <input
                type="text"
                name="user_content"
                defaultValue={this.state.user}
                onChange={event => this.userChangeHandler(event)}
              />
            </form>
            <form>
              <label> Choose Room: </label>
              <RoomList
                rooms={this.state.rooms}
                onChange={event => this.myChangeHandler(event)}
              />
            </form>
          </div>
          <button
            className="search_button"
            onClick={() => this.toggleSearchBox()}
          >
            {this.state.openSearchBox ? "Hide Search Box" : "Show Search Box"}
          </button>
        </div>
        <div className="split">
          <ChatWindow
            user={this.state.user}
            idxCurrentRoom={this.state.idxCurrentRoom}
            rooms={this.state.rooms}
            messages={this.state.messages}
            sendMessage={this.sendMessage.bind(this)}
            openSearchBox={this.state.openSearchBox}
          />
          <SearchWindow
            user={this.state.user}
            room={this.state.rooms[this.state.idxCurrentRoom]}
            openSearchBox={this.state.openSearchBox}
          />
        </div>
      </div>
    );
  }
}
