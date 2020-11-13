import moment from 'moment';
import { parse } from '@fast-csv/parse';

export const parseCsvData = (data, callback) => {
  const chartData = [];
  const chartTypes = {};
  const chartScale = {};

  const csvDataStream = parse({ headers: true })
    .on('error', () => {
      // TODO: error state if necessary
    })
    .on('data', (row) => {
      const rowData = { ...row };

      Object.keys(rowData).forEach((column) => {
        if (rowData[column].match(/^\d+$/)) { // number type
          rowData[column] = parseInt(rowData[column], 10);
          if (!(column in chartTypes)) chartTypes[column] = 'number'; // interpolate type and scale from first row
          if (!(column in chartScale)) chartScale[column] = 'linear';
        } else if (moment(rowData[column]).isValid()) { // datetime type
          rowData[column] = moment(rowData[column]).unix(); // TODO: missing case where datetime might be a number '2017'
          if (!(column in chartTypes)) chartTypes[column] = 'time';
          if (!(column in chartScale)) chartScale[column] = 'time';
        } else {
          if (!(column in chartTypes)) chartTypes[column] = 'category';
          if (!(column in chartScale)) chartScale[column] = 'linear';
        }
      });

      chartData.push(rowData);
    })
    .on('end', () => {
      callback(chartData, chartTypes, chartScale);
    });

  csvDataStream.write(data);
  csvDataStream.end();
};

export default null;
