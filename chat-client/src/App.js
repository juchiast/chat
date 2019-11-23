import React from "react";
import Messages from './message-list';
import Input from './input';

import './App.css';
import './room-selector.css'

function RoomList(props) {
    const rooms = props.rooms;
    const roomItems = rooms.map((room) =>
        <li key={room.toString()}>{room}</li>
    );
    return (
      <div>{roomItems}</div>
    );
}

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: [
            ],
            rooms: [1, 2, 3], // update from API
            user: null,
        }
    }

    //connect to server
    componentWillMount() {
    }

    // when has new messages, do sth
    newMessage(message) {
    }
    // send event server
    sendnewMessage(message) {
    }

    getRoom() {
        console.log('Select room');
    }

    render () {
        return (
           <div className="app__content">
                <h1>Super App</h1>
                <div className="room_form">
                    <button className="dropbtn" onClick={() => this.getRoom()}>Dropdown</button>
                    <RoomList className="dropdown-content" rooms={this.state.rooms}/>
                </div>
                <div className="chat_window">
                    <Messages user={this.state.user} messages={this.state.messages} typing={this.state.typing}/>
                    <Input sendMessage={this.sendnewMessage.bind(this)}/>
                </div>
            </div>
        )
    }
}
