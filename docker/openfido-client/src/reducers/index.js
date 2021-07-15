import { combineReducers } from 'redux';
import user from './user';
import pipelines from './pipelines';
import charts from './charts';
import organization from './organization';

export default combineReducers({
  user,
  pipelines,
  charts,
  organization,
});
