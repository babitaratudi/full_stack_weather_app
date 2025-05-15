import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders the app', () => {
  render(<App />);
  expect(screen.getByText(/Welcome to the Weather App/i)).toBeInTheDocument();
});
