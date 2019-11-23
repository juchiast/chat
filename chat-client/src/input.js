import React from 'react';

export default class Input extends React.Component {
    enterKey(e) {
        if (e.keyCode === 13) {
            this.props.sendMessage(this.refs.message);
        }
    }
    render () {
        return (
            <div className="bottom_wrapper clearfix">
                <div className="message_input_wrapper">
                    <input ref="message" className="message_input" placeholder="Type your message here..." onKeyUp={(e) => this.enterKey(e)}/>
                </div>
                <div className="send_message" onClick={() => this.props.sendMessage(this.refs.message)}>
                    <div className="icon"></div>
                    <div className="text">Send</div>
                </div>
            </div>
        )
    }
}