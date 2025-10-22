import { Movie } from './movie';

export interface Actor {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
}

export interface ActorProfile extends Actor {
  movies: Movie[];
}

export interface ActorFilters {
  include_movies?: boolean;
}
