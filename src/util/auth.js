export const USER_KEY = 'user';

export default class Auth {
  static loginUser(user) {
    window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  static isUserLoggedIn() {
    return !!window.localStorage.getItem(USER_KEY);
  }

  static getUser() {
    if (Auth.isUserLoggedIn()) {
      return JSON.parse(window.localStorage.getItem(USER_KEY));
    }
    return null;
  }

  static getAuthToken() {
    if (this.isUserLoggedIn()) {
      return this.getUser().token;
    }
    return null;
  }

  static logoutUser() {
    window.localStorage.removeItem(USER_KEY);
  }
}
