import { combineReducers } from 'redux';
import user from './user';
import pipelines from './pipelines';

export default combineReducers({
  user,
  pipelines,
});
