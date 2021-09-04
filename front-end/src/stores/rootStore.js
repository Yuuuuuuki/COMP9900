import Vue from 'vue';
import { DinerApi } from '@/apis/dinerApi';
import { EateryApi } from '@/apis/eateryApi';

export class RootStore {
  mode = '';
  userInf = null;
  getInfPromise = null;

  getUserInf() {
    if (this.mode === 'diner') {
      this.getInfPromise = DinerApi.getDinerInf()
        .then((res) => {
          this.userInf = res;
        });
    }
    if (this.mode === 'eatery') {
      this.getInfPromise = EateryApi.getEateryInf()
        .then((res) => {
          this.userInf = res;
        });
    }
    if (this.mode === 'admin' && sessionStorage.getItem('role') === 'admin') {
      this.userInf = { id: -1 };
    }
    return this.getInfPromise;
  }
}

export const rootStore = Vue.observable(new RootStore());
