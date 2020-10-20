import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { load, save } from 'redux-localstorage-simple';
import { logger } from 'redux-logger';
import { composeWithDevTools } from 'redux-devtools-extension';
import reducers from 'reducers';

const localStorageSaveConfig = {
  states: [
    'user',
  ],
};

const localStorageLoadConfig = {
  states: [
    'user',
  ],
};

const middlewares = [
  thunk,
  save(localStorageSaveConfig),
];

if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
}

const store = composeWithDevTools(applyMiddleware(...middlewares))(createStore)(reducers, load(localStorageLoadConfig));

export default store;
