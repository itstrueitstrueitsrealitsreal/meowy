import React from "react";
import { useStreamExample, throttleBasic } from "@llm-ui/react";
import LLMOutputRenderer from "./LLMOutputRenderer";

const example = `## Python

\`\`\`python
print('Hello llm-ui!')
\`\`\`

## Typescript

\`\`\`typescript
console.log('Hello llm-ui!');
\`\`\`

## Image
![image](https://cdn2.thecatapi.com/images/7qv.jpg)
`;

const StreamedExample = () => {
  const { isStreamFinished, output } = useStreamExample(example);

  return (
    <LLMOutputRenderer
      output={output}
      isStreamFinished={isStreamFinished}
      throttle={throttleBasic({
        readAheadChars: 10,
        targetBufferChars: 9,
        adjustPercentage: 0.2,
        frameLookBackMs: 7500,
        windowLookBackMs: 2000,
      })}
    />
  );
};

export default StreamedExample;
