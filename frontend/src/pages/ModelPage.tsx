import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import Report from "@src/components/report/Report";
import { Select, MenuItem } from "@mui/material";
import { useState } from "react";

function ModelPage() {
  const rootStore = useRootStore();
  const [selected, setSelected] = useState(0);
  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px 20px 0px 20px;
        gap: 20px;
      `}
    >
      <Select
        value={selected}
        onChange={(e) => setSelected(Number(e.target.value))}
        css={css`
          width: 200px;
          height: 50px;
          background-color: #ffffff;
        `}
      >
        {rootStore.report.map((rep) => (
          <MenuItem value={`${rep.index}`}>{`모델 - ${rep.index}`}</MenuItem>
        ))}
      </Select>
      <Report report={rootStore.report[selected]!} />
    </div>
  );
}

export default observer(ModelPage);
