import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useState } from "react";
import { Tabs, Tab, Divider } from "@mui/material";
import DataDistributionChart from "./components/detail/DataDistributionChart";
import { useRootStore } from "./store/RootStoreProvider";

function App() {
  const rootStore = useRootStore();
  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        padding: 20px;
        gap: 20px;
      `}
    >
      <DataDistributionChart width={1000} height={300} dataDistribution={rootStore.fraudDataDist} />
      <DataDistributionChart
        width={1000}
        height={300}
        dataDistribution={rootStore.notFraudDataDist}
      />
    </div>
  );
}

export default observer(App);
