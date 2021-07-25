import request from './request.js'
module.exports={
	get_HS_list(data){
		var url='/API/HS_list';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"get_HS_list"
		);
	},
	get_HY_list(data){
		var url='/API/HY_list';
		console.log(url)
		return request(
			url,
			'POST',//method
			data,
			"get_HY_list"
		); 
	},
	get_DQ_list(data){
		var url='/API/DQ_list';
		console.log(url)
		return request(
			url,
			'POST',//method
			data,
			"get_DQ_list"
		); 
	},
	get_TJ_list(data){
		var url='/API/TJ_list';
		console.log(url)
		return request(
			url,
			'POST',//method
			data,
			"get_TJ_list"
		); 
	}
}