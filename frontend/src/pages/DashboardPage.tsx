import React from 'react';
import { useQuery } from '@tanstack/react-query';
import * as problemsApi from '../api/problems';

const DashboardPage: React.FC = () => {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['problemStats'],
    queryFn: () => problemsApi.getProblemStats()
  });

  const { data: reviewProblems, isLoading: reviewsLoading } = useQuery({
    queryKey: ['reviewProblems'],
    queryFn: () => problemsApi.getReviewProblems()
  });

  if (statsLoading || reviewsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900">Total Problems</h3>
          <p className="mt-2 text-3xl font-bold text-blue-600">
            {stats?.total_problems || 0}
          </p>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900">By Difficulty</h3>
          <div className="mt-2 space-y-2">
            {stats?.by_difficulty && Object.entries(stats.by_difficulty).map(([difficulty, count]) => (
              <div key={difficulty} className="flex justify-between">
                <span className="text-gray-600">{difficulty}</span>
                <span className="font-medium">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900">By Status</h3>
          <div className="mt-2 space-y-2">
            {stats?.by_status && Object.entries(stats.by_status).map(([status, count]) => (
              <div key={status} className="flex justify-between">
                <span className="text-gray-600">{status}</span>
                <span className="font-medium">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Today's Reviews */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900">Today's Reviews</h2>
        <div className="mt-4">
          {reviewProblems && reviewProblems.length > 0 ? (
            <div className="space-y-4">
              {reviewProblems.map((problem: any) => (
                <div
                  key={problem.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div>
                    <h3 className="font-medium text-gray-900">
                      {problem.title}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Stage: {problem.stage} • Difficulty: {problem.difficulty}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => {/* TODO: Handle complete */}}
                      className="btn-primary"
                    >
                      Complete
                    </button>
                    <button
                      onClick={() => {/* TODO: Handle postpone */}}
                      className="btn-secondary"
                    >
                      Postpone
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              No reviews scheduled for today
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 