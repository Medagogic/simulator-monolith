"use client"

import { EmitEvent } from "@/src/scribe/ScribeClient";
import React, { createContext, useContext, useEffect, useState, ReactNode, use } from "react";
import { io, Socket } from "socket.io-client";
import { PatientIO } from "./PatientIO";
import { ChatterIO } from "./ChatterIO";

// Defining the context shape
interface ISocketContext {
    socket: Socket | null;
    patientIO: PatientIO | null;
    chatterIO: ChatterIO | null;
}

const SocketContext = createContext<ISocketContext | null>(null);

interface SocketProviderProps {
    session_id: string;
    children: ReactNode;
}

export const SocketProvider: React.FC<SocketProviderProps> = ({ session_id, children }) => {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [patientIO, setPatientIO] = useState<PatientIO | null>(null);
    const [chatterIO, setChatterIO] = useState<ChatterIO | null>(null);
    let connecting = false;

    useEffect(() => {
        if (!socket && typeof window !== "undefined" && !connecting) {
            console.log("Connecting socket");
            connecting = true;
            const socket_url = `http://localhost:5000/session`
            const newSocket = io(socket_url);
            setPatientIO(new PatientIO(newSocket));
            setChatterIO(new ChatterIO(newSocket));

            newSocket.on("connect", () => {
                console.log("Socket connected");
                newSocket.emit(EmitEvent.JOIN_SESSION, session_id, () => {console.log(`Joined session ${session_id}`)});
            });

            setSocket(newSocket);
        }

        return () => {
            if (socket) {
                console.log("Disconnecting socket");
                socket.disconnect();  // This will close the socket connection.
            }
        };
    }, [socket]);

    return (
        <SocketContext.Provider value={{ socket:socket, patientIO:patientIO, chatterIO:chatterIO }}>
            {children}
        </SocketContext.Provider>
    );
};

export const useSocket = (): Socket | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useSocket must be used within a SocketProvider");
    }

    return context.socket;
};

export const usePatientIO = (): PatientIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("usePatientIO must be used within a SocketProvider");
    }

    return context.patientIO;
};

export const useChatterIO = (): ChatterIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useChatterIO must be used within a SocketProvider");
    }

    return context.chatterIO;
}