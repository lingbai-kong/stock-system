<template>
	<view>
		<view style="height: 190rpx;"></view>
		<image class="backimg" :src="backimg_url"></image>
		<view style="text-align: center; padding-left: 30rpx; padding-right: 30rpx;">
			<view>
				<image :src="icon_url" class="logo"></image>
			</view>
			<view>
				<form>
					<input placeholder="请输入您的邮箱" type="text" class="input" v-model="name"/>
					<input placeholder="请输入您的密码" type="text" password="true" class="input" v-model="password"/>
				</form>
			</view>
			<view class="forget" @click="forget">
				<text class="forget_test">忘记密码？</text>
			</view>
			<view>
				<button class="button" @click="login()">登陆账户</button>
			</view>
			<view>
				<button class="button" @click="register()" style="margin-top: 30rpx;">新用户注册</button>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '../../src/user.js'
	export default{
		components: {
			api
		},
		methods:{
			forget:function(e){
				uni.navigateTo({
				    url:'../changepw/changepw'
				})
			},
			register:function(e){
				uni.navigateTo({
				    url:'../register/register'
				})
			},
			login:function(e){
				if(this.name.length==0){
					uni.showToast({
						title:'注册邮箱名不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false;
				}
				if(this.password==0){
					uni.showToast({
						title:'密码不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false;
				}
				var data={email:this.name,pw:this.password};
				api.login({
					data
				}).then(res=>{
					console.log("登录",res);
					if(res.statusCode==200){
						if(res.data.msg=='OK'){
							getApp().globalData.kind=res.data.kind;
							getApp().globalData.uid=res.data.uid;
							getApp().globalData.jwt=res.data.jwt;
							
							if(res.data.kind=='user'){
								uni.showToast({
									title:'登陆成功！',
									duration:400,
									complete:function(ep){
										setTimeout(function(){
											{
												uni.switchTab({
												    url:'../home/home'
												});
											}
										},500)
									}
								})
							}
							else{
								uni.showToast({
									title:'登陆成功！',
									duration:400,
									complete:function(ep){
										setTimeout(function(){
											{
												uni.navigateTo({
													url:'../manage/manage'
												});
											}
										},500)
									}
								})
							}
						}
						else{
							uni.showToast({
								title:res.data.msg+'！',
								duration:800,
								icon:'none',
								position:'bottom'
							});
						}
						console.log("登录成功");
					}else{
						console.log("登录失败");
					}
				});
			}
		},
		onLoad(){
			console.log("成功加载")
		},
		onBackPress(options) {
		    return true
		},
		data(){
			return{
				backimg_url:'/static/login_back.jpg',
				icon_url:'/static/login_head_icon.jpg',
				name:"",
				password:""
			};
		}
	}
</script>

<style>
	.backimg{
	    position: fixed;
	    width: 100%;
	    height: 100%;
	    top: 0;
	    left: 0;
	    z-index: -1;
	}
	.logo {
		height: 240rpx;
		width: 240rpx;
		margin-top: 150rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
		border-radius: 35rpx;
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
		background-color: #ffffff;
		color: #000000;
	}
	.forget_test{
		font-size:medium;
		font-style: italic;
		text-decoration: underline;
		color: #F9F88C;
	}
	.forget{
		margin-left: 380rpx;
		margin-top: 20rpx;
	}
</style>