//#ifndef H5
		export const baseURL="http://192.168.31.120:8000";
//#endif 
//#ifdef H5
		export const baseURL="http://127.0.0.1:5000";
//#endif
//export const baseURL="http://192.168.31.120:8000";
//export const baseURL="http://127.0.0.1:5000";
const header = {}
const request = (url,method,data,temp) => {
    return new Promise((resolve,reject) => {
        uni.request({
            method:method,
            url:baseURL + url,
            data:data,
            dataType:'json',
			header:header
        }).then((response) => {
            let [error,res] = response;          
            resolve(res);
			console.log("--",temp,"--返回包：",res);
        });
    });
}
export default request