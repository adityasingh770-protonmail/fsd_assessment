import { apiClient } from './api';
import { Director, DirectorProfile } from '@/types';

export const directorService = {
  /**
   * Get all directors
   */
  async getDirectors(): Promise<Director[]> {
    return apiClient.get<Director[]>('/directors');
  },

  /**
   * Get a single director by ID
   */
  async getDirectorById(id: number, includeMovies: boolean = true): Promise<DirectorProfile> {
    const params = includeMovies ? '?include_movies=true' : '';
    return apiClient.get<DirectorProfile>(`/directors/${id}${params}`);
  },

  /**
   * Create a new director
   */
  async createDirector(director: Partial<Director>): Promise<Director> {
    return apiClient.post<Director>('/directors', director);
  },

  /**
   * Update an existing director
   */
  async updateDirector(id: number, director: Partial<Director>): Promise<Director> {
    return apiClient.put<Director>(`/directors/${id}`, director);
  },

  /**
   * Delete a director
   */
  async deleteDirector(id: number): Promise<void> {
    return apiClient.delete<void>(`/directors/${id}`);
  },
};
