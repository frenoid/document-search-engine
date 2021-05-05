import { authHeader } from '../../src/helpers/auth-header'

test('authHeader should return header given user with token', () => {
  const mockUser = {
    token: "abcdef"
  };
  localStorage.setItem('user', JSON.stringify(mockUser));
  
  const header = authHeader();
  const expectedHeader = {"Authorization": "Bearer abcdef"};

  expect(header).toStrictEqual(expectedHeader);
});

test('authHeader should return empty object given user without token', () => {
  const mockUser = {
    name: "sponge bob"
  };

  localStorage.setItem('user', JSON.stringify(mockUser));
  const header = authHeader();

  const expectedHeader = {};

  expect(header).toStrictEqual(expectedHeader);
});