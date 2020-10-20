import { createStore, applyMiddleware, compose } from 'redux';
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

let composeMiddleware = compose;

if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
  composeMiddleware = composeWithDevTools;
}

const store = composeMiddleware(applyMiddleware(...middlewares))(createStore)(reducers, load(localStorageLoadConfig));

export default store;
