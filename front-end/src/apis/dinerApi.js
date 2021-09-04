import {BaseApi} from './baseApi';

export class DinerApi extends BaseApi {
  static async getDinerInf() {
    const role = sessionStorage.getItem('role');
    const id = sessionStorage.getItem('id');
    if (!role) {
      return null;
    }
    const res = await this.request.post('/api/get_user_info', {role, id})
    return res.data;
  }

  static async modifyDinerInf(data) {
    const res = await this.request.post('/api/diner_update', data)
    sessionStorage.setItem('role', 'diner');
    return res.data.result === 0 ? 1 : 0;
  }

  static async getEateryInf(id) {
    const res = await this.request.post('/api/get_user_info', {role: "eatery", id})
    return {
      avatar: res.data.avatar,
      email: res.data.email,
      eateryName: res.data.eateryName,
      region: res.data.region,
      street: res.data.street,
      cuisine: res.data.cuisine,
      menu: res.data.menu,
    };
  }

  static async getValidList(eatery_id, date) {
    const res = await this.request.post('/api/eatery_valid_voucher', {eatery_id, date})
    return res.data.map(i => {
      return {
        total: i.total,
        booked: i.booked,
        startTime: i.startTime,
        endTime: i.endTime,
      };
    });
  }

  static async getCommendList(eatery_id) {
    const res = await this.request.post('/api/eatery_comment_voucher', {eatery_id})
    return res.data.map(i => {
      return {
        id: i.id,
        date: i.date,
        avatar: i.avatar,
        userName: i.userName,
        email: i.email,
        comment: i.comment,
        rate: i.rate,
      };
    });
  }

  static async bookEatery(data) {
    const diner_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/diner_book_voucher', {
      diner_id: diner_id,
      eatery_id: data.id,
      date: data.date,
      startTime: data.startTime,
      endTime: data.endTime
    })
    return res.data.result;
  }

  static async getValid(filter) {
    const diner_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/diner_valid_voucher', {date: filter.date, diner_id})
    return res.data.map(i => {
      return {
        eateryName: i.eateryName,
        date: i.date,
        startTime: i.startTime,
        endTime: i.endTime,
        validCode: i.voucher_id,
      };
    });
  }

  static async getUsed(filter) {
    const diner_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/diner_checked_voucher', {date: filter.date, diner_id})
    return res.data.map(i => {
      return {
        eateryName: i.eateryName,
        date: i.date,
        startTime: i.startTime,
        endTime: i.endTime,
        id: i.voucher_id,
        rate: i.rate,
        comment: i.comment,
      };
    });
  }

  static async getOverdue(filter) {
    const diner_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/diner_overdued_voucher', {date: filter.date, diner_id})
    return res.data.map(i => {
      return {
        eateryName: i.eateryName,
        date: i.date,
        startTime: i.startTime,
        endTime: i.endTime,
        validCode: i.voucher_id,
      };
    });
  }

  static async comment(data) {
    const res = await this.request.post('/api/diner_review_voucher', data)
    return res.data.result === 0 ? 1 : 0;
  }
}
