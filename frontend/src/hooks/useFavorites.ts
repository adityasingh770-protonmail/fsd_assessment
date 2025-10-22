import { useState, useEffect, useCallback } from 'react';
import {
  getFavorites,
  addToFavorites as addToFavoritesUtil,
  removeFromFavorites as removeFromFavoritesUtil,
  isFavorite as isFavoriteUtil,
  clearFavorites as clearFavoritesUtil,
} from '@/utils/localStorage';

export const useFavorites = () => {
  const [favorites, setFavorites] = useState<number[]>([]);

  // Load favorites on mount
  useEffect(() => {
    setFavorites(getFavorites());
  }, []);

  // Add movie to favorites
  const addToFavorites = useCallback((movieId: number) => {
    const newFavorites = addToFavoritesUtil(movieId);
    setFavorites(newFavorites);
  }, []);

  // Remove movie from favorites
  const removeFromFavorites = useCallback((movieId: number) => {
    const newFavorites = removeFromFavoritesUtil(movieId);
    setFavorites(newFavorites);
  }, []);

  // Toggle favorite status
  const toggleFavorite = useCallback((movieId: number) => {
    if (isFavoriteUtil(movieId)) {
      removeFromFavorites(movieId);
    } else {
      addToFavorites(movieId);
    }
  }, [addToFavorites, removeFromFavorites]);

  // Check if movie is favorite
  const isFavorite = useCallback((movieId: number): boolean => {
    return favorites.includes(movieId);
  }, [favorites]);

  // Clear all favorites
  const clearFavorites = useCallback(() => {
    clearFavoritesUtil();
    setFavorites([]);
  }, []);

  return {
    favorites,
    addToFavorites,
    removeFromFavorites,
    toggleFavorite,
    isFavorite,
    clearFavorites,
  };
};
