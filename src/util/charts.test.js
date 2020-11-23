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

const TSV_FILE = `timestamp,line8to9:power_out_real,line8to9:power_out.real,line8to9:power_in.real,line34to15:power_out_real,line34to15:power_out.real,line34to15:power_in.real,node_15:pole_stress,node_15:resisting_moment,node_15:total_moment,node_15:critical_wind_speed,node_15:susceptibility,node_15:pole_status,node_15:current_uptime,node_901:pole_stress,node_901:resisting_moment,node_901:total_moment,node_901:critical_wind_speed,node_901:susceptibility,node_901:pole_status,node_901:current_uptime,node_15001:pole_stress,node_15001:resisting_moment,node_15001:total_moment,node_15001:critical_wind_speed,node_15001:susceptibility,node_15001:pole_status,node_15001:current_uptime,node_3:pole_stress,node_3:resisting_moment,node_3:total_moment,node_3:critical_wind_speed,node_3:susceptibility,node_3:pole_status,node_3:current_uptime,weather:temperature
2003-02-01T00:00:00-00:00,-48696.2,-48696.2,-48625.3,+0.000150023,+0.000150023,+0.000150088,+0.000432497,+61721.9,+26.6945,+72.1273,+0.100562,OK,+0,+0.000213196,+90767.5,+19.3513,+102.731,+0.0495712,OK,+0,+0.000187114,+61721.9,+11.549,+109.657,+0.0435068,OK,+0,+0.000417625,+61721.9,+25.7766,+73.4003,+0.097104,OK,+0,+46.942
2003-02-01T00:01:00-00:00,-56706.4,-56706.4,-56629,+0.000149945,+0.000149945,+0.000150009,+0.000493273,+61721.9,+30.4458,+72.1273,+0.107395,OK,+1,+0.000243155,+90767.5,+22.0706,+102.731,+0.0529397,OK,+1,+0.000213408,+61721.9,+13.172,+109.657,+0.0464632,OK,+1,+0.000476312,+61721.9,+29.3989,+73.4003,+0.103703,OK,+1,+46.942
2003-02-01T00:02:00-00:00,-63073.1,-63073.1,-62987,+0.000149926,+0.000149926,+0.00014999,+0.000557298,+61721.9,+34.3975,+72.1273,+0.114153,OK,+2,+0.000274716,+90767.5,+24.9353,+102.731,+0.0562706,OK,+2,+0.000241108,+61721.9,+14.8816,+109.657,+0.0493866,OK,+2,+0.000538135,+61721.9,+33.2148,+73.4003,+0.110227,OK,+2,+46.942
2003-02-01T00:03:00-00:00,-69142.1,-69142.1,-69047.8,+0.000149862,+0.000149862,+0.000149926,+0.00062444,+61721.9,+38.5416,+72.1273,+0.120834,OK,+3,+0.000307813,+90767.5,+27.9394,+102.731,+0.0595639,OK,+3,+0.000270155,+61721.9,+16.6745,+109.657,+0.052277,OK,+3,+0.000602968,+61721.9,+37.2163,+73.4003,+0.116679,OK,+3,+46.942
2003-02-01T00:04:00-00:00,-74416.7,-74416.7,-74311.3,+0.000149846,+0.000149846,+0.00014991,+0.000694566,+61721.9,+42.87,+72.1273,+0.127438,OK,+4,+0.000342381,+90767.5,+31.0771,+102.731,+0.0628195,OK,+4,+0.000300495,+61721.9,+18.5471,+109.657,+0.0551343,OK,+4,+0.000670683,+61721.9,+41.3959,+73.4003,+0.123056,OK,+4,+46.942
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
      const { chartScales } = await parseCsvData(CSV_FILE);
      expect(chartScales).toEqual({
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

  describe('anticipation ieee123_model_2.csv', () => {
    it('can be parsed', async () => {
      const { chartData } = await parseCsvData(TSV_FILE);
      expect(chartData.length).toEqual(5);
      expect(Object.keys(chartData[0])).toEqual([
        'timestamp',
        'line8to9:power_out_real',
        'line8to9:power_out.real',
        'line8to9:power_in.real',
        'line34to15:power_out_real',
        'line34to15:power_out.real',
        'line34to15:power_in.real',
        'node_15:pole_stress',
        'node_15:resisting_moment',
        'node_15:total_moment',
        'node_15:critical_wind_speed',
        'node_15:susceptibility',
        'node_15:pole_status',
        'node_15:current_uptime',
        'node_901:pole_stress',
        'node_901:resisting_moment',
        'node_901:total_moment',
        'node_901:critical_wind_speed',
        'node_901:susceptibility',
        'node_901:pole_status',
        'node_901:current_uptime',
        'node_15001:pole_stress',
        'node_15001:resisting_moment',
        'node_15001:total_moment',
        'node_15001:critical_wind_speed',
        'node_15001:susceptibility',
        'node_15001:pole_status',
        'node_15001:current_uptime',
        'node_3:pole_stress',
        'node_3:resisting_moment',
        'node_3:total_moment',
        'node_3:critical_wind_speed',
        'node_3:susceptibility',
        'node_3:pole_status',
        'node_3:current_uptime',
        'weather:temperature',
      ]);
    });

    it('can parse -numbers', async () => {
      const { chartData } = await parseCsvData(TSV_FILE);
      expect(chartData[0]['line8to9:power_out_real']).toEqual(-48696.2);
    });

    it('can parse +numbers', async () => {
      const { chartData } = await parseCsvData(TSV_FILE);
      expect(chartData[0]['line34to15:power_out_real']).toEqual(0.000150023);
    });

    it('can detect columns', async () => {
      const { chartTypes } = await parseCsvData(TSV_FILE);
      expect(chartTypes).toEqual({
        'line34to15:power_in.real': 'number',
        'line34to15:power_out.real': 'number',
        'line34to15:power_out_real': 'number',
        'line8to9:power_in.real': 'number',
        'line8to9:power_out.real': 'number',
        'line8to9:power_out_real': 'number',
        'node_15001:critical_wind_speed': 'number',
        'node_15001:current_uptime': 'number',
        'node_15001:pole_status': 'category',
        'node_15001:pole_stress': 'number',
        'node_15001:resisting_moment': 'number',
        'node_15001:susceptibility': 'number',
        'node_15001:total_moment': 'number',
        'node_15:critical_wind_speed': 'number',
        'node_15:current_uptime': 'number',
        'node_15:pole_status': 'category',
        'node_15:pole_stress': 'number',
        'node_15:resisting_moment': 'number',
        'node_15:susceptibility': 'number',
        'node_15:total_moment': 'number',
        'node_3:critical_wind_speed': 'number',
        'node_3:current_uptime': 'number',
        'node_3:pole_status': 'category',
        'node_3:pole_stress': 'number',
        'node_3:resisting_moment': 'number',
        'node_3:susceptibility': 'number',
        'node_3:total_moment': 'number',
        'node_901:critical_wind_speed': 'number',
        'node_901:current_uptime': 'number',
        'node_901:pole_status': 'category',
        'node_901:pole_stress': 'number',
        'node_901:resisting_moment': 'number',
        'node_901:susceptibility': 'number',
        'node_901:total_moment': 'number',
        timestamp: 'time',
        'weather:temperature': 'number',
      });
    });
  });
});
