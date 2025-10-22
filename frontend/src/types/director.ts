import { Movie } from './movie';

export interface Director {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
}

export interface DirectorProfile extends Director {
  movies: Movie[];
}
