import apiClient from './client';

interface GetProblemsParams {
  difficulty?: string;
  status?: string;
  skip?: number;
  limit?: number;
}

interface UpdateProblemData {
  title?: string;
  difficulty?: string;
  notes?: string;
}

export const getProblems = async (params: GetProblemsParams = {}) => {
  const response = await apiClient.get('/problems', { params });
  return response.data;
};

export const addProblem = async (problemNumber: number) => {
  const response = await apiClient.post('/problems', { problem_number: problemNumber });
  return response.data;
};

export const updateProblem = async (problemId: number, data: UpdateProblemData) => {
  const response = await apiClient.put(`/problems/${problemId}`, data);
  return response.data;
};

export const getReviewProblems = async () => {
  const response = await apiClient.get('/problems/review');
  return response.data;
};

export const completeReview = async (problemId: number) => {
  const response = await apiClient.post(`/problems/${problemId}/complete`);
  return response.data;
};

export const postponeReview = async (problemId: number, days: number = 1) => {
  const response = await apiClient.post(`/problems/${problemId}/postpone`, { days });
  return response.data;
};

export const getProblemStats = async () => {
  const response = await apiClient.get('/problems/stats');
  return response.data;
}; 