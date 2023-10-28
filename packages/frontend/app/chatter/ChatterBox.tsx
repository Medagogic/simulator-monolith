// ChatterBox.tsx
"use client"

import React, { ReactElement, useEffect, useRef, useState } from 'react';
import { Button, MessageList } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import "app/chatter/ChatterBox.css"
import { useChatStore } from '../storage/ChatStore';
import { FiPaperclip } from 'react-icons/fi';
import AttachmentList from '../sim-session/AttachmentList/AttachmentList';
import { useChatterIO } from '../socketio/SocketContext';
import { ChatEvent, HumanMessage, MessageFromNPC } from "@/src/scribe/scribetypes"

import { DefaultApi, Configuration } from "@/src/api"
import { useTeamStore } from '../storage/TeamStore';
import Input from './Input';
const api_config = new Configuration({ basePath: process.env.API_HOST })
const api = new DefaultApi(api_config)

const ChatterBox: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const setToNPCId = useChatStore((state) => state.setToNPCId);
  const teamById = useTeamStore((state) => state.teamById);

  const [showAttachments, setShowAttachments] = useState(false);
  const attachments = useChatStore((state) => state.attachments); // Retrieve attachments from your store
  const chatterIO = useChatterIO()!;

  const [messageList, setMessageList] = useState<any[]>([]);

  function toggleAttachments() {
    setShowAttachments(!showAttachments);
  }

  useEffect(() => {
    setMessageList(message_list());
  }, [messages, teamById]);

  function getNPCName(npc_id: string): string {
    const npc = teamById[npc_id];
    if (npc) {
      return npc.definition.name;
    } else {
      return npc_id;
    }
  }

  function message_list(): any[] {
    return messages.map((chatStoreMessage) => {
      let position: 'right' | 'left' | 'center';
      let title: string | undefined;
      let content: string | ReactElement;
      let type: string = "text";
      let className: string = "chat-message";
      let replyButton: boolean = false;
      let npc_id: string | undefined;

      switch (chatStoreMessage.type) {
        case 'human':
          position = 'right';
          // title = 'User';
          const human = chatStoreMessage.message as HumanMessage;
          content = human.message;
          if (human.target_npc_id) {
            const npcName = getNPCName(human.target_npc_id);
            content = (
              <div className="flex flex-col">
                <div>To {npcName}</div>
                <div className="flex-grow">{human.message}</div>
              </div>
            )
          }
          break;
        case 'npc':
          position = 'left';
          const npc = chatStoreMessage.message as MessageFromNPC;
          title = getNPCName(npc.npc_id);
          npc_id = npc.npc_id;
          content = npc.message;
          className = `${className} npc-message ${npc.npc_id}`
          // replyButton = true;
          break;
        case 'event':
          const evt = chatStoreMessage.message as ChatEvent;
          position = 'center';
          if (evt.npc_id) {
            title = getNPCName(evt.npc_id);
            className = `${className} npc-event ${evt.npc_id}`
          } else {
            title = "System"
            className = `${className} system-event`
          }
          content = evt.event;
          type = "system";
          break;
        default:
          throw new Error('Unsupported message type');
      }

      return {
        position,
        type: type,
        title,
        text: content,
        className: className,
        replyButton,
        npc_id
      };
    });
  }

  function send_message(message: string, target_npc_id?: string) {
    chatterIO.sendMessage(message, target_npc_id);
  }


  function handleReplyClick(data: any) {
    setToNPCId(data.npc_id);
  }

  return (
    <div className={`bg-gray-700 relative h-full flex flex-col`}>
      <header className='flex-shrink'>
      </header>

      <button
        onClick={toggleAttachments}
        className="absolute top-0 right-0 m-3 text-white rounded-full p-2" // tailwind classes for styling
        style={{ zIndex: 10 }} // Ensure button is above other elements, adjust if necessary
      >
        <FiPaperclip size={18} title="Recieved documents" /> {/* Icon for the button */}
      </button>

      <MessageList
        className="flex-grow overflow-y-auto chat-styling"
        lockable={true}
        toBottomHeight={'100%'}
        dataSource={messageList}
        referance={React.createRef()}
        onReplyClick={handleReplyClick}
      />

      <footer className='flex-shrink'>
        {/* ... any footer content, perhaps a text input and send button for new messages */}
        <Input
          onSendMessage={send_message}
          placeholder="Type here..."
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
