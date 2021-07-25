<template>
	<view>
		<view class="topbox">
			<view class="searchinput">
				<image class="searchlogo" src="../../static/search.png"/>
				<input placeholder="Search" v-model="search_value"/>
			</view>
			<view>
				<v-tabs
					:v-model="tab_index"
					:tabs="tab_list"
					:pills="false"
					:scroll="false"
					:fixed="true"
					bgColor="#f0f0f0"
					line-height="0rpx"
					lineColor="#f9273f"
					activeColor="#f9273f"
					@change="changeTab"
				></v-tabs>
			</view>
		</view>
		<view style="height: 190rpx;"></view>
		<view class="Plist" v-if="tab_index==0">
			<view class="Pitem" v-if="search_value==''||item[1].indexOf(search_value) != -1" v-for="(item,index) in people_list" :key="index" @click="choosePeople(item)">
				<view class="Pitem_col">
					<view>{{item[1]}}</view>
					<view style="font-size:12px;color: #535353;">{{item[0]}}</view>
				</view>
				<view class="Pitem_col">
					<view>{{item[2]}}</view>
				</view>
				<view class="Pitem_col">
					<view style="font-size: xx-small;">{{item[3]}}</view>
				</view>
			</view>
		</view>
		<view style="position:fixed; bottom: 20rpx; right:20rpx; border: solid #000000 5rpx; border-radius: 300rpx;" @click="setme()">
			<image style="height: 100rpx;width: 100rpx;" src="../../static/setme.png">
		</view>
		<uni-popup ref="popup" type="bottom">
			<view v-if="kind=='super'" class="pop">
				<view class="poptext" @click="changeMGd()">{{change_grade_text}}</view>
				<view class="poptext" @click="changePw()">修改密码</view>
				<view class="poptext" @click="deleteM()">删除管理员</view>
			</view>
			<view v-else class="pop">
				<view class="poptext" @click="changeUst()">{{change_status_text}}</view>
				<view class="poptext" @click="changePw()">修改密码</view>
			</view>
		</uni-popup>
		<uni-popup ref="popcenter" type="center">
			<view class="newPw">
				<text style="color: black; font-size: 30rpx; margin-left: 30rpx;">修改密码</text>
				<input class="in_pw" type="password" placeholder="新密码" v-model="new_pw" @blur="checkpw()"/>
				<input class="in_pw" type="password" placeholder="确认密码" v-model="new_repw" @blur="checkrepw()"/>
				<view class="in_button">
					<view style="width: 400rpx;"></view>
					<button class="button" size="mini" @click="submitNewPw()">确认</button>
				</view>
			</view>
		</uni-popup>
		<uni-popup ref="popself" type="center">
			<view class="self">
				<text style="color: black; font-size: 30rpx; margin-left: 30rpx;">个人信息</text>
				<view style="margin-left: 15rpx;">账户:</view>
				<input class="in" type="text" disabled="true" :value="self_msg[0]"/>
				<view style="margin-left: 15rpx;">级别:</view>
				<input class="in" type="text" disabled="true" :value="self_msg[1]"/>
				<view style="margin-left: 15rpx;">姓名:</view>
				<input class="in" type="text" v-model="self_msg[2]" @blur="checkname()"/>
				<view style="margin-left: 15rpx;">手机号:</view>
				<input class="in" type="text" v-model="self_msg[3]" @blur="checktelno()"/>
				<view class="in_button">
					<view style="width: 400rpx;"></view>
					<button class="button" size="mini" @click="changePw()">修改密码</button>
					<button class="button" size="mini" @click="updateMsg()">更新</button>
				</view>
			</view>
		</uni-popup>
	</view>
</template>

