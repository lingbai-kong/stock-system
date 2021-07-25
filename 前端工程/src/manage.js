import request from './request.js'
module.exports={
	getPeopleList(data){
		var url='/manager/people';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"get_people_list"
		);
	},
	changeManagerGrade(data){
		var url='/manager/people/changeMGd';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"change_manager_grade"
		);
	},
	changeUserStatus(data){
		var url='/manager/people/changeUst';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"change_user_status"
		);
	},
	deleteManager(data){
		var url='/manager/people/deleteM';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"delete_manager"
		);
	},
	changePw(data){
		var url='/manager/people/changePw';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"change_password"
		);
	},
	getManagerMsg(data){
		var url='/manager/message';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"get_manager_message"
		);
	},
	updateManagerMsg(data){
		var url='/manager/updateMsg';
		console.log(url);
		return request(
			url,
			'POST',//method
			data,
			"update_manager_message"
		);
	}
}