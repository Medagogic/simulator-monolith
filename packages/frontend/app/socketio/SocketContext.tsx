"use client"

import { EmitEvent } from "@/src/scribe/ScribeClient";
import React, { createContext, useContext, useEffect, useState, ReactNode, use } from "react";
import { io, Socket } from "socket.io-client";
import { PatientIO } from "./PatientIO";
import { ChatterIO } from "./ChatterIO";
import { TeamIO } from "./TeamIO";
import { DeviceIO } from "./DeviceIO";
import { SessionIO } from "./SessionIO";
import { DrClippyIO } from "./DrClippyIO";
import { LearnerActionEvaluatorIO } from "./LearnerActionEvaluatorIO";
import { useSessionStore } from "../storage/SessionStore";

// Defining the context shape
interface ISocketContext {
    socket: Socket | null;
    sessionIO: SessionIO | null;
    patientIO: PatientIO | null;
    chatterIO: ChatterIO | null;
    teamIO: TeamIO | null;
    deviceIO: DeviceIO | null;
    drClippyIO: DrClippyIO | null;
    learnerActionEvaluatorIO: LearnerActionEvaluatorIO | null;
}

const SocketContext = createContext<ISocketContext | null>(null);

interface SocketProviderProps {
    session_id: string;
    children: ReactNode;
}

interface ContextSingleton {
    session_id: string | null;
    socket: Socket;

    sessionIO: SessionIO;
    patientIO: PatientIO;
    chatterIO: ChatterIO;
    teamIO: TeamIO;
    deviceIO: DeviceIO;
    drClippyIO: DrClippyIO;
    learnerActionEvaluatorIO: LearnerActionEvaluatorIO;
}

let context_singleton: ContextSingleton | null = null;

const getContextSingleton = () => {
  if (context_singleton === null) {
    const socket_url = `http://localhost:5000/session`;
    const socket = io(socket_url);
    const sessionIO = new SessionIO(socket);
    const patientIO = new PatientIO(socket);
    const chatterIO = new ChatterIO(socket);
    const teamIO = new TeamIO(socket);
    const deviceIO = new DeviceIO(socket);
    const drClippyIO = new DrClippyIO(socket);
    const learnerActionEvaluatorIO = new LearnerActionEvaluatorIO(socket);

    context_singleton = {
        socket: socket,
        session_id: null,

        sessionIO: sessionIO,
        patientIO: patientIO,
        chatterIO: chatterIO,
        teamIO: teamIO,
        deviceIO: deviceIO,
        drClippyIO: drClippyIO,
        learnerActionEvaluatorIO: learnerActionEvaluatorIO,
    };
  }
  return context_singleton;
};

export const SocketProvider: React.FC<SocketProviderProps> = ({ session_id, children }) => {
    const sessionStore = useSessionStore();

    const [socket, setSocket] = useState<Socket | null>(null);
    const [sessionIO, setSessionIO] = useState<SessionIO | null>(null);
    const [patientIO, setPatientIO] = useState<PatientIO | null>(null);
    const [chatterIO, setChatterIO] = useState<ChatterIO | null>(null);
    const [teamIO, setTeamIO] = useState<TeamIO | null>(null);
    const [deviceIO, setDeviceIO] = useState<DeviceIO | null>(null);
    const [drClippyIO, setDrClippyIO] = useState<DrClippyIO | null>(null);
    const [learnerActionEvaluatorIO, setLearnerActionEvaluatorIO] = useState<LearnerActionEvaluatorIO | null>(null);

    useEffect(() => {
        if (typeof window !== "undefined") {
            const contextSingleton = getContextSingleton();

            setSocket(contextSingleton.socket);
            setSessionIO(contextSingleton.sessionIO);
            setPatientIO(contextSingleton.patientIO);
            setChatterIO(contextSingleton.chatterIO);
            setTeamIO(contextSingleton.teamIO);
            setDeviceIO(contextSingleton.deviceIO);
            setDrClippyIO(contextSingleton.drClippyIO);
            setLearnerActionEvaluatorIO(contextSingleton.learnerActionEvaluatorIO);

            if (contextSingleton.session_id != session_id) {
                contextSingleton.session_id = session_id;
                contextSingleton.socket!.on("connect", () => {
                    console.log("Socket connected");
                    sessionStore.setConnected(true);
                    contextSingleton.socket!.emit(EmitEvent.JOIN_SESSION, session_id, () => {console.log(`Joined session ${session_id}`)});
                });
            }
        }

        return () => {
        };
    }, []);

    return (
        <SocketContext.Provider value={{
            socket:socket,
            sessionIO: sessionIO,
            patientIO:patientIO,
            chatterIO:chatterIO,
            teamIO: teamIO,
            deviceIO: deviceIO,
            drClippyIO: drClippyIO,
            learnerActionEvaluatorIO: learnerActionEvaluatorIO,
            }}>
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

export const useSessionIO = (): SessionIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useSessionIO must be used within a SocketProvider");
    }

    return context.sessionIO;
}

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

export const useDeviceIO = (): DeviceIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useDeviceIO must be used within a SocketProvider");
    }

    return context.deviceIO;
}

export const useDrClippyIO = (): DrClippyIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useDrClippyIO must be used within a SocketProvider");
    }

    return context.drClippyIO;
}

export const useLearnerActionEvaluatorIO = (): LearnerActionEvaluatorIO | null => {
    const context = useContext(SocketContext);

    if (!context) {
        throw new Error("useLearnerActionEvaluatorIO must be used within a SocketProvider");
    }

    return context.learnerActionEvaluatorIO;
}