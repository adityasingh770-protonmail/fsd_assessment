import { apiClient } from './api';
import { Genre } from '@/types';

export const genreService = {
  /**
   * Get all genres
   */
  async getGenres(): Promise<Genre[]> {
    return apiClient.get<Genre[]>('/genres');
  },

  /**
   * Get a single genre by ID
   */
  async getGenreById(id: number): Promise<Genre> {
    return apiClient.get<Genre>(`/genres/${id}`);
  },

  /**
   * Create a new genre
   */
  async createGenre(genre: Partial<Genre>): Promise<Genre> {
    return apiClient.post<Genre>('/genres', genre);
  },

  /**
   * Update an existing genre
   */
  async updateGenre(id: number, genre: Partial<Genre>): Promise<Genre> {
    return apiClient.put<Genre>(`/genres/${id}`, genre);
  },

  /**
   * Delete a genre
   */
  async deleteGenre(id: number): Promise<void> {
    return apiClient.delete<void>(`/genres/${id}`);
  },
};
