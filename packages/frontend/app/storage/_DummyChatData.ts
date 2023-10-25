const dummyMessages = [
    {
        message: { message: "Hello", timestamp: 1635100000, npc_id: "npc_1" },
        type: "npc",
    },
    {
        message: { message: "Hi", timestamp: 1635101000 },
        type: "human",
    },
    {
        message: { event: "joined", timestamp: 1635102000 },
        type: "event",
    },
    {
        message: { message: "How are you?", timestamp: 1635103000, npc_id: "npc_2" },
        type: "npc",
    },
    {
        message: { message: "I'm fine", timestamp: 1635104000, target_npc_id: "npc_2" },
        type: "human",
    },
    {
        message: { event: "left", timestamp: 1635105000, npc_id: "npc_1" },
        type: "event",
    },
    {
        message: { message: "Goodbye", timestamp: 1635106000, npc_id: "npc_3" },
        type: "npc",
    },
    {
        message: { message: "See you", timestamp: 1635107000 },
        type: "human",
    },
    {
        message: { event: "npc_moved", timestamp: 1635108000, npc_id: "npc_3" },
        type: "event",
    },
    {
        message: { message: "Why did you move?", timestamp: 1635109000, npc_id: "npc_3" },
        type: "npc",
    },
    {
        message: { message: "No reason", timestamp: 1635110000, target_npc_id: "npc_3" },
        type: "human",
    },
    {
        message: { event: "trade_opened", timestamp: 1635111000 },
        type: "event",
    },
    {
        message: { message: "Want to trade?", timestamp: 1635112000, npc_id: "npc_2" },
        type: "npc",
    },
    {
        message: { message: "Sure", timestamp: 1635113000, target_npc_id: "npc_2" },
        type: "human",
    },
    {
        message: { event: "trade_closed", timestamp: 1635114000 },
        type: "event",
    },
    {
        message: { message: "Thanks", timestamp: 1635115000, npc_id: "npc_2" },
        type: "npc",
    },
    {
        message: { message: "You're welcome", timestamp: 1635116000, target_npc_id: "npc_2" },
        type: "human",
    },
    {
        message: { event: "npc_died", timestamp: 1635117000, npc_id: "npc_3" },
        type: "event",
    },
    {
        message: { message: "Oh no", timestamp: 1635118000 },
        type: "human",
    },
    {
        message: { event: "respawned", timestamp: 1635119000, npc_id: "npc_3" },
        type: "event",
    },
    {
        message: { message: "I'm back", timestamp: 1635120000, npc_id: "npc_3" },
        type: "npc",
    },
];


export function getDummyMessages() {
    (dummyMessages as Array<any>).forEach(msg => {
      if ('timestamp' in msg.message) {
        msg.message.timestamp = new Date(msg.message.timestamp * 1000).toUTCString();
      }
    });
    return dummyMessages;
}