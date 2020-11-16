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
        if (rowData[column].match(/^-?[0-9]+([,.][0-9]+)?$/)) { // number type
          rowData[column] = parseFloat(rowData[column]);
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

export const TOTAL_GRAPH_POINTS = 800;

export const getLimitedDataPointsForGraph = ({
  data,
  minIndex,
  maxIndex,
  totalGraphPoints = TOTAL_GRAPH_POINTS,
}) => {
  if (!data || !data.length) {
    return [];
  }

  let timeSubsetData = [...data];

  if (timeSubsetData.length <= totalGraphPoints) {
    return timeSubsetData;
  }

  if (minIndex !== undefined && maxIndex !== undefined) {
    timeSubsetData = timeSubsetData.slice(minIndex, maxIndex);

    if (timeSubsetData.length <= totalGraphPoints) {
      return timeSubsetData;
    }
  }

  // get first item, because in the for loop, we dont start getting the data until index === 1
  const limitedDataSet = [timeSubsetData[0]];

  timeSubsetData.forEach((point, index) => {
    const nth = Math.ceil((index * totalGraphPoints) / timeSubsetData.length);

    if (limitedDataSet.length + 1 === nth) {
      limitedDataSet.push(timeSubsetData[index]);
    }
  });

  // get last item, similar to first item above
  limitedDataSet.push(timeSubsetData[timeSubsetData.length - 1]);

  return limitedDataSet;
};
