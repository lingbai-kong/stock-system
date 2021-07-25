import request from './request.js'
module.exports={
	get_assert(data){
		var url='/deal/assert_list';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取资产信息"
		);
	},
	get_position(data){
		var url='/deal/position_list';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取持仓信息"
		);
	},
	buy(data){
		var url='/deal/buy';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"购买股票"
		);
	},
	sale(data){
		var url='/deal/sale';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"卖出股票"
		);
	},
	get_detail(data){
		var url='/deal/detail';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"获取交易明细"
		);
	}
}