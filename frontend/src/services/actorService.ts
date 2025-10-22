import { apiClient } from './api';
import { Actor, ActorProfile, ActorFilters } from '@/types';

export const actorService = {
  /**
   * Get all actors
   */
  async getActors(filters?: ActorFilters): Promise<Actor[]> {
    const params = new URLSearchParams();

    if (filters?.include_movies) {
      params.append('include_movies', 'true');
    }

    const queryString = params.toString();
    const url = `/actors${queryString ? `?${queryString}` : ''}`;

    return apiClient.get<Actor[]>(url);
  },

  /**
   * Get a single actor by ID
   */
  async getActorById(id: number): Promise<ActorProfile> {
    return apiClient.get<ActorProfile>(`/actors/${id}`);
  },

  /**
   * Create a new actor
   */
  async createActor(actor: Partial<Actor>): Promise<Actor> {
    return apiClient.post<Actor>('/actors', actor);
  },

  /**
   * Update an existing actor
   */
  async updateActor(id: number, actor: Partial<Actor>): Promise<Actor> {
    return apiClient.put<Actor>(`/actors/${id}`, actor);
  },

  /**
   * Delete an actor
   */
  async deleteActor(id: number): Promise<void> {
    return apiClient.delete<void>(`/actors/${id}`);
  },
};
