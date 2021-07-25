<template>
	<view>
		<view style="height: 50rpx;"></view>
		<view class="title">资产明细</view>
		<view class="topbox">
			<view class="topbox_col">
				<view class="value">{{(assert[0]+stock_assert).toFixed(2)}}</view>
				<view class="label">总资产</view>
				<view class="value">{{assert[0]}}</view>
				<view class="label">可用资产</view>
				<view class="value">{{(100*stock_assert/(assert[0]+stock_assert)).toFixed(2)}}%</view>
				<view class="label">仓位</view>
			</view>
			<view class="topbox_col">
				<view class="value">{{assert[1]}}</view>
				<view class="label">起始资产</view>
				<view class="value">
					<view :class="[assert[0]+stock_assert>assert[1]? 'red':'green']">{{(assert[0]+stock_assert-assert[1]).toFixed(2)}}</view>
				</view>
				<view class="label">总盈亏</view>
				<view class="value">
					<view :class="[assert[0]+stock_assert>assert[1]? 'red':'green']">{{(100*(assert[0]+stock_assert-assert[1])/assert[1]).toFixed(2)}}%</view>
				</view>
				<view class="label">盈亏比</view>
			</view>
		</view>
		<view class="charts-box">
			<qiun-data-charts type="ring" :opts="{legend:{position:'bottom'}}" :eopts="ringOpts" :chartData="Piedata" :echartsH5="true" :echartsApp="true"/>
		</view>
		<view class="title">持仓股票</view>
		<scroll-view style="height:300rpx;" scroll-y="true" scroll-left="120">
			<view class='HSlist'>
				<view class="HSitem" v-for="(item,index) in position" :key="index" @click="choose_Stock(item)">
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
		<view class="title">交易明细</view>
		<scroll-view style="height:300rpx;" scroll-y="true" scroll-left="120">
			<view class='HSlist'>
				<view class="HSitem" v-for="(item,index) in detail" :key="index">
					<view class="HSitem_col">
						<view>{{item[0].substr(14,28)}}</view>
						<view style="font-size:12px;color: #535353;">日期:{{item[2]}}</view>
					</view>
					<view class="HSitem_col">
						<view>{{item[1]}}</view>
						<view class="SEL_msg">成交价:{{item[3]}}</view>
					</view>
					<view class="HSitem_col">
						<view>成交量{{item[4]}}</view>
						<view class="SEL_msg">买入卖出:{{item[5]}}</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import api from '../../src/deal.js'
	export default {
		components: {
			api
		},
		data() {
			return {
				assert:[],
				position:[],
				detail:[],
				stock_assert:0,
				Piedata:{
					"series": [{
						data:[
							
						]
					}]
				},
				ringOpts:{
				  color:['#4ccfff','#f9273f'],
				  legend:{show:false}
				}
			}
		},
		onShow(){
			this.Piedata.series[0].data=[]
			this.get_assert()
			this.get_position()
			this.get_detail()
		},
		methods: {
			get_assert(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				api.get_assert({
					data:data
				}).then(res=>{
					console.log("获取资产信息",res);
					if(res.statusCode==200){
						console.log("成功获取资产信息");
						if(res.data.msg=='OK')
						{
							this.assert=res.data.data
							let temp=this.Piedata
							temp.series[0].data.push({name:"可用资产",value:res.data.data[0].toFixed(2)})
							this.Piedata=temp
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
			get_position(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				api.get_position({
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
							let temp=this.Piedata
							temp.series[0].data.push({name:"股票资产",value:this.stock_assert.toFixed(2)})
							this.Piedata=temp
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
			get_detail:function(){
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
				api.get_detail({
					data:data
				}).then(res=>{
					console.log("获取交易明细",res);
					if(res.statusCode==200){
						console.log("成功获取交易明细");
						if(res.data.msg=='OK')
						{
							this.detail=res.data.data
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
						console.log("获取交易明细失败");
					}
				});
			},
			choose_Stock(item){
				console.log('选中了',item[0])
				uni.navigateTo({
					url:'../Kline/Kline?symbol='+item[0]+'&name='+item[3]
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
		background-color: #f0f0f0;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		margin: 20rpx;
		.topbox_col{
			text-align: center;
			width:40%;
			.value{
				font-size: x-large;
				.red{
					color:red
				}
				.green{
					color:green
				}
			}
			.label{
				color:#555555;
				font-size: large;
			}
		}
	}
	.charts-box {
		width:100%;
		height:300rpx;
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
