import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Calendar, BarChart3, Tag, ExternalLink, Copy, CheckCircle } from 'lucide-react';
import { Blog } from '../types';
import { blogsApi } from '../services/api';

const BlogDetail = () => {
  const { slug } = useParams<{ slug: string }>();
  const [blog, setBlog] = useState<Blog | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (slug) {
      fetchBlog(slug);
    }
  }, [slug]);

  const fetchBlog = async (slug: string) => {
    try {
      setLoading(true);
      const data = await blogsApi.getBlogBySlug(slug);
      setBlog(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch blog');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyUrl = () => {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading blog...</p>
        </div>
      </div>
    );
  }

  if (error || !blog) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card border-red-800">
          <p className="text-red-400">{error || 'Blog not found'}</p>
          <Link to="/blogs" className="text-primary-400 hover:text-primary-300 mt-4 inline-block">
            ← Back to Blogs
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/blogs"
        className="inline-flex items-center space-x-2 text-primary-400 hover:text-primary-300 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Blogs</span>
      </Link>

      {/* Blog Header */}
      <div className="card mb-6">
        <h1 className="text-3xl font-bold text-white mb-4">{blog.title}</h1>

        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400 mb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(blog.created_at)}</span>
          </div>
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4" />
            <span>SEO Score: {blog.validation_score.toFixed(0)}/100</span>
          </div>
          <div className="flex items-center space-x-2">
            <Tag className="w-4 h-4" />
            <span>{blog.primary_keyword}</span>
          </div>
        </div>

        <p className="text-gray-300 mb-4">{blog.meta_description}</p>

        <div className="flex items-center space-x-3 pt-4 border-t border-gray-800">
          <button
            onClick={handleCopyUrl}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-colors text-sm"
          >
            {copied ? (
              <>
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy URL</span>
              </>
            )}
          </button>
          <a
            href={`/blogs/${blog.slug}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm"
          >
            <ExternalLink className="w-4 h-4" />
            <span>Open in New Tab</span>
          </a>
        </div>
      </div>

      {/* SEO Metadata */}
      <div className="card mb-6">
        <h2 className="text-xl font-bold text-white mb-4">SEO Metadata</h2>
        <div className="space-y-3">
          <div>
            <label className="text-sm text-gray-400">Meta Title</label>
            <p className="text-gray-200">{blog.meta_title}</p>
          </div>
          <div>
            <label className="text-sm text-gray-400">URL Slug</label>
            <p className="text-gray-200 font-mono text-sm">/blogs/{blog.slug}</p>
          </div>
          <div>
            <label className="text-sm text-gray-400">H1 Heading</label>
            <p className="text-gray-200">{blog.h1}</p>
          </div>
          <div>
            <label className="text-sm text-gray-400">Secondary Keywords</label>
            <div className="flex flex-wrap gap-2 mt-2">
              {blog.secondary_keywords.map((keyword, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 border border-gray-700"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Blog Content */}
      <div className="card mb-6">
        <h2 className="text-xl font-bold text-white mb-4">Blog Content</h2>
        <div
          className="prose prose-invert prose-primary max-w-none"
          dangerouslySetInnerHTML={{ __html: blog.content }}
          style={{
            color: '#e5e7eb',
            lineHeight: '1.7'
          }}
        />
      </div>

      {/* FAQ Section */}
      {blog.faq && blog.faq.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold text-white mb-4">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {blog.faq.map((item, index) => (
              <div key={index} className="border-l-2 border-primary-600 pl-4">
                <h3 className="font-semibold text-white mb-2">{item.question}</h3>
                <p className="text-gray-300">{item.answer}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BlogDetail;
