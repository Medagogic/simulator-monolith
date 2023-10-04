import { FC, useState } from "react";
import { FaCheck, FaComment, FaSave } from 'react-icons/fa'; // Assuming you're using react-icons for the checkmark
import { MdCancel } from 'react-icons/md';
import "./SectionWrapper.css"

export type SectionStatus = 'none' | 'accepted' | 'commented';

type SectionProps = {
    title: string;
    children: React.ReactNode;
    onStatusChange: (status: SectionStatus, comment: string) => void;
};

const SectionWrapper: FC<SectionProps> = ({ title, children, onStatusChange }) => {
    const [commentValue, setCommentValue] = useState<string>('');
    const [sectionStatus, setSectionStatus] = useState<SectionStatus>('none');

    const handleAccept = () => {
        setSectionStatus('accepted');
        onStatusChange('accepted', '');
    };

    const handleComment = () => {
        setSectionStatus('commented');
        onStatusChange('commented', commentValue);
    };

    const handleCommentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newComment = e.target.value;
        setCommentValue(newComment);
        onStatusChange('commented', newComment);
    };

    const handleCancelComment = () => {
        setSectionStatus('none');
        setCommentValue('');
    };

    const baseClasses = "bg-white p-6 rounded-lg shadow-lg mb-6 flex justify-between section-wrapper";
    const additionalClass = sectionStatus === 'accepted' ? "accepted" : "";

    return (
        <div className={`${baseClasses} ${additionalClass}`}>
            <div className="prose">
                <h2 className="text-2xl font-semibold mb-4">{title}
                    <div className="flex items-center mt-4 buttons">
                        {/* Show the "Accept" icon button only if it's not 'commented' or 'accepted' */}
                        {sectionStatus !== 'commented' && sectionStatus !== 'accepted' && (
                            <button onClick={handleAccept} className="px-4 py-2 bg-green-600 text-white rounded-md mb-2">
                                <FaCheck />  {/* Replace with your icon */}
                            </button>
                        )}

                        {/* Always show the "Comment" icon button */}
                        {sectionStatus !== 'commented' && (
                            <button onClick={handleComment} className="px-4 py-2 bg-yellow-500 text-white rounded-md mb-2 ml-2">
                                <FaComment />  {/* Replace with your icon */}
                            </button>
                        )}
                    </div>
                </h2>
                {children}
            </div>

            <div className="icon-wrapper">
                {sectionStatus === 'accepted' && (
                    <FaCheck className="text-green-600 text-3xl mb-4" />
                )}
                {sectionStatus === "commented" && (
                    <FaComment className="text-yellow-500 text-3xl mb-4" />
                )}
            </div>

            {/* <div> className="ml-4 flex flex-col justify-between h-full"> */}
            <div>
                <div className="comment-section">
                    {sectionStatus === 'commented' && (
                        <>
                            <textarea
                                placeholder="Add your comments here..."
                                className="mt-4 w-full p-2 usercomments h-full"
                                value={commentValue}
                                onChange={handleCommentChange}
                            ></textarea>

                            <div className="flex flex-row self-center">
                            <button className="px-4 py-2 bg-green-500 text-white rounded-md ml-2"
                                style={{
                                    margin: "2px",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "4px"
                                }}>
                                Save
                                <FaSave />
                            </button>

                            <button onClick={handleCancelComment} className="px-4 py-2 bg-red-500 text-white rounded-md ml-2"
                                style={{
                                    margin: "2px",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "4px"
                                }}>
                                Cancel
                                <MdCancel />
                            </button>
                            </div>
                        </>
                    )}
                </div>


            </div>
        </div>

    );
};

export default SectionWrapper;
