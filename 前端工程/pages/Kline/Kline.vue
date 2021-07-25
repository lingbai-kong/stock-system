<template>
	<view>
		<view class="topbox">
			<view class="topbox_left">
				<view class="topbox_left1" style="font-size: 30px;font-weight: 1000;">
					<text :class="[lastday_data[1]>0 ? 'text_red':'text_green']">{{(lastday_data[5]-0).toFixed(2)}}</text>
				</view>
				<view class="topbox_left2">
					<view class="topbox_left2_item">
						<text :class="[lastday_data[1]>0 ? 'text_red':'text_green']">{{(lastday_data[5]-lastday_data[1]).toFixed(2)}}</text>
					</view>
					<view class="topbox_left2_item">
						<text :class="[lastday_data[1]>0 ? 'text_red':'text_green']">{{((lastday_data[5]-lastday_data[1])*100/lastday_data[1]).toFixed(2)}}%</text>
					</view>
				</view>
			</view>
			<view class="topbox_right">
				<view class="topbox_right_line">
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">昨收</view>
						<view style="font-size:12px;">{{(lastday_data[1]-0).toFixed(2)}}</view>
					</view>
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">最高</view>
						<view style="font-size:12px;">{{(lastday_data[3]-0).toFixed(2)}}</view>
					</view>
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">成交量</view>
						<view style="font-size:12px;">{{(lastday_data[6]/10000).toFixed(2)}}万</view>
					</view>
				</view>
				<view class="topbox_right_line">
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">今开</view>
						<view style="font-size:12px;">{{(lastday_data[2]-0).toFixed(2)}}</view>
					</view>
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">最低</view>
						<view style="font-size:12px;">{{(lastday_data[4]-0).toFixed(2)}}</view>
					</view>
					<view class="topbox_right_item">
						<view style="color:#808080;font-size:12px;">成交额</view>
						<view style="font-size:12px;">{{(lastday_data[7]/10000).toFixed(2)}}万</view>
					</view>
				</view>
			</view>
		</view>
		
		<view style="height: 160rpx;"></view>
		
		<view>
			<v-tabs
				:v-model="tab_index"
				:tabs="['日K', '周K']"
				:pills="false"
				:scroll="false"
				:fixed="false"
				bgColor="#ffffff"
				line-height="5rpx"
				lineColor="#f9273f"
				activeColor="#f9273f"
				@change="changeTab"
			></v-tabs>
		</view>
		
		<view> 
			<canvas id="kline" canvas-id='kline' class='kline' style="width: 750rpx; height: 1220rpx;" 
			  @touchstart="KLineTouchStart" @touchmove='KLineTouchMove' @touchend='KLineTouchEnd' ></canvas>  
		</view>
		<view class="picker_group">
			<picker class="picker" name="method1" :value="method1_value" :range="method1_range" @change="method1_picker">{{method1_range[method1_value]}}</picker>
			<picker class="picker" name="method2" :value="method2_value" :range="method2_range" @change="method2_picker">{{method2_range[method2_value]}}</picker>
		</view>
		<view class="messagebox">
			<view class="keyword_group">
				<view class="keyword">{{stock_data[2]}}</view>
				<view class="keyword">{{stock_data[3]}}</view>
				<view class="keyword">{{stock_data[4]}}</view>
			</view>
			<text class="text">简介:{{stock_data[1]}}</text>
		</view>
		<view style="height: 90rpx;"/>
		
		<view class="bottombox">
			<button v-if="is_ZX==false" class="bottom_button" @click="select()">添加自选</button>
			<button v-else class="bottom_button" @click="remove()">删除自选</button>
			<button class="bottom_button" @click="deal()">交易</button>
		</view>
		<!-- <view class="button-sp-area">
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLinePeriod(PERIOD_ID.KLINE_DAY_ID)">日线</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLinePeriod(PERIOD_ID.KLINE_WEEK_ID)">周线</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLinePeriod(PERIOD_ID.KLINE_MINUTE_ID)">1分钟</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLinePeriod(PERIOD_ID.KLINE_15MINUTE_ID)">15分钟</button>
		</view>
		
		<view class="button-sp-area">
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(0,'BOLL')">BOLL</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(1,'RSI')">RSI</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(2,'WR')">WR</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(0,'MA')">MA</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(1,'VOL')">VOL</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeKLineIndex(1,'MACD')">MACD</button>
		</view>
		
		<view class="button-sp-area">
			<button class="mini-btn" type="default" size="mini" @click="ChangeSymbol('000001.sz')">000001.sz</button>
			<button class="mini-btn" type="default" size="mini" @click="ChangeSymbol('600000.sh')">600000.sh</button>
		</view> -->
		
		<uni-popup ref="popdeal" type="center" style="z-index: 200;">
			<view class="self">
				<text style="color: black; font-size: 30rpx; margin-left: 30rpx;">交易</text>
				<view style="margin-left: 15rpx;">股票代码:</view>
				<input class="in" type="text" disabled="true" :value="Symbol.substr(0,6)"/>
				<view style="margin-left: 15rpx;">股票名称:</view>
				<input class="in" type="text" disabled="true" :value="Name"/>
				<view style="margin-left: 15rpx;">交易量:</view>
				<input class="in" type="number" v-model="deal_vol"/>
				<radio-group class="radio_group" @change="chooseBS">
					<radio class="radio" color="#f9273f" value="B">买入</radio>
					<radio class="radio" color="#f9273f" value="S">卖出</radio>
				</radio-group>
				<view class="in_button">
					<view style="width: 400rpx;"></view>
					<button class="button" size="mini" @click="submit_deal()">确定</button>
				</view>
			</view>
		</uni-popup>
	</view>
	
