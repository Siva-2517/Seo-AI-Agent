import axios from 'axios';
import { Blog, ExecutionStatus, GenerationResponse, ResearchResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generationApi = {
  createBlog: async (): Promise<GenerationResponse> => {
    const response = await api.post('/generation/create', {});
    return response.data;
  },

  getExecutionStatus: async (executionId: string): Promise<ExecutionStatus> => {
    const response = await api.get(`/generation/${executionId}`);
    return response.data;
  },
};

export const blogsApi = {
  getAllBlogs: async (): Promise<Blog[]> => {
    const response = await api.get('/blogs/');
    return response.data;
  },

  getBlogBySlug: async (slug: string): Promise<Blog> => {
    const response = await api.get(`/blogs/${slug}`);
    return response.data;
  },

  getBlogById: async (id: number): Promise<Blog> => {
    const response = await api.get(`/blogs/id/${id}`);
    return response.data;
  },
};

export const researchApi = {
  getResearchData: async (executionId: string): Promise<ResearchResponse> => {
    const response = await api.get(`/research/${executionId}`);
    return response.data;
  },
};

export const healthApi = {
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
