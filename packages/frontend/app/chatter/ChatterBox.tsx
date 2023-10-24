// ChatterBox.tsx
"use client"

import React, { useState } from 'react';
import { Button, Input, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import "app/chatter/ChatterBox.css"
import { useChatStore } from './ChatStore';
import { FiPaperclip } from 'react-icons/fi';
import AttachmentList from '../sim-session/AttachmentList/AttachmentList';
import {DefaultApi, Configuration} from "@/src/api"
import { useChatterIO } from '../socketio/SocketContext';
import { ChatEvent, HumanMessage, MessageFromNPC } from "@/src/scribe/scribetypes"

const api_config = new Configuration({basePath: process.env.API_HOST})
const api = new DefaultApi(api_config)

const ChatterBox: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const currentMessage = useChatStore((state) => state.currentMessage);
  const setCurrentMessage = useChatStore((state) => state.setCurrentMessage); // Assuming you have this in your store
  
  const [showAttachments, setShowAttachments] = useState(false);
  const attachments = useChatStore((state) => state.attachments); // Retrieve attachments from your store
  const chatterIO = useChatterIO()!;

  function toggleAttachments() {
    setShowAttachments(!showAttachments);
  }

  function message_list(): any[] {
    return messages.map((chatStoreMessage) => {
      let position: 'right' | 'left' | 'center';
      let title: string;
      let text: string;
      let type: string = "text";
  
      switch (chatStoreMessage.type) {
        case 'human':
          position = 'right'; // Assuming 'human' type messages are 'user' sent.
          title = 'User'; // This is an assumption. Replace with actual data if available.
          const human = chatStoreMessage.message as HumanMessage;
          text = human.message; // Assuming 'message' field holds the text in 'HumanMessage'.
          break;
        case 'npc':
          position = 'left';
          const npc = chatStoreMessage.message as MessageFromNPC;
          title = npc.npc_id; // Assuming NPC's id should be displayed as title.
          text = npc.message;
          break;
        case 'event':
          position = 'center';
          title = 'Event';
          const evt = chatStoreMessage.message as ChatEvent;
          text = evt.event;
          type = "system";
          break;
        default:
          throw new Error('Unsupported message type');
      }
  
      return {
        position,
        type: type,
        title,
        text
      };
    });
  }

  function send_message() {
    chatterIO.sendMessage(currentMessage);
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
