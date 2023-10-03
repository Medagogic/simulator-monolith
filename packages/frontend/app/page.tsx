"use client"
import React, { useState, useEffect, FC, FormEvent } from 'react';
import { Configuration, DefaultApi } from '@/src/api';
import { io, Socket } from "socket.io-client";
import Link from 'next/link';


interface SessionData {
  session_id: string;
  sids_in_session: Array<string>;
  creation_datetime?: string;
}

const api = new DefaultApi(new Configuration({
  basePath: 'http://localhost:5000',
}));

const Chat: FC = () => {
  const [sessions, setSessions] = useState<SessionData[]>([]);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [newMessage, setNewMessage] = useState<string>('');

  useEffect(() => {
    const refreshSessions = async () => {
      try {
        const res = await api.handleListSessionsSessionListGet();
        setSessions(res.data);
      } catch (error) {
        console.error('Failed to fetch sessions:', error);
      }
    };

    refreshSessions();
    const intervalId = setInterval(refreshSessions, 5000);

    return () => {
      clearInterval(intervalId);
      if (socket) {
        socket.disconnect();
      }
    };
  }, [api, socket]);

  const handleJoinSession = (sessionId: string) => {
    const namespace = `${sessionId}/chat`;
    const newSocket = io(`http://localhost:5000/${namespace}`,
    {
      path: "/socket.io",
      transports: ["websocket"], // important!
      autoConnect: true
    });

    newSocket.on("connect", () => {
      console.log("Connected to session:", sessionId);
    });

    newSocket.on("response", (message: {content: string}) => {
      setMessages(prevMessages => [...prevMessages, message.content]);
      console.log(message);
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected from session:", sessionId);
    });

    setSocket(newSocket);
  };

  const handleSendMessage = (e: FormEvent) => {
    e.preventDefault();
    if (socket && newMessage.trim()) {
      socket.emit("message", newMessage);
      setNewMessage('');
    }
  };

  return (
    <main style={{"height": "100vh"}}>
      <div>
        <Link href="/chatter">Go to chatter</Link>
        <h2>Sessions</h2>
        <ul>
          {sessions.map(session => (
            <li key={session.session_id}>
              <button onClick={() => handleJoinSession(session.session_id)}>
                Join Session {session.session_id}
              </button>
            </li>
          ))}
        </ul>
      </div>
      {socket && (
        <div>
          <h2>Chat Room</h2>
          <ul>
            {messages.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
          <form onSubmit={handleSendMessage}>
            <input
              type="text"
              value={newMessage}
              onChange={e => setNewMessage(e.target.value)}
              placeholder="Type your message here"
            />
            <button type="submit">Send</button>
          </form>
        </div>
      )}
    </main>
  );
};

export default Chat;
