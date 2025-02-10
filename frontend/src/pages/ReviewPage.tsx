import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as problemsApi from '../api/problems';

const ReviewPage: React.FC = () => {
  const queryClient = useQueryClient();
  const { data: problems, isLoading } = useQuery({
    queryKey: ['reviewProblems'],
    queryFn: () => problemsApi.getReviewProblems()
  });

  const completeMutation = useMutation({
    mutationFn: problemsApi.completeReview,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviewProblems'] });
      queryClient.invalidateQueries({ queryKey: ['problemStats'] });
    },
  });

  const postponeMutation = useMutation({
    mutationFn: ({ problemId, days }: { problemId: number; days: number }) =>
      problemsApi.postponeReview(problemId, days),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviewProblems'] });
      queryClient.invalidateQueries({ queryKey: ['problemStats'] });
    },
  });

  const handleComplete = async (problemId: number) => {
    try {
      await completeMutation.mutateAsync(problemId);
    } catch (error) {
      console.error('Failed to complete review:', error);
    }
  };

  const handlePostpone = async (problemId: number, days: number = 1) => {
    try {
      await postponeMutation.mutateAsync({ problemId, days });
    } catch (error) {
      console.error('Failed to postpone review:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Today's Reviews</h1>

      {problems && problems.length > 0 ? (
        <div className="space-y-4">
          {problems.map((problem: any) => (
            <div key={problem.id} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {problem.leetcode_number}. {problem.title}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Difficulty: {problem.difficulty} • Stage: {problem.stage}
                  </p>
                </div>

                <div className="flex space-x-2">
                  <button
                    onClick={() => handleComplete(problem.id)}
                    disabled={completeMutation.isPending}
                    className="btn-primary"
                  >
                    {completeMutation.isPending ? 'Completing...' : 'Complete'}
                  </button>

                  <div className="relative">
                    <button
                      onClick={() => handlePostpone(problem.id)}
                      disabled={postponeMutation.isPending}
                      className="btn-secondary"
                    >
                      {postponeMutation.isPending ? 'Postponing...' : 'Postpone'}
                    </button>
                  </div>
                </div>
              </div>

              {/* Problem Link and Notes */}
              <div className="mt-4 flex items-center space-x-4">
                <a
                  href={`https://leetcode.com/problems/${problem.title.toLowerCase().replace(/\s+/g, '-')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-500"
                >
                  View on LeetCode
                </a>
                {problem.notes && (
                  <div className="text-sm text-gray-500">
                    Notes: {problem.notes}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500">No reviews scheduled for today!</p>
          <p className="mt-2 text-sm text-gray-400">
            Add more problems or come back tomorrow.
          </p>
        </div>
      )}
    </div>
  );
};

export default ReviewPage;