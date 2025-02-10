import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import * as problemsApi from '../api/problems';

const ProblemsPage: React.FC = () => {
  const [difficulty, setDifficulty] = useState<string>('');
  const [status, setStatus] = useState<string>('');
  const [page, setPage] = useState(1);
  const limit = 10;

  const { data, isLoading } = useQuery({
    queryKey: ['problems', { difficulty, status, page }],
    queryFn: () => problemsApi.getProblems({
      difficulty,
      status,
      skip: (page - 1) * limit,
      limit,
    })
  });

  const [newProblemNumber, setNewProblemNumber] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const [error, setError] = useState('');

  const handleAddProblem = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsAdding(true);

    try {
      const number = parseInt(newProblemNumber);
      if (isNaN(number)) {
        throw new Error('Please enter a valid problem number');
      }
      await problemsApi.addProblem(number);
      setNewProblemNumber('');
      // TODO: Invalidate problems query
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add problem');
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Problems</h1>

        {/* Add Problem Form */}
        <form onSubmit={handleAddProblem} className="flex space-x-2">
          <input
            type="number"
            value={newProblemNumber}
            onChange={(e) => setNewProblemNumber(e.target.value)}
            placeholder="Problem number"
            className="input-field w-40"
          />
          <button
            type="submit"
            disabled={isAdding}
            className="btn-primary"
          >
            {isAdding ? 'Adding...' : 'Add Problem'}
          </button>
        </form>
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      {/* Filters */}
      <div className="flex space-x-4">
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="input-field"
        >
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>

        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="input-field"
        >
          <option value="">All Statuses</option>
          <option value="Active">Active</option>
          <option value="Completed">Completed</option>
        </select>
      </div>

      {/* Problems List */}
      {isLoading ? (
        <div className="text-center py-8">Loading...</div>
      ) : (
        <div className="space-y-4">
          {data?.problems.map((problem: any) => (
            <div
              key={problem.id}
              className="card flex items-center justify-between"
            >
              <div>
                <h3 className="font-medium text-gray-900">
                  {problem.leetcode_number}. {problem.title}
                </h3>
                <p className="text-sm text-gray-500">
                  Difficulty: {problem.difficulty} • Stage: {problem.stage}
                </p>
                <p className="text-sm text-gray-500">
                  Next Review: {new Date(problem.next_review_date).toLocaleDateString()}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <a
                  href={`https://leetcode.com/problems/${problem.title.toLowerCase().replace(/\s+/g, '-')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-500"
                >
                  View on LeetCode
                </a>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {data && (
        <div className="flex justify-between items-center">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="btn-secondary"
          >
            Previous
          </button>
          <span className="text-gray-600">
            Page {page} of {Math.ceil(data.total / limit)}
          </span>
          <button
            onClick={() => setPage(p => p + 1)}
            disabled={page * limit >= (data.total || 0)}
            className="btn-secondary"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ProblemsPage; 