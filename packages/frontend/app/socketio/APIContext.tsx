"use client"

import React, { ReactNode, createContext, useContext } from 'react';
import { DefaultApi, Configuration } from "@/src/api";

interface IAPIContext {
  apiInstance: DefaultApi;
  sessionId?: string;
}

interface APIProviderProps {
  sessionId?: string;
  children: ReactNode;
}

interface APIContextSingleton {
  apiInstance: DefaultApi;
  sessionId?: string;
}

const APIContext = createContext<IAPIContext | null>(null);

let context_singleton: APIContextSingleton | null = null;

function getContextSingleton(sessionID?: string) {
  if (context_singleton === null) {
    console.log("Creating new API context singleton at", process.env.NEXT_PUBLIC_API_HOST);
    const apiConfig = new Configuration({
      basePath: process.env.NEXT_PUBLIC_API_HOST,
    });
    const apiInstance = new DefaultApi(apiConfig);
    context_singleton = { apiInstance: apiInstance, sessionId: sessionID };
  } else if (context_singleton.sessionId !== sessionID) {
    context_singleton.sessionId = sessionID;
  }
  return context_singleton;
}

export const APIProvider: React.FC<APIProviderProps> = ({ sessionId , children }) => {
  const apiSingleton = getContextSingleton(sessionId);

  return (
    <APIContext.Provider value={{apiInstance: apiSingleton.apiInstance, sessionId: apiSingleton.sessionId}}>
      {children}
    </APIContext.Provider>
  );
};

export const useAPI = () => {
  const context = useContext(APIContext);
  if (!context) {
    throw new Error("useApi must be used within an ApiProvider");
  }
  return context.apiInstance;
};

export const sessionRequestParams = () => {
  const context = useContext(APIContext);
  if (!context) {
    throw new Error("APIRequestParams must be used within an ApiProvider");
  }
  return {
    sessionId: context.sessionId
  };
}