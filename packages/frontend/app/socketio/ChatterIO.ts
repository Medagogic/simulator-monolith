import { ScribeClient, EmitEvent } from "@/src/scribe/ScribeClient";
import {  CombatLogUpdateData, Evt_Chat_Event, Evt_Chat_HumanMessage, Evt_Chat_NPCMessage, SIO_ChatHistory } from "@/src/scribe/scribetypes";
import { useChatStore, ChatStoreMessage } from "../storage/ChatStore";
import { useCombatLogStore } from "../storage/CombatLogStore";

export class ChatterIO extends ScribeClient {
    on_full_chat_history(data: SIO_ChatHistory): void {
        // console.log("on_full_chat_history", data);
        data.messages.forEach((m: any) => {
            const chatStoreMsg: ChatStoreMessage = {
                message: m,
                type: m.type!
            };
            useChatStore.getState().addMessage(chatStoreMsg);
        });
    }

    on_chat_message(data: Evt_Chat_NPCMessage) {
        const m: ChatStoreMessage = {
            message: data,
            type: data.type!
        };
        useChatStore.getState().addMessage(m);
    }

    on_chat_event(data: Evt_Chat_Event): void {
        const m: ChatStoreMessage = {
            message: data,
            type: data.type!
        };
        useChatStore.getState().addMessage(m);
    }


    on_combatlog_update(data: CombatLogUpdateData): void {
        useCombatLogStore.getState().setLogs(data.log);
    }

    joinSession(session_id: string) {
        this.socket.emit(EmitEvent.JOIN_SESSION, session_id);
    }

    sendMessage(message_text: string, target_npc_id?: string) {
        const m: Evt_Chat_HumanMessage = {
            content: message_text,
            target_npc_id: target_npc_id,
            type: "chat_human_message"
        };
        useChatStore.getState().addMessage({
            message: m,
            type: "chat_human_message"
        });
        this.socket.emit(EmitEvent.CHAT_MESSAGE, m);
    }
}