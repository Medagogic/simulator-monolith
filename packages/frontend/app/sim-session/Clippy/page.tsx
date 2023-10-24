"use client"

import Clippy from "./Clippy";

const ClippyTestPage: React.FC = () => {
    return (
        <Clippy onClick={(suggestion) => console.log(suggestion)}/>
    );
};

export default ClippyTestPage;