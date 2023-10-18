import { ScribeClient, EmitEvent } from "@/src/scribe/ScribeClient";
import { ChatMessage } from "@/src/scribe/scribetypes";
import { useChatStore, ChatStoreMessage } from "./ChatStore";

export class ChatterIO extends ScribeClient {
    on_chat_message(data: ChatMessage) {
        console.log(data.sender, this.socket.id);
        if (data.sender === this.socket.id) {
            return;
        }
        const m: ChatStoreMessage = {
            text: data.message,
            sender: data.sender,
            date: new Date(data.timestamp)
        };
        useChatStore.getState().addMessage(m);
    }

    joinSession(session_id: string) {
        this.socket.emit(EmitEvent.JOIN_SESSION, session_id);
    }

    sendMessage(message: string) {
        this.socket.emit(EmitEvent.CHAT_MESSAGE, message);
    }
}