</template>

<script>
import {JSCommon} from '../../umychart.uniapp/umychart.wechat.3.0.js'
import api from '../../src/Kline.js'
import zxapi from '../../src/select.js'
import jyapi from '../../src/deal.js'
import uniPopup from '@/components/uni-popup/uni-popup.vue'
import uniPopupMessage from '@/components/uni-popup/uni-popup-message.vue'
import uniPopupDialog from '@/components/uni-popup/uni-popup-dialog.vue'
function DefaultData() { }

DefaultData.GetKLineOption = function () 
{
    let data = 
    {
        Type: '历史K线图', 
        
        Windows: //窗口指标
        [
            {Index:"MA",Modify: false, Change: false}, 
            {Index:"VOL",Modify: false, Change: false},
			{Index:"MACD",Modify: false, Change: false},
        ], 
 
        CorssCursorTouchEnd:true,
		IsShowRightMenu:false,       //是否显示右键菜单
		CorssCursorInfo:{ Left:2,Right:2 },
  
        Border: //边框
        {
            Left:   1,
            Right:  1, //右边间距
            Top:    1,
            Bottom: 25,
        },
 
        KLine:
        {
            Right:1,                            //复权 0 不复权 1 前复权 2 后复权
            Period:0,                           //周期: 0 日线 1 周线 2 月线 3 年线 
            PageSize:12,
            IsShowTooltip:false,
        },
		
		Frame:  //子框架设置 (Height 窗口高度比例值)
		[
			{   SplitCount:3,
				Height:3,
				IsShowLeftText:true, 
				IsShowRightText:false
			},
			{
				SplitCount:2,
				Height:1,
				IsShowLeftText:true, 
				IsShowRightText:false
			},
			{
				SplitCount:2,
				Height:1,
				IsShowLeftText:true, 
				IsShowRightText:false
			}
		],
		
		ExtendChart:
		[
			{Name:'KLineTooltip' },
		],
        
    };
 
    return data;
}

//周期枚举
var PERIOD_ID=
{
    KLINE_DAY_ID:0,
    KLINE_WEEK_ID:1,
    KLINE_MONTH_ID:2,
    KLINE_YEAR_ID:3,

    KLINE_MINUTE_ID:4,
    KLINE_5MINUTE_ID:5,
    KLINE_15MINUTE_ID:6,
    KLINE_30MINUTE_ID:7,
    KLINE_60MINUTE_ID:8
}

var g_KLine=
{
	JSChart:null
};

