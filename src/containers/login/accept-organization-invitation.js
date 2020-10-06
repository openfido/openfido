import React, { useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import { ROUTE_PIPELINES, ROUTE_CREATE_NEW_ACCOUNT_INVITATION } from 'config/routes';
import { changeOrganization } from 'actions/user';
import { acceptOrganizationInvitation } from 'actions/organization';


const AcceptOrganizationInvitation = () => {
  const { organization_uuid, invitation_token } = useParams();
  const history = useHistory();
  const profile = useSelector((state) => state.user.profile);
  const invitationToken = useSelector((state) => state.organization.invitationToken);
  const acceptInvitationError = useSelector((state) => state.organization.acceptInvitationError);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(acceptOrganizationInvitation(organization_uuid, invitation_token));
  }, []);

  useEffect(() => {
    if (invitationToken && !acceptInvitationError) {
      if (!profile) {
        history.push(ROUTE_CREATE_NEW_ACCOUNT_INVITATION);
      } else {
        dispatch(changeOrganization(organization_uuid));
        history.push(ROUTE_PIPELINES);
      }
    }
  });

  return null;
};

export default AcceptOrganizationInvitation;
