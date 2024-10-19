import React, { createContext, useContext, useMemo } from "react";
import { RootStore } from "./RootStore";

const RootContext = createContext<RootStore | null>(null);

export const RootStoreProvider = ({ children }: { children: React.ReactElement }) => {
  const store = useMemo(() => {
    const rootStore = new RootStore();
    return rootStore;
  }, []);
  return <RootContext.Provider value={store}>{children}</RootContext.Provider>;
};

export const useRootStore = () => {
  const context = useContext(RootContext);

  if (context === null) {
    throw Error("Context.Provider 범위를 벗어났습니다.");
  }
  return context;
};
