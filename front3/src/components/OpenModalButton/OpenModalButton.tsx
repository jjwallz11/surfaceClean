// components/OpenModalButton/OpenModalButton.tsx

import { ReactElement } from 'react';
import { useModal } from '../../context/Modal';

interface OpenModalButtonProps {
  modalComponent: ReactElement;
  buttonText: string;
  onButtonClick?: () => void;
  onModalClose?: () => void;
}

function OpenModalButton({
  modalComponent,
  buttonText,
  onButtonClick,
  onModalClose
}: OpenModalButtonProps) {
  const { setModalContent, setOnModalClose } = useModal();

  const onClick = () => {
    if (onModalClose) setOnModalClose(onModalClose);
    setModalContent(modalComponent);
    if (typeof onButtonClick === 'function') onButtonClick();
  };

  return <button onClick={onClick}>{buttonText}</button>;
}

export default OpenModalButton;