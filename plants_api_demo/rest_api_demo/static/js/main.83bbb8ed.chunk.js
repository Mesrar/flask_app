(this["webpackJsonpreact-flask-app-plants"]=this["webpackJsonpreact-flask-app-plants"]||[]).push([[0],{10:function(n){n.exports=JSON.parse('[{"id":"AL","val":"01"},{"id":"AK","val":"02"},{"id":"AS","val":"60"},{"id":"AZ","val":"04"},{"id":"AR","val":"05"},{"id":"CA","val":"06"},{"id":"CO","val":"08"},{"id":"CT","val":"09"},{"id":"DE","val":"10"},{"id":"DC","val":"11"},{"id":"FL","val":"12"},{"id":"FM","val":"64"},{"id":"GA","val":"13"},{"id":"GU","val":"66"},{"id":"HI","val":"15"},{"id":"ID","val":"16"},{"id":"IL","val":"17"},{"id":"IN","val":"18"},{"id":"IA","val":"19"},{"id":"KS","val":"20"},{"id":"KY","val":"21"},{"id":"LA","val":"22"},{"id":"ME","val":"23"},{"id":"MH","val":"68"},{"id":"MD","val":"24"},{"id":"MA","val":"25"},{"id":"MI","val":"26"},{"id":"MN","val":"27"},{"id":"MS","val":"28"},{"id":"MO","val":"29"},{"id":"MT","val":"30"},{"id":"NE","val":"31"},{"id":"NV","val":"32"},{"id":"NH","val":"33"},{"id":"NJ","val":"34"},{"id":"NM","val":"35"},{"id":"NY","val":"36"},{"id":"NC","val":"37"},{"id":"ND","val":"38"},{"id":"MP","val":"69"},{"id":"OH","val":"39"},{"id":"OK","val":"40"},{"id":"OR","val":"41"},{"id":"PW","val":"70"},{"id":"PA","val":"42"},{"id":"PR","val":"72"},{"id":"RI","val":"44"},{"id":"SC","val":"45"},{"id":"SD","val":"46"},{"id":"TN","val":"47"},{"id":"TX","val":"48"},{"id":"UM","val":"74"},{"id":"UT","val":"49"},{"id":"VT","val":"50"},{"id":"VA","val":"51"},{"id":"VI","val":"78"},{"id":"WA","val":"53"},{"id":"WV","val":"54"},{"id":"WI","val":"55"},{"id":"WY","val":"56"}]')},17:function(n,e,t){},18:function(n,e,t){},25:function(n,e,t){"use strict";t.r(e);var i=t(1),a=t(0),l=t.n(a),d=t(3),r=t.n(d),c=(t(17),t.p,t(18),t(2)),o=t(11),v=t(9),s=t(28),u=t(4),f=t(10),p=["#0e3b5e","#0077c9","#43b4ff","#c0e6ff"],j={VT:[50,-8],NH:[34,2],MA:[30,-1],RI:[28,2],CT:[35,10],NJ:[34,1],DE:[33,0],MD:[47,10],DC:[49,21]},b=f.map((function(n){return Object(o.a)({fill:p[(Math.random()*(p.length-1)).toFixed()]},n)})),h=function(){var n=Object(a.useState)(""),e=Object(c.a)(n,2),t=e[0],l=e[1];return Object(i.jsx)(u.ComposableMap,{projection:"geoAlbersUsa",children:Object(i.jsx)(u.Geographies,{geography:"https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json",id:"test",children:function(n){var e=n.geographies;return Object(i.jsxs)(i.Fragment,{children:[e.map((function(n){var e=b.find((function(e){return e.val===n.id}));return Object(i.jsx)(u.Geography,{geography:n,onClick:function(){return n=e.id,void fetch("/api/doc/v1/plants/".concat(n)).then((function(n){return n.json()})).then((function(e){return Object(v.a)("Plant count :".concat(JSON.stringify(e.abs_value).concat("\t")).concat("Percentage by State: ").concat(JSON.stringify(e.percent)),"State of :".concat(n))}));var n},onMouseEnter:function(){return l(n.id)},onMouseLeave:function(){return l(null)},fill:n.id===t?"#f5821f":e.fill,stroke:"#FFFFFF"},n.rsmKey)})),e.map((function(n){var e,a=Object(s.a)(n),d=b.find((function(e){return e.val===n.id})),r=(e=function(n){var e=/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(n);return e?[parseInt(e[1],16),parseInt(e[2],16),parseInt(e[3],16)]:null}(d.fill),Math.round((299*parseInt(e[0],10)+587*parseInt(e[1],10)+114*parseInt(e[2],10))/1e3)>125?"#444444":"#FFFFFF");return Object(i.jsx)("g",{children:d&&a[0]>-160&&a[0]<-67&&(-1===Object.keys(j).indexOf(d.id)?Object(i.jsx)(u.Marker,{coordinates:a,children:Object(i.jsx)("text",{y:"2",fontSize:14,textAnchor:"middle",onMouseEnter:function(){return l(n.id)},onMouseLeave:function(){return l(null)},style:{cursor:"pointer"},fill:n.id===t?"#FFFFFF":r,children:d.id})}):Object(i.jsx)(u.Annotation,{subject:a,dx:j[d.id][0],dy:j[d.id][1],children:Object(i.jsx)("text",{x:4,fontSize:14,alignmentBaseline:"middle",onMouseEnter:function(){return l(n.id)},onMouseLeave:function(){return l(null)},style:{cursor:"pointer"},children:d.id})}))},n.rsmKey+"-name")}))]})}})})};var O=function(){return Object(i.jsx)("div",{className:"App",children:Object(i.jsx)("div",{children:Object(i.jsx)(h,{})})})},F=function(n){n&&n instanceof Function&&t.e(3).then(t.bind(null,29)).then((function(e){var t=e.getCLS,i=e.getFID,a=e.getFCP,l=e.getLCP,d=e.getTTFB;t(n),i(n),a(n),l(n),d(n)}))};r.a.render(Object(i.jsx)(l.a.StrictMode,{children:Object(i.jsx)(O,{})}),document.getElementById("root")),F()}},[[25,1,2]]]);
//# sourceMappingURL=main.83bbb8ed.chunk.js.map