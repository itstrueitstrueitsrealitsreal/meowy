import React from "react";
import parseHtml from "html-react-parser";
import { useCodeBlockToHtml } from "@llm-ui/code";
import type { CodeToHtmlOptions } from "@llm-ui/code";
import type { LLMOutputComponent } from "@llm-ui/react";
import { getHighlighterCore } from "shiki/core";
import { loadHighlighter, allLangs, allLangsAlias } from "@llm-ui/code";
import { bundledThemes } from "shiki/themes";
import { bundledLanguagesInfo } from "shiki/langs";
import getWasm from "shiki/wasm";

const highlighter = loadHighlighter(
  getHighlighterCore({
    langs: allLangs(bundledLanguagesInfo),
    langAlias: allLangsAlias(bundledLanguagesInfo),
    themes: Object.values(bundledThemes),
    loadWasm: getWasm,
  }),
);

const codeToHtmlOptions: CodeToHtmlOptions = {
  theme: "github-dark",
};

const CodeBlock: LLMOutputComponent = ({ blockMatch }) => {
  const { html, code } = useCodeBlockToHtml({
    markdownCodeBlock: blockMatch.output,
    highlighter,
    codeToHtmlOptions,
  });

  if (!html) {
    return (
      <pre className="shiki">
        <code>{code}</code>
      </pre>
    );
  }
  return <>{parseHtml(html)}</>;
};

export default CodeBlock;
