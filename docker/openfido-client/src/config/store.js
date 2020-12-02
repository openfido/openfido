import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import { load, save } from 'redux-localstorage-simple';
import { logger } from 'redux-logger';
import { composeWithDevTools } from 'redux-devtools-extension';
import reducers from 'reducers';
import { DEFAULT_STATE as userDefaultState } from 'reducers/user';

const localStorageSaveConfig = {
  states: [
    'user.profile',
    'user.currentOrg',
  ],
};

const localStorageLoadConfig = {
  states: [
    'user.profile',
    'user.currentOrg',
  ],
  preloadedState: {
    user: userDefaultState,
  },
  disableWarnings: true,
};

const middlewares = [
  thunk,
  save(localStorageSaveConfig),
];

let composeMiddleware = compose;

if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
  composeMiddleware = composeWithDevTools;
}

const store = composeMiddleware(applyMiddleware(...middlewares))(createStore)(reducers, load(localStorageLoadConfig));

export default store;
