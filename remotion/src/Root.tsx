import React from "react";
import { Composition } from "remotion";
import { DiwaliMarket } from "./DiwaliMarket";
import { DiwaliStory } from "./DiwaliStory";
import { DialogueShort } from "./DialogueShort";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="DiwaliMarket" component={DiwaliMarket} durationInFrames={600} fps={30} width={1080} height={1920} />
    <Composition id="DiwaliStory" component={DiwaliStory} durationInFrames={1800} fps={30} width={1080} height={1920} />
    <Composition id="DialogueShort" component={DialogueShort} durationInFrames={3600} fps={30} width={1080} height={1920} />
  </>
);
