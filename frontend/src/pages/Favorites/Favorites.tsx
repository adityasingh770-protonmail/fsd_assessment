import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  Button,
  Paper,
  Alert,
} from '@mui/material';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { MovieCard } from '@/components/MovieCard';
import { LoadingSpinner } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorBoundary';
import { movieService } from '@/services';
import { useFavorites } from '@/hooks';
import { Movie } from '@/types';

export const Favorites = () => {
  const [favoriteMovies, setFavoriteMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { favorites, toggleFavorite, clearFavorites, isFavorite } = useFavorites();

  useEffect(() => {
    const fetchFavoriteMovies = async () => {
      if (favorites.length === 0) {
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        // Fetch each favorite movie
        const moviePromises = favorites.map((id) => movieService.getMovieById(id));
        const responses = await Promise.all(moviePromises);
        // API returns { success, data } structure, extract the movie data
        const movies = responses.map(response => (response as any).data || response);
        setFavoriteMovies(movies);
      } catch (err) {
        setError((err as Error).message || 'Failed to load favorite movies');
      } finally {
        setLoading(false);
      }
    };

    fetchFavoriteMovies();
  }, [favorites]);

  const handleClearAll = () => {
    if (window.confirm('Are you sure you want to clear all favorites?')) {
      clearFavorites();
      setFavoriteMovies([]);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading your favorites..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        onRetry={() => window.location.reload()}
      />
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <FavoriteIcon sx={{ fontSize: 40, color: 'error.main' }} />
          <Typography variant="h3" component="h1" sx={{ fontWeight: 700 }}>
            My Favorites
          </Typography>
        </Box>

        {favoriteMovies.length > 0 && (
          <Button
            variant="outlined"
            color="error"
            startIcon={<DeleteSweepIcon />}
            onClick={handleClearAll}
          >
            Clear All
          </Button>
        )}
      </Box>

      {favoriteMovies.length === 0 ? (
        <Paper elevation={2} sx={{ p: 6, textAlign: 'center' }}>
          <FavoriteIcon sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
          <Typography variant="h5" gutterBottom color="text.secondary">
            No favorites yet
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Start exploring movies and add them to your favorites to see them here!
          </Typography>
          <Button variant="contained" href="/" sx={{ mt: 2 }}>
            Browse Movies
          </Button>
        </Paper>
      ) : (
        <>
          <Alert severity="info" sx={{ mb: 3 }}>
            You have {favoriteMovies.length} movie{favoriteMovies.length !== 1 ? 's' : ''} in your favorites
          </Alert>

          <Grid container spacing={3}>
            {favoriteMovies.map((movie) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={movie.id}>
                <MovieCard
                  movie={movie}
                  isFavorite={isFavorite(movie.id)}
                  onToggleFavorite={toggleFavorite}
                />
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Container>
  );
};
