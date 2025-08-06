// pages/FAQsPage/FAQsPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { getAllFaqs } from "../../redux/faqs";
import FAQCard from "../../components/FAQCard/FAQCard";
import "./FAQsPage.css";

const FAQsPage = () => {
  const dispatch = useDispatch<any>();
  const faqs = useSelector((state: RootState) =>
    Object.values(state.faqs.all)
  );

  useEffect(() => {
    dispatch(getAllFaqs());
  }, [dispatch]);

  return (
    <div className="faqs-page">
      <h1>Frequently Asked Questions</h1>
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