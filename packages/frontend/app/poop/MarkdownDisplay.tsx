"use client"

import React, { useState, useRef, useEffect, useMemo } from 'react';
import { parse as marked, options } from 'marked';
import CommentBubble, { CommentBubbleProps } from './CommentBubble';
import rangy from 'rangy';
import 'rangy/lib/rangy-textrange';
import 'rangy/lib/rangy-highlighter';
import 'rangy/lib/rangy-classapplier';


const MarkdownDisplay: React.FC<{ content: string }> = ({ content }) => {
  const markdownRef = useRef<HTMLDivElement>(null);
  const [comments, setComments] = useState<Array<CommentBubbleProps>>([]);

  useEffect(() => {
    rangy.init();

    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  const handleMouseUp = (e: MouseEvent) => {
    const selection = rangy.getSelection();

    if (selection && selection.rangeCount > 0) {
      var rangyRange = selection.getRangeAt(0);

      if (rangyRange.toString().trim() !== '') {
        rangyRange.expand("word");
        selection.setSingleRange(rangyRange); // Update the selection
        const rangeRect = rangyRange.nativeRange.getBoundingClientRect();
        const markdownRect = markdownRef.current!.getBoundingClientRect();

        const position = {
          top: rangeRect.top + (rangeRect.height / 2) - markdownRect.top,
          left: markdownRect.right
        };

        addComment({
          position: position,
          rangyRange: rangyRange,
          onComment: (comment: string) => {
            console.log(comment);  // Handle the comment as you see fit
          }
        });
      }
    }
  };

  function addComment(props: CommentBubbleProps) {
    setComments(prevComments => [...prevComments, props]);
  }

  const markup = useMemo(() => {
    return { __html: marked(content) };
  }, [content]);

  return (
    <div ref={markdownRef}>
      <div dangerouslySetInnerHTML={markup} />
      {comments.map((props, index) => (
        <CommentBubble
          key={index}
          position={props.position}
          onComment={props.onComment}
          rangyRange={props.rangyRange}
        />
      ))}
    </div>
  );
};

export default MarkdownDisplay;
