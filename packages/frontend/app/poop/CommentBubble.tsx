"use client"

import React, { useState, useEffect, useRef } from 'react';
import rangy from 'rangy';
import 'rangy/lib/rangy-textrange';
import 'rangy/lib/rangy-highlighter';
import 'rangy/lib/rangy-classapplier';

export type CommentBubbleProps = {
  position: { top: number; left: number };
  onComment: (comment: string) => void;
  rangyRange: RangyRange | null;
  onCancel: () => void;
};

const CommentBubble: React.FC<CommentBubbleProps> = ({ position, onComment, rangyRange, onCancel }) => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [commentText, setCommentText] = useState<string>("");
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const highlighter = rangy.createHighlighter(document);
  highlighter.addClassApplier(rangy.createClassApplier("highlight"));
  highlighter.addClassApplier(rangy.createClassApplier("poop"));

  const [highlight, setHighlight] = useState<any>(null);

  useEffect(() => {
    if (rangyRange) {
      rangy.getSelection().removeAllRanges();
    }
    setupHighlighter();
    textAreaRef.current!.focus();
  }, [rangyRange]);

  function setupHighlighter() {
    if (highlight) {
      return
    }

    rangy.getSelection().setSingleRange(rangyRange!);
    const highlights = highlighter.highlightSelection("poop");
    rangy.getSelection().collapseToStart();

    if (highlights.length > 0) {
      const newHighlight = highlights[0];
      setHighlight(newHighlight);
      console.log(newHighlight);
      newHighlight.getHighlightElements().forEach((element: HTMLElement) => {
        element.onmouseenter = (e: MouseEvent) => {
          setIsHovered(true);
          newHighlight.getHighlightElements().forEach((element: HTMLElement) => {
            element.classList.toggle("highlight", true);
          });
        };
        element.onmouseleave = (e: MouseEvent) => {
          setIsHovered(false);
          newHighlight.getHighlightElements().forEach((element: HTMLElement) => {
            element.classList.toggle("highlight", false);
          });
        };
      });
    }
  }

  function setHighlighted(highlighted: boolean) {
    if (highlight) {
      highlight.getHighlightElements().forEach((element: HTMLElement) => {
        element.classList.toggle("highlight", highlighted);
      });
    }
  }

  function close() {
    if (highlight) {
      highlight.unapply();
    }
    highlighter.removeAllHighlights();
    onCancel();
  }


  const handleMouseOver = () => {
    setHighlighted(true);
    setIsHovered(true);
  };

  const handleMouseOut = () => {
    setHighlighted(false);
    setIsHovered(false);
  };

  const handleBlur = () => {
    if (commentText === '') {
      close();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      // submit the comment
    } else if (e.key === 'Escape') {
      onCancel(); // cancel the comment
    }
  };

  return (
    <div
      className={`comment-bubble ${isHovered ? 'hovered' : ''}`}
      style={{
        top: `${position.top}px`,
        left: `${position.left + 10}px`
      }}
      onMouseOver={handleMouseOver}
      onMouseOut={handleMouseOut}
      onBlur={handleBlur}
    >
      <textarea
        placeholder="Enter your comment"
        onChange={e => setCommentText(e.target.value)}
        ref={textAreaRef}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
};

export default CommentBubble;
