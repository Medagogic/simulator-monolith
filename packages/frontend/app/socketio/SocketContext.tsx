"use client"

import { EmitEvent } from "@/src/scribe/ScribeClient";
import React, { createContext, useContext, useEffect, useState, ReactNode, use } from "react";
import { io, Socket } from "socket.io-client";
import { PatientIO } from "./PatientIO";
import { ChatterIO } from "./ChatterIO";
import { TeamIO } from "./TeamIO";

// Defining the context shape
interface ISocketContext {
    socket: Socket | null;
    patientIO: PatientIO | null;
    chatterIO: ChatterIO | null;
    teamIO: TeamIO | null;
}

const SocketContext = createContext<ISocketContext | null>(null);

interface SocketProviderProps {
    session_id: string;
    children: ReactNode;
}

interface ContextSingleton {
    socket: Socket;
    patientIO: PatientIO;
    chatterIO: ChatterIO;
    teamIO: TeamIO;
    session_id: string | null;
}

let context_singleton: ContextSingleton | null = null;

const getContextSingleton = () => {
  if (context_singleton === null) {
    const socket_url = `http://localhost:5000/session`;
    const socket = io(socket_url);
    const patientIO = new PatientIO(socket);
    const chatterIO = new ChatterIO(socket);
    const teamIO = new TeamIO(socket);
    context_singleton = {
        socket: socket,
        patientIO: patientIO,
        chatterIO: chatterIO,
        teamIO: teamIO,
        session_id: null
    };
  }
  return context_singleton;
};

export const SocketProvider: React.FC<SocketProviderProps> = ({ session_id, children }) => {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [patientIO, setPatientIO] = useState<PatientIO | null>(null);
    const [chatterIO, setChatterIO] = useState<ChatterIO | null>(null);
    const [teamIO, setTeamIO] = useState<TeamIO | null>(null);

    useEffect(() => {
        if (typeof window !== "undefined") {
            const contextSingleton = getContextSingleton();

            setSocket(contextSingleton.socket);
            setPatientIO(contextSingleton.patientIO);
            setChatterIO(contextSingleton.chatterIO);
            setTeamIO(contextSingleton.teamIO);

            if (contextSingleton.session_id != session_id) {
                contextSingleton.session_id = session_id;
                contextSingleton.socket!.on("connect", () => {
                    console.log("Socket connected");
                    contextSingleton.socket!.emit(EmitEvent.JOIN_SESSION, session_id, () => {console.log(`Joined session ${session_id}`)});
                });
            }
        }

        return () => {
        };
    }, []);

    return (
        <SocketContext.Provider value={{ socket:socket, patientIO:patientIO, chatterIO:chatterIO, teamIO: teamIO }}>
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