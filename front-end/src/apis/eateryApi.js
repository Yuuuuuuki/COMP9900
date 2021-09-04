import {BaseApi} from './baseApi';

export class EateryApi extends BaseApi {
  static async getEateryInf() {
    const role = sessionStorage.getItem('role');
    const id = sessionStorage.getItem('id');
    if (!role) {
      return null;
    }
    const res = await this.request.post('/api/get_user_info', {role, id})
    return res.data
  }

  static async modifyEateryInf(data) {
    const res = await this.request.post('/api/eatery_update', data)
    sessionStorage.setItem('role', 'eatery');
    return res.data.result === 0 ? 1 : 0;
  }

  static async getValidList() {
    const eatery_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/eatery_valid_voucher', {eatery_id})
    return res.data.map(i => {
      return {
        date: i.date,
        userName: i.userName,
        startTime: i.startTime,
        endTime: i.endTime,
        total: i.total,
        checked: i.checked,
        periodic: i.periodic,
      };
    });
  }

  static async checkCode(voucher_id) {
    const eatery_id = sessionStorage.getItem('id');
    if (!voucher_id) {
      return
    }
    const res = await this.request.post('/api/eatery_check_voucher', {voucher_id, eatery_id})
    return res.data.result;
  }

  static async addVoucher(data) {
    const res = await this.request.post('/api/release_voucher', data)
    return res.data.result === 0 ? 1 : 0;
  }

  static async getHistoryList(filter) {
    const eatery_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/eatery_history_voucher', {date: filter.date, eatery_id})
    return res.data
  }

  static async getCommentList(filter) {
    const eatery_id = sessionStorage.getItem('id');
    const res = await this.request.post('/api/eatery_comment_voucher', {date: filter.date, eatery_id})
    return res.data.map(i => {
      return {
        date: i.date,
        userName: i.userName,
        email: i.email,
        rate: i.rate,
        comment: i.comment,
      };
    });
  }

  static async cancelPeriodic(id) {
    console.log('id2' + id)
    const res = await this.request.post('/api/eatery_delete_periodic_voucher', {voucher_id: id})
    return res.data.result === 0 ? 1 : 0;
  }


}
