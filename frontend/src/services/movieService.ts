import { apiClient } from './api';
import { Movie, MovieDetail, MovieFilters, PaginatedResponse } from '@/types';

export const movieService = {
  /**
   * Get all movies with optional filters and pagination
   */
  async getMovies(filters?: MovieFilters): Promise<PaginatedResponse<Movie>> {
    const params = new URLSearchParams();

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }

    const queryString = params.toString();
    const url = `/movies${queryString ? `?${queryString}` : ''}`;

    return apiClient.get<PaginatedResponse<Movie>>(url);
  },

  /**
   * Get a single movie by ID
   */
  async getMovieById(id: number): Promise<MovieDetail> {
    return apiClient.get<MovieDetail>(`/movies/${id}`);
  },

  /**
   * Create a new movie
   */
  async createMovie(movie: Partial<Movie>): Promise<Movie> {
    return apiClient.post<Movie>('/movies', movie);
  },

  /**
   * Update an existing movie
   */
  async updateMovie(id: number, movie: Partial<Movie>): Promise<Movie> {
    return apiClient.put<Movie>(`/movies/${id}`, movie);
  },

  /**
   * Delete a movie
   */
  async deleteMovie(id: number): Promise<void> {
    return apiClient.delete<void>(`/movies/${id}`);
  },
};
