import { ScribeClient } from "@/src/scribe/ScribeClient";
import { NPCThinking, SIO_NPCData } from "@/src/scribe/scribetypes";
import { useTeamStore } from "../storage/TeamStore";
import { APINPCData } from "@/src/api";

export class TeamIO extends ScribeClient {
    on_npc_data(data: SIO_NPCData): void {
        console.log(`Received NPC data for ${data.id}`);

        const npc_data: APINPCData = {
            id: data.id,
            definition: {
                name: data.definition.name,
                role: data.definition.role,
                specialities: data.definition.specialities,
                yearsOfExperience: data.definition.years_of_experience,
            },
            currentTask: data.current_task as string
        }

        // useTeamStore.getState().teamById[data.id] = npc_data;
        useTeamStore.getState().setNPCData(data.id, npc_data);

        console.log(`Updated storage for NPC ${data.id}`, npc_data);
    }

    on_npc_thinking_updated(data: NPCThinking): void {
        const about: string | null = data.about === undefined ? null : data.about;
        useTeamStore.getState().setThinkingAbout(data.npc_id, about);
    }
}