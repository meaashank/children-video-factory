import React from "react";
import { Composition } from "remotion";
import { DiwaliMarket } from "./DiwaliMarket";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="DiwaliMarket"
    component={DiwaliMarket}
    durationInFrames={600}
    fps={30}
    width={1080}
    height={1920}
  />
);
