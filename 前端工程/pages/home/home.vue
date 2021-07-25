<template>
	<view>
		<view style="height: 50rpx;"></view>
		<view class="topbox">
			<view class="messagebox">
				<view class="name">{{user_msg[2]}}</view>
				<view class="item">uid: {{user_msg[0]}}</view>
				<!-- <view class="item">邮箱: {{user_msg[4]}}</view> -->
				<view class="item">总资产: {{(assert[0]+stock_assert).toFixed(2)}}</view>
				<button class="button" size="mini" @click="changepw">修改密码</button>
				<button class="button" size="mini" @click="logout">注销</button>
			</view>
			<image class="photo" src="../../static/head.jpg"></image>
		</view>
		
		<view class="title">W型股推荐</view>
		<scroll-view style="height:500rpx;" scroll-y="true" scroll-left="120">
			<view class='HSlist'>
				<view class="HSitem" v-for="(item,index) in TJdata" :key="index" @click="choose_Stock(item)">
					<view class="HSitem_col">
						<view>{{item[3]}}</view>
						<view style="font-size:12px;color: #535353;">{{item[0].substr(0,6)}}</view>
					</view>
					<view class="HSitem_col">
						<view>{{(item[1]-0).toFixed(2)}}</view>
						<view class="SEL_msg">当日收盘价</view>
					</view>
					<view class="HSitem_col">
						<view :class="[item[2]>item[1] ? 'HSitem_red':'HSitem_green']">{{(item[2]-0).toFixed(2)}}</view>
						<view class="SEL_msg">次日预测价</view>
					</view>
				</view>
			</view>
		</scroll-view>
		<view class="title">持仓警示</view>	
		<scroll-view style="height:500rpx;" scroll-y="true" scroll-left="120">
			<view class='HSlist'>
				<view class="HSitem" v-if="item[4]<item[2]" v-for="(item,index) in position" :key="index" @click="choose_Stock(item)">
					<view class="HSitem_col">
						<view>{{item[3]}}</view>
						<view style="font-size:12px;color: #535353;">{{item[0].substr(0,6)}}</view>
					</view>
					<view class="HSitem_col">
						<view :class="[item[4]>item[2]? 'HSitem_red':'HSitem_green']">{{(item[4]-0).toFixed(2)}}</view>
						<view class="SEL_msg">成本价:{{item[2]}}</view>
					</view>
					<view class="HSitem_col">
						<view :class="[item[4]>item[2] ? 'HSitem_red':'HSitem_green']">{{(100*(item[4]-item[2])/item[2]).toFixed(2)}}%</view>
						<view class="SEL_msg">持股数:{{item[1]}}</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import hqapi from '../../src/quotation.js'
	import dealapi from '../../src/deal.js'
	import userapi from '../../src/user.js'
	export default {
		components: {
			hqapi,
			dealapi,
			userapi
		},
		data() {
			return {
				TJdata:[],
				position:[],
				stock_assert:0,
				assert:[],
				user_msg:[]
			}
		},
		onShow(){
			this.get_TJ_list()
			this.get_position()
			this.get_assert()
			this.get_user_message()
		},
		methods: {
			get_TJ_list(){
				hqapi.get_TJ_list({
					data:{}
				}).then(res=>{
					console.log("获取推荐行情列表",res);
					if(res.statusCode==200){
						console.log("成功获取推荐行情列表");
						this.TJdata=res.data.data
					}else{
						console.log("获取推荐行情列表失败");
					}
				});
			},
			get_position(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				dealapi.get_position({
					data:data
				}).then(res=>{
					console.log("获取持仓信息",res);
					if(res.statusCode==200){
						console.log("成功获取持仓信息");
						if(res.data.msg=='OK')
						{
							this.position=res.data.data
							this.stock_assert=0
							for(var i=0;i<res.data.data.length;i++)
							{
								this.stock_assert=this.stock_assert+res.data.data[i][1]*res.data.data[i][4]
							}
						}
						else
						{
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
					}else{
						console.log("获取持仓信息失败");
					}
				});
			},
			get_assert(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				dealapi.get_assert({
					data:data
				}).then(res=>{
					console.log("获取资产信息",res);
					if(res.statusCode==200){
						console.log("成功获取资产信息");
						if(res.data.msg=='OK')
						{
							this.assert=res.data.data
						}
						else
						{
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
					}else{
						console.log("获取资产信息失败");
					}
				});
			},
			get_user_message(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				userapi.get_user_message({
					data:data
				}).then(res=>{
					console.log("获取用户信息",res);
					if(res.statusCode==200){
						console.log("成功获取用户信息");
						if(res.data.msg=='OK')
						{
							this.user_msg=res.data.data
						}
						else
						{
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
					}else{
						console.log("获取用户信息失败");
					}
				});
			},
			choose_Stock(item){
				console.log('选中了',item[0])
				uni.navigateTo({
					url:'../Kline/Kline?symbol='+item[0]+'&name='+item[3]
				})
			},
			changepw(){
				uni.navigateTo({
				    url:'../changepw/changepw'
				})
			},
			logout(){
				getApp().globalData.kind='';
				getApp().globalData.uid='';
				getApp().globalData.jwt='';
				uni.navigateTo({
					url:'../login/login'
				})
			}
		}
	}
</script>

<style lang="scss">
	.title{
		margin:15rpx;
		font-size: large;
		color:#808080;
		border-bottom: solid #f9273f 2rpx;
	}
	.topbox{
		border-left: solid 10rpx #f9273f;
		margin: 25rpx;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		.messagebox{
			width: 400rpx;
			margin-left: 15rpx;
			text-align: left;
			.name{
				font-size: xx-large;
			}
			.item{
				color: #555555;
				font-size: large;
			}
		}
		.photo{
			width: 250rpx;
			height: 250rpx;
		}
	}
	.HSlist{
		margin-top: 15rpx;
		.HSitem{
			display: flex;
			flex-direction: row;
			justify-content: space-around;
			flex-wrap: wrap;
			border-top: 1rpx solid #f0f0f0;
			.HSitem_col{
				width: 33%;
				text-align:center;
				.HSitem_red{
					color: red;
				}
				.HSitem_green{
					color:green;
				}
				.SEL_msg{
					font-size: x-small;
				}
			}
		}
	}
</style>
