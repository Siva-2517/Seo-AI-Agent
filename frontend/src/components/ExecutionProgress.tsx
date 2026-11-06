import { useEffect, useState } from 'react';
import { CheckCircle2, Clock, Loader2, AlertCircle, ChevronRight } from 'lucide-react';
import { ExecutionStatus, ExecutionLog } from '../types';
import { generationApi } from '../services/api';

interface ExecutionProgressProps {
  executionId: string;
  onComplete: (status: ExecutionStatus) => void;
}

const agentSteps = [
  { key: 'seo_research', label: 'SEO Research' },
  { key: 'keyword_selection', label: 'Keyword Selection' },
  { key: 'content_planning', label: 'Content Planning' },
  { key: 'duplicate_detection', label: 'Duplicate Detection' },
  { key: 'blog_writer', label: 'Blog Writing' },
  { key: 'seo_validation', label: 'SEO Validation' },
  { key: 'publisher', label: 'Publishing' },
];

const ExecutionProgress: React.FC<ExecutionProgressProps> = ({ executionId, onComplete }) => {
  const [status, setStatus] = useState<ExecutionStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let intervalId: number;

    const pollStatus = async () => {
      try {
        const data = await generationApi.getExecutionStatus(executionId);
        setStatus(data);

        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(intervalId);
          onComplete(data);
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch status');
        clearInterval(intervalId);
      }
    };

    // Initial poll
    pollStatus();

    // Poll every 2 seconds
    intervalId = window.setInterval(pollStatus, 2000);

    return () => clearInterval(intervalId);
  }, [executionId, onComplete]);

  const getStepStatus = (stepKey: string) => {
    if (!status) return 'pending';

    const currentAgent = status.current_agent || '';

    const stepIndex = agentSteps.findIndex(s => s.key === stepKey);
    const currentIndex = agentSteps.findIndex(s => s.key === currentAgent);

    if (status.status === 'completed' && stepKey === 'publisher') {
      return 'completed';
    }

    if (stepIndex < currentIndex) return 'completed';
    if (stepKey === currentAgent) return 'running';
    return 'pending';
  };

  const getStepIcon = (stepKey: string) => {
    const stepStatus = getStepStatus(stepKey);

    switch (stepStatus) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-primary-400" />;
      case 'running':
        return <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-gray-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  if (error) {
    return (
      <div className="card border-red-800">
        <div className="flex items-center space-x-3 text-red-400">
          <AlertCircle className="w-6 h-6" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-white mb-6">Agent Execution Progress</h3>

      {/* Agent Steps */}
      <div className="space-y-4 mb-6">
        {agentSteps.map((step, index) => {
          const stepStatus = getStepStatus(step.key);

          return (
            <div key={step.key}>
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  {getStepIcon(step.key)}
                </div>
                <div className="flex-1">
                  <p className={`font-medium ${
                    stepStatus === 'running' ? 'text-blue-400' :
                    stepStatus === 'completed' ? 'text-primary-400' :
                    'text-gray-400'
                  }`}>
                    {step.label}
                  </p>
                </div>
                {stepStatus === 'running' && (
                  <span className="text-xs text-blue-400 animate-pulse">Running...</span>
                )}
                {stepStatus === 'completed' && (
                  <span className="text-xs text-primary-400">Completed</span>
                )}
              </div>
              {index < agentSteps.length - 1 && (
                <div className="ml-2.5 mt-2 mb-2">
                  <ChevronRight className="w-4 h-4 text-gray-600 rotate-90" />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Execution Logs */}
      {status && status.execution_logs.length > 0 && (
        <div className="mt-6 border-t border-gray-800 pt-4">
          <h4 className="text-sm font-semibold text-gray-400 mb-3">Execution Logs</h4>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {status.execution_logs.slice(-10).reverse().map((log: ExecutionLog, index: number) => (
              <div key={index} className="flex items-start space-x-2 text-sm">
                <span className={`inline-block w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                  log.level === 'error' ? 'bg-red-500' :
                  log.level === 'warning' ? 'bg-yellow-500' :
                  'bg-primary-500'
                }`}></span>
                <div className="flex-1">
                  <span className="text-gray-500 text-xs">{log.agent}:</span>
                  <span className="text-gray-300 ml-2">{log.message}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Status */}
      {status && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Status:</span>
            <span className={`font-semibold ${
              status.status === 'completed' ? 'text-primary-400' :
              status.status === 'failed' ? 'text-red-400' :
              'text-blue-400'
            }`}>
              {status.status.toUpperCase()}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExecutionProgress;
