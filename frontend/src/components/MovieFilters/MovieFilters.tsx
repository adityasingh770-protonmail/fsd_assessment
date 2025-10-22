import { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Paper,
  Grid,
  Slider,
  Typography,
  SelectChangeEvent,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import { MovieFilters as MovieFiltersType, Genre, Director, Actor } from '@/types';
import { genreService, directorService, actorService } from '@/services';

interface MovieFiltersProps {
  filters: MovieFiltersType;
  onFiltersChange: (filters: MovieFiltersType) => void;
}

export const MovieFilters = ({ filters, onFiltersChange }: MovieFiltersProps) => {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [directors, setDirectors] = useState<Director[]>([]);
  const [actors, setActors] = useState<Actor[]>([]);
  const [searchTerm, setSearchTerm] = useState(filters.search || '');
  const [ratingRange, setRatingRange] = useState<number[]>([
    filters.min_rating || 0,
    filters.max_rating || 10,
  ]);

  // Load filter options
  useEffect(() => {
    const loadFilterOptions = async () => {
      try {
        const [genresData, directorsData, actorsData] = await Promise.all([
          genreService.getGenres(),
          directorService.getDirectors(),
          actorService.getActors(),
        ]);
        setGenres(genresData);
        setDirectors(directorsData);
        setActors(actorsData);
      } catch (error) {
        console.error('Error loading filter options:', error);
      }
    };

    loadFilterOptions();
  }, []);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = () => {
    onFiltersChange({ ...filters, search: searchTerm, page: 1 });
  };

  const handleGenreChange = (e: SelectChangeEvent<string>) => {
    onFiltersChange({ ...filters, genre: e.target.value, page: 1 });
  };

  const handleDirectorChange = (e: SelectChangeEvent<string>) => {
    onFiltersChange({ ...filters, director: e.target.value, page: 1 });
  };

  const handleActorChange = (e: SelectChangeEvent<string>) => {
    onFiltersChange({ ...filters, actor: e.target.value, page: 1 });
  };

  const handleYearChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const year = e.target.value ? parseInt(e.target.value) : undefined;
    onFiltersChange({ ...filters, year, page: 1 });
  };

  const handleRatingChange = (_event: Event, newValue: number | number[]) => {
    setRatingRange(newValue as number[]);
  };

  const handleRatingCommitted = () => {
    onFiltersChange({
      ...filters,
      min_rating: ratingRange[0],
      max_rating: ratingRange[1],
      page: 1,
    });
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setRatingRange([0, 10]);
    onFiltersChange({
      page: 1,
      page_size: filters.page_size,
    });
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Filter Movies
      </Typography>

      <Grid container spacing={2}>
        {/* Search */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              label="Search movies"
              variant="outlined"
              value={searchTerm}
              onChange={handleSearchChange}
              onKeyPress={(e) => e.key === 'Enter' && handleSearchSubmit()}
              placeholder="Search by title or description..."
            />
            <Button
              variant="contained"
              onClick={handleSearchSubmit}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </Box>
        </Grid>

        {/* Genre Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>Genre</InputLabel>
            <Select
              value={filters.genre || ''}
              label="Genre"
              onChange={handleGenreChange}
            >
              <MenuItem value="">All Genres</MenuItem>
              {genres.map((genre) => (
                <MenuItem key={genre.id} value={genre.name}>
                  {genre.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Director Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>Director</InputLabel>
            <Select
              value={filters.director || ''}
              label="Director"
              onChange={handleDirectorChange}
            >
              <MenuItem value="">All Directors</MenuItem>
              {directors.map((director) => (
                <MenuItem key={director.id} value={director.name}>
                  {director.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Actor Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>Actor</InputLabel>
            <Select
              value={filters.actor || ''}
              label="Actor"
              onChange={handleActorChange}
            >
              <MenuItem value="">All Actors</MenuItem>
              {actors.map((actor) => (
                <MenuItem key={actor.id} value={actor.name}>
                  {actor.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Year Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            type="number"
            label="Release Year"
            variant="outlined"
            value={filters.year || ''}
            onChange={handleYearChange}
            placeholder="e.g., 2023"
          />
        </Grid>

        {/* Rating Filter */}
        <Grid item xs={12} md={6}>
          <Typography gutterBottom>
            Rating: {ratingRange[0]} - {ratingRange[1]}
          </Typography>
          <Slider
            value={ratingRange}
            onChange={handleRatingChange}
            onChangeCommitted={handleRatingCommitted}
            valueLabelDisplay="auto"
            min={0}
            max={10}
            step={0.5}
            marks={[
              { value: 0, label: '0' },
              { value: 5, label: '5' },
              { value: 10, label: '10' },
            ]}
          />
        </Grid>

        {/* Clear Filters Button */}
        <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center' }}>
          <Button
            variant="outlined"
            color="secondary"
            onClick={handleClearFilters}
            startIcon={<ClearIcon />}
            fullWidth
          >
            Clear All Filters
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};