export default 
{
	name:'HQChart',
	components: {
		api,
		zxapi,
		jyapi,
		uniPopup,
		uniPopupMessage,
		uniPopupDialog,
	},
	data() 
	{
		let data=
		{
			Symbol:'600519.sh',
			Name:'',
			KLine:
			{
				Option:DefaultData.GetKLineOption(),
				IsShow:false,
				Display:'none',
				Width:350,
				Height:300,
			},
			
			PERIOD_ID:PERIOD_ID,
			
			WindowHeight:0,
			WindowWidth:0,
			
			lastday_data:[],
			tab_index:0,
			
			method1_value:0,
			method1_range:['MA','BOLL'],
			
			method2_value:0,
			method2_range:['VOL','MACD','RSI'],
			
			is_ZX:false,
			
			assert:[],
			it_position:[],
			
			deal_vol:0,
			BS:'',
			
			stock_data:[]
		};
		
		return data;
	},
	
	onLoad(option) 
	{
		uni.getSystemInfo({
			success: (res) => {
				this.WindowHeight=res.windowHeight
				this.WindowWidth=res.windowWidth
				this.KLine.Height=parseInt(res.windowHeight*0.8)
				this.KLine.Width=res.windowWidth
			}
		});
		this.Symbol=option.symbol
		this.Name=option.name
		this.CreateKLineChart()
		uni.setNavigationBarTitle({
			title: option.name+'('+option.symbol.substr(0,6)+')'
		});
		this.fresh_is_ZX(option.symbol)
		this.get_Msg()
	},
	onReady()
	{
		this.ChangeKLinePeriod(PERIOD_ID.KLINE_DAY_ID);
	},
	
	methods: 
	{
		//
		CreateKLineChart:function()
		{
			if (this.KLine.JSChart) return;
			
			let element = new JSCommon.JSCanvasElement();
			// #ifdef APP-PLUS
			element.IsUniApp=true;	//canvas需要指定下 是uniapp的app
			// #endif
			element.ID = 'kline';
			element.Height = this.KLine.Height;  //高度宽度需要手动绑定!!
			element.Width = this.KLine.Width;
					
			g_KLine.JSChart = JSCommon.JSChart.Init(element);
			this.KLine.Option.NetworkFilter=this.NetworkFilter;
			this.KLine.Option.Symbol=this.Symbol;
			this.KLine.Option.IsFullDraw=true; 	//每次手势移动全屏重绘
			g_KLine.JSChart.SetOption(this.KLine.Option);
		},
		
		//K线周期切换
		ChangeKLinePeriod:function(period)
		{
			if (!g_KLine.JSChart)    //不存在创建
			{
				this.KLine.Option.Period=period;
				this.CreateKLineChart();
			}
			else
			{
				g_KLine.JSChart.ChangePeriod(period);
			}
		},
		
		//切换指标 windowIndex=窗口索引 0开始, name=指标名字/ID
		ChangeKLineIndex:function(windowIndex, name)
		{
			if (!g_KLine.JSChart) return;
			
			g_KLine.JSChart.ChangeIndex(windowIndex,name);
		},
		
		//切换股票
		ChangeSymbol:function(symbol)
		{
			if (!g_KLine.JSChart) return;
			
			g_KLine.JSChart.ChangeSymbol(symbol);
		},
		
		NetworkFilter:function(data, callback)	//网络协议回调
		{
		    console.log('[NetworkFilter] data', data);
		    data.PreventDefault=true;	//设置hqchart不请求数据
			//console.log(data.Request.Data)
			api.get_Kline_history_data({
				data:data.Request
			}).then(res=>{
				console.log("获取K线数据",res);
				if(res.statusCode==200){
					console.log("成功获取K线数据");
					var hqchartData={code:0,data:[]}
					hqchartData.symbol=res.data.symbol
					hqchartData.name=res.data.name
					hqchartData.data=res.data.data
					console.log(res.data.data[res.data.data.length-1])
					this.lastday_data=res.data.data[res.data.data.length-1]
					callback({'data':hqchartData});
				}else{
					console.log("获取K线数据失败");
				}
			});
		},

		//KLine事件
		KLineTouchStart: function (event) 
		{
		  if (g_KLine.JSChart) g_KLine.JSChart.OnTouchStart(event);
		},
		
		KLineTouchMove: function (event) 
		{
		  if (g_KLine.JSChart) g_KLine.JSChart.OnTouchMove(event);
		},
		
		KLineTouchEnd: function (event) 
		{
		  if (g_KLine.JSChart) g_KLine.JSChart.OnTouchEnd(event);
		},
		changeTab(index){
			console.log('当前选中索引：' + index)
			this.tab_index=index
			if(index==0)
			{
				this.ChangeKLinePeriod(PERIOD_ID.KLINE_DAY_ID)
			}
			else if(index==1)
			{
				this.ChangeKLinePeriod(PERIOD_ID.KLINE_WEEK_ID)
			}
		},
		method1_picker(e){
			console.log('picker1发送选择改变，携带值为', e.target.value)
			this.method1_value = e.target.value
			this.ChangeKLineIndex(0,this.method1_range[e.target.value])
		},
		method2_picker(e){
			console.log('picker2发送选择改变，携带值为', e.target.value)
			this.method2_value = e.target.value
			this.ChangeKLineIndex(0,this.method2_range[e.target.value])
		},
		fresh_is_ZX(Sid){
			var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
			var that=this
			zxapi.get_ZX_list({
				data:data
			}).then(res=>{
				console.log("获取自选列表",res);
				if(res.statusCode==200){
					console.log("成功获取自选列表");
					if(res.data.msg=='OK')
					{
						var result=false
						for(let i=0;i<res.data.data.length;i++)
						{
							if(res.data.data[i][0]==Sid)
							{
								result=true
								break
							}
						}
						this.is_ZX=result
						console.log(this.is_ZX)
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
		select()
		{
			var that=this
			console.log("将"+this.Symbol+"添加自选")
			var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt,sid:this.Symbol,date:this.lastday_data[0],price:this.lastday_data[5]}
			api.select_Kline({
				data
			}).then(res=>{
				console.log("添加自选",res);
				if(res.statusCode==200){
					if(res.data=='OK'){
						uni.showToast({
							title:'加入自选成功！',
							duration:800,
							icon:'none',
							position:'bottom'
						});
						console.log("加入自选成功");
						that.is_ZX=!that.is_ZX
					}
					else{
						uni.showToast({
							title:res.data+'！',
							duration:800,
							icon:'none',
							position:'bottom'
						});
						console.log("加入自选失败");
					}
				}
			});
		},
		remove(){
			var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt,sid:this.Symbol}
			var that=this
			zxapi.ZX_remove({
				data:data
			}).then(res=>{
				console.log("获取自选列表",res);
				if(res.statusCode==200){
					console.log("成功获取自选列表");
					if(res.data=='OK')
					{
						uni.showToast({
							title:'删除自选成功！',
							duration:800,
							icon:'none',
							position:'bottom'
						});
						that.is_ZX=!that.is_ZX
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
		deal(){
			this.$refs.popdeal.open()
			var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt}
			jyapi.get_assert({
				data:data
			}).then(res=>{
				console.log("获取资产信息",res);
				if(res.statusCode==200){
					console.log("成功获取资产信息");
					if(res.data.msg=='OK')
					{
						this.assert=res.data.data
						console.log(this.assert[0],this.assert[1])
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
			jyapi.get_position({
				data:data
			}).then(res=>{
				console.log("获取持仓信息",res);
				if(res.statusCode==200){
					console.log("成功获取持仓信息");
					if(res.data.msg=='OK')
					{
						this.it_position=[0,0]
						for(var i=0;i<res.data.data.length;i++)
						{
							if(res.data.data[i][0]==this.Symbol)
							{
								this.it_position=[res.data.data[i][1],res.data.data[i][2]]
								break
							}
						}
						console.log(this.it_position[0],this.it_position[1])
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
		chooseBS(event){
			this.BS=event.detail.value
			console.log(event.detail.value)
		},
		check_deal(){
			var BS=this.BS
			var position_vol=this.it_position[0]
			var position_cost=this.it_position[1]
			var assert=this.assert[0]
			var price=this.lastday_data[5]
			var deal_vol=this.deal_vol
			if(deal_vol==0)
			{
				uni.showToast({
					title:'交易量不能为0！',
					icon:'none',
					duration:2000,
				})
				return false
			}
			if(BS=='B')
			{
				if(deal_vol*price>assert)
				{
					uni.showToast({
						title:'账户可用资产不足！',
						icon:'none',
						duration:2000,
					})
					return false
				}
				else
				{
					return true
				}
			}
			else if(BS=='S')
			{
				if(deal_vol>position_vol)
				{
					uni.showToast({
						title:'股票持仓不足！',
						icon:'none',
						duration:2000,
					})
					return false
				}
				else
				{
					return true
				}
			}
			else
			{
				uni.showToast({
					title:'请选中交易类型！',
					icon:'none',
					duration:2000,
				})
				return false
			}
		},
		submit_deal(){
			if(this.check_deal())
			{
				console.log("成功发起交易")
				var data={uid:getApp().globalData.uid,jwt:getApp().globalData.jwt,sid:this.Symbol,vol:this.deal_vol}
				if(this.BS=='B'){
					jyapi.buy({
						data:data
					}).then(res=>{
						console.log("购买股票",res);
						if(res.statusCode==200){
							if(res.data=='OK')
							{
								console.log("成功买入股票");
								uni.showToast({
									title:'成功购买股票',
									icon:'none',
									duration:2000
								})
							}
							else if(res.data=='登录已过期，请重新登录')
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
							else
							{
								uni.showToast({
									title:res.data,
									icon:'none',
									duration:2000,
								})
							}
						}else{
							console.log("购买股票失败");
						}
					});
				}
				else
				{
					jyapi.sale({
						data:data
					}).then(res=>{
						console.log("卖出股票",res);
						if(res.statusCode==200){
							if(res.data=='OK')
							{
								console.log("成功卖出股票");
								uni.showToast({
									title:'成功卖出股票',
									icon:'none',
									duration:2000
								})
							}
							else if(res.data=='登录已过期，请重新登录')
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
							else
							{
								uni.showToast({
									title:res.data,
									icon:'none',
									duration:2000,
								})
							}
						}else{
							console.log("卖出股票失败");
						}
					});
				}
				this.$refs.popdeal.close()
				this.deal_vol=0
			}
		},
		get_Msg(){
			api.get_message({
				data:{sid:this.Symbol}
			}).then(res=>{
				console.log("获取股票信息",res);
				if(res.statusCode==200){
					this.stock_data=res.data.data
					console.log("成功获取股票信息");
				}else{
					console.log("获取股票信息失败");
				}
			});
		}
	}
}
</script>

<style lang="scss">
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200upx;
		width: 200upx;
		margin-top: 200upx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50upx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36upx;
		color: #8f8f94;
	}	
	.topbox{
		// top: 90rpx;
		// position: fixed;
		// z-index: 10;
		// width: 750rpx;
		/* #ifndef H5 */
		top: 0rpx;
		/* #endif */
		/* #ifdef H5 */
		top: 90rpx;
		/* #endif */
		position: fixed;
		z-index: 100;
		border-bottom:#f0f0f0 solid 3rpx;
		width: 750rpx;
		height: 130rpx;
		background-color: white;
		
		padding-top: 15rpx;
		padding-bottom: 15rpx;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		.topbox_left{
			width: 50%;
			.topbox_left1{
				text-align: center;
			}
			.topbox_left2{
				display: flex;
				flex-direction: row;
				justify-content: space-around;
				flex-wrap: wrap;
				.topbox_left2_item{
					text-align: center;
					width: 50%;
				}
			}
		}
		.topbox_right{
			width: 50%;
			.topbox_right_line{
				display: flex;
				flex-direction: row;
				justify-content: space-around;
				flex-wrap: wrap;
				.topbox_right_item{
					width: 33%;
					text-align: left;
				}
			}
		}
	}
	.text_red{
		color:red;
	}
	.text_green{
		color:green;
	}
	.picker_group{
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		width: 240rpx;
		.picker{
			width:45%;
			background-color: #f0f0f0;
			font-size: 12px;
			text-align: center;
			border: #808080 solid 3rpx;
		}
	}
	.messagebox{
		margin: 20rpx;
		background-color: #f0f0f0;
		.keyword_group{
			display: flex;
			flex-direction: row;
			justify-content: space-around;
			flex-wrap: wrap;
			.keyword{
				font-size: large;
			}
		}
		.text{
			color: #333333;
		}
	}
	.bottombox{
		position: fixed;
		bottom: 0rpx;
		width: 750rpx;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		flex-wrap: wrap;
		.bottom_button{
			width:50%;
			height: 90rpx;
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
		.radio_group{
			text-align: center;
			.radio{
				margin: 10rpx;
				margin-left: 90rpx;
				margin-right: 90rpx;
			}
		}
	}
</style>