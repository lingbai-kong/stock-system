import request from './request.js'
module.exports={
	get_ZX_list(data){
		var url='/user/ZX_list';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取自选股"
		);
	},
	ZX_remove(data){
		var url='/user/ZX_remove';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"删除自选股"
		);
	}
}