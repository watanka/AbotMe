import { render, screen } from '@testing-library/react';
import App from './App';

test('프로필 이름이 화면에 보인다', () => {
    render(<App />);
    expect(screen.getByText('신은성')).toBeInTheDocument();
});