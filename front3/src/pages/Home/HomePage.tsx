// front3/src/pages/HomePage/HomePage.tsx

import OpenModalButton from '../../components/OpenModalButton/OpenModalButton';
import LoginModal from '../../components/LoginModal/LoginModal';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <h1>Welcome to Surface Clean</h1>
      <p>This page is restricted to authorized users only.</p>
      <OpenModalButton
        modalComponent={<LoginModal />}
        buttonText="Admin Login"
      />
    </div>
  );
};

export default HomePage;