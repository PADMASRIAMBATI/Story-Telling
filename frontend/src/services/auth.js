export const getToken = () => localStorage.getItem('token');
export const getUser = () => JSON.parse(localStorage.getItem('user') || 'null');
export const setAuth = (token, user) => {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
};
export const clearAuth = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};
export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};