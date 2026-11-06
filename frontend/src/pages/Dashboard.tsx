import { useState, useEffect } from 'react';
import { Sparkles, AlertCircle } from 'lucide-react';
import { Blog, ExecutionStatus } from '../types';
import { blogsApi, generationApi } from '../services/api';
import StatsOverview from '../components/StatsOverview';
import ExecutionProgress from '../components/ExecutionProgress';
import BlogCard from '../components/BlogCard';

const Dashboard = () => {
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [executionId, setExecutionId] = useState<string | null>(null);
  const [generatedBlogId, setGeneratedBlogId] = useState<number | null>(null);

  useEffect(() => {
    fetchBlogs();
  }, []);

  const fetchBlogs = async () => {
    try {
      setLoading(true);
      const data = await blogsApi.getAllBlogs();
      setBlogs(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch blogs');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBlog = async () => {
    try {
      setError(null);
      setIsGenerating(true);
      setGeneratedBlogId(null);

      const response = await generationApi.createBlog();
      setExecutionId(response.execution_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start blog generation');
      setIsGenerating(false);
    }
  };

  const handleExecutionComplete = async (status: ExecutionStatus) => {
    setIsGenerating(false);

    if (status.status === 'completed') {
      // Refresh blogs list
      await fetchBlogs();

      // Find the newly generated blog
      const logs = status.execution_logs;
      const publishLog = logs.find(log => log.message.includes('Blog ID:'));
      if (publishLog) {
        const match = publishLog.message.match(/Blog ID: (\d+)/);
        if (match) {
          setGeneratedBlogId(parseInt(match[1]));
        }
      }
    } else if (status.status === 'failed') {
      setError(status.error_message || 'Blog generation failed');
    }
  };

  const recentBlogs = blogs.slice(0, 3);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">SEO Agent Dashboard</h1>
        <p className="text-gray-400">Automated AI-powered SEO blog generation system</p>
      </div>

      {/* Stats Overview */}
      {!loading && <StatsOverview blogs={blogs} />}

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-900/20 border border-red-800 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-red-400" />
            <span className="text-red-400">{error}</span>
          </div>
        </div>
      )}

      {/* Main Action */}
      <div className="mb-8">
        <div className="card gradient-bg border-primary-800/50">
          <div className="text-center py-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-900/50 rounded-full mb-4">
              <Sparkles className="w-8 h-8 text-primary-400" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Generate SEO Blog</h2>
            <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
              Start the AI workflow to research keywords, plan content, and generate a complete SEO-optimized blog post automatically.
            </p>
            <button
              onClick={handleCreateBlog}
              disabled={isGenerating}
              className="btn-primary inline-flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  <span>Create Blog Page</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Execution Progress */}
      {isGenerating && executionId && (
        <div className="mb-8">
          <ExecutionProgress
            executionId={executionId}
            onComplete={handleExecutionComplete}
          />
        </div>
      )}

      {/* Success Message */}
      {generatedBlogId && (
        <div className="mb-6 bg-primary-900/20 border border-primary-800 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <Sparkles className="w-5 h-5 text-primary-400" />
            <span className="text-primary-400">Blog generated successfully! View it in the list below.</span>
          </div>
        </div>
      )}

      {/* Recent Blogs */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Recent Blogs</h2>
          {blogs.length > 3 && (
            <a href="/blogs" className="text-primary-400 hover:text-primary-300 text-sm font-medium">
              View All →
            </a>
          )}
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading blogs...</p>
          </div>
        ) : recentBlogs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentBlogs.map(blog => (
              <BlogCard key={blog.id} blog={blog} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 card">
            <p className="text-gray-400">No blogs generated yet. Click "Create Blog Page" to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
