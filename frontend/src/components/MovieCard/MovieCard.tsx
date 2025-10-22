import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  IconButton,
  Chip,
  Box,
  Rating,
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import InfoIcon from '@mui/icons-material/Info';
import { useNavigate } from 'react-router-dom';
import { Movie } from '@/types';
import { formatDuration, formatGenres, truncateText } from '@/utils';

interface MovieCardProps {
  movie: Movie;
  isFavorite: boolean;
  onToggleFavorite: (movieId: number) => void;
}

export const MovieCard = ({ movie, isFavorite, onToggleFavorite }: MovieCardProps) => {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate(`/movies/${movie.id}`);
  };

  const handleToggleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation();
    onToggleFavorite(movie.id);
  };

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 6,
        },
      }}
    >
      <CardMedia
        component="img"
        height="300"
        image={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'}
        alt={movie.title}
        sx={{
          objectFit: 'cover',
          cursor: 'pointer',
        }}
        onClick={handleViewDetails}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography
          gutterBottom
          variant="h6"
          component="div"
          sx={{
            fontWeight: 600,
            cursor: 'pointer',
            '&:hover': {
              color: 'primary.main',
            },
          }}
          onClick={handleViewDetails}
        >
          {truncateText(movie.title, 50)}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Rating value={movie.rating / 2} precision={0.1} readOnly size="small" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {movie.rating.toFixed(1)}/10
          </Typography>
        </Box>

        <Typography variant="body2" color="text.secondary" paragraph>
          {truncateText(movie.description, 100)}
        </Typography>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 1 }}>
          {movie.genres && movie.genres.length > 0 ? (
            movie.genres.slice(0, 3).map((genre) => (
              <Chip
                key={genre.id}
                label={genre.name}
                size="small"
                variant="outlined"
                color="primary"
              />
            ))
          ) : (
            <Chip label="No genres" size="small" variant="outlined" />
          )}
        </Box>

        <Typography variant="caption" color="text.secondary" display="block">
          {movie.release_year} • {formatDuration(movie.duration_minutes)}
        </Typography>

        {movie.director && (
          <Typography variant="caption" color="text.secondary" display="block">
            Director: {movie.director.name}
          </Typography>
        )}
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <IconButton
          aria-label="view details"
          color="primary"
          onClick={handleViewDetails}
        >
          <InfoIcon />
        </IconButton>
        <IconButton
          aria-label="add to favorites"
          color="error"
          onClick={handleToggleFavorite}
        >
          {isFavorite ? <FavoriteIcon /> : <FavoriteBorderIcon />}
        </IconButton>
      </CardActions>
    </Card>
  );
};
