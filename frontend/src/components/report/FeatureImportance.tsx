import { Card } from "@mui/material";
import { ResponsivePie } from "@nivo/pie";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";

type feature_importance = {
  label: string[];
  value: number[];
};

export default function FeatureImportance(props: {
  data?: feature_importance;
  width: number;
  height: number;
}) {
  return (
    <Card
      css={css`
        width: ${props.width}px;
        height: ${props.height}px;
        border-radius: 20px;
        padding: 20px;
      `}
      elevation={0}
    >
      <Typography variant="h6">Feature Importance</Typography>
      {props.data && props.data.label.length <= props.data.value.length && (
        <ResponsivePie
          data={props.data.label
            .map((label: string, index: number) => {
              return {
                id: label,
                value: Number(props.data!.value[index]!.toFixed(6)),
              };
            })
            .sort((a, b) => b.value - a.value)
            .filter((_, index) => index < 12)}
          margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
          innerRadius={0.5}
          padAngle={0.7}
          cornerRadius={3}
          activeOuterRadiusOffset={8}
          colors={{ scheme: "blues" }}
          borderWidth={1}
          borderColor={{
            from: "color",
            modifiers: [["darker", 0.2]],
          }}
          arcLinkLabelsSkipAngle={10}
          arcLinkLabelsTextColor="#333333"
          arcLinkLabelsThickness={2}
          arcLinkLabelsColor={{ from: "color" }}
          arcLabelsSkipAngle={10}
          arcLabelsTextColor={{
            from: "color",
            modifiers: [["darker", 2]],
          }}
        />
      )}
    </Card>
  );
}
