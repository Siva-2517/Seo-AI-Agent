import { Blog } from '../types';
import { Calendar, Eye, BarChart3, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';

interface BlogCardProps {
  blog: Blog;
}

const BlogCard: React.FC<BlogCardProps> = ({ blog }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-orange-400';
  };

  return (
    <div className="card hover:border-primary-800 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2">
            {blog.title}
          </h3>
          <p className="text-sm text-gray-400 mb-3 line-clamp-2">
            {blog.meta_description}
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-4 text-sm text-gray-400 mb-4">
        <div className="flex items-center space-x-1">
          <Calendar className="w-4 h-4" />
          <span>{formatDate(blog.created_at)}</span>
        </div>
        <div className="flex items-center space-x-1">
          <BarChart3 className="w-4 h-4" />
          <span className={getScoreColor(blog.validation_score)}>
            {blog.validation_score.toFixed(0)}/100
          </span>
        </div>
      </div>

      <div className="mb-4">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-900/30 text-primary-400 border border-primary-800/50">
          {blog.primary_keyword}
        </span>
      </div>

      <div className="flex items-center space-x-3">
        <Link
          to={`/blogs/${blog.slug}`}
          className="flex-1 text-center bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm"
        >
          <div className="flex items-center justify-center space-x-2">
            <Eye className="w-4 h-4" />
            <span>View Blog</span>
          </div>
        </Link>
        <a
          href={`/blogs/${blog.slug}`}
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
};

export default BlogCard;
