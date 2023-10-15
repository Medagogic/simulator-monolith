// components/Modal.tsx
import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { FiX } from 'react-icons/fi';

interface ModalProps {
    isOpen: boolean;
    closeModal: () => void;
}

export interface Attachment {
    itemName: string;
    itemUrl: string;
    timestamp: string; // Consider using a more specific type if needed
}

const attachments: Attachment[] = [
    { itemName: "Blood test results", itemUrl: "#", timestamp: "2023-01-01 14:00:00" },
    { itemName: "Chest xray", itemUrl: "#", timestamp: "2023-01-02 15:00:00" },
];

const AttachmentList: React.FC<ModalProps> = ({ isOpen, closeModal }) => {
    return (
        <Transition appear show={isOpen} as={Fragment}>
            <Dialog
                as="div"
                className="fixed inset-0 z-10 overflow-y-auto"
                onClose={closeModal}
            >
                <div className="min-h-screen px-4 text-center">
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <Dialog.Overlay className="fixed inset-0 bg-black opacity-70" />
                    </Transition.Child>

                    {/* This element is to trick the browser into centering the modal contents. */}
                    <span className="inline-block h-screen align-middle" aria-hidden="true">
                        &#8203;
                    </span>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0 scale-95"
                        enterTo="opacity-100 scale-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100 scale-100"
                        leaveTo="opacity-0 scale-95"
                    >
                        <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
                            <button
                                type="button"
                                className="absolute top-0 right-0 p-2 rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                                onClick={closeModal}
                            >
                                <FiX className="h-6 w-6" aria-hidden="true" />
                            </button>

                            <Dialog.Title
                                as="h3"
                                className="text-lg font-medium leading-6 text-gray-900"
                            >
                                Recieved Documents
                            </Dialog.Title>
                            <div className="mt-2">

                                {/* List of attachments */}
                                <ul>
                                    {attachments.map((attachment, index) => (
                                        <li key={index} className="border-t border-gray-200 pt-2">
                                            <a
                                                href={attachment.itemUrl}
                                                className="text-blue-500 hover:underline"
                                                rel="noopener noreferrer"
                                            >
                                                {attachment.itemName}
                                            </a>
                                            <span className="text-gray-500 text-sm ml-2">{attachment.timestamp}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="mt-4">
                                <button
                                    type="button"
                                    className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-500 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                                    onClick={closeModal}
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </Transition.Child>
                </div>
            </Dialog>
        </Transition>
    );
};

export default AttachmentList;
