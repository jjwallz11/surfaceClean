// front3/src/components/AddFAQModal/AddFAQModal.tsx

import { useState } from "react";
import { useDispatch } from "react-redux";
import * as faqActions from "../../redux/faqs";
import BaseModal from "../BaseModal/BaseModal";
import "../BaseModal/BaseModal.css";

const AddFAQModal = () => {
  const dispatch = useDispatch<any>();
  const [showModal, setShowModal] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [scheduledPostDate, setScheduledPostDate] = useState("");

  const handleSubmit = () => {
    dispatch(
      faqActions.createFaq({
        question,
        answer,
        scheduled_post_date: scheduledPostDate || undefined,
      })
    );
    setShowModal(false);
  };

  return (
    <>
      {/* Use the shared .btn-add class so it matches Testimonials/Machines */}
      <button
        type="button"
        onClick={() => setShowModal(true)}
        className="btn-add"
      >
        ADD FAQ
      </button>

      {showModal && (
        <BaseModal
          title="Add FAQ"
          onClose={() => setShowModal(false)}
          onSave={handleSubmit}
        >
          <input
            className="modal-input"
            placeholder="Question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <textarea
            className="modal-textarea"
            placeholder="Answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />
          <input
            className="modal-input"
            type="date"
            value={scheduledPostDate}
            onChange={(e) => setScheduledPostDate(e.target.value)}
          />
        </BaseModal>
      )}
    </>
  );
};

export default AddFAQModal;