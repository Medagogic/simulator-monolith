// ChatterBox.tsx
"use client"

import React, { use, useEffect, useState } from 'react';
import { Button, Input, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import "app/chatter/ChatterBox.css"



interface DirectInputProps {
    onSubmit: (message: string) => void;
  }


const DirectInput: React.FC<DirectInputProps> = ({ onSubmit: onSubmit }) => {
    const [currentMessage, setCurrentMessage] = useState("");


  function send_message() {
    onSubmit(currentMessage);
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

  );
}

export default DirectInput;
