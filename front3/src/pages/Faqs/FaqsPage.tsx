// pages/FAQsPage/FAQsPage.tsx
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { getAllFaqs, getLiveFaqs } from "../../redux/faqs";
import FAQCard from "../../components/FAQCard/FAQCard";
import AddFAQModal from "../../components/AddFAQModal/AddFAQModal";
import "./FaqsPage.css";

const FAQsPage = () => {
  const dispatch = useDispatch<any>();
  const faqs = useSelector((state: RootState) => Object.values(state.faqs.all));
  const user = useSelector((state: RootState) => state.session.user);

  useEffect(() => {
    if (user) {
      dispatch(getAllFaqs());
    } else {
      dispatch(getLiveFaqs());
    }
  }, [dispatch, user]);

  return (
    <div className="faqs-page">
      <h1>Frequently Asked Questions</h1>

      {user && (
        <div className="add-faq-container">
          <AddFAQModal />
        </div>
      )}

      <div className="faq-list">
        {faqs.length ? (
          faqs.map((faq) => <FAQCard key={faq.id} faq={faq} />)
        ) : (
          <p>No FAQs posted yet.</p>
        )}
      </div>
    </div>
  );
};

export default FAQsPage;