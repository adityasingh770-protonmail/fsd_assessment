import { Box, Container, Typography } from '@mui/material';

export const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="xl">
        <Typography variant="body2" color="text.secondary" align="center">
          Movie Explorer Platform - Full Stack Development Assignment
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center">
          Built with React, TypeScript, Material-UI & Flask
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          {new Date().getFullYear()} - Educational Project
        </Typography>
      </Container>
    </Box>
  );
};
