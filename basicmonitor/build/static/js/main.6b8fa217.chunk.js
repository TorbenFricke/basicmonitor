(this.webpackJsonpmonitoing=this.webpackJsonpmonitoing||[]).push([[0],{14:function(e,t,a){e.exports=a(23)},21:function(e,t,a){},23:function(e,t,a){"use strict";a.r(t);var n=a(1),l=a(2),r=a(0),i=a.n(r),c=a(12),s=a.n(c),o=(a(19),a(20),a(21),a(3)),m=a(4),u=a(6),d=a(5),h=function(e){var t=e.handleClose,a=e.show,n=e.children,l=e.title;var c=Object(r.useCallback)((function(e){"Escape"===e.key&&t()}),[t]);return Object(r.useEffect)((function(){return document.addEventListener("keydown",c,!1),function(){document.removeEventListener("keydown",c,!1)}}),[c]),i.a.createElement("div",{className:"modal fade ".concat(a?"show":""),tabIndex:"-1",role:"dialog",style:{display:a?"block":"none",backgroundColor:"rgba(1,1,31,0.22)",backdropFilter:"blur(8px)",overflowY:"auto"},onClick:function(e){return function(e){e.target.classList.contains("modal")&&t()}(e)}},i.a.createElement("div",{className:"modal-dialog modal-xl",role:"document"},i.a.createElement("div",{className:"modal-content shadow"},i.a.createElement("div",{className:"modal-header bg-light"},i.a.createElement("h5",{className:"modal-title"},l),i.a.createElement("button",{type:"button",className:"close",onClick:function(){t()}},i.a.createElement("span",{"aria-hidden":"true"},"\xd7"))),i.a.createElement("div",{className:"modal-body"},n))))};function f(e){return i.a.createElement("li",{className:"list-group-item list-group-item-action ".concat(e.active?"active":""),style:{cursor:"default"},onClick:e.onClick},i.a.createElement("span",{style:{width:"48px"}},e.iconLeft),e.children,i.a.createElement("span",{className:"float-right"},e.iconRight))}function v(e){return i.a.createElement("div",{className:"form-group"},"label"in e?i.a.createElement("label",null,e.label||"label"):null,i.a.createElement("div",{className:"input-group"},i.a.createElement("select",{className:"form-control",placeholder:e.placeholder||"",onChange:e.onChange,value:e.value,name:e.name,disabled:e.disabled},e.children)))}function p(e){return i.a.createElement("div",{className:"form-group"},"label"in e?i.a.createElement("label",null,e.label||"label"):null,i.a.createElement("div",{className:"input-group"},i.a.createElement("input",{type:e.type||"text",className:"form-control",placeholder:e.placeholder||"",onChange:e.onChange,value:e.value,list:e.list||"",name:e.name,disabled:e.disabled}),"suffix"in e?i.a.createElement("div",{className:"input-group-append"},i.a.createElement("span",{className:"input-group-text"},e.suffix)):""))}function b(e){var t=Object(r.useState)(!1),a=Object(l.a)(t,2),n=a[0],c=a[1];return[i.a.createElement("li",{className:"list-group-item list-group-item-action",onClick:function(){return c(!n)},style:{cursor:"pointer",borderBottom:"none"},key:"1"},i.a.createElement("i",{className:"fas fa-chevron-right fa-sm mr-2",style:n?{transform:"rotate(90deg)"}:{}}),i.a.createElement("span",{className:"text-monospace"},e.label),i.a.createElement("span",{className:"float-right font-weight-light"},e.value)),i.a.createElement("li",{className:"list-group-item custom-collapse ".concat(n?"show":""," py-0"),key:"2"},i.a.createElement("div",{className:"py-3"},n?e.children:null))]}function g(e){var t=Object(n.a)({type:"HTML",interval:"5",name:"",url:"",retain_for:"90"},e.initialState),a=Object(r.useState)(t),c=Object(l.a)(a,2),s=c[0],o=c[1],m="editMode"in e&&e.editMode;function u(e){var t={};t[e.nativeEvent.target.name]=e.nativeEvent.target.value,o(Object(n.a)({},s,{},t))}return i.a.createElement("form",{onSubmit:function(a){a.preventDefault();var l=Object(n.a)({},s,{interval:60*s.interval,retain_for:24*s.retain_for*60*60});m?fetch("./sensors/"+s.id,{method:"put",body:JSON.stringify(l)}):fetch("./sensors",{method:"post",body:JSON.stringify(l)}).then((function(e){o(t)}));try{e.handleClose()}catch(r){}},className:"row"},i.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},i.a.createElement("h4",null,"Type"),i.a.createElement(v,{label:" ",type:"select",value:s.type,list:"form-add-sensor-types",name:"type",onChange:u,disabled:m},i.a.createElement("option",{value:"HTML"},"HTML - Grabs HTTP response from a URL"),i.a.createElement("option",{value:"CPUPercentage"},"CPUPercentage - Host system CPU usage"),i.a.createElement("option",{value:"RAMPercentage"},"RAMPercentage - Host system memory usage"),i.a.createElement("option",{value:"Uptime"},"Uptime - Host system uptime"))),i.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},i.a.createElement("h4",null,"Info"),i.a.createElement(p,{label:"Name:",name:"name",value:s.name,onChange:u}),i.a.createElement(p,{label:"Update interval:",type:"number",name:"interval",placeholder:"5",suffix:"minutes",value:s.interval,onChange:u}),i.a.createElement(p,{label:"Retain for:",type:"number",name:"retain_for",placeholder:"90",suffix:"days",value:s.retain_for,onChange:u})),i.a.createElement("div",{className:"col-lg-4"},i.a.createElement("h4",null,"Type Specific Info"),"HTML"===s.type?i.a.createElement(p,{label:"Target URL:",type:"text",name:"url",value:s.url,onChange:u}):""),i.a.createElement("div",{className:"col-lg-12"},i.a.createElement("button",{type:"submit",className:"btn btn-primary mt-2 px-4"},m?"Apply":"Create Sensor")))}var E=a(13),y=a.n(E);function N(e){if(null!==e)return(e=e.toString()).length<30?e:"".concat(e.slice(0,27),"...")}var k=new Proxy({elapsed:function(e){return"".concat(Math.round(1e3*e)," ms")},time:function(e){return new Date(1e3*e).toLocaleString()},percentage:function(e){return"".concat(Math.round(10*e)/10," %")},seconds:function(e){return"".concat(Math.round(e)," (").concat(Math.round(10*e/60/60/24)/10," days)")},url:function(e){return i.a.createElement("a",{href:decodeURIComponent(e),target:"_blank",rel:"noopener noreferrer"},decodeURIComponent(e))},interval:function(e){return"".concat(Math.round(e/60*10)/10," minutes")},retain_for:function(e){return"".concat(Math.round(e/24/60/60*10)/10," days")},expression:function(e){return i.a.createElement("div",{className:"text-monospace"},e)},broken:function(e){return e?i.a.createElement("span",{className:"fas fa-times text-danger"}):i.a.createElement("span",{className:"fas fa-check text-success"})},last_notify:function(e){return e<0?"never":"".concat(new Date(1e3*e).toLocaleString()," (").concat(y()(1e3*e).fromNow(),")")},queued_messages:function(e){return e.map((function(e,t){return i.a.createElement("div",{key:t},e)}))}},{get:function(e,t){return t in e?e[t]:N}}),O=["last_reading","last_update","kwargs","enabled","id","name"],j=new Proxy({url:"Target URL",retain_for:"Retain readings for",broken:"Working?",last_notify:"Last notified",queued_messages:"Queued messages"},{get:function(e,t){return t in e?e[t]:i.a.createElement("span",{className:"text-capitalize"},t)}});function w(e){return null==e?null:Object.keys(e).map((function(t){return i.a.createElement(b,{key:t,label:t,value:k[t](e[t])},e[t])}))}function x(e){var t=e.label,a=e.children;return i.a.createElement("div",{className:"row mb-2"},i.a.createElement("div",{className:"col-sm-4"},i.a.createElement("h5",null,t)),i.a.createElement("div",{className:"col-sm-8",style:{overflow:"hidden"}},a))}var S=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).hideModal=function(){n.setState({showModal:!1})},n.state={updating:!1,showModal:!1},n.itemLabel="Item",n.fetchUrlPath="/item",n}return Object(m.a)(a,[{key:"renderFormView",value:function(){return null}},{key:"renderSubclassed",value:function(){return null}},{key:"refresh",value:function(){var e=this,t="."+"".concat(this.fetchUrlPath,"/").concat(this.props.id,"/update");this.setState({updating:!0}),fetch(t).then((function(e){return e.json()})).then((function(t){e.setState({item:Object(n.a)({},e.item(),{last_reading:t}),updating:!1})}))}},{key:"item",value:function(){var e=this,t=this.props.globalState[this.itemLabel].find((function(t){return t.id===e.props.id}));return null==t?{}:t}},{key:"setItem",value:function(e){var t=this.props.globalState[this.itemLabel],a=t.findIndex((function(t){return t.id===e.id}));t[a]=e;var n={};n[this.itemLabel]=t,this.props.setGlobalState(n)}},{key:"update",value:function(){var e=this,t="."+"".concat(this.fetchUrlPath,"/").concat(this.props.id);fetch(t).then((function(e){return e.json()})).then((function(t){e.setItem(t)}))}},{key:"componentDidUpdate",value:function(e,t,a){this.props.id!==e.id&&null==this.item().last_reading&&this.update()}},{key:"delete",value:function(){var e="."+"".concat(this.fetchUrlPath,"/").concat(this.props.id);fetch(e,{method:"DELETE",data:this.item()})}},{key:"attributeRows",value:function(e){var t=this,a={variables:function(e){return Object.keys(e).map((function(a){var n=e[a],l=n.id;try{l=t.props.globalState.Sensor.find((function(e){return e.id===n.id})).name}catch(r){}return i.a.createElement("div",{className:"text-monospace text-large",key:a},i.a.createElement("code",{className:""},a)," = ",i.a.createElement("kbd",null,l),".",i.a.createElement("kbd",null,n.channel),"[",i.a.createElement("kbd",null,n.row),"]")}))}};if(null!=e)return Object.entries(e).map((function(e){var t=e[0],n=e[1];return null==n||""===n||O.includes(t)?null:i.a.createElement(x,{label:j[t],key:t},t in a?a[t](n):k[t](n))}))}},{key:"render",value:function(){var e=this;return i.a.createElement("div",{className:"card shadow"},this.state.showModal?i.a.createElement(h,{title:"Edit item",show:!0,handleClose:this.hideModal},this.renderFormView()):null,i.a.createElement("div",{className:"card-header bg-dark py-3"},i.a.createElement("h2",{className:"mb-0 text-white"},this.item().name||"",i.a.createElement("span",{className:"float-right"},i.a.createElement("button",{className:"btn btn-light mr-2",onClick:function(){return e.refresh()}},this.state.updating?i.a.createElement("i",{className:"spinner-border spinner-border-sm"}):i.a.createElement("i",{className:"fa fa-sync"})),i.a.createElement("button",{className:"btn btn-light mr-2",onClick:function(){return e.setState({showModal:!0})}},i.a.createElement("i",{className:"fa fa-edit"})),i.a.createElement("button",{className:"btn btn-light",onClick:function(){return e.delete()}},i.a.createElement("i",{className:"fa fa-trash text-danger"}))))),i.a.createElement("div",{className:"card-body"},this.attributeRows(this.item()),this.renderSubclassed()))}}]),a}(i.a.Component),C=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Sensor",n.fetchUrlPath="/sensors",n}return Object(m.a)(a,[{key:"renderFormView",value:function(){return i.a.createElement(g,{handleClose:this.hideModal,editMode:!0,initialState:Object(n.a)({},this.item(),{interval:this.item().interval/60,retain_for:this.item().retain_for/24/60/60,url:decodeURIComponent(this.item().url)})})}},{key:"renderSubclassed",value:function(){var e=this;return i.a.createElement("div",null,"HTML"===this.item().type?i.a.createElement("button",{className:"btn btn-sm btn-outline-primary",onClick:function(){window.open(e.item().url).document.write(e.item().last_reading.content)}},i.a.createElement("span",{className:"fa fa-external-link-alt mr-2"}),"Open HTML content of last reading in new window"):null,i.a.createElement("hr",null),i.a.createElement("h5",null,"Channels",i.a.createElement("span",{className:"text-muted font-weight-normal"}," (last reading)")),i.a.createElement("ul",{className:"list-group"},w(this.item().last_reading)))}}]),a}(S),M=a(8),_=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).hideModal=function(){n.setState({showModal:!1})},n.state={active:"",showModal:!1,filter:""},n.itemLabel="Item",n.basicEventHandlerItemPrefix="item",n.fetchUrlPath="/items",n}return Object(m.a)(a,[{key:"renderDetailView",value:function(){return null}},{key:"renderFormView",value:function(){return null}},{key:"setItems",value:function(e){var t={};t[this.itemLabel]=e,this.props.setGlobalState(t)}},{key:"items",value:function(){return null==this.props.globalState[this.itemLabel]&&(this.props.globalState[this.itemLabel]=[]),this.props.globalState[this.itemLabel]}},{key:"updateItem",value:function(e){var t=this,a="."+"".concat(this.fetchUrlPath,"/").concat(e);fetch(a).then((function(e){return e.json()})).then((function(a){var n=t.props.globalState[t.itemLabel],l=n.findIndex((function(t){return t.id===e}));n[l]=a,t.setItems(n)}))}},{key:"eventHandler",value:function(e){if(e.message===this.basicEventHandlerItemPrefix+" deleted"){var t=e.data.id,a=0,n=this.items().filter((function(e,n){return e.id===t&&(a=n),e.id!==t}));this.setItems(n),this.items().length>0&&(a=this.items().length<=a?a-1:a,this.setState({active:this.items()[a].id}))}if(e.message===this.basicEventHandlerItemPrefix+" added"&&this.setItems([].concat(Object(M.a)(this.items()),[e.data])),e.message===this.basicEventHandlerItemPrefix+" edited"&&this.updateItem(e.data.id),e.message===this.basicEventHandlerItemPrefix+" updated"){var l=e.data.id;if(this.state.active===l)this.updateItem(l);else{var r=this.items(),i=r.findIndex((function(e){return e.id===l}));r[i].last_reading&&(r[i].last_reading=null),this.setItems(r)}}}},{key:"update",value:function(){var e=this,t="."+this.fetchUrlPath;fetch(t).then((function(e){return e.json()})).then((function(t){e.setItems(t),""===e.state.active&&e.items().length>0&&e.setState({active:"id"in e.items()[0]?e.items()[0].id:""})}))}},{key:"componentDidMount",value:function(){this.update(),this.props.eventManager&&this.props.eventManager.subscribe(this)}},{key:"componentWillUnmount",value:function(){this.props.eventManager&&this.props.eventManager.unsubscribe(this)}},{key:"ItemList",value:function(e){var t=this;return null==e?null:e.map((function(e){return i.a.createElement(f,{key:e.id,onClick:function(){return t.setState({active:e.id})},active:t.state.active===e.id,iconRight:i.a.createElement("div",{className:"badge badge-light font-weight-normal"},e.type)},e.name)}))}},{key:"render",value:function(){var e=this;return i.a.createElement("div",{className:"row"},i.a.createElement("div",{className:"col-md-4 mb-3"},i.a.createElement(h,{title:"Add New ".concat(this.itemLabel),show:this.state.showModal,handleClose:this.hideModal},this.renderFormView()),i.a.createElement("ul",{className:"list-group shadow"},i.a.createElement("li",{className:"bg-light list-group-item btn btn-outline-primary text-dark py-3",style:{cursor:"pointer",borderBottomLeftRadius:0,borderBottomRightRadius:0,height:"76px"},onClick:function(){return e.setState({showModal:!0})}},i.a.createElement("span",{className:"h2 align-bottom float-left mb-0"},"New ",this.itemLabel),i.a.createElement("h2",{className:"mb-0"},i.a.createElement("span",{className:"float-right"},i.a.createElement("i",{className:"fa fa-xs fa-plus"})))),i.a.createElement("input",{className:"bg-light input-group-sm list-group-item icon-placeholder py-2",placeholder:"\uf002 Filter",value:this.state.filter,onChange:function(t){return e.setState({filter:t.target.value})}}),this.ItemList(this.items().filter((function(t){var a=e.state.filter.toLowerCase();return Object.keys(t).some((function(e){try{return t[e].toLowerCase().includes(a)}catch(n){return!1}}))}))))),i.a.createElement("div",{className:"col-md-8 mb-3"},this.renderDetailView()))}}]),a}(i.a.Component),L=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Sensor",n.basicEventHandlerItemPrefix="sensor",n.fetchUrlPath="/sensors",n}return Object(m.a)(a,[{key:"renderDetailView",value:function(){return i.a.createElement(C,{id:this.state.active,eventManager:this.props.eventManager,globalState:this.props.globalState,setGlobalState:this.props.setGlobalState})}},{key:"renderFormView",value:function(){return i.a.createElement(g,{handleClose:this.hideModal})}}]),a}(_),I=function(){function e(){Object(o.a)(this,e),this.subscriptions=[],this.listen()}return Object(m.a)(e,[{key:"subscribe",value:function(e){this.subscriptions.push(e)}},{key:"unsubscribe",value:function(e){var t=this.subscriptions.indexOf(e);delete this.subscriptions[t]}},{key:"handleEvent",value:function(e){this.subscriptions.forEach((function(t){try{t.eventHandler(e)}catch(a){console.log(a)}}))}},{key:"listen",value:function(){var e=this,t=new TextDecoder("utf-8");fetch("./events").then((function(a){var n=a.body.getReader();n.read().then((function a(l){var r=l.done,i=l.value,c=t.decode(i);try{var s=JSON.parse(c);e.handleEvent(s)}catch(o){console.log("Cannot parse JSON:\n"+c)}if(!r)return n.read().then(a);console.log("Finished event stream")}))}))}}]),e}(),P=function(e){var t=e.content,a=e.initialActive,n=e.reloadContent,c=Object(r.useState)(a),s=Object(l.a)(c,2),o=s[0],m=s[1];return i.a.createElement("div",null,i.a.createElement("nav",{className:"navbar navbar-light bg-light pb-0 mb-3"},i.a.createElement("div",{className:"container"},i.a.createElement("ul",{className:"nav nav-tabs"},Object.keys(t).map((function(e){return i.a.createElement("li",{className:"nav-item bg-light",key:e,onClick:function(){m(e)}},i.a.createElement("div",{className:"nav-link ".concat(o===e?"active":""," text-dark px-3"),style:{cursor:"pointer"}},e))}))))),i.a.createElement("div",{className:"container"},n?t[o]:i.a.createElement("div",{className:"tab-content"},Object.keys(t).map((function(e){return i.a.createElement("div",{className:"tab-pane ".concat(o===e?"active":""),key:e},t[e])})))))},U=a(10);function D(e){var t=e.onClick;return i.a.createElement("div",{className:"row mt-1"},i.a.createElement("div",{className:"pl-2",style:{width:"48px"}},i.a.createElement("button",{type:"button",className:"btn btn-sm btn-light mr-2",onClick:function(e){e.preventDefault(),null!=t&&t()}},i.a.createElement("span",{className:"fa fa-plus"}))))}function R(e){var t=e.handleRemove,a=e.value,c=e.handleChange,s=Object(r.useState)(a),o=Object(l.a)(s,2),m=o[0],u=o[1],d=Object(r.useState)([]),h=Object(l.a)(d,2),f=h[0],v=h[1],p=Object(r.useState)(0),b=Object(l.a)(p,2),g=b[0],E=b[1],y=Object(r.useState)({time:0}),N=Object(l.a)(y,2),k=N[0],O=N[1];function j(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1;E((function(t){return t+e}))}function w(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:m.row,a="".concat(".","/query/").concat(e,"?row=").concat(t);j(),fetch(a).then((function(e){return e.json()})).then((function(e){null!=e[0]&&O(e[0]),j(-1)}))}function x(e){e.preventDefault();var t=Object(n.a)({},m);t[e.nativeEvent.target.name]=e.nativeEvent.target.value,u(t),c(t),"id"===e.nativeEvent.target.name&&w(e.nativeEvent.target.value),"row"===e.nativeEvent.target.name&&w(m.id,e.nativeEvent.target.value)}return Object(r.useEffect)((function(){u(a),fetch("./sensors/").then((function(e){return e.json()})).then((function(e){v(e)})),a.id&&w(a.id)}),[a.id]),i.a.createElement("div",{className:"row py-2"},i.a.createElement("div",{className:"pl-2",style:{width:"36px"}},i.a.createElement("button",{type:"button",className:"btn btn-sm btn-light mr-2",onClick:function(e){e.preventDefault(),t()}},i.a.createElement("span",{className:"fa fa-minus"}))),i.a.createElement("div",{className:"pl-2",style:{width:"35%"}},i.a.createElement("select",{className:"form-control form-control-sm mr-2",placeholder:"Sensor",name:"id",value:m.id,onChange:x},i.a.createElement("option",{value:""}),f.map((function(e){return i.a.createElement("option",{key:e.id,value:e.id},e.name)})))),i.a.createElement("div",{className:"pl-2",style:{width:"35%"}},i.a.createElement("select",{className:"form-control form-control-sm mr-2",placeholder:"Channel",name:"channel",value:m.channel,onChange:x},Object.keys(k).map((function(e){return i.a.createElement("option",{key:e,value:e},e)})))),i.a.createElement("div",{className:"pl-2",style:{width:"20%",maxWidth:"90px"}},i.a.createElement("input",{type:"number",className:"form-control form-control-sm mr-2",placeholder:"-1",name:"row",value:m.row,onChange:x})),i.a.createElement("div",{className:"col-12 mt-1"}),i.a.createElement("div",{className:"pl-2",style:{width:"36px"}}," "),i.a.createElement("div",{className:"pl-2",style:{width:"70%"}},i.a.createElement("div",{className:"input-group input-group-sm"},i.a.createElement("input",{type:"text",className:"form-control",placeholder:"Variable name (can be used in Expression)",name:"variable",value:m.variable,onChange:x}),i.a.createElement("div",{className:"input-group-append w-50"},i.a.createElement("div",{className:"input-group-text w-100 bg-light"},i.a.createElement("span",{className:"text-truncate text-nowrap text-monospace"},"= ",k[m.channel]))))),i.a.createElement("div",{className:"pl-2",style:{width:"20%",maxWidth:"90px"}},i.a.createElement("button",{type:"button",className:"btn btn-sm btn-light w-100",onClick:function(e){e.preventDefault(),w(m.id)}},g>0?i.a.createElement("i",{className:"spinner-border spinner-border-sm"}):i.a.createElement("i",{className:"fa fa-sync"}))))}var T={channel:"time",row:-1,id:"",variable:"t"},A={name:"New Trigger",retain_for:7776e3,expression:"",variables:{t:T},action_ids:[],message:""};function H(e){var t=e.editMode,a=void 0!==t&&t,c=e.handleClose,s=e.initialState,o=void 0===s?A:s,m=o.variables,u=Object(U.a)(o,["variables"]),d=Object(r.useState)(u),h=Object(l.a)(d,2),f=h[0],v=h[1],p=Object.keys(m).map((function(e){return Object(n.a)({},m[e],{variable:e})})),b=Object(r.useState)(p),g=Object(l.a)(b,2),E=g[0],y=g[1],N=Object(r.useState)(""),k=Object(l.a)(N,2),O=k[0],j=k[1],w=Object(r.useState)(!1),x=Object(l.a)(w,2),S=x[0],C=x[1];function _(e){e.preventDefault();var t=e.nativeEvent.target,a=Object(n.a)({},f),l=t.value;t.dataset.factor&&null!=l&&(l*=t.dataset.factor),a[t.name]=l,v(a)}function L(){var e={};return E.map((function(t){var a=t.variable,n=Object(U.a)(t,["variable"]);return e[a]=n,null})),e}function I(e,t){var a={expression:e,variables:t};fetch("./evaluate",{method:"post",body:JSON.stringify(a)}).then((function(e){return e.json()})).then((function(e){j(e.message),C(e.error)}))}return Object(r.useEffect)((function(){""!==o.expression&&I(o.expression,L())}),[o.expression]),i.a.createElement("form",{onSubmit:function(e){e.preventDefault();var t=Object(n.a)({},f,{variables:L()});a?fetch("./triggers/"+f.id,{method:"put",body:JSON.stringify(t)}):fetch("./triggers",{method:"post",body:JSON.stringify(t)}).then((function(){j(""),C(""),y(p),v(u)}));try{c()}catch(l){}}},i.a.createElement("div",{className:"row"},i.a.createElement("div",{className:"col-md-6"},i.a.createElement("label",null,"Name:"),i.a.createElement("input",{type:"text",className:"form-control mb-2",name:"name",value:f.name,onChange:_})),i.a.createElement("div",{className:"col-md-6"},i.a.createElement("label",null,"Retain history for:"),i.a.createElement("div",{className:"input-group mb-2"},i.a.createElement("input",{type:"number",className:"form-control",name:"retain_for","data-factor":86400,value:f.retain_for/86400,onChange:_}),i.a.createElement("div",{className:"input-group-append"},i.a.createElement("span",{className:"input-group-text"},"days"))))),i.a.createElement("hr",null),i.a.createElement("h4",null,"Variables"),i.a.createElement("div",{className:"row"},i.a.createElement("div",{style:{width:"36px"},className:"px-2"}," "),i.a.createElement("div",{style:{width:"35%"},className:"px-2"},"Sensor:"),i.a.createElement("div",{style:{width:"35%"},className:"px-2"},"Channel:"),i.a.createElement("div",{style:{width:"20%",maxWidth:"90px"},className:"px-2"},"Index:")),E.map((function(e,t){return i.a.createElement(R,{key:t,value:E[t],handleRemove:function(){y(E.filter((function(e,a){return a!==t})))},handleChange:function(e){var a=Object(M.a)(E);a[t]=e,y(a)}})})),i.a.createElement(D,{onClick:function(){y([].concat(Object(M.a)(E),[E.length>0?E.slice(-1)[0]:T]))}}),i.a.createElement("hr",null),i.a.createElement("h4",null,"Expression"),i.a.createElement("input",{type:"text",className:"form-control text-monospace mb-1",placeholder:'A == 3 or "substing" in long_string',onChange:function(e){e.preventDefault(),v(Object(n.a)({},f,{expression:e.nativeEvent.target.value})),I(e.nativeEvent.target.value,L())},value:f.expression}),""===f.expression?null:i.a.createElement("div",{className:"alert ".concat(S?"alert-danger":[!0,!1].includes(O)?"alert-success":"alert-warning")},O.toString()),i.a.createElement("h4",null,"Action"),i.a.createElement("input",{type:"text",className:"form-control",placeholder:"asdad-asdasd-adsads-dasdsa-adsasd",onChange:function(e){e.preventDefault(),v(Object(n.a)({},f,{action_ids:[e.nativeEvent.target.value]}))},value:f.action_ids[0]}),i.a.createElement("input",{type:"text",className:"form-control",placeholder:"Message",onChange:function(e){e.preventDefault(),v(Object(n.a)({},f,{message:e.nativeEvent.target.value}))},value:f.message}),i.a.createElement("div",{className:"col-lg-12"},i.a.createElement("button",{type:"submit",className:"btn btn-primary mt-2 px-4"},a?"Apply":"Create Trigger")))}var V=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Trigger",n.fetchUrlPath="/triggers",n}return Object(m.a)(a,[{key:"renderFormView",value:function(){return i.a.createElement(H,{handleClose:this.hideModal,editMode:!0,initialState:this.item()})}},{key:"renderSubclassed",value:function(){return i.a.createElement("div",null,i.a.createElement("hr",null),i.a.createElement("h5",null,"Last Check"),i.a.createElement("ul",{className:"list-group"},w(this.item().last_reading)))}}]),a}(S),F=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Trigger",n.basicEventHandlerItemPrefix="trigger",n.fetchUrlPath="/triggers",n}return Object(m.a)(a,[{key:"renderDetailView",value:function(){return i.a.createElement(V,{id:this.state.active,eventManager:this.props.eventManager,globalState:this.props.globalState,setGlobalState:this.props.setGlobalState})}},{key:"renderFormView",value:function(){return i.a.createElement(H,{handleClose:this.hideModal})}}]),a}(_);function G(e){var t=Object(n.a)({type:"DebugAction",interval:"5",name:"",url:"",retain_for:"90"},e.initialState),a=Object(r.useState)(t),c=Object(l.a)(a,2),s=c[0],o=c[1],m="editMode"in e&&e.editMode;function u(e){var t={};t[e.nativeEvent.target.name]=e.nativeEvent.target.value,o(Object(n.a)({},s,{},t))}return i.a.createElement("form",{onSubmit:function(a){a.preventDefault();var l=Object(n.a)({},s,{interval:60*s.interval,retain_for:24*s.retain_for*60*60});m?fetch("./actions/"+s.id,{method:"put",body:JSON.stringify(l)}):fetch("./actions",{method:"post",body:JSON.stringify(l)}).then((function(){o(t)}));try{e.handleClose()}catch(r){}},className:"row"},i.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},i.a.createElement("h4",null,"Type"),i.a.createElement(v,{label:" ",type:"select",value:s.type,list:"form-add-sensor-types",name:"type",onChange:u,disabled:m},i.a.createElement("option",{value:"DebugAction"},"DebugAction - Debug print statement"),i.a.createElement("option",{value:"PushoverAction"},"Pushover - Sends a push notification"))),i.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},i.a.createElement("h4",null,"Info"),i.a.createElement(p,{label:"Name:",name:"name",value:s.name,onChange:u}),i.a.createElement(p,{label:"Cooldown:",type:"cooldown",name:"interval",placeholder:"5",suffix:"minutes",value:s.interval,onChange:u}),i.a.createElement(p,{label:"Retain for:",type:"number",name:"retain_for",placeholder:"90",suffix:"days",value:s.retain_for,onChange:u})),i.a.createElement("div",{className:"col-lg-4"},i.a.createElement("h4",null,"Type Specific Info"),"PushoverAction"===s.type?[i.a.createElement(p,{label:"Api token:",type:"text",name:"api_token",value:s.api_token,key:"api_token",onChange:u}),i.a.createElement(p,{label:"User key:",type:"text",name:"user_key",value:s.user_key,key:"user_key",onChange:u}),i.a.createElement(p,{label:"Device:",type:"text",name:"device",value:s.device,key:"device",onChange:u})]:""),i.a.createElement("div",{className:"col-lg-12"},i.a.createElement("button",{type:"submit",className:"btn btn-primary mt-2 px-4"},m?"Apply":"Create Action"),i.a.createElement("button",{type:"button",className:"btn btn-secondary mt-2 px-4 ml-2",onClick:function(){var e="".concat(s.name,": Test message :)");fetch("./actions/"+s.id+"/update",{method:"post",body:JSON.stringify({message:e,force_send:!0})})}},"Send Test Notification")))}var J=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Action",n.fetchUrlPath="/actions",n}return Object(m.a)(a,[{key:"renderFormView",value:function(){return i.a.createElement(G,{handleClose:this.hideModal,editMode:!0,initialState:this.item()})}},{key:"renderSubclassed",value:function(){return i.a.createElement("div",null,i.a.createElement("hr",null),i.a.createElement("h5",null,"Last Message"),i.a.createElement("ul",{className:"list-group"},w(this.item().last_reading)))}}]),a}(S),W=function(e){Object(u.a)(a,e);var t=Object(d.a)(a);function a(e){var n;return Object(o.a)(this,a),(n=t.call(this,e)).itemLabel="Action",n.basicEventHandlerItemPrefix="action",n.fetchUrlPath="/actions",n}return Object(m.a)(a,[{key:"renderDetailView",value:function(){return i.a.createElement(J,{id:this.state.active,eventManager:this.props.eventManager,globalState:this.props.globalState,setGlobalState:this.props.setGlobalState})}},{key:"renderFormView",value:function(){return i.a.createElement(G,{handleClose:this.hideModal})}}]),a}(_),B=new I;function q(){var e=Object(r.useState)({}),t=Object(l.a)(e,2),a=t[0],c=t[1];function s(e){c(Object(n.a)({},a,{},e))}return i.a.createElement(P,{initialActive:"Sensors",content:{Sensors:i.a.createElement(L,{eventManager:B,globalState:a,setGlobalState:s}),Triggers:i.a.createElement(F,{eventManager:B,globalState:a,setGlobalState:s}),Actions:i.a.createElement(W,{eventManager:B,globalState:a,setGlobalState:s})}})}s.a.render(i.a.createElement(i.a.StrictMode,null,i.a.createElement(q,null)),document.getElementById("root"))}},[[14,1,2]]]);
//# sourceMappingURL=main.6b8fa217.chunk.js.map