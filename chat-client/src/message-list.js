import React from 'react';
import Message from './message-item';


export default class MessageItem extends React.Component {
    render() {
        return (
            <ul className="messages">
                {this.props.messages.map(item =>
                    <Message key={item.id} is_user={item.user_name === this.props.user ? true : false} 
                        user={item.user_name} message={item.content} />
                )}
            </ul>
        )
    }
}