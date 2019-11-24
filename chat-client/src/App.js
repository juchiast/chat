import React from "react";
import ChatWindow from './chat-window';
import SearchWindow from './search-window';

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: null,
            rooms: this.getRoom(),
            openSearchBox: false,
        }
    }

    getRoom() {
        return [10, 20, 30]; // update from API]
    }

    toggleSearchBox() {
        console.log('clicked');
        this.setState({openSearchBox: !this.state.openSearchBox})
    }

    render() {
        return (
            <div>
                <ChatWindow user={this.state.user} rooms={this.state.rooms} openSearchBox={this.state.openSearchBox} toggleSearchBox={() => this.toggleSearchBox()}/>
                <SearchWindow user={this.state.user} rooms={this.state.rooms} openSearchBox={this.state.openSearchBox}/>
            </div>
        )
    }
}
