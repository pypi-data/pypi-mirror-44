function addSettingsToChangePassword(obj)
{let properties=obj.definition.properties;['old_password','password','password2'].forEach(function(name){properties[name].format='password';})}
function addSettingsToUserSettings(path){let user_settings=guiSchema.path[path];if(!user_settings)
{return;}
user_settings.canEdit=true;user_settings.canEditInView=true;user_settings.methodEdit='post';if(user_settings&&user_settings.method)
{user_settings.method.post='edit';}
try{['chartLineSettings','widgetSettings'].forEach(function(name){user_settings.schema.get.fields[name].format='inner_api_object';user_settings.schema.get.fields[name].readOnly=false;})
user_settings.schema.get.fields['autoupdateInterval'].readOnly=false;user_settings.schema.get.fields['autoupdateInterval'].min=1;user_settings.schema.get.fields['autoupdateInterval'].default=guiDashboard.model.autoupdateInterval/1000;user_settings.schema.get.fields['autoupdateInterval'].title='Data autoupdate interval';user_settings.schema.get.fields['autoupdateInterval'].format='time_interval';user_settings.schema.edit={fields:$.extend(true,{},user_settings.schema.get.fields),operationId:'user_settings_edit',query_type:'post',}}
catch(e){}}
function gui_user_settings_update(){let base_update=gui_page_object.update.apply(this,arguments);return $.when(base_update).done(data=>{guiDashboard.setUserSettingsFromApiAnswer(data.data)})}
function gui_user_settings_getDataFromForm(){let base_data_from_form=gui_base_object.getDataFromForm.apply(this,arguments);base_data_from_form['skinsSettings']=$.extend(true,{},guiDashboard.model.skinsSettings);base_data_from_form['selectedSkin']=guiDashboard.model.selectedSkin;return base_data_from_form;}
tabSignal.connect("openapi.completed",function()
{addSettingsToUserSettings('/user/{pk}/settings/');let user=guiSchema.path['/user/'];try{user.schema.new.fields['password'].format="password";user.schema.new.fields['password2'].format="password";}
catch(e){}})
tabSignal.connect("openapi.schema.definition.ChangePassword",addSettingsToChangePassword);gui_user_settings={update:function()
{return gui_user_settings_update.apply(this,arguments);},getDataFromForm:function()
{return gui_user_settings_getDataFromForm.apply(this,arguments);},}