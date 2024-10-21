import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useState } from "react";
import { Tabs, Tab, Divider } from "@mui/material";
import DataDistributionChart from "./components/report/FraudDistributionChart";
import { useRootStore } from "./store/RootStoreProvider";
import FraudAnalysis from "./pages/FraudAnalysis";

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
      <FraudAnalysis />
    </div>
  );
}

export default observer(App);
