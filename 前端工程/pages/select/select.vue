<template>
	<view>
		<view class="topbox">
			<view class="searchinput">
				<image class="searchlogo" src="../../static/search.png"/>
				<input placeholder="Search" @input="inputchange($event)"/>
			</view>
		</view>
		<view style="height: 150rpx;"></view>
		<view class='HSlist'>
			<view class="HSitem" v-if="(search_value==''||item[0].indexOf(search_value) != -1||item[1].indexOf(search_value) != -1)" v-for="(item,index) in HSdata" :key="index" @click="choose_Stock(item)" @longpress="remove(item)">
				<view class="HSitem_col">
					<view>{{item[1]}}</view>
					<view style="font-size:12px;color: #535353;">{{item[0].substr(0,6)}}</view>
				</view>
				<view class="HSitem_col">
					<view :class="[item[3]>0 ? 'HSitem_red':'HSitem_green']">{{(item[2]-0).toFixed(2)}}</view>
					<view class="SEL_msg">自选价:{{item[5]}}</view>
				</view>
				<view class="HSitem_col">
					<view :class="[item[3]>0 ? 'HSitem_red':'HSitem_green']">{{(item[3]-0).toFixed(2)}}%</view>
					<view class="SEL_msg">自选日:{{item[4]}}</view>
				</view>
			</view>
		</view>
	</view>
</template>
<script>
	import api from '../../src/select.js'
	export default {
		components: {
			api
		},
		data() {
			return {
				search_value:'',
				HSdata:[]
			}
		},
		onShow(){
			this.fresh_list()
		},
		methods: {
			inputchange(event){
				this.search_value=event.detail.value
				console.log('搜索框内容为'+this.search_value)
			},
			choose_Stock(item){
				console.log('选中了',item[0])
				uni.navigateTo({
					url:'../Kline/Kline?symbol='+item[0]+'&name='+item[1]
				})
			},
			fresh_list(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				api.get_ZX_list({
					data:data
				}).then(res=>{
					console.log("获取自选列表",res);
					if(res.statusCode==200){
						console.log("成功获取自选列表");
						if(res.data.msg=='OK')
						{
							this.HSdata=res.data.data
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
						console.log("获取自选列表失败");
					}
				});
			},
			remove(item){
				console.log('选中了',item[0])
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt,sid:item[0]}
				var that=this
				uni.showModal({
					title:'删除自选股'+item[1]+'?' ,
					content:'',
					success: function(res) {
						if (res.confirm) {
							console.log('用户点击确定');
							api.ZX_remove({
								data:data
							}).then(res=>{
								console.log("获取自选列表",res);
								if(res.statusCode==200){
									console.log("成功获取自选列表");
									if(res.data=='OK')
									{
										that.fresh_list()
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
									console.log("获取自选列表失败");
								}
							});
						}
					}
				})
			}
		}
	}
</script>
<style lang='scss'>
	.topbox{
		top: 0rpx;
		position: fixed;
		z-index: 10;
		height: 150rpx;
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
