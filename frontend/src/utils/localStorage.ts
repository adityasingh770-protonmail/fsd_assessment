import { FAVORITES_STORAGE_KEY } from '@/config/constants';

/**
 * Get favorites from localStorage
 */
export const getFavorites = (): number[] => {
  try {
    const favorites = localStorage.getItem(FAVORITES_STORAGE_KEY);
    return favorites ? JSON.parse(favorites) : [];
  } catch (error) {
    console.error('Error reading favorites from localStorage:', error);
    return [];
  }
};

/**
 * Save favorites to localStorage
 */
export const saveFavorites = (favorites: number[]): void => {
  try {
    localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify(favorites));
  } catch (error) {
    console.error('Error saving favorites to localStorage:', error);
  }
};

/**
 * Add a movie to favorites
 */
export const addToFavorites = (movieId: number): number[] => {
  const favorites = getFavorites();
  if (!favorites.includes(movieId)) {
    const newFavorites = [...favorites, movieId];
    saveFavorites(newFavorites);
    return newFavorites;
  }
  return favorites;
};

/**
 * Remove a movie from favorites
 */
export const removeFromFavorites = (movieId: number): number[] => {
  const favorites = getFavorites();
  const newFavorites = favorites.filter((id) => id !== movieId);
  saveFavorites(newFavorites);
  return newFavorites;
};

/**
 * Check if a movie is in favorites
 */
export const isFavorite = (movieId: number): boolean => {
  const favorites = getFavorites();
  return favorites.includes(movieId);
};

/**
 * Clear all favorites
 */
export const clearFavorites = (): void => {
  try {
    localStorage.removeItem(FAVORITES_STORAGE_KEY);
  } catch (error) {
    console.error('Error clearing favorites from localStorage:', error);
  }
};
