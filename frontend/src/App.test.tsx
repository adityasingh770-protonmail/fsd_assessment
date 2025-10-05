import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import App from './App';
import theme from './theme';

describe('App', () => {
  it('renders Movie Explorer Platform heading', () => {
    render(
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <App />
        </ThemeProvider>
      </BrowserRouter>
    );

    const heading = screen.getByText(/Movie Explorer Platform/i);
    expect(heading).toBeInTheDocument();
  });

  it('renders welcome message', () => {
    render(
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <App />
        </ThemeProvider>
      </BrowserRouter>
    );

    const message = screen.getByText(/Welcome to the Movie Explorer Platform/i);
    expect(message).toBeInTheDocument();
  });
});