<template>
	<view>
		<image class="backimg" :src="backimg_url"></image>
		<view style="height: 150rpx;"></view>
		<view style="text-align: center; padding-left: 30rpx; padding-right: 30rpx;">
			<view>
				<text style="font-family:'Times New Roman';font-size:xx-large; color: #FFFFFF;" @click="tap()">CHANGE PASSWORD</text>
			</view>
			<view style="margin-top: 100rpx;">
				<form>
					<input placeholder="邮箱" type="text" class="input" v-model="email" :disabled="lock" @blur="checkemail()"/>
					<input placeholder="新密码" type="password" class="input" v-model="pw" :disabled="lock" @blur="checkpw()"/>
					<input placeholder="确认密码" type="password" class="input" v-model="repw" :disabled="lock" @blur="checkrepw()"/>
					<view class="auth_box">
						<input placeholder="验证码" type="text" class="auth_code" v-model="auth" @blur="checkauth()"/>
						<button class="auth_btn" @click="sendauth()">发送验证码</button>
					</view>
				</form>
			</view>
			<view>
				<button class="button" @click="submit()">修改密码</button>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '../../src/user.js'
	export default {
		components: {
			api
		},
		data() {
			return {
				backimg_url:'/static/login_back.jpg',
				lock:false,
				email:'',
				pw:'',
				repw:'',
				auth:'',
			}
		},
		methods: {
			checkemail(){
				var value=this.email;
				var RE=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
				if (value.length==0)
				{
					uni.showToast({
						title:'邮箱不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				else if(!RE.test(value)){
					uni.showToast({
						title:'邮箱格式不正确！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				var flag=true;
				return flag;
			},
			checkpw(){
				var value=this.pw; 
				if (value=="")
				{
					uni.showToast({
						title:'密码不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				} 
				if (value.length<4||value.length>32) 
				{
					uni.showToast({
						title:'密码长度为4-32位！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				} 
				return true;
			},
			checkrepw(){
				var pw=this.pw;
				var repw=this.repw;
				if(pw=="")
				{
					uni.showToast({
						title:'密码不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				if(pw!=repw)
				{
					uni.showToast({
						title:'确认密码与密码不一致！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false;
				}
				return true;
			},
			checkauth(){
				var value=this.auth;
				if (value.length==0)
				{
					uni.showToast({
						title:'验证码不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				return true;
			},
			sendauth(){
				if(this.checkemail()&&this.checkpw()&&this.checkrepw())
				{
					api.ckemail(this.email).then(res=>{
						console.log("验证邮箱",res);
						if(res.statusCode==200){
							if(res.data=='FAIL'){
								var data={email:this.email};
								api.reauth({
									data
								}).then(res=>{
									console.log("发送验证码",res);
									if(res.statusCode==200){
										uni.showToast({
											title:'成功发送验证码！',
											duration:800,
											icon:'none',
											position:'bottom'
										});
										console.log("成功发送验证码");
									}else{
										console.log("发送验证码失败");
									}
								});
								this.lock=true;
							}
							else
							{
								uni.showToast({
									title:'该邮箱不存在！',
									duration:800,
									icon:'none',
									position:'bottom'
								});
							}
							console.log("成功验证邮箱");
						}else{
							console.log("验证邮箱失败");
						}
					});	
				}
			},
			submit(){
				if(this.checkemail()&&this.checkpw()&&this.checkrepw()&&this.checkauth())
				{
					var data={email:this.email,pw:this.pw,auth:this.auth};
					api.changepw({
						data
					}).then(res=>{
						console.log("修改密码",res);
						if(res.statusCode==200){
							if(res.data=='OK'){
								uni.showToast({
									title:'修改密码成功！',
									duration:800,
									icon:'none',
									position:'bottom'
								});
								getApp().globalData.kind='';
								getApp().globalData.uid='';
								getApp().globalData.jwt='';
								uni.navigateTo({
									url:'../login/login'
								})
							}
							else{
								uni.showToast({
									title:res.data+'！',
									duration:800,
									icon:'none',
									position:'bottom'
								});
							}
							console.log("成功修改密码");
						}else{
							console.log("修改密码失败");
						}
					});
				}
			},
		}
	}
</script>

<style lang="scss">
	.backimg{
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: -1;
	}
	.input{
		text-align: left;
		margin-left: 80rpx;
		margin-right: 80rpx;
		margin-top: 30rpx;
		background-color:#F2F2F2;
		padding: 15rpx;
		color: #353535;
	}
	.button{
		width: 400rpx;
		margin-top: 90rpx;
		background-color: #FFFFFF;
		color: #000000;
	}
	.auth_box{
		margin-left: 80rpx;
		margin-right: 80rpx;
		margin-top: 30rpx;
		padding-top: 15rpx;
		padding-bottom: 15rpx;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		.auth_code{
			padding: 15rpx;
			margin-left: 0;
			margin-right: 0;
			text-align: left;
			background-color:#F2F2F2;
			color: #353535;
			width: 50%;
		}
		.auth_btn{
			flex:end;
			font-size: small;
			width: 40%;
		}
	}
</style>
