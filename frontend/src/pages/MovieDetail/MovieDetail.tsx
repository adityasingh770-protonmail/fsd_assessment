import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Chip,
  IconButton,
  Paper,
  Rating,
  Button,
  Divider,
  Card,
  CardContent,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import PersonIcon from '@mui/icons-material/Person';
import { LoadingSpinner } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorBoundary';
import { movieService } from '@/services';
import { useFavorites } from '@/hooks';
import { MovieDetail as MovieDetailType } from '@/types';
import { formatDuration, formatDate } from '@/utils';

export const MovieDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<MovieDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { isFavorite, toggleFavorite } = useFavorites();

  useEffect(() => {
    const fetchMovie = async () => {
      if (!id) return;

      setLoading(true);
      setError(null);

      try {
        const data = await movieService.getMovieById(parseInt(id));
        setMovie(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load movie details');
      } finally {
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (loading) {
    return <LoadingSpinner message="Loading movie details..." />;
  }

  if (error || !movie) {
    return (
      <ErrorMessage
        message={error || 'Movie not found'}
        onRetry={() => window.location.reload()}
      />
    );
  }

  const movieIsFavorite = isFavorite(movie.id);

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
          variant="outlined"
        >
          Back
        </Button>
      </Box>

      <Grid container spacing={4}>
        {/* Movie Poster */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3}>
            <Box
              component="img"
              src={movie.poster_url || 'https://via.placeholder.com/400x600?text=No+Poster'}
              alt={movie.title}
              sx={{
                width: '100%',
                height: 'auto',
                display: 'block',
              }}
            />
          </Paper>
        </Grid>

        {/* Movie Details */}
        <Grid item xs={12} md={8}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
              {movie.title}
            </Typography>
            <IconButton
              color="error"
              onClick={() => toggleFavorite(movie.id)}
              size="large"
            >
              {movieIsFavorite ? <FavoriteIcon fontSize="large" /> : <FavoriteBorderIcon fontSize="large" />}
            </IconButton>
          </Box>

          {/* Rating */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Rating value={movie.rating / 2} precision={0.1} readOnly size="large" />
            <Typography variant="h5" sx={{ ml: 2, fontWeight: 600 }}>
              {movie.rating.toFixed(1)}/10
            </Typography>
          </Box>

          {/* Genres */}
          <Box sx={{ mb: 3 }}>
            {movie.genres && movie.genres.length > 0 ? (
              movie.genres.map((genre) => (
                <Chip
                  key={genre.id}
                  label={genre.name}
                  color="primary"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))
            ) : (
              <Typography color="text.secondary">No genres available</Typography>
            )}
          </Box>

          {/* Meta Information */}
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary' }} />
              <Typography variant="body1">
                <strong>Release Year:</strong> {movie.release_year}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <AccessTimeIcon sx={{ mr: 1, color: 'text.secondary' }} />
              <Typography variant="body1">
                <strong>Duration:</strong> {formatDuration(movie.duration_minutes)}
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Description */}
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
            Overview
          </Typography>
          <Typography variant="body1" paragraph sx={{ mb: 3, lineHeight: 1.8 }}>
            {movie.description}
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* Director */}
          {movie.director && (
            <Card sx={{ mb: 3 }} elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Director
                </Typography>
                <Button
                  component={RouterLink}
                  to={`/directors/${movie.director.id}`}
                  startIcon={<PersonIcon />}
                  variant="text"
                  size="large"
                >
                  {movie.director.name}
                </Button>
                {movie.director.bio && (
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {movie.director.bio}
                  </Typography>
                )}
                {movie.director.birth_date && (
                  <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                    Born: {formatDate(movie.director.birth_date)}
                    {movie.director.nationality && ` • ${movie.director.nationality}`}
                  </Typography>
                )}
              </CardContent>
            </Card>
          )}

          {/* Cast */}
          {movie.actors && movie.actors.length > 0 && (
            <Card elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Cast
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {movie.actors.map((actor) => (
                    <Button
                      key={actor.id}
                      component={RouterLink}
                      to={`/actors/${actor.id}`}
                      variant="outlined"
                      size="small"
                      startIcon={<PersonIcon />}
                    >
                      {actor.name}
                    </Button>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};
