import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import SampleTable from "@src/components/serving/SampleTable";
import ServingResult from "@src/components/serving/ServingResult";
import { Button } from "@mui/material";
import { useState } from "react";

function ServingPage() {
  const rootStore = useRootStore();
  const [result, setResult] = useState<number[]>([]);
  const infer = () => {};
  const generate = () => {};
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        padding: 20px;
        gap: 20px;
      `}
    >
      <div>
        <div>
          <Button
            css={css`
              height: 56px;
              width: 120px;
              font-size: 25px;
            `}
            variant={"outlined"}
            onClick={infer}
          >
            generate
          </Button>
          <Button
            css={css`
              height: 56px;
              width: 120px;
              font-size: 25px;
            `}
            variant={"outlined"}
            onClick={infer}
          >
            추론
          </Button>
        </div>
        <SampleTable data={rootStore.sampleData} />
      </div>
      <ServingResult result={result} />
    </div>
  );
}

export default observer(ServingPage);
