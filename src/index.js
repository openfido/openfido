import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import { logger } from 'redux-logger';
import thunk from 'redux-thunk';
import {
  BrowserRouter,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom';
import { composeWithDevTools } from 'redux-devtools-extension';

import Auth from 'util/auth';
import Login from 'containers/login';
import ForgotPassword from 'containers/forgotPassword';
import ChangePassword from 'containers/changePassword';
import App from 'containers/app';
import Pipelines from 'containers/pipelines';
import reducers from 'reducers';
import {
  ROUTE_LOGIN,
  ROUTE_FORGOT_PASSWORD,
  ROUTE_CHANGE_PASSWORD,
  ROUTE_PIPELINES,
} from 'config/routes';
import * as serviceWorker from './serviceWorker';
import 'antd/dist/antd.compact.min.css';
import 'index.css';

// Auth.logoutUser();

const middlewares = [];
middlewares.push(thunk);
if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
}

const store = composeWithDevTools(applyMiddleware(...middlewares))(createStore)(reducers);

const requireLogin = (component) => () => {
  if (Auth.isUserLoggedIn()) {
    return (<App>{component}</App>);
  }

  return <Redirect to="/login" />;
};

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <Switch>
        <Route exact path={ROUTE_LOGIN} render={() => (<Login />)} />
        <Route exact path={ROUTE_FORGOT_PASSWORD} render={() => (<ForgotPassword />)} />
        <Route exact path={ROUTE_CHANGE_PASSWORD} render={() => (<ChangePassword />)} />
        <Route exact path={ROUTE_PIPELINES} render={requireLogin(<Pipelines />)} />
        <Redirect to={ROUTE_PIPELINES} />
      </Switch>
    </BrowserRouter>
  </Provider>,
  window.document.getElementById('root'),
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
