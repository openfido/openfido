import moment from 'moment';
import { parse } from '@fast-csv/parse';

export const parseCsvData = (data, callback) => {
  const chartData = [];

  const csvDataStream = parse({ headers: true })
    .on('error', () => {
      // TODO: error state if necessary
    })
    .on('data', (row) => {
      const rowData = { ...row };

      Object.keys(rowData).forEach((column) => {
        if (rowData[column].match(/^\d+$/)) { // number type
          rowData[column] = parseInt(rowData[column], 10);
        } else if (moment(rowData[column]).isValid()) { // datetime type
          rowData[column] = moment(rowData[column]).unix();
        } // else, category string type
      });

      chartData.push(rowData);
    })
    .on('end', () => {
      callback(chartData);
    });

  csvDataStream.write(data);
  csvDataStream.end();
};

export default null;
