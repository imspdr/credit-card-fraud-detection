import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useState } from "react";
import { useRootStore } from "@src/store/RootStoreProvider";
import FraudDistributionChart from "@src/components/eda/FraudDistributionChart";
import UserChart from "@src/components/eda/UserChart";
import { Button } from "@mui/material";

function FraudAnalysis() {
  const rootStore = useRootStore();
  const [selected, setSelected] = useState(0);
  const listTab = [
    {
      label: "Fraud data 분포 비교",
      value: 0,
    },
    {
      label: "User 시간대별 결제 빈도",
      value: 1,
    },
  ];
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        padding: 20px;
        justify-content: center;
        gap: 20px;
        overflow: auto;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: column;
          gap: 20px;
        `}
      >
        {listTab.map((item) => (
          <Button
            css={css`
              width: 200px;
              height: 100px;
              border-radius: 20px;
              overflow: auto;
              padding: 20px;
              font-size: 20px;
              color: #000000;
              border-radius: 20px;
              display: flex;
              align-items: center;
              justify-content: center;
              background-color: #ffffff;
            `}
            onClick={() => {
              setSelected(item.value);
            }}
          >
            {item.label}
          </Button>
        ))}
      </div>
      <>
        {selected == 0 && (
          <FraudDistributionChart
            width={1000}
            height={600}
            fraud={rootStore.fraudDataDist}
            notFraud={rootStore.notFraudDataDist}
          />
        )}
        {selected == 1 && (
          <UserChart width={1000} height={600} perUserDist={rootStore.perUserDist} />
        )}
      </>
    </div>
  );
}

export default observer(FraudAnalysis);
