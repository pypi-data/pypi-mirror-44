window.qunitTestsArray['guiPaths.hook']={test:function()
{let path='/hook/'
let params={create:[{is_valid:false,data:{},},{is_valid:true,data:{type:{value:"HTTP"},recipients:{value:rundomString(6)}},},],update:[{is_valid:true,data:{type:{value:"HTTP"},name:{value:rundomString(6)},},},]}
guiTests.testForPath(path,params)}}