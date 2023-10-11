// ChatterBox.tsx
"use client"

import React, { use } from 'react';
import { Button, Input, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import "./ChatterBox.css";
import { useChatStore, Message } from './ChatStore';

const ChatterBox: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const currentMessage = useChatStore((state) => state.currentMessage);
  const sendMessage = useChatStore((state) => state.sendMessage);
  const setCurrentMessage = useChatStore((state) => state.setCurrentMessage); // Assuming you have this in your store


  function message_type(message: Message): string {
    return message.sender === 'system' ? 'system' : 'text';
  }

  function message_list(): any[] {
    return messages.map((message, index) => ({
      position: message.sender === 'user' ? 'right' : 'left',
      type: message_type(message),
      title: message.sender,
      text: message.text,
    }));
  }

  function send_message() {
    sendMessage(currentMessage);
    setCurrentMessage("");
  }

  function handleKeyPress(event: React.KeyboardEvent) {
    if (event.key === 'Enter') {
      send_message();
    }
  }

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    setCurrentMessage(event.target.value); // Update the currentMessage in the store
  }

  return (
    <div className="chat-page bg-gray-700">
      <header className="chat-header">
        {/* ... any header content */}
      </header>
      <div className="chat-box flex-grow">
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
          value={currentMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type here..."
          multiline={false}
          maxHeight={200}
          rightButtons={<Button text='Send' onClick={send_message}/>}
          className='chat-input'
        />
      </footer>
    </div>
  );
}

export default ChatterBox;
