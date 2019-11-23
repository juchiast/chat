import React from "react";
import Messages from './message-list';
import Input from './input';

import './App.css';

function RoomList(props) {
    const rooms = props.rooms;
    console.log(rooms);
    const roomItems = rooms.map((room, idx) =>
        <option value={idx}> {room} </option>
    );
    return (
        <select className="room_selection" onChange={(event) => props.onChange(event)}>
            {roomItems}
        </select>
    );
}

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: [
            ],
            rooms: [10, 20, 30], // update from API
            idxCurrentRoom: null,
            user: null,
        }
    }

    // // connect to server
    // componentWillMount() {
    // }

    // when has new messages, do sth
    newMessage(message) {
    }
    // send event server
    sendnewMessage(message) {
    }

    myChangeHandler(event) {
        console.log('Change room to ' + event.target.value);
        this.setState({idxCurrentRoom: event.target.value});
        // get API message
    }

    render () {
        return (
           <div className="app__content">
                <h1>Super App</h1>
                <form>
                    <label>
                    Choose room:
                    <RoomList className="room_window" 
                        rooms={this.state.rooms} onChange={(event) => this.myChangeHandler(event)}/>
                    </label>
                </form>
                <div className="chat_window">
                    <Messages user={this.state.user} messages={this.state.messages} typing={this.state.typing}/>
                    <Input sendMessage={this.sendnewMessage.bind(this)}/>
                </div>
            </div>
        )
    }
}
