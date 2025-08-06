import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { getTestimonials } from "../../redux/testimonials";
import TestimonialCard from "../../components/TestimonialCard/TestimonialCard";
import "./TestimonialsPage.css";

const TestimonialsPage = () => {
  const dispatch = useDispatch<any>();
  const testimonials = useSelector((state: RootState) =>
    Object.values(state.testimonials.all)
  );

  useEffect(() => {
    dispatch(getTestimonials());
  }, [dispatch]);

  return (
    <div className="testimonials-page">
      <h1>Customer Testimonials</h1>
      <div className="testimonial-list">
        {testimonials.map((testimonial) => (
          <TestimonialCard key={testimonial.id} testimonial={testimonial} />
        ))}
      </div>
    </div>
  );
};

export default TestimonialsPage;