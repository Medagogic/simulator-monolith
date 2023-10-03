"use client"

import React, { useState, useEffect, useRef } from 'react';
import Mark from 'mark.js';
import rangy from 'rangy';
import 'rangy/lib/rangy-textrange';
import 'rangy/lib/rangy-highlighter';
import 'rangy/lib/rangy-classapplier';

export type CommentBubbleProps = {
  position: { top: number; left: number };
  onComment: (comment: string) => void;
  rangyRange: RangyRange | null;
};

const CommentBubble: React.FC<CommentBubbleProps> = ({ position, onComment, rangyRange }) => {
    const textAreaRef = useRef<HTMLTextAreaElement>(null);
    const [commentText, setCommentText] = useState<string>("");
    const highlighter = rangy.createHighlighter(document);
    const classApplier = rangy.createClassApplier("highlight");
    highlighter.addClassApplier(classApplier);

    const [highlight, setHighlight] = useState<any>(null);

  useEffect(() => {
    if (rangyRange) {
        rangy.getSelection().removeAllRanges();
    }


  }, [rangyRange]);


  const handleMouseOver = () => {
    if (highlight) {
        highlight.apply();
        return;
    } else {
        rangy.getSelection().setSingleRange(rangyRange!);
        const highlights = highlighter.highlightSelection("highlight");
        rangy.getSelection().collapseToStart();

        if (highlights.length > 0) {
            setHighlight(highlights[0]);
        }
    }
  };

  const handleMouseOut = () => {
    if (highlight) {
        highlight.unapply();
    }
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: `${position.top}px`,
        left: `${position.left + 10}px`,
        zIndex: 10,
        background: 'white',
        border: '1px solid #ccc',
        borderRadius: '4px',
        padding: '10px',
        height: 'auto'
      }}
      onMouseOver={handleMouseOver}
      onMouseOut={handleMouseOut}
    >
      <textarea
        placeholder="Enter your comment"
        onChange={e => setCommentText(e.target.value)}
        ref={textAreaRef}
      />
      <button onClick={() => onComment(commentText)}>Add Comment</button>
    </div>
  );
};

export default CommentBubble;
