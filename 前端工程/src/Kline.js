import request from './request.js'
module.exports={
	get_Kline_history_data(data){
		var url='/API/KLine2';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取K线数据"
		);
	},
	select_Kline(data){
		var url='/user/select';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"添加自选股"
		);
	},
	get_message(data){
		var url='/API/message';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取股票信息"
		);
	}
}