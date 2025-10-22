import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import MovieIcon from '@mui/icons-material/Movie';
import FavoriteIcon from '@mui/icons-material/Favorite';

export const Navbar = () => {
  return (
    <AppBar position="sticky">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <MovieIcon sx={{ display: 'flex', mr: 1 }} />
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{
              mr: 2,
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
              flexGrow: { xs: 1, sm: 0 },
            }}
          >
            Movie Explorer
          </Typography>

          <Box sx={{ flexGrow: 1, display: 'flex', gap: 2, ml: 4 }}>
            <Button
              component={RouterLink}
              to="/"
              sx={{ color: 'white', display: 'block' }}
            >
              Movies
            </Button>
          </Box>

          <Button
            component={RouterLink}
            to="/favorites"
            startIcon={<FavoriteIcon />}
            sx={{ color: 'white' }}
          >
            Favorites
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
