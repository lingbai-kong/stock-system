<template>
	<view>
		<image class="backimg" :src="backimg_url"></image>
		<view style="height: 150rpx;"></view>
		<view v-if="click_cnt<10" style="text-align: center; padding-left: 30rpx; padding-right: 30rpx;">
			<view>
				<text style="font-family:'Times New Roman';font-size:xx-large; color: #FFFFFF;" @click="tap()">WELCOME</text>
			</view>
			<view style="margin-top: 100rpx;">
				<form>
					<input placeholder="邮箱" type="text" class="input" v-model="email" :disabled="lock" @blur="checkemail()"/>
					<input placeholder="密码" type="password" class="input" v-model="pw" :disabled="lock" @blur="checkpw()"/>
					<input placeholder="确认密码" type="password" class="input" v-model="repw" :disabled="lock" @blur="checkrepw()"/>
					<input placeholder="姓名" type="text" class="input" v-model="name" :disabled="lock" @blur="checkname()"/>
					<input placeholder="身份证号" type="text" class="input" v-model="pid" :disabled="lock" @blur="checkpid()"/>
					<view class="auth_box">
						<input placeholder="验证码" type="text" class="auth_code" v-model="auth" @blur="checkauth()"/>
						<button class="auth_btn" @click="sendauth()">发送验证码</button>
					</view>
				</form>
			</view>
			<view>
				<button class="button" @click="submit()">注册</button>
			</view>
		</view>
		<view v-else style="text-align: center; padding-left: 30rpx; padding-right: 30rpx;">
			<view>
				<text style="font-family:'Times New Roman';font-size:xx-large; color: #FFFFFF;">MANAGER</text>
			</view>
			<view style="margin-top: 100rpx;">
				<form>
					<input placeholder="密码" type="password" class="input" v-model="pw" @blur="checkpw()"/>
					<input placeholder="确认密码" type="password" class="input" v-model="repw" @blur="checkrepw()"/>
					<input placeholder="姓名" type="text" class="input" v-model="name" @blur="checkname()"/>
					<input placeholder="手机号" type="text" class="input" v-model="telno" @blur="checktelno()"/>
				</form>
			</view>
			<view>
				<button class="button" @click="apply()">申请</button>
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
				click_cnt:0,
				lock:false,
				email:'',
				pw:'',
				repw:'',
				name:'',
				pid:'',
				auth:'',
				telno:''
			}
		},
		methods: {
			tap(){
				this.click_cnt=this.click_cnt+1;
			},
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
			checkname(){
				var value=this.name;
				if (value.length==0)
				{
					uni.showToast({
						title:'姓名不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				return true;
			},
			checkpid(){
				var idcode=this.pid;
				if (idcode.length==0)
				{
					uni.showToast({
						title:'身份证号码不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				if (idcode.length!=18)
				{
					uni.showToast({
						title:'身份证号码长度不正确！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				// 加权因子
				var weight_factor = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2];
				// 校验码
				var check_code = ['1', '0', 'X' , '9', '8', '7', '6', '5', '4', '3', '2'];
				var code = idcode + "";
				var last = idcode[17];//最后一位
				var seventeen = code.substring(0,17);
				// ISO 7064:1983.MOD 11-2
				// 判断最后一位校验码是否正确
				var arr = seventeen.split("");
				var len = arr.length;
				var num = 0;
				for(var i = 0; i < len; i++){
					num = num + arr[i] * weight_factor[i];
				}
				// 获取余数
				var resisue = num%11;
				var last_no = check_code[resisue];
				// 格式的正则
				// 正则思路
				/*
				第一位不可能是0
				第二位到第六位可以是0-9
				第七位到第十位是年份，所以七八位为19或者20
				十一位和十二位是月份，这两位是01-12之间的数值
				十三位和十四位是日期，是从01-31之间的数值
				十五，十六，十七都是数字0-9
				十八位可能是数字0-9，也可能是X
				*/
				var idcard_patter = /^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|[1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$/;
				// 判断格式是否正确
				var format = idcard_patter.test(idcode);
				// 返回验证结果，校验码和格式同时正确才算是合法的身份证号码
				var answer = last === last_no && format ? true : false;
				if(!answer)
				{
					uni.showToast({
						title:'身份证号码格式不正确！',
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
				if(this.checkemail()&&this.checkpw()&&this.checkrepw()&&this.checkname()&&this.checkpid())
				{
					api.ckemail(this.email).then(res=>{
						console.log("验证邮箱",res);
						if(res.statusCode==200){
							if(res.data=='FAIL'){
								uni.showToast({
									title:'该邮箱已经注册！',
									duration:800,
									icon:'none',
									position:'bottom'
								});
							}
							else
							{
								var data={email:this.email,pw:this.pw,name:this.name,pid:this.pid};
								api.auth({
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
										this.lock=true;
									}else{
										console.log("发送验证码失败");
									}
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
				if(this.checkemail()&&this.checkpw()&&this.checkrepw()&&this.checkname()&&this.checkpid()&&this.checkauth())
				{
					api.ckemail(this.email).then(res=>{
						console.log("验证邮箱",res);
						if(res.statusCode==200){
							if(res.data=='FAIL'){
								uni.showToast({
									title:'该邮箱已经注册！',
									duration:800,
									icon:'none',
									position:'bottom'
								});
							}
							else
							{
								var data={email:this.email,pw:this.pw,name:this.name,pid:this.pid,auth:this.auth};
								api.register({
									data
								}).then(res=>{
									console.log("注册",res);
									if(res.statusCode==200){
										if(res.data=='OK'){
											uni.showToast({
												title:'注册成功！',
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
										console.log("成功注册");
									}else{
										console.log("注册失败");
									}
								});
							}
							console.log("成功验证邮箱");
						}else{
							console.log("验证邮箱失败");
						}
					});
				}
			},
			checktelno(){
				var value=this.telno;
				if (value.length==0)
				{
					uni.showToast({
						title:'手机号不能为空！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				if(value.length!=11)
				{
					uni.showToast({
						title:'手机号格式不正确！',
						duration:800,
						icon:'none',
						position:'bottom'
					});
					return false; 
				}
				return true;
			},
			apply(){
				if(this.checkpw()&&this.checkrepw()&&this.checkname()&&this.checktelno()){
					var data={pw:this.pw,name:this.name,telno:this.telno};
					api.apply({
						data
					}).then(res=>{
						console.log("申请",res);
						if(res.statusCode==200){
							uni.showToast({
								title:'申请成功，请等待通过！',
								duration:800,
								icon:'none',
								position:'bottom'
							});
							uni.showModal({
								title: '请牢记账户ID',
								content:res.data ,
								showCancel:false,
								success: function(res) {
									if (res.confirm) {
										console.log('用户点击确定');
										uni.navigateBack({});
									}
								}
							});
							console.log("成功申请");
						}else{
							console.log("注册失败");
						}
					});
				}
			}
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
