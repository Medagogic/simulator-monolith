"use client"

import React, { useState, useRef, useEffect, useMemo } from 'react';
import { parse as marked, options } from 'marked';
import CommentBubble, { CommentBubbleProps } from './CommentBubble';
import rangy from 'rangy';
import 'rangy/lib/rangy-textrange';
import 'rangy/lib/rangy-highlighter';
import 'rangy/lib/rangy-classapplier';
import { v4 as uuidv4 } from 'uuid';
import TurndownService from 'turndown';
import { gfm, tables, strikethrough, taskListItems } from 'turndown-plugin-gfm';


const MarkdownDisplay: React.FC<{ content: string }> = ({ content }) => {
  const markdownRef = useRef<HTMLDivElement>(null);
  const [commentBubbleProps, setCommentBubbleProps] = useState<Array<CommentBubbleProps>>([]);
  const turndownService = new TurndownService({headingStyle: "atx", bulletListMarker: "-", codeBlockStyle: "fenced"});
  turndownService.use([gfm, tables, strikethrough, taskListItems]);

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
          top: (rangeRect.top - markdownRect.top) + 10,
          left: markdownRect.right
        };

        const selectedHtml = rangyRange.toHtml();
        const selectedMarkdown = turndownService.turndown(selectedHtml);
        console.log(selectedHtml);
        console.log(selectedMarkdown);

        const props = {
          key: uuidv4(),
          position: position,
          rangyRange: rangyRange,
          selectedText: selectedMarkdown,
          onComment: (comment: string) => {
            setCommentBubbleProps(commentBubbleProps => commentBubbleProps.map(commentBubbleProps => {
              if (commentBubbleProps.key === props.key) {
                return {
                  ...commentBubbleProps,
                  commentText: comment
                }
              }
              return commentBubbleProps
            }))
          },
          onCancel: () => {
            console.log("cancel")
            setCommentBubbleProps(commentBubbleProps => commentBubbleProps.filter(comment => comment.key !== props.key));
          }
        };
        addComment(props)
      }
    }
  };

  function addComment(props: CommentBubbleProps) {
    setCommentBubbleProps(prevComments => [...prevComments, props]);
  }

  const markup = useMemo(() => {
    return { __html: marked(content) };
  }, [content]);

  function describeComment(props: CommentBubbleProps): string {
    return `${props.selectedText} -> ${props.commentText}`;
  }

  return (
    <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
      <div ref={markdownRef} className='prose markdown-outer'>
        <div dangerouslySetInnerHTML={markup} className='markdown-container' />
      </div>
      {commentBubbleProps.map((props, index) => (
          <CommentBubble
            key={props.key}
            position={{
              top: props.position.top,
              left: markdownRef.current!.getBoundingClientRect().right - 20,
            }}
            onComment={props.onComment}
            rangyRange={props.rangyRange}
            onCancel={props.onCancel}
            commentText={props.commentText}
            selectedText={props.selectedText}
          />
        ))}
      <div style={{
        border: "1px solid black",
        borderRadius: "5px",
        padding: "5px",
        marginTop: "10px",
      }}>
        <h1>Instructions</h1>
        {commentBubbleProps.map((props, index) => (
          <div key={props.key}>
            <p>{index + 1}: {describeComment(props)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MarkdownDisplay;
