import React from "react";
import ChatWindow from './chat-window';
import SearchWindow from './search-window';


function RoomList(props) {
    const rooms = props.rooms;
    const roomItems = rooms.map((room, idx) =>
        <option key={idx} value={idx}> {room} </option>
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
            user: "duy",
            rooms: this.getRoom(),
            idxCurrentRoom: 0,
            openSearchBox: false,
        }
    }

    getRoom() {
        return [10, 20, 30]; // update from API]
    }

    myChangeHandler(event) {
        console.log('Change room to ' + event.target.value);
        this.setState({idxCurrentRoom: event.target.value});
        // get API message
    }

    toggleSearchBox() {
        console.log('clicked');
        this.setState({openSearchBox: !this.state.openSearchBox})
    }

    render() {
        return (
            <div>
                <div className="room_window">
                    <form className="room_form">
                        <label> Choose room: </label>
                        <RoomList rooms={this.state.rooms} onChange={(event) => this.myChangeHandler(event)}/>
                    </form>
                    <button className="search_button" onClick={() => this.toggleSearchBox()}>
                        {this.state.openSearchBox ? 'Hide Search Box' : 'Show Search Box'}
                    </button>
                </div>
                <div className="split">
                    <ChatWindow user={this.state.user} rooms={this.state.rooms} openSearchBox={this.state.openSearchBox}/>
                    <SearchWindow user={this.state.user} rooms={this.state.rooms} openSearchBox={this.state.openSearchBox}/>
                </div>
            </div>
        )
    }
}
