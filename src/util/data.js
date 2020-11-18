import moment from 'moment';

export const createdAtSort = (dateA, dateB) => {
  if (!dateA || !dateB || !dateA.created_at || !dateB.created_at) return -1;

  return moment(dateA.created_at) - moment(dateB.created_at);
};

export default null;
