import axios from "axios";
import jwtDecode from "jwt-decode";
import { BASE_URL } from "config/Constants";

class CustomAxios {

    static _instance = new CustomAxios();
  
    static instance = () => {
  
      return CustomAxios._instance;
  
    };
  
  
  
    constructor() {
  
        this.publicAxios = axios.create({ baseURL: BASE_URL });
  
        this.privateAxios = axios.create({
  
            baseURL: BASE_URL,
  
            withCredentials: true
  
        });
  
    }
  
  }
  
  
  
  export const customAxios = CustomAxios.instance();