$(function(){function j(){return g.is(":not(:visible)")}function p(){j()?k():l()}function l(){g.hide();b.css("width",q);c.css("margin-left",r);d.css({"margin-left":"0",height:c.height()});d.find("span").text("\u00bb");d.attr("title",_("Expand sidebar"));document.cookie="sidebar=collapsed"}function k(){c.css("margin-left",s);b.css("width",h);g.show();d.css({"margin-left":h-12,height:c.height()});d.find("span").text("\u00ab");d.attr("title",_("Collapse sidebar"));document.cookie="sidebar=expanded"}
var c=$(".bodywrapper"),b=$(".sphinxsidebar"),g=$(".sphinxsidebarwrapper");if(b.length){var s=c.css("margin-left"),h=b.width(),r=".8em",q=".8em",m=$(".related").css("background-color"),n=$(".document").css("background-color");g.css({"float":"left","margin-right":"0",width:h-28});b.append('<div id="sidebarbutton"><span>&laquo;</span></div>');var a=$("#sidebarbutton"),n=a.css("background-color"),e;e=window.innerHeight?window.innerHeight:$(window).height();a.find("span").css({display:"block","margin-top":(e-
b.position().top-20)/2});a.click(p);a.attr("title",_("Collapse sidebar"));a.css({color:"#FFFFFF","border-left":"1px solid "+m,"font-size":"1.2em",cursor:"pointer",height:c.height(),"padding-top":"1px","margin-left":h-12});a.hover(function(){$(this).css("background-color",m)},function(){$(this).css("background-color",n)});var d=$("#sidebarbutton");if(document.cookie){a=document.cookie.split(";");for(e=0;e<a.length;e++){var f=a[e].split("=");"sidebar"==f[0]&&(f=f[1],"collapsed"==f&&!j()?l():"expanded"==
f&&j()&&k())}}}});