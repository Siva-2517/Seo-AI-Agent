import { Link, useLocation } from 'react-router-dom';
import { Sparkles } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-8 h-8 text-primary-500" />
            <span className="text-xl font-bold text-white">SEO Agent</span>
          </div>

          <nav className="flex space-x-6">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/')
                  ? 'text-primary-400 bg-primary-900/20'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/blogs"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/blogs')
                  ? 'text-primary-400 bg-primary-900/20'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800'
              }`}
            >
              Generated Blogs
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
