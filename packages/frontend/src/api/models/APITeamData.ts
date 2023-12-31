/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { APINPCData } from './APINPCData';
import {
    APINPCDataFromJSON,
    APINPCDataFromJSONTyped,
    APINPCDataToJSON,
} from './APINPCData';

/**
 * 
 * @export
 * @interface APITeamData
 */
export interface APITeamData {
    /**
     * 
     * @type {Array<APINPCData>}
     * @memberof APITeamData
     */
    npcData: Array<APINPCData>;
}

/**
 * Check if a given object implements the APITeamData interface.
 */
export function instanceOfAPITeamData(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "npcData" in value;

    return isInstance;
}

export function APITeamDataFromJSON(json: any): APITeamData {
    return APITeamDataFromJSONTyped(json, false);
}

export function APITeamDataFromJSONTyped(json: any, ignoreDiscriminator: boolean): APITeamData {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'npcData': ((json['npc_data'] as Array<any>).map(APINPCDataFromJSON)),
    };
}

export function APITeamDataToJSON(value?: APITeamData | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'npc_data': ((value.npcData as Array<any>).map(APINPCDataToJSON)),
    };
}

