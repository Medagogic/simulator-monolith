/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Event = string;
export type Timestamp = string;
export type NpcId = string | null;
export type Message = string;
export type Timestamp1 = string;
export type NpcId1 = string;
/**
 * The body temperature in degrees Celsius or Fahrenheit
 */
export type Temperature = number;
/**
 * The heart rate in beats per minute
 */
export type HeartRate = number;
/**
 * The number of breaths taken per minute
 */
export type RespiratoryRate = number;
export type Systolic = number;
export type Diastolic = number;
/**
 * The blood glucose level
 */
export type BloodGlucose = number;
/**
 * The oxygen saturation in percentage
 */
export type OxygenSaturation = number;
/**
 * The capillary refill time in seconds
 */
export type CapillaryRefill = number;
export type Interventions = string[];
export type Message1 = string;
export type Timestamp2 = string;
export type TargetNpcId = string | null;

export interface ScribeEvents {
  chat_event: ChatEvent;
  chat_message: MessageFromNPC;
  patient_vitals_update: VitalSigns;
  __server_on_join_session?: {
    session_id?: {
      [k: string]: unknown;
    };
  };
  __server_on_leave_session?: {};
  __server_on_apply_interventions?: {
    data?: InterventionData;
  };
  __server_on_chat_message?: {
    data?: HumanMessage;
    return?: {
      [k: string]: unknown;
    };
  };
}
export interface ChatEvent {
  event: Event;
  timestamp: Timestamp;
  npc_id?: NpcId;
}
export interface MessageFromNPC {
  message: Message;
  timestamp: Timestamp1;
  npc_id: NpcId1;
}
export interface VitalSigns {
  temperature: Temperature;
  heart_rate: HeartRate;
  respiratory_rate: RespiratoryRate;
  blood_pressure: BloodPressureModel;
  blood_glucose: BloodGlucose;
  oxygen_saturation: OxygenSaturation;
  capillary_refill: CapillaryRefill;
}
export interface BloodPressureModel {
  systolic: Systolic;
  diastolic: Diastolic;
  [k: string]: unknown;
}
export interface InterventionData {
  interventions: Interventions;
}
export interface HumanMessage {
  message: Message1;
  timestamp: Timestamp2;
  target_npc_id?: TargetNpcId;
}
