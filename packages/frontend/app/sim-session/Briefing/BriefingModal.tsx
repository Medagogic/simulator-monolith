// BriefingModal.tsx
import React from 'react';
import { Dialog, Transition } from '@headlessui/react';

interface Props {
  title: string;
  content: string;
  isOpen: boolean;
  onClose: () => void;
}

const BriefingModal: React.FC<Props> = ({ title, content, isOpen, onClose }) => {
  return (
    <Transition show={isOpen} as={React.Fragment}>
      <Dialog
        as="div"
        className="fixed inset-0 z-20 overflow-y-auto"
        static
        open={isOpen}
        onClose={onClose}
      >
        <div className="flex items-center justify-center min-h-screen">
          <Dialog.Overlay className="fixed inset-0 bg-black bg-opacity-50 z-10" />

          <div className="bg-gray-700 p-6 rounded-lg w-1/2 shadow-xl z-30 text-white"> {/* Dark theme styling here */}
            <Dialog.Title className="text-lg font-medium">
              {title}
            </Dialog.Title>

            <div className="mt-2">
              <p className="text-sm">{content}</p>
            </div>

            <div className="mt-4">
              <button
                type="button"
                className="text-blue-400 hover:text-blue-500"
                onClick={onClose}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};

export default BriefingModal;
