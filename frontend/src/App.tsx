import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Blogs from './pages/Blogs';
import BlogDetail from './pages/BlogDetail';
import './styles/index.css';

const App = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/blogs" element={<Blogs />} />
            <Route path="/blogs/:slug" element={<BlogDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;