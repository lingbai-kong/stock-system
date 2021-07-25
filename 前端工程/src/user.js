import request from './request.js'
module.exports={
	ckemail(email){
		var url='/user/ckemail/'+email;
		return request(
			url,
			'GET',
			{},
			'ckemail'
		);
	},
	auth(data){
		var url='/user/auth';
		return request(
			url,
			'POST',//method
			data,
			"auth_user"
		);
	},
	reauth(data){
		var url='/user/reauth';
		return request(
			url,
			'POST',//method
			data,
			"reauth_user"
		);
	},
	changepw(data){
		var url='/user/changepw';
		return request(
			url,
			'POST',//method
			data,
			"change_password"
		);
	},
	register(data){
		var url='/user/register';
		return request(
			url,
			'POST',
			data,
			'register'
		);
	},
	login(data){
		var url='/user/login';
		return request(
			url,
			'POST',
			data,
			'login'
		);
	},
	apply(data){
		var url='/manager/apply';
		return request(
			url,
			'POST',
			data,
			'apply'
		);
	},
	get_user_message(data){
		var url='/user/message';
		return request(
			url,
			'POST',
			data,
			'get_user_message'
		);
	}
}