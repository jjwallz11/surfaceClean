// front3/src/pages/Testimonials/TestimonialsPage.tsx

import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import {
  getTestimonials,
  removeTestimonial,
  editTestimonial,
} from "../../redux/testimonials";
import ConfirmationModal from "../../components/ConfirmationModal/ConfirmationModal";
import { useModal } from "../../context/Modal";
import TestimonialCard from "../../components/TestimonialCard/TestimonialCard";
import "./TestimonialsPage.css";

const TestimonialsPage = () => {
  const dispatch = useDispatch<any>();
  const { setModalContent } = useModal();
  const testimonials = useSelector((state: RootState) => state.testimonials);
  const user = useSelector((state: RootState) => state.session.user);

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editFields, setEditFields] = useState({
    content: "",
  });

  const editRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    dispatch(getTestimonials());
  }, [dispatch]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (editRef.current && !editRef.current.contains(e.target as Node)) {
        setEditingId(null);
      }
    };
    if (editingId !== null) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [editingId]);

  const testimonialList = Object.values(testimonials || {});

  const handleEdit = async (id: number) => {
    await dispatch(editTestimonial(id, {
      content: editFields.content,
    }));
    setEditingId(null);
  };

  const handleDelete = (id: number) => {
    setModalContent(
      <ConfirmationModal
        title="Confirm Delete"
        message="Are you sure you want to delete this testimonial?"
        onConfirm={() => dispatch(removeTestimonial(id))}
        onCancel={() => setModalContent(null)}
      />
    );
  };

  return (
    <div className="testimonials-page-container">
      <h1>Customer Testimonials</h1>
      <div className="testimonials-grid">
        {testimonialList.map((testimonial) => (
          <div key={testimonial.id} className="testimonial-wrapper">
            <TestimonialCard testimonial={testimonial} />
            {user && (
              <div className="admin-controls" ref={editRef}>
                {editingId === testimonial.id ? (
                  <>
                    <textarea
                      value={editFields.content}
                      onChange={(e) =>
                        setEditFields({ ...editFields, content: e.target.value })
                      }
                      placeholder="Content"
                    />
                    <button onClick={() => handleEdit(testimonial.id)}>Save</button>
                    <button onClick={() => setEditingId(null)}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => {
                      setEditFields({
                        content: testimonial.content,
                      });
                      setEditingId(testimonial.id);
                    }}>
                      Edit
                    </button>
                    <button onClick={() => handleDelete(testimonial.id)}>Delete</button>
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TestimonialsPage;