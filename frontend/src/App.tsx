import { Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/Layout';
import {
  MoviesList,
  MovieDetail,
  ActorProfile,
  DirectorProfile,
  Favorites,
  NotFound,
} from '@/pages';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<MoviesList />} />
        <Route path="movies/:id" element={<MovieDetail />} />
        <Route path="actors/:id" element={<ActorProfile />} />
        <Route path="directors/:id" element={<DirectorProfile />} />
        <Route path="favorites" element={<Favorites />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;