import {BaseApi} from './baseApi';

export class CommonApi extends BaseApi {
  // sign in
  static async login(user, password, role) {
    const res = await this.request.post('/api/login', {email: user, password, role});
    sessionStorage.setItem('role', role);
    sessionStorage.setItem('id', res.data.ID);
    return res.data.result === 0 ? 1 : 0;
  }

  // register for diner
  static async registerDiner(data) {
    const res = await this.request.post('/api/diner_register', data)
    sessionStorage.setItem('role', 'diner');
    sessionStorage.setItem('id', res.data.ID);
    return res.data.result === 0 ? 1 : 0;
  }

  // register for eatery
  static async registerEatery(data) {
    const res = await this.request.post('/api/eatery_register', data);
    sessionStorage.setItem('role', 'eatery');
    sessionStorage.setItem('id', res.data.ID);
    return res.data.result === 0 ? 1 : 0;
  }

  // log out
  static async logout() {
    sessionStorage.removeItem('id');
    sessionStorage.removeItem('role');
    return 1;
  }

  // get cuisines from db
  static async getCuisineList() {
    const res = await this.request.get('/api/get_cuisine_list');
    return res.data
  }

  // get regions
  static async getRegionList() {
    const res = await this.request.get('/api/get_region_list');
    return res.data
  }

  // get eateries show in diner homepage
  static async getEateryList(filter) {
    const res = await this.request.post('/api/detail_search_eatery', filter);
    return res.data.map(i => {
      return {
        id: i.id,
        name: i.eateryName,
        logo: i.avatar,
        content: i.intro,
        rate: i.avgReview,
      };
    });
  }


  static async sendPasswordEmail(email) {
    const res = await this.request.post('/api/reset_password', {email});
    return res.data.result === 0 ? 1 : 0;
  }

  static async getRemendList(id) {
    const res = await this.request.post('/api/recommendation', {eatery_id: id});
    return res.data.map(i => {
      return {
        id: i.id,
        name: i.eateryName,
        avatar: i.avatar,
        content: i.intro,
        rate: i.avgReview,
      };
    });
  }
}
