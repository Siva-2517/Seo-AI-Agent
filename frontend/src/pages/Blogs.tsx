import { useState, useEffect } from 'react';
import { FileText, Search } from 'lucide-react';
import { Blog } from '../types';
import { blogsApi } from '../services/api';
import BlogCard from '../components/BlogCard';

const Blogs = () => {
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [filteredBlogs, setFilteredBlogs] = useState<Blog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchBlogs();
  }, []);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredBlogs(blogs);
    } else {
      const query = searchQuery.toLowerCase();
      const filtered = blogs.filter(blog =>
        blog.title.toLowerCase().includes(query) ||
        blog.primary_keyword.toLowerCase().includes(query) ||
        blog.meta_description.toLowerCase().includes(query)
      );
      setFilteredBlogs(filtered);
    }
  }, [searchQuery, blogs]);

  const fetchBlogs = async () => {
    try {
      setLoading(true);
      const data = await blogsApi.getAllBlogs();
      setBlogs(data);
      setFilteredBlogs(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch blogs');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Generated Blogs</h1>
        <p className="text-gray-400">Browse all AI-generated SEO blog posts</p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search blogs by title, keyword, or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-gray-900 border border-gray-800 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-primary-600"
          />
        </div>
      </div>

      {/* Stats */}
      <div className="mb-6 flex items-center space-x-4 text-sm text-gray-400">
        <div className="flex items-center space-x-2">
          <FileText className="w-4 h-4" />
          <span>{blogs.length} total blogs</span>
        </div>
        {searchQuery && (
          <span>• {filteredBlogs.length} matching results</span>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 bg-red-900/20 border border-red-800 rounded-lg p-4">
          <span className="text-red-400">{error}</span>
        </div>
      )}

      {/* Blogs Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading blogs...</p>
        </div>
      ) : filteredBlogs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBlogs.map(blog => (
            <BlogCard key={blog.id} blog={blog} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 card">
          <FileText className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">
            {searchQuery ? 'No blogs match your search.' : 'No blogs generated yet.'}
          </p>
        </div>
      )}
    </div>
  );
};

export default Blogs;
