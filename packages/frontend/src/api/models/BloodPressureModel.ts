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
/**
 * 
 * @export
 * @interface BloodPressureModel
 */
export interface BloodPressureModel {
    /**
     * 
     * @type {number}
     * @memberof BloodPressureModel
     */
    systolic: number;
    /**
     * 
     * @type {number}
     * @memberof BloodPressureModel
     */
    diastolic: number;
}

/**
 * Check if a given object implements the BloodPressureModel interface.
 */
export function instanceOfBloodPressureModel(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "systolic" in value;
    isInstance = isInstance && "diastolic" in value;

    return isInstance;
}

export function BloodPressureModelFromJSON(json: any): BloodPressureModel {
    return BloodPressureModelFromJSONTyped(json, false);
}

export function BloodPressureModelFromJSONTyped(json: any, ignoreDiscriminator: boolean): BloodPressureModel {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'systolic': json['systolic'],
        'diastolic': json['diastolic'],
    };
}

export function BloodPressureModelToJSON(value?: BloodPressureModel | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'systolic': value.systolic,
        'diastolic': value.diastolic,
    };
}

