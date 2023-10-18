// ChatterBox.tsx
"use client"

import React, { use, useState } from 'react';
import { Button, Input, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import "app/chatter/ChatterBox.css"
import { useChatStore, Message } from './ChatStore';
import { FiPaperclip } from 'react-icons/fi';
import AttachmentList from '../sim-session/AttachmentList/AttachmentList';
import {DefaultApi, Configuration} from "@/src/api"

const api_config = new Configuration({basePath: process.env.API_HOST})
const api = new DefaultApi(api_config)

const ChatterBox: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const currentMessage = useChatStore((state) => state.currentMessage);
  const sendMessage = useChatStore((state) => state.sendMessage);
  const setCurrentMessage = useChatStore((state) => state.setCurrentMessage); // Assuming you have this in your store
  
  const [showAttachments, setShowAttachments] = useState(false);
  const attachments = useChatStore((state) => state.attachments); // Retrieve attachments from your store

  function toggleAttachments() {
    setShowAttachments(!showAttachments);
  }


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
    <div className={`chatPage bg-gray-700 relative`}>
      <header>
      </header>

      <button 
        onClick={toggleAttachments} 
        className="absolute top-0 right-0 m-3 text-white rounded-full p-2" // tailwind classes for styling
        style={{ zIndex: 10 }} // Ensure button is above other elements, adjust if necessary
      >
        <FiPaperclip size={18} title="Recieved documents"/> {/* Icon for the button */}
      </button>

      <div className="flex-grow">
        <MessageList
          className="messageList"
          lockable={true}
          toBottomHeight={'100%'}
          dataSource={message_list()}
          referance={React.createRef()}
        />
      </div>

      <footer>
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

      
        <AttachmentList
          isOpen={showAttachments}
          closeModal={toggleAttachments}
        />
    </div>
  );
}

export default ChatterBox;
