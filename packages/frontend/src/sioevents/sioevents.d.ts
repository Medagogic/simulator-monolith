/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Timestamp = number;
export type Value = number;
export type Name = string;

export interface SIOEvents {
  test_event: SimUpdateData;
}
export interface SimUpdateData {
  timestamp: Timestamp;
  value: Value;
  name: Name;
}