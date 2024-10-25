import { Card } from "@mui/material";
import { css } from "@emotion/react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { Base, ModelReport, Transaction } from "@src/store/type";

export default function SampleTable(props: { data: Transaction[] }) {
  return (
    <TableContainer
      component={Paper}
      css={css`
        width: 1000px;
        height: 600px;
        font-size: 8px;
        overflow-x: auto;
      `}
    >
      {props.data.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              {[...Object.keys(props.data[0]!)].map((key) => (
                <TableCell
                  css={css`
                    height: 20px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                  `}
                >
                  {key}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {props.data.map((row) => (
              <TableRow>
                {[...Object.keys(props.data[0]!)].map((key) => (
                  <TableCell
                    css={css`
                      height: 20px;
                      overflow: hidden;
                      text-overflow: ellipsis;
                      white-space: nowrap;
                    `}
                  >
                    {row[key as keyof Transaction]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </TableContainer>
  );
}
