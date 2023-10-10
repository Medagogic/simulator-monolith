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
  SessionData,
} from '../models/index';
import {
    ExerciseCreationParamsFromJSON,
    ExerciseCreationParamsToJSON,
    GeneratedExerciseDataFromJSON,
    GeneratedExerciseDataToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    SessionDataFromJSON,
    SessionDataToJSON,
} from '../models/index';

export interface HandleGenerateStaticApiGenerateExercisePostRequest {
    exerciseCreationParams: ExerciseCreationParams;
}

/**
 * 
 */
export class DefaultApi extends runtime.BaseAPI {

    /**
     * Handle Create Session
     */
    async handleCreateSessionSessionNewPostRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/session/new`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Handle Create Session
     */
    async handleCreateSessionSessionNewPost(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.handleCreateSessionSessionNewPostRaw(initOverrides);
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
     * Handle List Sessions
     */
    async handleListSessionsSessionListGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<SessionData>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/session/list`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(SessionDataFromJSON));
    }

    /**
     * Handle List Sessions
     */
    async handleListSessionsSessionListGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<SessionData>> {
        const response = await this.handleListSessionsSessionListGetRaw(initOverrides);
        return await response.value();
    }

    /**
     * Handle Test
     */
    async handleTestSessionsSessionIdChatTestGetGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/sessions/<session_id>/chat/test-get`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Handle Test
     */
    async handleTestSessionsSessionIdChatTestGetGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.handleTestSessionsSessionIdChatTestGetGetRaw(initOverrides);
    }

    /**
     * Save Api Json
     */
    async saveApiJsonSaveDocsPostRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/save_docs`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Save Api Json
     */
    async saveApiJsonSaveDocsPost(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.saveApiJsonSaveDocsPostRaw(initOverrides);
    }

}
