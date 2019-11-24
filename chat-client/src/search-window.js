import React from "react";
import Messages from './message-list';

import './App.css';

export default class SearchWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: this.props.user,
            room: this.props.room,
            messages: [],
            query_text: '',
        }
    }

    queryChangeHandler(event) {
        this.setState({query_text: event.target.value});
    }

    query(event) {
        event.preventDefault();
        // call API -> update this.state.messages
    }

    render() {
        let render_value = this.props.openSearchBox ? 
                <div className="search_box">
                    <form onSubmit={(event) => this.query(event)}>
                        <input type="text" name="search_content" 
                                onChange={(event) => this.queryChangeHandler(event)}/>
                        <input type="submit" value="Search" />
                    </form>
                    <Messages user={this.state.user} messages={this.state.messages}/>
                </div> 
            : null;
        return render_value;
    }
}