import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useState } from "react";
import { Tabs, Tab, Divider } from "@mui/material";
import FraudAnalysis from "./pages/FraudAnalysis";
import ModelPage from "./pages/ModelPage";
import ServingPage from "./pages/ServingPage";

function App() {
  const [tab, setTab] = useState(2);

  const tabInfos = [
    {
      value: 0,
      name: "EDA",
    },
    {
      value: 1,
      name: "모델 정보",
    },
    {
      value: 2,
      name: "테스트",
    },
  ];

  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        padding: 10px;
      `}
    >
      <Tabs value={tab} onChange={(e, v) => setTab(v)}>
        {tabInfos.map((tabinfo) => (
          <Tab
            css={css`
              width: 140px;
              font-size: 20px;
            `}
            value={tabinfo.value}
            label={tabinfo.name}
          />
        ))}
      </Tabs>
      <Divider
        css={css`
          width: 100%;
          color: #d6d6d6;
        `}
      />
      {(function test(v: number) {
        switch (v) {
          case 0:
            return <FraudAnalysis />;
          case 1:
            return <ModelPage />;
          case 2:
            return <ServingPage />;
          default:
            return <FraudAnalysis />;
        }
      })(tab)}
    </div>
  );
}

export default observer(App);
