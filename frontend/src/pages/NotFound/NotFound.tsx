import { Container, Typography, Button, Box, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
        }}
      >
        <Paper elevation={3} sx={{ p: 6, textAlign: 'center' }}>
          <ErrorOutlineIcon
            sx={{
              fontSize: 120,
              color: 'warning.main',
              mb: 2,
            }}
          />
          <Typography variant="h1" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
            404
          </Typography>
          <Typography variant="h5" gutterBottom color="text.secondary">
            Page Not Found
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph sx={{ mt: 2 }}>
            The page you're looking for doesn't exist or has been moved.
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<HomeIcon />}
            onClick={() => navigate('/')}
            sx={{ mt: 3 }}
          >
            Go to Home
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};
