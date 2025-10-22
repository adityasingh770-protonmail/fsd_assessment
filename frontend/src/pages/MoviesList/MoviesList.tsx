import { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Typography,
  Pagination,
  Box,
  Alert,
} from '@mui/material';
import { MovieCard } from '@/components/MovieCard';
import { MovieFilters } from '@/components/MovieFilters';
import { LoadingSpinner } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorBoundary';
import { movieService } from '@/services';
import { useFavorites } from '@/hooks';
import { Movie, MovieFilters as MovieFiltersType } from '@/types';
import { DEFAULT_PAGE_SIZE } from '@/config/constants';

export const MoviesList = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState<MovieFiltersType>({
    page: 1,
    page_size: DEFAULT_PAGE_SIZE,
  });

  const { toggleFavorite, isFavorite } = useFavorites();

  // Fetch movies whenever filters change
  useEffect(() => {
    const fetchMovies = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await movieService.getMovies(filters);
        setMovies(response.data || []);
        setTotalPages(response.meta?.total_pages || 1);
      } catch (err) {
        setError((err as Error).message || 'Failed to load movies');
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, [filters]);

  const handleFiltersChange = (newFilters: MovieFiltersType) => {
    setFilters(newFilters);
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, page: number) => {
    setFilters({ ...filters, page });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading && movies.length === 0) {
    return <LoadingSpinner message="Loading movies..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        onRetry={() => setFilters({ ...filters })}
      />
    );
  }

  return (
    <Container maxWidth="xl">
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 3, fontWeight: 700 }}>
        Explore Movies
      </Typography>

      <MovieFilters filters={filters} onFiltersChange={handleFiltersChange} />

      {loading ? (
        <LoadingSpinner message="Loading movies..." />
      ) : movies.length === 0 ? (
        <Alert severity="info" sx={{ mt: 3 }}>
          No movies found. Try adjusting your filters.
        </Alert>
      ) : (
        <>
          <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
            Found {movies.length} movies
          </Typography>

          <Grid container spacing={3}>
            {movies.map((movie) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={movie.id}>
                <MovieCard
                  movie={movie}
                  isFavorite={isFavorite(movie.id)}
                  onToggleFavorite={toggleFavorite}
                />
              </Grid>
            ))}
          </Grid>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={filters.page || 1}
                onChange={handlePageChange}
                color="primary"
                size="large"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};
