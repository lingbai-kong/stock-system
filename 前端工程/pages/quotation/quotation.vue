<template>
	<view>
		<view class="topbox">
			<view class="searchinput">
				<image class="searchlogo" src="../../static/search.png"/>
				<input placeholder="Search" @input="inputchange($event)"/>
			</view>	
			<view>
				<v-tabs
				  :v-model="tab_index"
				  :tabs="['沪深', '行业', '地区']"
				  :pills="false"
				  :scroll="false"
				  :fixed="true"
				  bgColor="#f0f0f0"
				  line-height="5rpx"
				  lineColor="#f9273f"
				  activeColor="#f9273f"
				  @change="changeTab"
				></v-tabs>
			</view>
		</view>
		<view style="height: 190rpx;"></view>
		<view v-if="tab_index==0">
			<view>
				<v-tabs
				  :v-model="HStab_index"
				  :tabs="HStabs"
				  :pills="false"
				  :scroll="false"
				  :fixed="true"
				  bgColor="#ffffff"
				  line-height="0rpx"
				  color="#262822"
				  activeColor="#f9273f"
				  @change="changeHSTab"
				></v-tabs>
			</view>
			<view class='HSlist'>
				<view class="HSitem" v-if="(search_value==''||item[0].indexOf(search_value) != -1||item[1].indexOf(search_value) != -1)" v-for="(item,index) in HSdata" :key="index" @click="choose_Stock(item)">
					<view class="HSitem_col">
						<view>{{item[1]}}</view>
						<view style="font-size:12px;color: #535353;">{{item[0].substr(0,6)}}</view>
					</view>
					<view class="HSitem_col">
						<view :class="[item[3]>0 ? 'HSitem_red':'HSitem_green']">{{(item[2]-0).toFixed(2)}}</view>
					</view>
					<view class="HSitem_col">
						<view :class="[item[3]>0 ? 'HSitem_red':'HSitem_green']">{{(item[3]-0).toFixed(2)}}%</view>
					</view>
				</view>
			</view>
			<view class="more" v-if="is_more" @click="more()">显示更多</view>
		</view>
		<view v-else-if="tab_index==1">
			<view class="block_group">
				<view class="block" v-for="(item,index) in HYdata" :key="index">
					<view class="name" v-if="item[0]!='None'">{{item[0]}}</view>
					<view class="name" v-else>其他</view>
					<view class="rate">
						<text :class="[item[1]>0 ? 'B_red':'B_green']">{{(item[1]-0).toFixed(2)}}%</text>
					</view>
				</view>
			</view>
		</view>
		<view v-else-if="tab_index==2">
			<view class="block_group">
				<view class="block" v-for="(item,index) in DQdata" :key="index">
					<view class="name" v-if="item[0]!='None'">{{item[0]}}</view>
					<view class="name" v-else>其他</view>
					<view class="rate">
						<text :class="[item[1]>0 ? 'B_red':'B_green']">{{(item[1]-0).toFixed(2)}}%</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '../../src/quotation.js'
	export default {
		components: {
			api
		},
		data() {
			return {
				search_value:'',
				tab_index:0,
				HStab_index:0,
				HStabs:['主板', '科创板', '创业板','中小板'],
				HSdata:[],
				HSdataPos:0,
				is_more:true,
				HYdata:[],
				DQdata:[]
			}
		},
		onLoad(){
			this.ADD_request_HS_data()
		},
		onReachBottom(){
			if(this.tab_index==0)
			{
				console.log('触发onReachBottom事件')
				this.ADD_request_HS_data()
			}
		},
		methods: {
			inputchange(event){
				this.search_value=event.detail.value
				console.log('搜索框内容为'+this.search_value)
			},
			changeTab(index){
				console.log('当前选中索引：' + index)
				this.tab_index=index
				if(index==0)
				{
					this.HSdata.length=0
					this.HSdataPos=0
					this.is_more=true
					this.ADD_request_HS_data()
				}
				else if(index==1)
				{
					this.HYdata.length=0
					this.request_HY_data()
				}
				else if(index==2)
				{
					this.DQdata.length=0
					this.request_DQ_data()
				}
			},
			changeHSTab(index){
				console.log('当前选中沪深索引：' + index)
				this.HStab_index=index
				this.HSdata.length=0
				this.HSdataPos=0
				this.is_more=true
				this.ADD_request_HS_data()
			},
			ADD_request_HS_data(){
				var Skind=this.HStabs[this.HStab_index]
				var data={Skind:Skind,DataPos:this.HSdataPos,RequestKind:'ADD'}
				api.get_HS_list({
					data:data
				}).then(res=>{
					console.log("获取沪深行情列表",res);
					if(res.statusCode==200){
						console.log("成功获取沪深行情列表");
						if(res.data.data.length!=0){
							this.HSdata=this.HSdata.concat(res.data.data)
							this.HSdataPos=this.HSdataPos+100
						}
						else{
							this.is_more=false;
						}
					}else{
						console.log("获取沪深行情列表失败");
					}
				});
			},
			choose_Stock(item){
				console.log('选中了',item[0])
				uni.navigateTo({
					url:'../Kline/Kline?symbol='+item[0]+'&name='+item[1]
				})
			},
			more()
			{
				this.ADD_request_HS_data()
			},
			request_HY_data()
			{
				api.get_HY_list({
					data:{}
				}).then(res=>{
					console.log("获取行业行情列表",res);
					if(res.statusCode==200){
						console.log("成功获取行业行情列表");
						this.HYdata=res.data.data
					}else{
						console.log("获取行业行情列表失败");
					}
				});
			},
			request_DQ_data()
			{
				api.get_DQ_list({
					data:{}
				}).then(res=>{
					console.log("获取地区行情列表",res);
					if(res.statusCode==200){
						console.log("成功获取地区行情列表");
						this.DQdata=res.data.data
					}else{
						console.log("获取地区行情列表失败");
					}
				});
			}
		}
	}
</script>

<style lang='scss'>
	.topbox{
		top: 0rpx;
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
			}
		}
	}
	.more{
		text-align: center;
		color: #808080;
	}
	.block_group{
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		.block{
			margin:5rpx;
			width:230rpx;
			border: 1rpx solid #c0c0c0;
			border-radius: 20rpx;
			.name{
				font-size: x-large;
				text-align: center;
			}
			.rate{
				text-align: center;
				.B_red{
					font-size: x-large;
					color: red;
				}
				.B_green{
					font-size: x-large;
					color: green;
				}
			}
		}
	}
</style>
