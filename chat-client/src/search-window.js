import React from "react";
import Messages from './message-list';

import './App.css';

export default class SearchWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: [],
            query_text: '',
        }
    }

    queryChangeHandler(event) {
        this.setState({query_text: event.target.value});
    }

    async query(event) {
        event.preventDefault();
        const query = {
            query: this.state.query_text,
        }
        const url = `http://localhost:8080/${this.props.room}/search/`;
        let resp = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(query),
        });
        resp = await resp.json();
        let messages = resp.messages;
        this.setState({ messages });
    }

    render() {
        let render_value = this.props.openSearchBox ? 
                <div className="search_box">
                    <form onSubmit={(event) => this.query(event)}>
                        <input type="text" name="search_content" 
                                onChange={(event) => this.queryChangeHandler(event)}/>
                        <input type="submit" value="Search" />
                    </form>
                    <Messages user={this.props.user} messages={this.state.messages}/>
                </div> 
            : null;
        return render_value;
    }
}