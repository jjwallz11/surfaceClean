// components/TestimonialCard/TestimonialCard.tsx

import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import * as testimonialActions from "../../redux/testimonials";
import ConfirmationModal from "../ConfirmationModal/ConfirmationModal";
import "./TestimonialCard.css";

interface TestimonialCardProps {
  testimonial: testimonialActions.Testimonial;
}

const TestimonialCard = ({ testimonial }: TestimonialCardProps) => {
  const dispatch = useDispatch();
  const user = useSelector((state: RootState) => state.session.user);
  const updatedTestimonial = useSelector(
    (state: RootState) => state.testimonials.testimonials[testimonial.id]
  );

  const [editing, setEditing] = useState(false);
  const [authorName, setAuthorName] = useState(testimonial.author_name);
  const [stars, setStars] = useState(testimonial.stars);
  const [notables, setNotables] = useState(testimonial.notables || "");
  const [content, setContent] = useState(testimonial.content);
  const [showConfirm, setShowConfirm] = useState(false);

  const isAdmin = !!user;

  useEffect(() => {
    if (updatedTestimonial) {
      setAuthorName(updatedTestimonial.author_name);
      setStars(updatedTestimonial.stars);
      setNotables(updatedTestimonial.notables || "");
      setContent(updatedTestimonial.content);
    }
  }, [updatedTestimonial]);

  const handleEdit = async () => {
    if (
      editing &&
      (
        authorName !== testimonial.author_name ||
        stars !== testimonial.stars ||
        notables !== (testimonial.notables || "") ||
        content !== testimonial.content
      )
    ) {
      await (dispatch as any)(
        testimonialActions.editTestimonial(testimonial.id, {
          author_name: authorName,
          stars,
          notables,
          content,
        })
      );
    }
    setEditing(!editing);
  };

  const handleDelete = () => {
    setShowConfirm(true);
  };

  const confirmDelete = () => {
    (dispatch as any)(testimonialActions.deleteTestimonial(testimonial.id));
    setShowConfirm(false);
  };

  return (
    <div className="testimonial-card">
      {editing ? (
        <>
          <input
            className="testimonial-input"
            value={authorName}
            onChange={(e) => setAuthorName(e.target.value)}
            placeholder="Author name"
          />
          <input
            className="testimonial-input"
            type="number"
            min="1"
            max="5"
            value={stars}
            onChange={(e) => setStars(Number(e.target.value))}
            placeholder="Stars"
          />
          <input
            className="testimonial-input"
            value={notables}
            onChange={(e) => setNotables(e.target.value)}
            placeholder="Notables (optional)"
          />
          <textarea
            className="testimonial-textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Content"
          />
        </>
      ) : (
        <>
          <h3 className="testimonial-author">{authorName} — {stars}★</h3>
          {notables && <p className="testimonial-notables"><strong>{notables}</strong></p>}
          <p className="testimonial-content">{content}</p>
        </>
      )}

      {isAdmin && (
        <div className="testimonial-actions">
          <button onClick={handleEdit} className="btn-edit">
            {editing ? "Save" : "Edit"}
          </button>
          <button onClick={handleDelete} className="btn-delete">
            Delete
          </button>
        </div>
      )}

      {showConfirm && (
        <ConfirmationModal
          title="Confirm Deletion"
          message="Are you sure you want to delete this testimonial?"
          onConfirm={confirmDelete}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
};

export default TestimonialCard;