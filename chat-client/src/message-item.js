import React from "react";

export default class messageItem extends React.Component {
  render() {
    return (
      <li
        className={
          this.props.is_user
            ? "message right appeared"
            : "message left appeared"
        }
      >
        <div className="avatar">{this.props.user}</div>
        <div className="text_wrapper text">{this.props.message}</div>
      </li>
    );
  }
}
