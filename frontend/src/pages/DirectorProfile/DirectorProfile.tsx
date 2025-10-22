import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Grid,
  Avatar,
  Divider,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PersonIcon from '@mui/icons-material/Person';
import { LoadingSpinner } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorBoundary';
import { MovieCard } from '@/components/MovieCard';
import { directorService } from '@/services';
import { useFavorites } from '@/hooks';
import { DirectorProfile as DirectorProfileType } from '@/types';
import { formatDate } from '@/utils';

export const DirectorProfile = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [director, setDirector] = useState<DirectorProfileType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { isFavorite, toggleFavorite } = useFavorites();

  useEffect(() => {
    const fetchDirector = async () => {
      if (!id) return;

      setLoading(true);
      setError(null);

      try {
        const response = await directorService.getDirectorById(parseInt(id));
        // API returns { success, data } structure, extract the director data
        const directorData = (response as any).data || response;
        setDirector(directorData);
      } catch (err) {
        setError((err as Error).message || 'Failed to load director profile');
      } finally {
        setLoading(false);
      }
    };

    fetchDirector();
  }, [id]);

  if (loading) {
    return <LoadingSpinner message="Loading director profile..." />;
  }

  if (error || !director) {
    return (
      <ErrorMessage
        message={error || 'Director not found'}
        onRetry={() => window.location.reload()}
      />
    );
  }

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

      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'start', gap: 3 }}>
          <Avatar
            sx={{
              width: 120,
              height: 120,
              bgcolor: 'secondary.main',
              fontSize: '3rem',
            }}
          >
            <PersonIcon fontSize="large" />
          </Avatar>

          <Box sx={{ flex: 1 }}>
            <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
              {director.name}
            </Typography>

            <Box sx={{ mb: 2 }}>
              {director.birth_date && (
                <Typography variant="body1" color="text.secondary">
                  <strong>Born:</strong> {formatDate(director.birth_date)}
                </Typography>
              )}
              {director.nationality && (
                <Typography variant="body1" color="text.secondary">
                  <strong>Nationality:</strong> {director.nationality}
                </Typography>
              )}
            </Box>

            {director.bio && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Biography
                </Typography>
                <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                  {director.bio}
                </Typography>
              </>
            )}
          </Box>
        </Box>
      </Paper>

      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 3 }}>
        Filmography
      </Typography>

      {director.movies && director.movies.length > 0 ? (
        <Grid container spacing={3}>
          {director.movies.map((movie) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={movie.id}>
              <MovieCard
                movie={movie}
                isFavorite={isFavorite(movie.id)}
                onToggleFavorite={toggleFavorite}
              />
            </Grid>
          ))}
        </Grid>
      ) : (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="text.secondary">
            No movies found for this director.
          </Typography>
        </Paper>
      )}
    </Container>
  );
};
