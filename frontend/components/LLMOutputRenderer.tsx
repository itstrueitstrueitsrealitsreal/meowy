import React from "react";
import { useLLMOutput, ThrottleFunction } from "@llm-ui/react";
import MarkdownComponent from "./MarkdownComponent";
import CodeBlock from "./CodeBlock";
import {
  findCompleteCodeBlock,
  findPartialCodeBlock,
  codeBlockLookBack,
} from "@llm-ui/code";
import { markdownLookBack } from "@llm-ui/markdown";

interface LLMOutputRendererProps {
  output: string;
  isStreamFinished: boolean;
  throttle?: ThrottleFunction;
}

const LLMOutputRenderer: React.FC<LLMOutputRendererProps> = ({
  output,
  isStreamFinished,
  throttle,
}) => {
  const { blockMatches } = useLLMOutput({
    llmOutput: output,
    isStreamFinished,
    throttle,
    fallbackBlock: {
      component: MarkdownComponent,
      lookBack: markdownLookBack(),
    },
    blocks: [
      {
        component: CodeBlock,
        findCompleteMatch: findCompleteCodeBlock(),
        findPartialMatch: findPartialCodeBlock(),
        lookBack: codeBlockLookBack(),
      },
    ],
  });
  return (
    <div>
      {blockMatches.map((blockMatch, index) => {
        const Component = blockMatch.block.component;
        return <Component key={index} blockMatch={blockMatch} />;
      })}
    </div>
  );
};

export default LLMOutputRenderer;
