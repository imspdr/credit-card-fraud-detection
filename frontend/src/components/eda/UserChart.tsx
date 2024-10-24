import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography, Select, MenuItem } from "@mui/material";
import { UserData } from "@src/store/type";
import { useEffect, useState } from "react";
import TimeChart from "./TimeChart";

export default function UserChart(props: {
  width: number;
  height: number;
  label?: string;
  perUserDist: UserData[];
}) {
  const [selectedUser, setSelectedUser] = useState("0");
  const [selectedData, setSelectedData] = useState(props.perUserDist[0]);

  useEffect(() => {
    setSelectedData(props.perUserDist.find((item) => String(item.user) === selectedUser));
  }, [selectedUser]);
  return (
    <Card
      css={css`
        width: ${props.width}px;
        height: ${props.height}px;
        border-radius: 20px;
        padding: 20px;

        display: flex;
        flex-direction: column;
        gap: 20px;
      `}
      elevation={0}
    >
      <div
        css={css`
          display: flex;
          flex-direction: row;
          justify-content: space-between;
        `}
      >
        <Typography variant="h6">
          {"USER 시간대별 결제 빈도 (상단 Fraud 하단 Not Fraud)"}
        </Typography>
        <Select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
          css={css`
            width: 200px;
          `}
        >
          {props.perUserDist.map((item) => (
            <MenuItem value={`${item.user}`}>{`user - ${item.user}`}</MenuItem>
          ))}
        </Select>
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: column;
          justify-content: center;
          gap: 10px;
        `}
      >
        {selectedData && (
          <TimeChart width={props.width - 10} height={props.height - 100} data={selectedData} />
        )}
      </div>
    </Card>
  );
}
