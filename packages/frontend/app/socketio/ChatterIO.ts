import { ScribeClient, EmitEvent } from "@/src/scribe/ScribeClient";
import { ChatEvent, CombatLogUpdateData, HumanMessage, MessageFromNPC, VitalSigns } from "@/src/scribe/scribetypes";
import { useChatStore, ChatStoreMessage } from "../chatter/ChatStore";

export class ChatterIO extends ScribeClient {
    on_chat_message(data: MessageFromNPC) {
        const m: ChatStoreMessage = {
            message: data,
            type: "npc"
        };
        useChatStore.getState().addMessage(m);
    }

    on_chat_event(data: ChatEvent): void {
        const m: ChatStoreMessage = {
            message: data,
            type: "event"
        };
        useChatStore.getState().addMessage(m);
    }

    on_combatlog_update(data: CombatLogUpdateData): void {
        data.log.forEach((m) => {
            console.log(m);
        });
    }

    joinSession(session_id: string) {
        this.socket.emit(EmitEvent.JOIN_SESSION, session_id);
    }

    sendMessage(message_text: string) {
        const m: HumanMessage = {
            message: message_text,
            timestamp: new Date().toISOString()
        };
        useChatStore.getState().addMessage({
            message: m,
            type: "human"
        });
        this.socket.emit(EmitEvent.CHAT_MESSAGE, m);
    }

    // on_patient_vitals_update(data: VitalSigns): void {
    //     console.log("on_patient_vitals_update", data);
    // }
}