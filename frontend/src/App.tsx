import { Routes, Route } from 'react-router-dom';
import { Container, Box, Typography } from '@mui/material';

function App() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            textAlign: 'center',
          }}
        >
          <Typography variant="h2" component="h1" gutterBottom color="primary">
            🎬 Movie Explorer Platform
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            Welcome to the Movie Explorer Platform
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Frontend is ready! Routes and components will be added in upcoming chunks.
          </Typography>
        </Box>
      </Container>

      <Routes>
        <Route path="/" element={<div />} />
        {/* Routes will be added in later chunks */}
      </Routes>
    </Box>
  );
}

export default App;