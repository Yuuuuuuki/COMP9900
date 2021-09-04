import {BaseApi} from './baseApi';

export class AdminApi extends BaseApi {
  static async getDinerList(filter) {
    const res = await this.request.post('/api/admin_diner', {email: filter.email})
    return res.data.map(i => {
      return {
        id: i.id,
        email: i.email,
        userName: i.userName,
        firstName: i.firstName,
        familyName: i.familyName,
        preference: i.preference,
      };
    });
  }

  static async updateDiner(data) {
    const res = await this.request.post('/api/diner_update', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async deleteDiner(id) {
    const res = await this.request.post('/api/admin_delete_diner', {diner_id: id})
    return res.data.result === 0 ? 1 : 0;
  }

  static async getEateryList(filter) {
    const res = await this.request.post('/api/admin_eatery', {email: filter.email})
    return res.data.map(i => {
      return {
        id: i.id,
        email: i.email,
        eateryName: i.eateryName,
        region: i.region,
        street: i.street,
        cuisine: i.cuisine,
        menu: i.menu,
      };
    });
  }

  static async updateEatery(data) {
    const res = await this.request.post('/api/eatery_update', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async deleteEatery(id) {
    const res = await this.request.post('/api/admin_delete_eatery', {eatery_id: id})
    return res.data.result === 0 ? 1 : 0;
  }

  static async addCuisine(data) {
    const res = await this.request.post('/api/add_cuisine', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async updateCuisine(data) {
    const res = await this.request.post('/api/update_cuisine', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async deleteCuisine(id) {
    const res = await this.request.post('/api/delete_cuisine', {cuisine_id: id})
    return res.data.result === 0 ? 1 : 0;
  }

  static async addRegion(data) {
    const res = await this.request.post('/api/add_region', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async updateRegion(data) {
    const res = await this.request.post('/api/update_region', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async deleteRegion(id) {
    const res = await this.request.post('/api/delete_region', {region_id: id})
    return res.data.result === 0 ? 1 : 0;
  }
}
