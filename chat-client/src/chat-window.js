import React from "react";
import Messages from './message-list';
import Input from './input';

import './App.css';

function RoomList(props) {
    const rooms = props.rooms;
    const roomItems = rooms.map((room, idx) =>
        <option value={idx}> {room} </option>
    );
    return (
        <select className="room_selection" onChange={(event) => props.onChange(event)}>
            {roomItems}
        </select>
    );
}

export default class ChatWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: this.getMessages(),
            idxCurrentRoom: 0,
        }
    }

    // // connect to server
    // componentWillMount() {
    // }

    getMessages() {
        return []
    }

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

    render() {
        return (
            <div className={this.props.openSearchBox ? 'split app_content' : 'split app_content_0'}>
                <div  className="room_form">
                <form>
                    <label> Choose room: </label>
                    <RoomList rooms={this.props.rooms} onChange={(event) => this.myChangeHandler(event)}/>
                </form>
                <button className="button_search" onClick={this.props.toggleSearchBox}> Search </button>
                </div>
                <div className="chat_window">
                    <Messages user={this.props.user} messages={this.state.messages}/>
                    <Input sendMessage={this.sendnewMessage.bind(this)}/>
                </div>
            </div>
        )
    }
}