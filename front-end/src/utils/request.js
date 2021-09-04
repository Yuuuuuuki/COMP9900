import axios from 'axios';
import qs from 'qs';

axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';

axios.interceptors.request.use(config => {
  if (config.url.indexOf('?') !== -1) {
    config.url += `&t=${new Date().getTime()}`;
  } else {
    config.url += `?t=${new Date().getTime()}`;
  }
  // config.transformRequest = [function (data, headers) {
  //   return qs.stringify(data, { allowDots: true });
  // }]
  // config.paramsSerializer = params => {
  //   return qs.stringify(params, { arrayFormat: 'repeat' });
  // }
  return config;
}, error => {
  return Promise.reject(error);
})


export default axios;
