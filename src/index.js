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
import ForgotPassword from 'containers/forgotPassword';
import ChangePassword from 'containers/changePassword';
import App from 'containers/app';
import Pipelines from 'containers/pipelines';
import { refreshUserToken } from 'actions/user';
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

  return (
    <Switch>
      <Route exact path={ROUTE_LOGIN}>
        {hasProfile && <Redirect to={ROUTE_PIPELINES} />}
        <Login />
      </Route>
      <Route exact path={ROUTE_FORGOT_PASSWORD} render={() => (<ForgotPassword />)} />
      <Route exact path={ROUTE_CHANGE_PASSWORD} render={() => (<ChangePassword />)} />
      <Route exact path={ROUTE_PIPELINES}>
        {!hasProfile && <Redirect to={ROUTE_LOGIN} />}
        <App><Pipelines /></App>
      </Route>
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
