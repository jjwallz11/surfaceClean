// front3/src/components/AddTestimonialModal/AddTestimonialModal.tsx

import { useState } from "react";
import { useDispatch } from "react-redux";
import * as testimonialActions from "../../redux/testimonials";
import BaseModal from "../BaseModal/BaseModal";
import "../BaseModal/BaseModal.css"

const AddTestimonialModal = () => {
  const dispatch = useDispatch<any>();
  const [showModal, setShowModal] = useState(false);

  const [authorName, setAuthorName] = useState("");
  const [stars, setStars] = useState(0);
  const [notables, setNotables] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = () => {
    dispatch(
      testimonialActions.createTestimonial({
        author_name: authorName,
        stars,
        notables,
        content,
      })
    );
    setShowModal(false);
  };

  const renderStars = () => {
    const starArray: JSX.Element[] = [];
    for (let i = 1; i <= 5; i++) {
      starArray.push(
        <img
          key={i}
          src={
            i <= stars
              ? "https://cdn.discordapp.com/emojis/1175836866696724580.webp?size=240"
              : "https://cdn-icons-png.flaticon.com/512/1828/1828970.png"
          }
          alt={i <= stars ? "Filled star" : "Empty star"}
          className="star-icon"
          onClick={() => setStars(i)}
        />
      );
    }
    return <div className="star-select-row">{starArray}</div>;
  };

  return (
    <>
      <button onClick={() => setShowModal(true)} className="btn-add">
        ADD TESTIMONIAL
      </button>

      {showModal && (
        <BaseModal
          title="Add Testimonial"
          onClose={() => setShowModal(false)}
          onSave={handleSubmit}
        >
          <input
            className="modal-input"
            placeholder="Author Name"
            value={authorName}
            onChange={(e) => setAuthorName(e.target.value)}
          />
          {renderStars()}
          <input
            className="modal-input"
            placeholder="Notables (optional)"
            value={notables}
            onChange={(e) => setNotables(e.target.value)}
          />
          <textarea
            className="modal-textarea"
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </BaseModal>
      )}
    </>
  );
};

export default AddTestimonialModal;