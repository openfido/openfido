import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux';
import { Provider, useSelector, useDispatch } from 'react-redux';
import { logger } from 'redux-logger';
import thunk from 'redux-thunk';
import {
  BrowserRouter,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom';
import { composeWithDevTools } from 'redux-devtools-extension';

import Login from 'containers/login';
import ResetPassword from 'containers/login/reset-password';
import ResetPasswordRequest from 'containers/login/reset-password-request';
import App from 'containers/app';
import Pipelines from 'containers/pipelines';
import { refreshUserToken } from 'actions/user';
import reducers from 'reducers';
import {
  ROUTE_LOGIN,
  ROUTE_RESET_PASSWORD,
  ROUTE_UPDATE_PASSWORD,
  ROUTE_PIPELINES,
} from 'config/routes';
import * as serviceWorker from './serviceWorker';
import 'antd/dist/antd.compact.min.css';
import 'index.css';

const middlewares = [];
middlewares.push(thunk);
if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
}

const store = composeWithDevTools(applyMiddleware(...middlewares))(createStore)(reducers);

const AppSwitch = () => {
  const profile = useSelector((state) => state.user.profile);
  const hasProfile = profile !== null;
  const dispatch = useDispatch();

  const [checkedJWTRefresh, setCheckedJWTRefresh] = useState(false);

  useEffect(() => {
    if (checkedJWTRefresh) return;
    setCheckedJWTRefresh(true);

    if (!profile) return;

    dispatch(refreshUserToken(profile.token));
  }, [dispatch, profile, checkedJWTRefresh]);

  const redirectToPipelines = hasProfile && <Redirect to={ROUTE_PIPELINES} />;
  const redirectToLogin = !hasProfile && <Redirect to={ROUTE_LOGIN} />;

  return (
    <Switch>
      <Route exact path={ROUTE_LOGIN}>
        {redirectToPipelines}
        <Login />
      </Route>
      <Route exact path={ROUTE_RESET_PASSWORD} render={() => (<ResetPassword />)} />
      <Route exact path={ROUTE_UPDATE_PASSWORD} render={() => (<ResetPasswordRequest />)} />
      <Route exact path={ROUTE_PIPELINES}>
        {redirectToLogin}
        <App><Pipelines /></App>
      </Route>
      {redirectToPipelines}
      {redirectToLogin}
    </Switch>
  );
};

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <AppSwitch />
    </BrowserRouter>
  </Provider>,
  window.document.getElementById('root'),
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
