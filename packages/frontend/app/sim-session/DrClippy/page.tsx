"use client"

import DrClippySuggestions from "./DrClippy";

const ClippyTestPage: React.FC = () => {
    return (
        <DrClippySuggestions onClick={(suggestion) => console.log(suggestion)}/>
    );
};

export default ClippyTestPage;