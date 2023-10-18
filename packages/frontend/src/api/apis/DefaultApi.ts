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


import * as runtime from '../runtime';
import type {
  ExerciseCreationParams,
  GeneratedExerciseData,
  HTTPValidationError,
} from '../models/index';
import {
    ExerciseCreationParamsFromJSON,
    ExerciseCreationParamsToJSON,
    GeneratedExerciseDataFromJSON,
    GeneratedExerciseDataToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
} from '../models/index';

export interface HandleGenerateStaticApiGenerateExercisePostRequest {
    exerciseCreationParams: ExerciseCreationParams;
}

export interface MedsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGetRequest {
    sessionId: string;
}

export interface TestEndpointNewSessionRouterSessionSessionIdTestSessionGetRequest {
    sessionId: string;
}

/**
 * 
 */
export class DefaultApi extends runtime.BaseAPI {

    /**
     * Create Session
     */
    async createSessionNewSessionRouterCreateSessionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/new-session-router/create-session`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Create Session
     */
    async createSessionNewSessionRouterCreateSessionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.createSessionNewSessionRouterCreateSessionGetRaw(initOverrides);
    }

    /**
     * Handle Generate
     */
    async handleGenerateStaticApiGenerateExercisePostRaw(requestParameters: HandleGenerateStaticApiGenerateExercisePostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<GeneratedExerciseData>> {
        if (requestParameters.exerciseCreationParams === null || requestParameters.exerciseCreationParams === undefined) {
            throw new runtime.RequiredError('exerciseCreationParams','Required parameter requestParameters.exerciseCreationParams was null or undefined when calling handleGenerateStaticApiGenerateExercisePost.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/static_api/generate_exercise`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: ExerciseCreationParamsToJSON(requestParameters.exerciseCreationParams),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => GeneratedExerciseDataFromJSON(jsonValue));
    }

    /**
     * Handle Generate
     */
    async handleGenerateStaticApiGenerateExercisePost(requestParameters: HandleGenerateStaticApiGenerateExercisePostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<GeneratedExerciseData> {
        const response = await this.handleGenerateStaticApiGenerateExercisePostRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * List Sessions
     */
    async listSessionsNewSessionRouterListSessionsGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/new-session-router/list-sessions`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * List Sessions
     */
    async listSessionsNewSessionRouterListSessionsGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.listSessionsNewSessionRouterListSessionsGetRaw(initOverrides);
    }

    /**
     * Medsim Vitals
     */
    async medsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGetRaw(requestParameters: MedsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.sessionId === null || requestParameters.sessionId === undefined) {
            throw new runtime.RequiredError('sessionId','Required parameter requestParameters.sessionId was null or undefined when calling medsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGet.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/new-session-router/session/{session_id}/medsim/vitals`.replace(`{${"session_id"}}`, encodeURIComponent(String(requestParameters.sessionId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Medsim Vitals
     */
    async medsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGet(requestParameters: MedsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.medsimVitalsNewSessionRouterSessionSessionIdMedsimVitalsGetRaw(requestParameters, initOverrides);
    }

    /**
     * Test Endpoint
     */
    async testEndpointNewSessionRouterSessionSessionIdTestSessionGetRaw(requestParameters: TestEndpointNewSessionRouterSessionSessionIdTestSessionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.sessionId === null || requestParameters.sessionId === undefined) {
            throw new runtime.RequiredError('sessionId','Required parameter requestParameters.sessionId was null or undefined when calling testEndpointNewSessionRouterSessionSessionIdTestSessionGet.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/new-session-router/session/{session_id}/test-session`.replace(`{${"session_id"}}`, encodeURIComponent(String(requestParameters.sessionId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Test Endpoint
     */
    async testEndpointNewSessionRouterSessionSessionIdTestSessionGet(requestParameters: TestEndpointNewSessionRouterSessionSessionIdTestSessionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.testEndpointNewSessionRouterSessionSessionIdTestSessionGetRaw(requestParameters, initOverrides);
    }

}
