"use client"

import React from 'react';
import MarkdownDisplay from './MarkdownDisplay';

const MarkdownPage: React.FC = () => {
  const sampleMarkdown = `
# This is a header

And this is a paragraph.

- Here's a list
  - Nested item 1
  - Nested item 2

## Another Header

> This is a blockquote. 

\`\`\`javascript
console.log("This is a code block in JavaScript.");
\`\`\`

[Click me](https://www.example.com) for a link.
`;

  return (
    <div style={{ padding: '20px' }}>
      <MarkdownDisplay content={sampleMarkdown} />
    </div>
  );
}

export default MarkdownPage;
