/* eslint-disable */
/**
* This file was automatically generated by Scribe's codegen tool.
* This class was generated by GPT3.5, so godspeed and good luck.
*/

import { Socket } from 'socket.io-client';

export enum EmitEvent {
	JOIN_SESSION = "join_session",
	LEAVE_SESSION = "leave_session",
	APPLY_INTERVENTIONS = "apply_interventions",
	CHAT_MESSAGE = "chat_message",
}

function subscribe(obj: ScribeClient, event: string, callback?: (data: any) => void) {
    if (callback) {
        obj.socket.on(event, (data) => {
            callback.call(obj, data);
        });
    }
}

import { ChatEvent, MessageFromNPC, VitalSigns } from "./scribetypes";

export abstract class ScribeClient {
    socket: Socket;
    on_chat_event?(data: ChatEvent): void;
    on_chat_message?(data: MessageFromNPC): void;
    on_patient_vitals_update?(data: VitalSigns): void;

    constructor(socket: Socket) {
        this.socket = socket;
        subscribe(this, "chat_event", this.on_chat_event);
        subscribe(this, "chat_message", this.on_chat_message);
        subscribe(this, "patient_vitals_update", this.on_patient_vitals_update);
    }
}