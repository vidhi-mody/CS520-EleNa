import { render, screen } from '@testing-library/react';
import { expect } from '@jest/globals'
import userEvent from "@testing-library/user-event";
import App from '../App';

test('renders app', () => {
  render(<App />);
});

test('alert when source and destination fields are not filled in', () => {
  render(<App />);
  window.alert = jest.fn();
  const findRouteButton = screen.getByText('Find Route');
  expect(findRouteButton).toBeInTheDocument();
  userEvent.click(findRouteButton);
  expect(window.alert).toBeCalledWith('Source and destination addresses are not filled in!');
});
