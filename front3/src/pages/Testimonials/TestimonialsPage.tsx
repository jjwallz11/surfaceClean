import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { getTestimonials } from "../../redux/testimonials";
import TestimonialCard from "../../components/TestimonialCard/TestimonialCard";
import AddTestimonialModal from "../../components/AddTestimonialModal/AddTestimonialModal";
import "./TestimonialsPage.css";
import CallNowButton from "../../components/CallNow/CallNow";

const TestimonialsPage = () => {
  const dispatch = useDispatch<any>();
  const testimonials = useSelector((state: RootState) =>
    Object.values(state.testimonials.all)
  );
  const user = useSelector((state: RootState) => state.session.user); // ⬅️ added

  useEffect(() => {
    dispatch(getTestimonials());
  }, [dispatch]);

  return (
    <div className="testimonials-page">
      <h1>Customer Testimonials</h1>
      {!user && <CallNowButton />}
      <div className="add-testimonial-container">
        {user && <AddTestimonialModal />} {/* ⬅️ only shows if logged in */}
      </div>

      <div className="testimonial-list">
        {testimonials.map((testimonial) => (
          <TestimonialCard key={testimonial.id} testimonial={testimonial} />
        ))}
      </div>
    </div>
  );
};

export default TestimonialsPage;