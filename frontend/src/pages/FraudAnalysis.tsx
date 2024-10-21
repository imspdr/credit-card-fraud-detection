import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import FraudDistributionChart from "@src/components/report/FraudDistributionChart";

function FraudAnalysis() {
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
      <FraudDistributionChart
        width={1000}
        height={600}
        fraud={rootStore.fraudDataDist}
        notFraud={rootStore.notFraudDataDist}
      />
    </div>
  );
}

export default observer(FraudAnalysis);
