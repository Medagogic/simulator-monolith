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
import type { ExerciseCreationABCDE } from './ExerciseCreationABCDE';
import {
    ExerciseCreationABCDEFromJSON,
    ExerciseCreationABCDEFromJSONTyped,
    ExerciseCreationABCDEToJSON,
} from './ExerciseCreationABCDE';
import type { ExerciseCreationFutureState } from './ExerciseCreationFutureState';
import {
    ExerciseCreationFutureStateFromJSON,
    ExerciseCreationFutureStateFromJSONTyped,
    ExerciseCreationFutureStateToJSON,
} from './ExerciseCreationFutureState';
import type { ExerciseCreationPatientBasicInfo } from './ExerciseCreationPatientBasicInfo';
import {
    ExerciseCreationPatientBasicInfoFromJSON,
    ExerciseCreationPatientBasicInfoFromJSONTyped,
    ExerciseCreationPatientBasicInfoToJSON,
} from './ExerciseCreationPatientBasicInfo';
import type { ExerciseCreationVitalSigns } from './ExerciseCreationVitalSigns';
import {
    ExerciseCreationVitalSignsFromJSON,
    ExerciseCreationVitalSignsFromJSONTyped,
    ExerciseCreationVitalSignsToJSON,
} from './ExerciseCreationVitalSigns';

/**
 * 
 * @export
 * @interface GeneratedExerciseData
 */
export interface GeneratedExerciseData {
    /**
     * 
     * @type {string}
     * @memberof GeneratedExerciseData
     */
    patientName: string;
    /**
     * 
     * @type {ExerciseCreationPatientBasicInfo}
     * @memberof GeneratedExerciseData
     */
    basicInfo: ExerciseCreationPatientBasicInfo;
    /**
     * 
     * @type {string}
     * @memberof GeneratedExerciseData
     */
    simulationInstructions: string;
    /**
     * 
     * @type {string}
     * @memberof GeneratedExerciseData
     */
    backgroundInformation: string;
    /**
     * 
     * @type {ExerciseCreationVitalSigns}
     * @memberof GeneratedExerciseData
     */
    vitalSigns: ExerciseCreationVitalSigns;
    /**
     * 
     * @type {ExerciseCreationABCDE}
     * @memberof GeneratedExerciseData
     */
    aBCDE: ExerciseCreationABCDE;
    /**
     * 
     * @type {ExerciseCreationFutureState}
     * @memberof GeneratedExerciseData
     */
    future: ExerciseCreationFutureState;
}

/**
 * Check if a given object implements the GeneratedExerciseData interface.
 */
export function instanceOfGeneratedExerciseData(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "patientName" in value;
    isInstance = isInstance && "basicInfo" in value;
    isInstance = isInstance && "simulationInstructions" in value;
    isInstance = isInstance && "backgroundInformation" in value;
    isInstance = isInstance && "vitalSigns" in value;
    isInstance = isInstance && "aBCDE" in value;
    isInstance = isInstance && "future" in value;

    return isInstance;
}

export function GeneratedExerciseDataFromJSON(json: any): GeneratedExerciseData {
    return GeneratedExerciseDataFromJSONTyped(json, false);
}

export function GeneratedExerciseDataFromJSONTyped(json: any, ignoreDiscriminator: boolean): GeneratedExerciseData {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'patientName': json['patientName'],
        'basicInfo': ExerciseCreationPatientBasicInfoFromJSON(json['basicInfo']),
        'simulationInstructions': json['simulationInstructions'],
        'backgroundInformation': json['backgroundInformation'],
        'vitalSigns': ExerciseCreationVitalSignsFromJSON(json['vitalSigns']),
        'aBCDE': ExerciseCreationABCDEFromJSON(json['ABCDE']),
        'future': ExerciseCreationFutureStateFromJSON(json['future']),
    };
}

export function GeneratedExerciseDataToJSON(value?: GeneratedExerciseData | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'patientName': value.patientName,
        'basicInfo': ExerciseCreationPatientBasicInfoToJSON(value.basicInfo),
        'simulationInstructions': value.simulationInstructions,
        'backgroundInformation': value.backgroundInformation,
        'vitalSigns': ExerciseCreationVitalSignsToJSON(value.vitalSigns),
        'ABCDE': ExerciseCreationABCDEToJSON(value.aBCDE),
        'future': ExerciseCreationFutureStateToJSON(value.future),
    };
}