<script>
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import uniPopupMessage from '@/components/uni-popup/uni-popup-message.vue'
	import uniPopupDialog from '@/components/uni-popup/uni-popup-dialog.vue'
	import api from '../../src/manage.js'
	export default {
		components: {
			uniPopup,
			uniPopupMessage,
			uniPopupDialog,
			api
		},
		data() {
			return {
				search_value:'',
				tab_index:0,
				tab_list:[],
				kind:'',
				uid:'',
				jwt:'',
				
				people_list:[],
				choose_people_uid:'',
				stock_list:[],
				
				change_grade_text:'',
				change_status_text:'',
				new_pw:'',
				new_repw:'',
				
				self_msg:[]
			}
		},
		// onLoad(){
		// 	this.kind=getApp().globalData.kind;
		// 	this.uid=getApp().globalData.uid;
		// 	this.jwt=getApp().globalData.jwt;
		// 	if(this.kind=='normal'){
		// 		this.tab_list=['人员'];
		// 		this.getPeople();
		// 	}
		// 	else{
		// 		this.tab_list=['人员','股票'];
		// 		this.getPeople();
		// 	}
		// },
		onShow(){
			this.kind=getApp().globalData.kind;
			this.uid=getApp().globalData.uid;
			this.jwt=getApp().globalData.jwt;
			if(this.kind=='normal'){
				this.tab_list=['用户'];
				this.getPeople();
			}
			else{
				this.tab_list=['管理员'];
				this.getPeople();
			}
		},
		methods: {
			checkpw:function(){
				var value=this.new_pw; 
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
			checkrepw:function(){
				var pw=this.new_pw;
				var repw=this.new_repw;
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
			checkname:function(){
				var value=this.self_msg[2];
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
			checktelno:function(){
				var value=this.self_msg[3];
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
			getPeople:function(){
				var data={kind:this.kind,uid:this.uid,jwt:this.jwt};
				api.getPeopleList({
					data
				}).then(res=>{
					console.log("获取人员列表",res);
					if(res.statusCode==200){
						if(res.data.msg=='OK'){
							this.people_list=res.data.data;
						}
						else{
							uni.showToast({
								title:'登录过期请重新登录',
								icon:'none',
								duration:2000,
								complete:function(ep){
									setTimeout(function(){
										{
											uni.navigateTo({
												url:'../login/login'
											});
										}
									},2500)
								}
							})
						}
						console.log("成功获取人员列表");
					}else{
						console.log("获取人员列表失败");
					}
				});
			},
			getStock:function(){
				
			},
			changeTab:function(index){
				this.tab_index=index;
				if(this.tab_index==0){
					this.getPeople();
				}
			},
			choosePeople:function(user){
				this.choose_people_uid=user[0];
				if(user[2]=='预备管理员'){
					this.change_grade_text='升级为正式管理员';
				}
				else{
					this.change_grade_text='降级为预备管理员';
				}
				if(user[2]=='正常'){
					this.change_status_text='注销用户';
				}
				else{
					this.change_status_text='恢复用户';
				}
				this.$refs.popup.open();
			},
			changeMGd:function(){
				var data={uid:this.uid,jwt:this.jwt,opid:this.choose_people_uid,method:this.change_grade_text};
				api.changeManagerGrade({
					data
				}).then(res=>{
					console.log("更改管理员等级",res);
					if(res.statusCode==200){
						if(res.data=='OK'){
							this.$refs.popup.close();
							this.getPeople();
						}
						else{
							uni.showToast({
								title:'登录过期请重新登录',
								icon:'none',
								duration:2000,
								complete:function(ep){
									setTimeout(function(){
										{
											uni.navigateTo({
												url:'../login/login'
											});
										}
									},2500)
								}
							})
						}
						console.log("成功更改管理员等级");
					}else{
						console.log("更改管理员等级失败");
					}
				});
			},
			changeUst:function(){
				var data={uid:this.uid,jwt:this.jwt,opid:this.choose_people_uid,method:this.change_status_text};
				api.changeUserStatus({
					data
				}).then(res=>{
					console.log("更改用户状态",res);
					if(res.statusCode==200){
						if(res.data=='OK'){
							this.$refs.popup.close();
							this.getPeople();
						}
						else{
							uni.showToast({
								title:'登录过期请重新登录',
								icon:'none',
								duration:2000,
								complete:function(ep){
									setTimeout(function(){
										{
											uni.navigateTo({
												url:'../login/login'
											});
										}
									},2500)
								}
							})
						}
						console.log("成功更改用户状态");
					}else{
						console.log("更改用户状态失败");
					}
				});
			},
			changePw:function(){
				this.$refs.popself.close();
				this.$refs.popcenter.open();
			},
			deleteM:function(){
				var that=this;
				uni.showModal({
					title:'确定删除管理员'+this.choose_people_uid+'?' ,
					content:'',
					success: function(res) {
						if (res.confirm) {
							console.log('用户点击确定');
							var data={uid:that.uid,jwt:that.jwt,opid:that.choose_people_uid};
							api.deleteManager({
								data
							}).then(res=>{
								console.log("删除管理员",res);
								if(res.statusCode==200){
									if(res.data=='OK'){
										that.$refs.popup.close();
										that.getPeople();
									}
									else{
										uni.showToast({
											title:'登录过期请重新登录',
											icon:'none',
											duration:2000,
											complete:function(ep){
												setTimeout(function(){
													{
														uni.navigateTo({
															url:'../login/login'
														});
													}
												},2500)
											}
										})
									}
									console.log("成功更改管理员等级");
								}else{
									console.log("更改管理员等级失败");
								}
							});
						}
					}
				});
			},
			submitNewPw:function(){
				if(this.checkpw()&&this.checkrepw()){
					var data={};
					if(this.uid==this.choose_people_uid){
						data={kind:'super',uid:this.uid,jwt:this.jwt,opid:this.choose_people_uid,newpw:this.new_pw};
					}
					else{
						data={kind:this.kind,uid:this.uid,jwt:this.jwt,opid:this.choose_people_uid,newpw:this.new_pw};
					}
					api.changePw({
						data
					}).then(res=>{
						console.log("修改密码",res);
						if(res.statusCode==200){
							if(res.data=='OK'){
								this.$refs.popcenter.close();
								this.$refs.popup.close();
								this.new_pw='';
								this.new_repw='';
								this.getPeople();
							}
							else{
								uni.showToast({
									title:'登录过期请重新登录',
									icon:'none',
									duration:2000,
									complete:function(ep){
										setTimeout(function(){
											{
												uni.navigateTo({
													url:'../login/login'
												});
											}
										},2500)
									}
								})
							}
							console.log("成功修改密码");
						}else{
							console.log("修改密码失败");
						}
					});
				}
			},
			setme:function(){
				var data={uid:this.uid,jwt:this.jwt};
				api.getManagerMsg({
					data
				}).then(res=>{
					console.log("管理员个人信息",res);
					if(res.statusCode==200){
						if(res.data.msg=='OK'){
							this.self_msg=res.data.data;
							this.choose_people_uid=res.data.data[0];
						}
						else{
							uni.showToast({
								title:'登录过期请重新登录',
								icon:'none',
								duration:2000,
								complete:function(ep){
									setTimeout(function(){
										{
											uni.navigateTo({
												url:'../login/login'
											});
										}
									},2500)
								}
							})
						}
						console.log("成功获取管理员个人信息");
					}else{
						console.log("获取管理员个人信息失败");
					}
				});
				this.$refs.popself.open();
			},
			updateMsg:function(){
				if(this.checkname()&&this.checktelno()){
					var data={uid:this.uid,jwt:this.jwt,name:this.self_msg[2],telno:this.self_msg[3]};
					api.updateManagerMsg({
						data
					}).then(res=>{
						console.log("更新管理员个人信息",res);
						if(res.statusCode==200){
							if(res.data=='OK'){
								this.$refs.popself.close();
								this.getPeople();
							}
							else{
								uni.showToast({
									title:'登录过期请重新登录',
									icon:'none',
									duration:2000,
									complete:function(ep){
										setTimeout(function(){
											{
												uni.navigateTo({
													url:'../login/login'
												});
											}
										},2500)
									}
								})
							}
							console.log("成功更新管理员个人信息");
						}else{
							console.log("更新管理员个人信息失败");
						}
					});
				}
			}
		}
	}
</script>

<style lang="scss">
	.topbox{
		/* #ifndef H5 */
		top: 0rpx;
		/* #endif */
		/* #ifdef H5 */
		top: 90rpx;
		/* #endif */
		position: fixed;
		z-index: 10;
		height: 190rpx;
		width: 750rpx;
		background-color: #f0f0f0;
		.searchinput{
			border-width: 3rpx;
			border-style: solid;
			border-color: #000000;
			margin-top: 60rpx;
			height: 50rpx;
			width: 710rpx;
			margin-left: 20rpx;
			margin-right: 20rpx;
			border-radius: 100rpx;
			display: flex;
			.searchlogo{
				margin-top: 5rpx;
				margin-left: 15rpx;
				margin-right: 5rpx;
				width: 40rpx;
				height: 40rpx;
			}
		}
	}
	.Plist{
		margin-top: 15rpx;
		.Pitem{
			display: flex;
			flex-direction: row;
			justify-content: space-around;
			flex-wrap: wrap;
			border-top: 1rpx solid #f0f0f0;
			.Pitem_col{
				width: 250rpx;
				text-align:center;
			}
		}
	}
	.pop{
		display: flex;
		flex-direction: column;
		background-color: #FFFFFF;
		.poptext{
			border-width: 1rpx;
			border-style: solid;
			border-color: #000000;
			height: 80rpx;
			display: flex; 
			justify-content: center;
			align-items: center;
		}
	}
	.newPw{
		width: 700rpx;
		border: 10rpx solid #f9273f;
		background-color: rgb(236,236,236);
		border-radius: 40rpx;
		.in_pw{
			height: 50rpx;
			border: 3rpx solid #000000;
			margin: 15rpx;
			background-color: #FFFFFF;
		}
		.in_button{
			width: 100%;
			display: flex;
			flex-direction: row;
			margin-bottom: 15rpx;
			.button{
				height: 50rpx;
				width:180rpx;
				text-align: center;
				font-size: 20rpx;
			}
		}
	}
	.self{
		width: 700rpx;
		border: 10rpx solid #f9273f;
		background-color: rgb(236,236,236);
		border-radius: 40rpx;
		.in{
			height: 50rpx;
			border: 3rpx solid #000000;
			margin: 15rpx;
			background-color: #FFFFFF;
		}
		.in_button{
			width: 100%;
			display: flex;
			flex-direction: row;
			margin-bottom: 15rpx;
			.button{
				height: 50rpx;
				width:180rpx;
				text-align: center;
				font-size: 20rpx;
			}
		}
	}
</style>
