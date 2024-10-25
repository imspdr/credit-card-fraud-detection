import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import SampleTable from "@src/components/serving/SampleTable";
import ServingResult from "@src/components/serving/ServingResult";
import { Button } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import { useState } from "react";
import { Transaction } from "@src/store/type";
import { inference } from "@src/store/apis";

function ServingPage() {
  const rootStore = useRootStore();
  const [result, setResult] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const infer = async () => {
    setLoading(true);
    const ret = await inference(rootStore.sampleData);
    setResult(ret);
    setLoading(false);
  };
  const generate = () => {
    const randomInput: Transaction[] = [];
    for (let i = 0; i < 10; i++) {
      let randomIndex = Math.floor(Math.random() * rootStore.evalData.length);
      randomInput.push(rootStore.evalData[randomIndex]!);
    }
    rootStore.sampleData = randomInput;
  };
  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        gap: 20px;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: row;
          gap: 20px;
        `}
      >
        <Button
          css={css`
            width: 120px;
          `}
          variant={"outlined"}
          onClick={generate}
        >
          샘플 생성
        </Button>
        <Button
          css={css`
            width: 120px;
          `}
          variant={"outlined"}
          onClick={infer}
        >
          추론
        </Button>
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: row;
          gap: 20px;
        `}
      >
        <SampleTable data={rootStore.sampleData} />
        <ServingResult result={result} loading={loading} />
      </div>
    </div>
  );
}

export default observer(ServingPage);
