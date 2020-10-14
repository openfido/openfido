import { useEffect } from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import queryString from 'query-string';

import {
  ROUTE_PIPELINES,
  ROUTE_CREATE_NEW_ACCOUNT_INVITATION,
} from 'config/routes';
import { changeOrganization } from 'actions/user';
import { acceptOrganizationInvitation } from 'actions/organization';

const AcceptOrganizationInvitation = () => {
  const { search } = useLocation();
  const { invitation_token } = queryString.parse(search);

  const history = useHistory();
  const profile = useSelector((state) => state.user.profile);
  const invitationOrganization = useSelector((state) => state.organization.invitationOrganization);
  const invitationToken = useSelector((state) => state.organization.invitationToken);
  const acceptInvitationError = useSelector((state) => state.organization.acceptInvitationError);
  const dispatch = useDispatch();

  useEffect(() => {
    if (profile) {
      dispatch(acceptOrganizationInvitation(invitation_token));
    }
  }, [dispatch, profile, invitation_token]);

  useEffect(() => {
    if (profile) {
      if (!acceptInvitationError && invitationToken && invitationOrganization) {
        dispatch(changeOrganization(invitationOrganization));
      }

      history.push(ROUTE_PIPELINES);
    } else {
      history.push(ROUTE_CREATE_NEW_ACCOUNT_INVITATION, { invitation_token });
    }
  }, [dispatch, history, profile, invitationOrganization, acceptInvitationError, invitation_token, invitationToken]);

  return null;
};

export default AcceptOrganizationInvitation;
