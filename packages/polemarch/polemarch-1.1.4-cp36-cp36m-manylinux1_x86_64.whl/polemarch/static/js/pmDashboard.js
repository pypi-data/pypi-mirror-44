var widget_sort={};guiDashboard.model.className="guiDashboard"
guiDashboard.model.count={projects:'-',inventories:'-',hosts:'-',groups:'-',users:'-',history:'-',}
guiDashboard.statsData={projects:'-',inventories:'-',hosts:'-',groups:'-',users:'-',templates:'-'}
guiDashboard.tpl_name='pmDashboard'
guiDashboard.statsDataLast=14;guiDashboard.statsDataLastQuery=14;guiDashboard.statsDataMomentType='day';guiDashboard.model.widgets=[[],]
guiDashboard.model.defaultWidgets=[[{name:'pmwTemplatesCounter',title:'Templates Counter',sort:1,active:true,opt:{},type:1,collapse:false,},{name:'pmwProjectsCounter',title:'Projects Counter',sort:2,active:true,opt:{},type:1,collapse:false,},{name:'pmwInventoriesCounter',title:'Inventories Counter',sort:3,active:true,opt:{},type:1,collapse:false,},{name:'pmwHostsCounter',title:'Hosts Counter',sort:4,active:true,opt:{},type:1,collapse:false,},{name:'pmwGroupsCounter',title:'Groups Counter',sort:5,active:true,opt:{},type:1,collapse:false,},{name:'pmwUsersCounter',title:'Users Counter',sort:6,active:true,opt:{},type:1,collapse:false,},{name:'pmwChartWidget',title:'Tasks history',sort:7,active:true,opt:{},type:0,collapse:false,},],]
guiDashboard.model.ChartLineSettings=[]
guiDashboard.model.defaultChartLineSettings=[{name:"all_tasks",title:"All tasks",color:"#1f77b4",bg_color:"rgba(31, 119, 180, 0.3)",active:true},{name:"ok",title:"OK",color:"#276900",bg_color:"rgba(39, 105, 0, 0.3)",active:true},{name:"error",title:"ERROR",color:"#dc3545",bg_color:"rgba(220, 53, 69, 0.3)",active:true},{name:"interrupted",title:"INTERRUPTED",color:"#9b97e4",bg_color:"rgba(155, 151, 228, 0.3)",active:true},{name:"delay",title:"DELAY",color:"#808419",bg_color:"rgba(128, 132, 25, 0.3)",active:true},{name:"offline",title:"OFFLINE",color:"#9e9e9e",bg_color:"rgba(158, 158, 158, 0.3)",active:true}]
guiDashboard.model.autoupdateInterval=15000;guiDashboard.model.skinsSettings={};guiDashboard.model.selectedSkin='default';guiDashboard.model.dataFromApiLoaded=false;guiDashboard.cloneChartLineSettingsTotally=function(){guiDashboard.model.ChartLineSettings=JSON.parse(JSON.stringify(guiDashboard.model.defaultChartLineSettings));return guiDashboard.model.ChartLineSettings;}
guiDashboard.cloneChartLineSettingsFromApi=function(data){guiDashboard.model.ChartLineSettings=JSON.parse(JSON.stringify(guiDashboard.model.defaultChartLineSettings));for(var i in guiDashboard.model.ChartLineSettings)
{for(var j in data)
{if(guiDashboard.model.ChartLineSettings[i].name==j)
{for(var k in data[j])
{if(guiDashboard.model.ChartLineSettings[i].hasOwnProperty(k))
{guiDashboard.model.ChartLineSettings[i][k]=data[j][k];}}}}}
return guiDashboard.model.ChartLineSettings;}
guiDashboard.cloneDefaultWidgetsTotally=function(){for(var i in guiDashboard.model.defaultWidgets[0])
{guiDashboard.model.widgets[0][i]={};for(var j in guiDashboard.model.defaultWidgets[0][i])
{guiDashboard.model.widgets[0][i][j]=guiDashboard.model.defaultWidgets[0][i][j];}}
console.log(guiDashboard.model.widgets[0]);return guiDashboard.model.widgets[0];}
guiDashboard.cloneDefaultWidgetsStaticSettingsOnly=function(){for(var i in guiDashboard.model.defaultWidgets[0])
{guiDashboard.model.widgets[0][i]={};guiDashboard.model.widgets[0][i].name=guiDashboard.model.defaultWidgets[0][i].name;guiDashboard.model.widgets[0][i].title=guiDashboard.model.defaultWidgets[0][i].title;guiDashboard.model.widgets[0][i].opt=guiDashboard.model.defaultWidgets[0][i].opt;guiDashboard.model.widgets[0][i].type=guiDashboard.model.defaultWidgets[0][i].type;}
return guiDashboard.model.widgets[0];}
guiDashboard.clonetWidgetsSettingsFromApiAndVerify=function(data){guiDashboard.cloneDefaultWidgetsStaticSettingsOnly();for(var i in guiDashboard.model.defaultWidgets[0])
{for(var j in data)
{if(guiDashboard.model.defaultWidgets[0][i].name==j)
{for(var k in guiDashboard.model.defaultWidgets[0][i])
{if(k in data[j]){guiDashboard.model.widgets[0][i][k]=data[j][k];}
else
{guiDashboard.model.widgets[0][i][k]=guiDashboard.model.defaultWidgets[0][i][k];}}}}}
return guiDashboard.model.widgets[0];}
guiDashboard.checkNecessityToLoadDashboardSettingsFromApi=function(defaultObj,currentObj)
{var bool1=false,bool2=false;for(var i in defaultObj){for(var j in currentObj)
{if(defaultObj[i].name==currentObj[j].name)
{for(var k in defaultObj[i])
{if(!(k in currentObj[j])){bool1=true;}}}}}
if(defaultObj.length!=currentObj.length)
{bool2=true;}
if(bool1||bool2)
{return true;}
else
{return false;}}
guiDashboard.getNewWidgetSettings=function(localObj)
{var obj={};obj.sort=localObj.sort;obj.active=localObj.active;obj.collapse=localObj.collapse;return obj;}
guiDashboard.getUserSettingsFromAPI=function()
{var userId=window.my_user_id;if(guiDashboard.checkNecessityToLoadDashboardSettingsFromApi(guiDashboard.model.defaultWidgets[0],guiDashboard.model.widgets[0])||guiDashboard.checkNecessityToLoadDashboardSettingsFromApi(guiDashboard.model.defaultChartLineSettings,guiDashboard.model.ChartLineSettings))
{let query={method:"get",data_type:["user",userId,"settings"],}
let def=new $.Deferred();$.when(api.query(query,true)).done(function(answer)
{let data=answer.data
guiDashboard.setUserSettingsFromApiAnswer(data);def.resolve()}).fail(e=>{console.warn(e)
webGui.showErrors(e)
def.reject()})
return def.promise()}
else
{return false;}}
guiDashboard.setUserSettingsFromApiAnswer=function(data)
{if($.isEmptyObject(data.widgetSettings))
{guiDashboard.cloneDefaultWidgetsTotally();}
else
{guiDashboard.clonetWidgetsSettingsFromApiAndVerify(data.widgetSettings);guiDashboard.model.widgets[0].sort(guiDashboard.sortCountWidget);}
if($.isEmptyObject(data.chartLineSettings))
{guiDashboard.cloneChartLineSettingsTotally();}
else
{guiDashboard.cloneChartLineSettingsFromApi(data.chartLineSettings);}
if(data.autoupdateInterval)
{guiDashboard.cloneAutoupdateIntervalFromApi(data.autoupdateInterval);}
else
{guiDashboard.cloneDefaultAutoupdateInterval()}
if(data.skinsSettings)
{guiDashboard.cloneDataSkinsFromApi(data.skinsSettings);}
else
{guiLocalSettings.set('skins_settings',guiDashboard.model.skinsSettings);}
if(data.selectedSkin)
{guiDashboard.cloneSelectedSkinFromApi(data.selectedSkin);}
else
{guiDashboard.setSelectedSkin(guiDashboard.model.selectedSkin);}
guiDashboard.model.dataFromApiLoaded=true;}
guiDashboard.cloneAutoupdateIntervalFromApi=function(interval)
{guiDashboard.model.autoupdateInterval=interval;guiLocalSettings.set('page_update_interval',guiDashboard.model.autoupdateInterval)}
guiDashboard.cloneDefaultAutoupdateInterval=function()
{guiLocalSettings.setIfNotExists('page_update_interval',guiDashboard.model.autoupdateInterval)}
guiDashboard.cloneDataSkinsFromApi=function(skins)
{guiDashboard.model.skinsSettings=$.extend(true,{},skins);guiLocalSettings.set('skins_settings',guiDashboard.model.skinsSettings);}
guiDashboard.setSelectedSkin=function(selectedSkin)
{guiCustomizer.setSkin(selectedSkin);guiCustomizer.skin.init();guiCustomizer.render();}
guiDashboard.cloneSelectedSkinFromApi=function(selectedSkin)
{guiDashboard.model.selectedSkin=selectedSkin;guiDashboard.setSelectedSkin(selectedSkin);}
guiDashboard.putUserDashboardSettingsToAPI=function()
{var userId=window.my_user_id;var widgetSettings={};for(var i in guiDashboard.model.widgets[0]){var objName=guiDashboard.model.widgets[0][i].name;widgetSettings[objName]=guiDashboard.getNewWidgetSettings(guiDashboard.model.widgets[0][i]);}
var chartLineSettings={};for(var i in guiDashboard.model.ChartLineSettings){var objName=guiDashboard.model.ChartLineSettings[i].name;chartLineSettings[objName]={active:guiDashboard.model.ChartLineSettings[i].active};}
let query={method:"post",data_type:["user",userId,"settings"],data:{autoupdateInterval:guiDashboard.model.autoupdateInterval,widgetSettings:widgetSettings,chartLineSettings:chartLineSettings,skinsSettings:guiDashboard.model.skinsSettings,selectedSkin:guiDashboard.model.selectedSkin,}}
let def=new $.Deferred();$.when(api.query(query,true)).done(d=>{def.resolve();}).fail(e=>{console.warn(e)
webGui.showErrors(e)
def.reject()})
return def.promise()}
guiDashboard.sortCountWidget=function(Obj1,Obj2)
{return Obj1.sort-Obj2.sort;}
guiDashboard.setNewWidgetActiveValue=function(thisButton)
{var widgetName=thisButton.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("id");for(var i in guiDashboard.model.widgets[0])
{if(guiDashboard.model.widgets[0][i].name==widgetName)
{guiDashboard.model.widgets[0][i].active=false;}}
guiDashboard.putUserDashboardSettingsToAPI();}
guiDashboard.setNewWidgetCollapseValue=function(thisButton)
{var widgetName=thisButton.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("id");for(var i in guiDashboard.model.widgets[0])
{if(guiDashboard.model.widgets[0][i].name==widgetName)
{guiDashboard.model.widgets[0][i].collapse=!guiDashboard.model.widgets[0][i].collapse;if(widgetName=="pmwChartWidget")
{if(guiDashboard.model.widgets[0][i].collapse==false)
{$("#period-list").slideDown(400);}
else
{$("#period-list").slideUp(400);}}}}
guiDashboard.putUserDashboardSettingsToAPI();}
guiDashboard.getOptionsFromTable=function(table_id,guiDashboard_obj)
{var modalTable=document.getElementById(table_id);var modalTableTr=modalTable.getElementsByTagName("tr");for(var i=1;i<modalTableTr.length;i++)
{var guiDashboard_obj_name=modalTableTr[i].getAttribute("rowname");var modalTableTrTds=modalTableTr[i].children;for(var j=0;j<modalTableTrTds.length;j++)
{var valueName=modalTableTrTds[j].getAttribute("valuename");if(valueName)
{var classList1=modalTableTrTds[j].children[0].classList;var selected=false;for(var k in classList1)
{if(classList1[k]=="selected")
{selected=true;}}
for(var z in guiDashboard_obj)
{if(guiDashboard_obj[z].name==guiDashboard_obj_name)
{guiDashboard_obj[z][valueName]=selected;}}}}}}
guiDashboard.saveWigdetsOptions=function()
{guiDashboard.getOptionsFromTable("modal-table",guiDashboard.model.widgets[0]);guiDashboard.putUserDashboardSettingsToAPI();}
guiDashboard.saveWigdetsOptionsFromModal=function()
{return $.when(guiDashboard.saveWigdetsOptions()).done(function(){guiModal.modalClose();return spajs.openURL("/");}).promise();}
guiDashboard.getDataForStatusChart=function(tasks_data,tasks_data_t,status,date_format)
{for(var i in tasks_data){tasks_data[i]=0;}
for(var i in guiDashboard.statsData.jobs[guiDashboard.statsDataMomentType])
{var val=guiDashboard.statsData.jobs[guiDashboard.statsDataMomentType][i];var time=+moment(val[guiDashboard.statsDataMomentType]).tz(window.timeZone).format("x");time=moment(time).tz(window.timeZone).format(date_format);if(val.status==status){tasks_data[time]=val.sum;}}
var chart_tasks_data1=[];for(var j in tasks_data_t)
{var time=tasks_data_t[j]
chart_tasks_data1.push(tasks_data[time]/1);}
return chart_tasks_data1;}
guiDashboard.loadStats=function()
{var thisObj=this;let query={type:"get",item:"stats",filters:"last="+guiDashboard.statsDataLastQuery,}
let def=new $.Deferred();$.when(api.query(query,true)).done(function(answer)
{thisObj.statsData=answer.data;def.resolve()}).fail(function(e){def.reject(e)})
return def.promise();}
guiDashboard.updateStatsDataLast=function(thisEl)
{var newLast=thisEl.value;switch(newLast){case'1095':guiDashboard.statsDataLast=3;guiDashboard.statsDataMomentType="year";break;case'365':guiDashboard.statsDataLast=13;guiDashboard.statsDataMomentType="month";break;case'90':guiDashboard.statsDataLast=3;guiDashboard.statsDataMomentType="month";break;default:guiDashboard.statsDataLast=+newLast;guiDashboard.statsDataMomentType="day";break;}
guiDashboard.statsDataLastQuery=+newLast;guiLocalSettings.set('chart_period',+newLast);guiDashboard.updateData();}
guiDashboard.stopUpdates=function()
{clearTimeout(this.model.updateTimeoutId)
this.model.updateTimeoutId=undefined;}
guiDashboard.toggleSortable=function(thisButton)
{var state=widget_sort.option("disabled");widget_sort.option("disabled",!state);if(thisButton.children[0].getAttribute("class")=="fa fa-lock")
{thisButton.children[0].setAttribute("class","fa fa-unlock");var sortableArr=$('.cursor-move1');for(var i=0;i<sortableArr.length;i++)
{$(sortableArr[i]).addClass('cursor-move');$(sortableArr[i]).removeClass('cursor-move1');}}
else
{thisButton.children[0].setAttribute("class","fa fa-lock");var sortableArr=$('.cursor-move');for(var i=0;i<sortableArr.length;i++)
{$(sortableArr[i]).addClass('cursor-move1');$(sortableArr[i]).removeClass('cursor-move');}}}
tabSignal.connect('guiLocalSettings.hideMenu',function(){setTimeout(function(){if(spajs.currentOpenMenu&&spajs.currentOpenMenu.id=='home')
{guiDashboard.updateData()}},200)})
guiDashboard.updateData=function()
{if(this.model.updateTimeoutId)
{clearTimeout(this.model.updateTimeoutId)
this.model.updateTimeoutId=undefined}
$.when(guiDashboard.loadStats()).done(function()
{pmwHostsCounter.updateCount();pmwTemplatesCounter.updateCount();pmwGroupsCounter.updateCount();pmwProjectsCounter.updateCount();pmwInventoriesCounter.updateCount();pmwUsersCounter.updateCount();guiDashboard.renderChart();guiDashboard.renderChartProgressBars();});this.model.updateTimeoutId=setTimeout(function(){guiDashboard.updateData()},1000*30)}
guiDashboard.getChartStartTime=function()
{let monthNum=moment().format("MM");let yearNum=moment().format("YYYY");let dayNum=moment().format("DD");let hourNum=",T00:00:00";let startTimeOrg="";switch(guiDashboard.statsDataMomentType){case"year":startTimeOrg=yearNum+"-01-01"+hourNum;break;case"month":startTimeOrg=yearNum+"-"+monthNum+"-01"+hourNum;break;case"day":startTimeOrg=yearNum+"-"+monthNum+"-"+dayNum+hourNum;break;}
let startTime=+moment(startTimeOrg).subtract(guiDashboard.statsDataLast-1,guiDashboard.statsDataMomentType).tz(window.timeZone).format("x");return startTime;}
guiDashboard.getChartData=function(startTime,date_format)
{let tasks_data={};let tasks_data_t=[];for(let i=-1;i<guiDashboard.statsDataLast;i++)
{let time=+moment(startTime).add(i,guiDashboard.statsDataMomentType).tz(window.timeZone).format("x");time=moment(time).tz(window.timeZone).format(date_format);tasks_data[time]=0;tasks_data_t.push(time);}
let chart_data_obj={datasets:[],labels:[]};for(let i in guiDashboard.model.ChartLineSettings)
{let lineChart=guiDashboard.model.ChartLineSettings[i];if(lineChart.name=='all_tasks')
{for(let i in guiDashboard.statsData.jobs[guiDashboard.statsDataMomentType]){let val=guiDashboard.statsData.jobs[guiDashboard.statsDataMomentType][i];let time=+moment(val[guiDashboard.statsDataMomentType]).tz(window.timeZone).format("x");time=moment(time).tz(window.timeZone).format(date_format);if(tasks_data[time]!==undefined)
{tasks_data[time]=val.all;}}
let chart_tasks_data=[];for(let j in tasks_data_t){let time=tasks_data_t[j]
chart_tasks_data.push(tasks_data[time]/1);chart_data_obj.labels.push(time);}
if(lineChart.active==true)
{chart_data_obj.datasets.push({label:'All tasks',data:chart_tasks_data,borderColor:lineChart.color,backgroundColor:lineChart.bg_color,})}}
if(lineChart.name!='all_tasks'&&lineChart.active==true)
{let chart_tasks_data_var=guiDashboard.getDataForStatusChart(tasks_data,tasks_data_t,lineChart.title,date_format);chart_data_obj.datasets.push({label:lineChart.title,data:chart_tasks_data_var,borderColor:guiDashboard.getChartLineColor(lineChart),backgroundColor:guiDashboard.getChartLineColor(lineChart,true),})}}
return chart_data_obj;}
guiDashboard.getChartLineColor=function(lineChart,bg)
{let alpha=1;let prop='color';if(bg)
{alpha=0.3;prop='bg_color';}
if(guiCustomizer.skin.value['history_status_'+lineChart.name])
{if(guiCustomizer.skin.value['history_status_'+lineChart.name][0]=="#")
{return hexToRgbA(guiCustomizer.skin.value['history_status_'+lineChart.name],alpha);}
return guiCustomizer.skin.value['history_status_'+lineChart.name]}
return lineChart[prop];}
guiDashboard.setChartSettings=function(ctx,chart_data_obj)
{guiDashboard.model.historyChart=new Chart(ctx,{type:'line',data:{datasets:chart_data_obj.datasets,labels:chart_data_obj.labels,},options:{maintainAspectRatio:false,legend:{labels:{fontColor:guiCustomizer.skin.value.chart_legend_text_color,},},scales:{yAxes:[{ticks:{beginAtZero:true,fontColor:guiCustomizer.skin.value.chart_axes_text_color,},gridLines:{color:guiCustomizer.skin.value.chart_axes_lines_color,}}],xAxes:[{ticks:{fontColor:guiCustomizer.skin.value.chart_axes_text_color,},gridLines:{color:guiCustomizer.skin.value.chart_axes_lines_color,}}]}}});}
guiDashboard.renderChart=function(need_update)
{let ctx=document.getElementById("chart_js_canvas");if(ctx&&ctx.getContext)
{ctx=ctx.getContext('2d');let startTime=guiDashboard.getChartStartTime();let date_format='DD.MM.YY';let chart_data_obj=guiDashboard.getChartData(startTime,date_format);if(guiDashboard.model.historyChart)
{if(guiDashboard.updateChartOrNot(guiDashboard.model.historyChart,chart_data_obj)||need_update)
{try
{guiDashboard.model.historyChart.destroy();}
catch(e){}
guiDashboard.setChartSettings(ctx,chart_data_obj);}}
else
{guiDashboard.setChartSettings(ctx,chart_data_obj);}}}
guiDashboard.renderChartProgressBars=function()
{let el=$("#chart_progress_bars");if(el.length!=0)
{let d=guiDashboard.formChartProgressBarsData();let opt={settings:guiDashboard.model.ChartLineSettings,stats_data:d.data,all:d.all,}
let html=spajs.just.render('chart_progress_bars',{opt:opt});$("#chart_progress_bars").html(html);}};guiDashboard.formChartProgressBarsData=function()
{let data={};let stats={};let all=0;if(guiDashboard.statsData&&guiDashboard.statsData.jobs&&guiDashboard.statsData.jobs.year)
{stats=guiDashboard.statsData.jobs.year;for(let i in stats)
{let record=stats[i];if(data[record.status])
{data[record.status].all+=record.all;data[record.status].sum+=record.sum;}
else
{data[record.status]={all:record.all,sum:record.sum,status:record.status,}}
if(all<data[record.status].all)
{all=data[record.status].all;}}
for(let i in data)
{data[i].all=all;}}
return{all:all,data:data};}
guiDashboard.updateChartOrNot=function(chart,new_data_obj)
{let chart_data=chart.config.data;let bool1=deepEqual(chart_data.labels,new_data_obj.labels);if(!bool1)
{return true;}
for(let i in chart_data.datasets)
{let old_item=chart_data.datasets[i];for(let j in new_data_obj.datasets)
{let new_item=new_data_obj.datasets[i];if(old_item.label==new_item.label)
{let bool2=deepEqual(new_item.data,old_item.data);if(!bool2)
{return true;}}}}
return false;}
guiDashboard.open=function(holder,menuInfo,data)
{setActiveMenuLi();var thisObj=this;return $.when(guiDashboard.getUserSettingsFromAPI()).always(function()
{for(var i in guiDashboard.model.widgets)
{for(var j in guiDashboard.model.widgets[i])
{if(guiDashboard.model.widgets[i][j].widget===undefined)
{let name=guiDashboard.model.widgets[i][j]['name']
if(!window[name])
{console.warn("widget name="+name+" not defined")
continue;}
guiDashboard.model.widgets[i][j].widget=new window[guiDashboard.model.widgets[i][j]['name']](guiDashboard.model.widgets[i][j].opt);}}}
guiDashboard.model.historyChart=undefined;thisObj.updateData()
$(holder).insertTpl(spajs.just.render(thisObj.tpl_name,{guiObj:thisObj}))
pmwAnsibleModuleWidget.render();pmwChartWidget.render();if($('select').is('#chart-period'))
{let chart_period=guiLocalSettings.get('chart_period')||guiDashboard.statsDataLastQuery;$('#chart-period').val(chart_period).change();}
if($('div').is('#dnd-container'))
{widget_sort=Sortable.create(document.getElementById("dnd-container"),{animation:150,handle:".dnd-block",draggable:".dnd-block",disabled:true,onUpdate:function(evt)
{var item=evt.item;var divArr=$('.dnd-block');var idArr=[];for(var i=0;i<divArr.length;i++)
{idArr.push(divArr[i].id);}
for(var i=0;i<idArr.length;i++)
{for(var j=0;j<guiDashboard.model.widgets[0].length;j++)
{if(idArr[i].toLowerCase()==guiDashboard.model.widgets[0][j].name.toLowerCase())
{guiDashboard.model.widgets[0][j].sort=i+1;guiDashboard.model.widgets[0].sort(guiDashboard.sortCountWidget);}}}
guiDashboard.putUserDashboardSettingsToAPI();}});}}).promise();}
guiDashboardWidget={id:'',model:{test:1},render:function(){},init:function(opt){mergeDeep(this.model,opt)}}
var pmwAnsibleModuleWidget=inheritance(guiDashboardWidget);pmwAnsibleModuleWidget.render=function()
{var div_id="#pmwAnsibleModuleWidget";return"";}
var pmwChartWidget=inheritance(guiDashboardWidget);pmwChartWidget.render=function()
{var div_id="#pmwChartWidget";var html=spajs.just.render('pmwChartWidget');$(div_id).html(html);return"";}
var pmwItemsCounter=inheritance(guiDashboardWidget);pmwItemsCounter.model.count='-';pmwItemsCounter.model.nameInStats="";pmwItemsCounter.render=function()
{var html=spajs.just.render('pmwItemsCounter',{model:this.model});return window.JUST.onInsert(html,function(){});}
pmwItemsCounter.updateCount=function()
{var thisObj=this;var statsData=guiDashboard.statsData;thisObj.model.count=statsData[thisObj.model.nameInStats];}
var pmwHostsCounter=inheritance(pmwItemsCounter);pmwHostsCounter.model.nameInStats="hosts";pmwHostsCounter.model.path="host";var pmwTemplatesCounter=inheritance(pmwItemsCounter);pmwTemplatesCounter.model.nameInStats="templates";pmwTemplatesCounter.model.path="";var pmwGroupsCounter=inheritance(pmwItemsCounter);pmwGroupsCounter.model.nameInStats="groups";pmwGroupsCounter.model.path="group";var pmwProjectsCounter=inheritance(pmwItemsCounter);pmwProjectsCounter.model.nameInStats="projects";pmwProjectsCounter.model.path="project";var pmwInventoriesCounter=inheritance(pmwItemsCounter);pmwInventoriesCounter.model.nameInStats="inventories";pmwInventoriesCounter.model.path="inventory";var pmwUsersCounter=inheritance(pmwItemsCounter);pmwUsersCounter.model.nameInStats="users";pmwUsersCounter.model.path="user";tabSignal.connect("webGui.start",function(){guiDashboard.getUserSettingsFromAPI();})
guiDashboard.showWidgetSettingsModal=function()
{let opt={title:'Widget settings',};let html=spajs.just.render('widget_settings_modal');guiModal.setModalHTML(html,opt);guiModal.modalOpen();}
tabSignal.connect("guiSkins.save",function(obj)
{guiDashboard.model.skinsSettings[obj.skin.name]=obj.skin.value;guiDashboard.putUserDashboardSettingsToAPI();})
tabSignal.connect("guiSkins.deleteSettings",function(obj)
{delete guiDashboard.model.skinsSettings[obj.skin.name];guiDashboard.putUserDashboardSettingsToAPI();});tabSignal.connect("guiSkin.changed",function(obj){if(guiDashboard.model.dataFromApiLoaded)
{guiDashboard.model.selectedSkin=obj.skinId;guiDashboard.putUserDashboardSettingsToAPI();}
guiDashboard.renderChart(true);guiDashboard.renderChartProgressBars();});