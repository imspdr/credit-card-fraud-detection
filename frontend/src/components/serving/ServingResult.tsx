import { Card } from "@mui/material";
import { css } from "@emotion/react";
import {
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
} from "@mui/material";

export default function ServingResult(props: { result: number[] }) {
  return (
    <TableContainer
      component={Paper}
      css={css`
        width: 100px;
        height: 600px;
        font-size: 8px;
      `}
    >
      {props.result.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>{"Result"}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.result.map((row) => (
              <TableRow>
                <TableCell>{row}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </TableContainer>
  );
}
