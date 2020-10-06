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
import ResetPasswordRequest from 'containers/login/reset-password-request';
import ResetPassword from 'containers/login/reset-password';
import Users from 'containers/users';
import AcceptOrganizationInvitation from 'containers/login/accept-organization-invitation';
import CreateNewAccountInvitation from 'containers/login/create-new-account-invitation';
import App from 'containers/app';
import Pipelines from 'containers/pipelines';
import Settings from 'containers/settings';
import { refreshUserToken } from 'actions/user';
import reducers from 'reducers';
import {
  ROUTE_LOGIN,
  ROUTE_RESET_PASSWORD,
  ROUTE_UPDATE_PASSWORD,
  ROUTE_PIPELINES,
  ROUTE_USERS,
  ROUTE_ACCEPT_ORGANIZATION_INVITATION, ROUTE_CREATE_NEW_ACCOUNT_INVITATION,
  ROUTE_SETTINGS,
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

    if (profile === null) return;

    const { uuid: user_uuid } = profile;

    dispatch(refreshUserToken(user_uuid));
  }, [dispatch, profile, checkedJWTRefresh]);

  const hasProfileRedirectToPipelines = hasProfile && <Redirect to={ROUTE_PIPELINES} />;
  const noProfileRedirectToLogin = !hasProfile && <Redirect to={ROUTE_LOGIN} />;

  return (
    <Switch>
      <Route exact path={ROUTE_LOGIN}>
        {hasProfileRedirectToPipelines}
        <Login />
      </Route>
      <Route exact path={ROUTE_RESET_PASSWORD}>
        <ResetPasswordRequest />
      </Route>
      <Route exact path={ROUTE_UPDATE_PASSWORD}>
        <ResetPassword />
      </Route>
      <Route exact path={ROUTE_ACCEPT_ORGANIZATION_INVITATION}>
        <AcceptOrganizationInvitation />
      </Route>
      <Route exact path={ROUTE_CREATE_NEW_ACCOUNT_INVITATION}>
        <CreateNewAccountInvitation />
      </Route>
      <Route exact path={ROUTE_PIPELINES}>
        {noProfileRedirectToLogin}
        <App><Pipelines /></App>
      </Route>
      <Route exact path={ROUTE_USERS}>
        {noProfileRedirectToLogin}
        {hasProfile && 'is_system_admin' in profile && (
          !profile.is_system_admin || !(profile.organizations && profile.organizations.length) ? (
            <Redirect to={ROUTE_PIPELINES} />
          ) : (
            <App><Users /></App>
          )
        )}
      </Route>
      <Route exact path={ROUTE_SETTINGS}>
        {noProfileRedirectToLogin}
        <App><Settings /></App>
      </Route>
      {hasProfileRedirectToPipelines}
      {noProfileRedirectToLogin}
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
