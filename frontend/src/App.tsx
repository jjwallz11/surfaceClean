import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePublic from "./pages/Home/Home_Public";
import HomeAdmin from "./pages/Home/Home_Admin";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePublic />} />
        <Route path="/admin" element={<HomeAdmin />} />
      </Routes>
    </Router>
  );
};

export default App;