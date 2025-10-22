export interface Movie {
  id: number;
  title: string;
  description: string;
  release_year: number;
  duration_minutes: number;
  rating: number;
  poster_url: string;
  director?: Director;
  actors?: Actor[];
  genres?: Genre[];
}

export interface MovieDetail extends Movie {
  director: Director;
  actors: Actor[];
  genres: Genre[];
}

export interface MovieFilters {
  page?: number;
  page_size?: number;
  genre?: string;
  director?: string;
  actor?: string;
  year?: number;
  search?: string;
  min_rating?: number;
  max_rating?: number;
}

export interface Director {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
}

export interface Actor {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
}

export interface Genre {
  id: number;
  name: string;
  description?: string;
}
