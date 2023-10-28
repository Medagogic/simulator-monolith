"use client"

import React, { FC, KeyboardEvent, useEffect, useRef, useState } from 'react';
import { FiSend, FiX } from 'react-icons/fi';
import { useChatStore } from '../storage/ChatStore';
import { useTeamStore } from '../storage/TeamStore';


type MessageTarget = {
    npc_id: string;
    npc_name: string;
}

type InputProps = {
    onSendMessage: (message: string, to_npc_id?: string) => void;
    placeholder?: string;
    className?: string;
    messageTarget?: MessageTarget;
};

const Input: FC<InputProps> = ({ onSendMessage, placeholder, className }) => {
    const currentMessage = useChatStore((state) => state.currentMessage);
    const [localValue, setLocalValue] = useState(currentMessage);

    const toNPCId = useChatStore((state) => state.toNPCId);
    const setToNPCId = useChatStore((state) => state.setToNPCId);
    const teamById = useTeamStore((state) => state.teamById);
    const setCurrentMessage = useChatStore((state) => state.setCurrentMessage);

    const [messageTarget, setMessageTarget] = useState<MessageTarget | undefined>(undefined);

    const npcNameRef = useRef<HTMLDivElement>(null);
    const [npcNameWidth, setNpcNameWidth] = useState(0);

    useEffect(() => {
        console.log("messageTarget", messageTarget)
        if (npcNameRef.current) {
            if (messageTarget != undefined) {
                setNpcNameWidth(npcNameRef.current.offsetWidth);
            } else {
                setNpcNameWidth(0);
            }
        }
    }, [messageTarget]);

    useEffect(() => {
        if (toNPCId) {
            let npcName = "Unknown NPC";
            if (teamById[toNPCId]) {
                const npcData = teamById[toNPCId];
                npcName = npcData.definition.name;
            }
            setMessageTarget({
                npc_id: toNPCId,
                npc_name: npcName,
            });
        } else {
            setMessageTarget(undefined);
        }
    }, [toNPCId]);

    useEffect(() => {
        setLocalValue(currentMessage);
    }, [currentMessage]);

    const handleKeyUp = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
        if (e.key === 'Backspace' && localValue === '' && messageTarget) {
            clearTarget();
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCurrentMessage(e.target.value);
    };

    function sendMessage() {
        onSendMessage(currentMessage, toNPCId);
        // setMessageTarget(undefined);
        setToNPCId(undefined);
        setNpcNameWidth(0);
        setCurrentMessage('');
    }

    const clearTarget = () => {
        // setMessageTarget(undefined);
        setToNPCId(undefined);
        setNpcNameWidth(0);
        setCurrentMessage('');
    };

    return (
        <div className={`${className} w-full flex items-center bg-gray-700 p-2 rounded relative`}>
            {messageTarget && (
                <div ref={npcNameRef} className="absolute flex items-center bg-blue-600 text-white p-1 rounded z-10 ml-1">
                    <span>To {messageTarget.npc_name}</span>
                    <button onClick={clearTarget} className="ml-2">
                        <FiX size={12} />
                    </button>
                </div>
            )}
            <input
                style={{ paddingLeft: `${npcNameWidth + 10}px` }} // Adjust padding based on npcNameWidth
                value={localValue}
                onChange={handleInputChange}
                onKeyUp={handleKeyUp}
                placeholder={placeholder}
                className='flex-auto bg-gray-600 text-white p-2 rounded relative z-0'
            />
            <button
                onClick={sendMessage}
                className='ml-2 bg-blue-600 text-white p-2 rounded hover:bg-blue-700 focus:outline-none'
            >
                <FiSend />
            </button>
        </div>
    );
};

export default Input;
