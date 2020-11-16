import moment from 'moment';
import { parseCsvData } from './charts';

const CSV_FILE = `timestamp,generation_kW,total_load_kW,flexible_load_kW,unserved_energy_%,storage_power_kW,storage_energy_kWh,category
2020-10-15T00:00:00-04:00,0.0,0.0,604.921,0.0,217.23899999999998,3000.0,category
2020-10-15T00:00:30-04:00,0.0,5.32215,615.1104,-2.1391701302586518e-05,222.3431,2998.188,category
2020-10-15T00:01:00-04:00,0.0,10.7292,615.1044,-0.00021391701303346506,222.3431,2996.333,category
2020-10-15T00:01:30-04:00,0.0,16.1362,615.1044,-0.00021391701303346506,222.3431,2994.4790000000003,category
2020-10-15T00:02:00-04:00,0.0,21.5432,615.1037,-0.00021391701303346506,222.3431,2992.625,category
2020-10-15T00:02:30-04:00,0.0,26.9502,587.07,-0.00021391701303346506,199.3098,2990.771,category
2020-10-15T00:03:00-04:00,0.0,32.1236,569.8041,-0.00021391701304106488,199.91270000000003,2989.1090000000004,category
2020-10-15T00:03:30-04:00,0.0,37.1531,556.9811,-0.00021391701304106488,195.43110000000001,2987.441,notcategory
2020-10-15T00:04:00-04:00,0.0,42.0757,526.8477,-0.00021391701302586518,187.0419,2985.811,category
2020-10-15T00:04:30-04:00,0.0,46.7472,491.74510000000004,-0.00021391701302586518,187.0419,2984.251,category
`;

describe('parseCsvData()', () => {
  describe('timeseries.csv', () => {
    it('can parse absorption timeseries.csv', async () => {
      const { chartData } = await parseCsvData(CSV_FILE);
      expect(chartData.length).toEqual(10);
      expect(Object.keys(chartData[0])).toEqual([
        'timestamp',
        'generation_kW',
        'total_load_kW',
        'flexible_load_kW',
        'unserved_energy_%',
        'storage_power_kW',
        'storage_energy_kWh',
        'category',
      ]);
    });

    it('can parse timestamps', async () => {
      const { chartData } = await parseCsvData(CSV_FILE);
      expect(moment('2020-10-15T00:00:00-04:00').unix()).toEqual(chartData[0].timestamp);
    });

    it('can detect columns', async () => {
      const { chartTypes } = await parseCsvData(CSV_FILE);
      expect(chartTypes).toEqual({
        timestamp: 'time',
        generation_kW: 'number',
        total_load_kW: 'number',
        flexible_load_kW: 'number',
        'unserved_energy_%': 'number',
        storage_power_kW: 'number',
        storage_energy_kWh: 'number',
        category: 'category',
      });
    });

    it('can detect scales', async () => {
      const { chartScale } = await parseCsvData(CSV_FILE);
      expect(chartScale).toEqual({
        timestamp: 'time',
        generation_kW: 'linear',
        total_load_kW: 'linear',
        flexible_load_kW: 'linear',
        'unserved_energy_%': 'linear',
        storage_power_kW: 'linear',
        storage_energy_kWh: 'linear',
        category: 'linear',
      });
    });

    it('can parse scientific numbers', async () => {
      const { chartData } = await parseCsvData(CSV_FILE);
      expect(chartData[1]['unserved_energy_%']).toEqual(-2.1391701302586518e-05);
    });
  });
});
