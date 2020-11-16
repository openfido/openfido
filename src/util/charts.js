import moment from 'moment';
import { parse } from '@fast-csv/parse';

const DATE_FORMATS = [
  'YYYY-MM-DDTHH:mm:ssZ',
];

export const toUnixTime = (str) => moment(str, DATE_FORMATS).unix();
export const validDateString = (str) => moment(str, DATE_FORMATS).isValid();

export const parseCsvData = (data) => {
  const chartData = [];
  const chartTypes = {};
  const chartScale = {};

  return new Promise((resolve, reject) => {
    const csvDataStream = parse({ headers: true })
      .on('error', reject)
      .on('data', (row) => {
        const rowData = { ...row };

        Object.keys(rowData).forEach((column) => {
          // interpolate type and scale from first row
          if (rowData[column].match(/^-?\d+([,.]\d+)?(e[+-]\d+)?$/)) {
            rowData[column] = parseFloat(rowData[column]);
            if (!(column in chartTypes)) chartTypes[column] = 'number';
            if (!(column in chartScale)) chartScale[column] = 'linear';
          } else if (validDateString(rowData[column])) { // datetime type
            rowData[column] = toUnixTime(rowData[column]);
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
        resolve({ chartData, chartTypes, chartScale });
      });

    csvDataStream.write(data);
    csvDataStream.end();
  });
};

export default null;
