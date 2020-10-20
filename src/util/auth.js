export const USER_KEY = 'user';

export default class Auth {
  static setUserToken(token) {
    window.localStorage.setItem(`${USER_KEY}_token`, JSON.stringify(token));
  }

  static getUserToken() {
    const userTokenItem = window.localStorage.getItem(`${USER_KEY}_token`);
    if (userTokenItem) {
      return JSON.parse(userTokenItem);
    }
    return null;
  }

  static clearUserToken() {
    window.localStorage.removeItem(USER_KEY);
  }
}
