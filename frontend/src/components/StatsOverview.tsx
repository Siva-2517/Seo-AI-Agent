import { FileText, CheckCircle2, TrendingUp, Target } from 'lucide-react';
import { Blog } from '../types';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon, trend }) => {
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {trend && <p className="text-sm text-primary-400 mt-1">{trend}</p>}
        </div>
        <div className="p-3 bg-primary-900/30 rounded-lg">
          {icon}
        </div>
      </div>
    </div>
  );
};

interface StatsOverviewProps {
  blogs: Blog[];
}

const StatsOverview: React.FC<StatsOverviewProps> = ({ blogs }) => {
  const totalBlogs = blogs.length;
  const avgScore = blogs.length > 0
    ? (blogs.reduce((sum, blog) => sum + blog.validation_score, 0) / blogs.length).toFixed(1)
    : '0';
  const publishedBlogs = blogs.filter(b => b.status === 'published').length;

  // Count unique keywords
  const uniqueKeywords = new Set(blogs.map(b => b.primary_keyword)).size;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard
        title="Total Blogs Generated"
        value={totalBlogs}
        icon={<FileText className="w-6 h-6 text-primary-400" />}
      />
      <StatsCard
        title="Keywords Researched"
        value={uniqueKeywords}
        icon={<Target className="w-6 h-6 text-primary-400" />}
      />
      <StatsCard
        title="Successful Publications"
        value={publishedBlogs}
        icon={<CheckCircle2 className="w-6 h-6 text-primary-400" />}
      />
      <StatsCard
        title="Avg. SEO Score"
        value={avgScore}
        icon={<TrendingUp className="w-6 h-6 text-primary-400" />}
        trend={`${avgScore}/100`}
      />
    </div>
  );
};

export default StatsOverview;
