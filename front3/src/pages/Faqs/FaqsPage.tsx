import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAllFaqs } from '../../redux/faqs';
import { RootState } from '../../redux/store';
import FAQCard from '../../components/FAQCard/FAQCard';
import './FAQsPage.css';

const FAQsPage = () => {
  const dispatch = useDispatch<any>();
  const faqs = useSelector((state: RootState) => state.faqs.faqs);

  useEffect(() => {
    dispatch(getAllFaqs());
  }, [dispatch]);

  const faqsArr = Object.values(faqs || {});

  return (
    <div className="faqs-page">
      <h1>Frequently Asked Questions</h1>
      {faqsArr.length ? (
        <ul className="faq-list">
          {faqsArr.map((faq) => (
            <li key={faq.id}>
              <FAQCard faq={faq} />
            </li>
          ))}
        </ul>
      ) : (
        <p>No FAQs posted yet.</p>
      )}
    </div>
  );
};

export default FAQsPage;