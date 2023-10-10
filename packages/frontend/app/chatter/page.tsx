"use client"

import React from 'react';
import { Button, Input, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css'
import "./page.css"


export type Message = {
    text: string;
    sender: 'user' | 'system' | "assistant";
    date: Date;
}

type ChatPageProps = {
    messages: Message[];
};

const ChatterBox: React.FC<ChatPageProps> = ({ messages=[] }) => {

  // messages.push({text: "Hello", sender: "user", date: new Date()});
  // messages.push({text: "Hi", sender: "assistant", date: new Date()});
  // messages.push({text: "This is a system message", sender: "system", date: new Date()});

  function message_type(message: Message): string {
    return message.sender === 'system' ? 'system' : 'text';
  }

  function message_list(): any[] {
    return messages.map((message, index) => (
      {
        position: message.sender === 'user' ? 'right' : 'left',
        type: message_type(message),
        title: message.sender,
        text: message.text,
      }
    ));
  }

  function send_message(message: any) {
    console.log(message);
  }

  return (
    <div className="chat-page">
      <header className="chat-header">
        {/* ... any header content */}
      </header>
      <div className="chat-box">
        <MessageList
          className={'message-list'}
          lockable={true}
          toBottomHeight={'100%'}
          dataSource={message_list()}
          referance={React.createRef()}
        />
      </div>

      <footer className="chat-footer">
        {/* ... any footer content, perhaps a text input and send button for new messages */}
        <Input
          placeholder="Type here..."
          multiline={false}
          maxHeight={200}
          onSubmit={send_message}
          rightButtons={<Button text='Send'/>}
        />
      </footer>
    </div>
  );
}

export default ChatterBox;
