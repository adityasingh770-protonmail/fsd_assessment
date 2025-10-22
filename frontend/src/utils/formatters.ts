/**
 * Format duration in minutes to hours and minutes
 * @example formatDuration(125) => "2h 5m"
 */
export const formatDuration = (minutes: number): string => {
  if (!minutes || minutes < 0) return 'N/A';

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  if (hours === 0) return `${mins}m`;
  if (mins === 0) return `${hours}h`;

  return `${hours}h ${mins}m`;
};

/**
 * Format rating to one decimal place
 * @example formatRating(7.856) => "7.9"
 */
export const formatRating = (rating: number): string => {
  if (!rating || rating < 0) return 'N/A';
  return rating.toFixed(1);
};

/**
 * Format date string to readable format
 * @example formatDate("1990-05-15") => "May 15, 1990"
 */
export const formatDate = (dateString: string): string => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch (error) {
    return dateString;
  }
};

/**
 * Format year from date string
 * @example formatYear("1990-05-15") => "1990"
 */
export const formatYear = (dateString: string): string => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.getFullYear().toString();
  } catch (error) {
    return dateString;
  }
};

/**
 * Truncate text to specified length with ellipsis
 * @example truncateText("Long text here", 10) => "Long text..."
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Format genre names to comma-separated string
 * @example formatGenres([{id: 1, name: "Action"}, {id: 2, name: "Drama"}]) => "Action, Drama"
 */
export const formatGenres = (genres: Array<{ name: string }>): string => {
  if (!genres || genres.length === 0) return 'N/A';
  return genres.map((g) => g.name).join(', ');
};

/**
 * Format actor names to comma-separated string
 * @example formatActors([{id: 1, name: "John Doe"}, {id: 2, name: "Jane Smith"}]) => "John Doe, Jane Smith"
 */
export const formatActors = (actors: Array<{ name: string }>): string => {
  if (!actors || actors.length === 0) return 'N/A';
  return actors.map((a) => a.name).join(', ');
};
