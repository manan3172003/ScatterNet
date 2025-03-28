import { unified } from "unified"
import remarkParse from "remark-parse"
import remarkRehype from "remark-rehype"
import rehypeStringify from "rehype-stringify"
import rehypeRaw from "rehype-raw";
import rehypeHighlight from "rehype-highlight";

type MarkdownRendererProps = {
  children: string;
};

export default function MarkdownRenderer({ children }: MarkdownRendererProps) {

    const result = unified()
  .use(remarkParse)
  .use(remarkRehype, {
    allowDangerousHtml: true,
  })
  .use(rehypeRaw)
  .use(rehypeHighlight)
  .use(rehypeStringify)
  .processSync(children)

    return (
            <div
            dangerouslySetInnerHTML={{__html: result}}
            />
    )
}
