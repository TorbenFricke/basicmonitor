(this.webpackJsonpmonitoing=this.webpackJsonpmonitoing||[]).push([[0],{14:function(e,t,a){e.exports=a(25)},21:function(e,t,a){},25:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),i=a(12),l=a.n(i),s=(a(19),a(20),a(21),a(2)),c=a(1),o=a(3),m=a(4),u=a(13),d=a(7),f=a(8),v="http://127.0.0.1:5000",b=function(){function e(t){var a=t.eventManager,n=t.itemLabel,r=void 0===n?"Item":n,i=t.eventHandlerItemPrefix,l=void 0===i?"item":i,s=t.fetchUrlPath,c=void 0===s?"/items":s;Object(d.a)(this,e),this.itemLabel=r,this.stateKey=r+"State",this.eventHandlerItemPrefix=l,this.fetchUrlPath=c,this.globalState={},this.setGlobalState=function(e){Object(u.a)(e)},this.eventManager=a,a.subscribe(this)}return Object(f.a)(e,[{key:"initializeGlobalState",value:function(e,t){this.globalState=e,this.setGlobalState=t}},{key:"eventHandler",value:function(e){if(e.message===this.eventHandlerItemPrefix+" deleted"){var t=e.data.id,a=0,n=this.items().filter((function(e,n){return e.id===t&&(a=n),e.id!==t}));this.setItems(n),this.items().length>0&&(a=this.items().length<=a?a-1:a,this.setState({active:this.items()[a].id}))}if(e.message===this.eventHandlerItemPrefix+" added"&&this.setItems([].concat(Object(m.a)(this.items()),[e.data])),e.message===this.eventHandlerItemPrefix+" edited"&&this.updateItem(e.data.id),e.message===this.eventHandlerItemPrefix+" updated"){var r=e.data.id;if(this.setActiveState({lastUpdateEvent:Date.now()/1e3},r),this.state().active===r)this.updateItem(r);else{var i=this.items(),l=i.findIndex((function(e){return e.id===r}));i[l].last_reading&&(i[l].last_reading=null),null!=e.data.reading&&(i[l].last_reading=e.data.reading),this.setItems(i)}}}},{key:"state",value:function(){return null==this.globalState[this.stateKey]&&(this.globalState[this.stateKey]={}),this.globalState[this.stateKey]}},{key:"setState",value:function(e){var t=this.state(),a={};a[this.stateKey]=Object(c.a)({},t,{},e),this.setGlobalState(a)}},{key:"activeState",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:this.state().active;return null==e?{}:null==this.globalState[e]?(this.globalState[e]={},{}):this.globalState[e]}},{key:"setActiveState",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:this.state().active;if(null!=t){var a={};a[t]=Object(c.a)({},this.activeState(t),{},e),this.setGlobalState(a)}}},{key:"items",value:function(){return null==this.globalState[this.itemLabel]?(this.globalState[this.itemLabel]=[],this.updateItems(),[]):this.globalState[this.itemLabel]}},{key:"setItems",value:function(e){var t={};t[this.itemLabel]=e,this.setGlobalState(t)}},{key:"item",value:function(){var e=this,t=this.items().find((function(t){return t.id===e.state().active}));return null==t&&(t={}),t}},{key:"setItem",value:function(e){var t=this.items(),a=t.findIndex((function(t){return t.id===e.id}));t[a]=e,this.setItems(t)}},{key:"updateItem",value:function(e){var t=this;if(null!=e){var a=v+"".concat(this.fetchUrlPath,"/").concat(e);fetch(a).then((function(e){return e.json()})).then((function(e){t.setItem(e)}))}}},{key:"updateItems",value:function(){var e=this,t=v+this.fetchUrlPath;fetch(t).then((function(e){return e.json()})).then((function(t){e.setItems(t),""===e.state().active&&e.items().length>0&&e.setState({active:"id"in e.items()[0]?e.items()[0].id:"form"})})).catch((function(){""===e.state().active&&e.setState({active:"form"})}))}},{key:"refreshItem",value:function(e){var t=this;if(null!=e){var a=v+"".concat(this.fetchUrlPath,"/").concat(e,"/update");return fetch(a).then((function(e){return e.json()})).then((function(e){t.setItem(Object(c.a)({},t.item(),{last_reading:e}))}))}}},{key:"deleteItem",value:function(e){if(null!=e){var t=v+"".concat(this.fetchUrlPath,"/").concat(e);return fetch(t,{method:"DELETE",data:{}})}}},{key:"addItem",value:function(e){var t=v+this.fetchUrlPath;return console.log(JSON.stringify(e)),fetch(t,{method:"POST",body:JSON.stringify(e)})}}]),e}();function h(e,t){return function(a){a.preventDefault();var n=a.nativeEvent.target,r=Object(c.a)({},e),i=n.value;n.dataset.factor&&null!=i&&(i*=n.dataset.factor),r[n.name]=i,t(r)}}function g(e){return r.a.createElement("div",{className:"form-group"},"label"in e?r.a.createElement("label",null,e.label||"label"):null,r.a.createElement("div",{className:"input-group"},r.a.createElement("select",{className:"form-control",placeholder:e.placeholder||"",onChange:e.onChange,value:e.value,name:e.name,disabled:e.disabled},e.children)))}function p(e){return r.a.createElement("div",{className:"form-group"},"label"in e?r.a.createElement("label",null,e.label||"label"):null,r.a.createElement("div",{className:"input-group"},r.a.createElement("input",{type:e.type||"text",className:"form-control",placeholder:e.placeholder||"",onChange:h(e.state,e.setState),value:null!=e.factor?e.state[e.name]/e.factor:e.state[e.name],list:e.list||"",name:e.name,disabled:e.disabled,"data-factor":e.factor}),"suffix"in e?r.a.createElement("div",{className:"input-group-append"},r.a.createElement("span",{className:"input-group-text"},e.suffix)):""))}function E(e){var t=e.handleClose,a=void 0===t?function(){}:t,n=e.editMode,i=void 0!==n&&n,l=e.label,s=void 0===l?"":l;return r.a.createElement("div",{className:"col-12"},r.a.createElement("button",{type:"submit",className:"btn btn-primary mt-2 px-4"},i?"Apply":"Create ".concat(s)),i?r.a.createElement("button",{type:"button",className:"btn btn-secondary mt-2 ml-2 px-4",onClick:a},"Cancel"):"")}function y(e,t,a,n,r,i,l){return function(s){s.preventDefault(),e?fetch(v+"/"+l+"/"+a.id,{method:"put",body:JSON.stringify(a)}):fetch(v+"/"+l,{method:"post",body:JSON.stringify(a)}).then((function(e){return n(r),e.json()})).then((function(e){i(e.id)})),t()}}var N={type:"HTML",interval:300,name:"",url:"",retain_for:7776e3};function k(e){var t=e.onClick;return r.a.createElement("button",{type:"button",className:"btn btn-sm btn-light",onClick:function(e){e.preventDefault(),null!=t&&t()}},r.a.createElement("span",{className:"fa fa-plus"}))}function S(e){var t=e.handleRemove,a=e.state,i=e.handleChange,l=e.sensorManager,o=Object(n.useState)(0),m=Object(s.a)(o,2),u=m[0],d=m[1],f=Object(n.useState)({time:0}),b=Object(s.a)(f,2),h=b[0],g=b[1];function p(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1;d((function(t){return t+e}))}function E(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:a.row,n="".concat(v,"/query/").concat(e,"?row=").concat(t);p(),fetch(n).then((function(e){return e.json()})).then((function(e){null!=e[0]&&g(e[0]),p(-1)}))}function y(e){e.preventDefault();var t=Object(c.a)({},a);t[e.nativeEvent.target.name]=e.nativeEvent.target.value,i(t),"id"===e.nativeEvent.target.name&&E(e.nativeEvent.target.value),"row"===e.nativeEvent.target.name&&E(a.id,e.nativeEvent.target.value)}return Object(n.useEffect)((function(){a.id&&E(a.id)}),[a.id]),[r.a.createElement("div",{key:"remove-button"},r.a.createElement("button",{type:"button",className:"btn btn-sm btn-light",onClick:function(e){e.preventDefault(),t()}},r.a.createElement("span",{className:"fa fa-minus"}))),r.a.createElement("div",{key:"sensor"},r.a.createElement("select",{className:"form-control form-control-sm mr-2",placeholder:"Sensor",name:"id",value:a.id,onChange:y},r.a.createElement("option",{value:""}),l.items().map((function(e){return r.a.createElement("option",{key:e.id,value:e.id},e.name)})))),r.a.createElement("div",{key:"channel"},r.a.createElement("select",{className:"form-control form-control-sm mr-2",placeholder:"Channel",name:"channel",value:a.channel,onChange:y},Object.keys(h).map((function(e){return r.a.createElement("option",{key:e,value:e},e)})))),r.a.createElement("div",{key:"index"},r.a.createElement("input",{type:"number",className:"form-control form-control-sm mr-2",placeholder:"-1",name:"row",value:a.row,onChange:y})),r.a.createElement("div",{key:"placeholder"}),r.a.createElement("div",{key:"variable"},r.a.createElement("input",{type:"text",className:"form-control form-control-sm",placeholder:"Variable name (can be used in Expression)",name:"variable",value:a.variable,onChange:y})),r.a.createElement("div",{key:"current-value"},r.a.createElement("div",{className:"form-control form-control-sm bg-light text-truncate text-nowrap text-monospace"},h[a.channel])),r.a.createElement("div",{key:"update-button",className:"mb-2"},r.a.createElement("button",{type:"button",className:"btn btn-sm btn-light w-100",onClick:function(e){e.preventDefault(),E(a.id)}},u>0?r.a.createElement("i",{className:"spinner-border spinner-border-sm"}):r.a.createElement("i",{className:"fa fa-sync"})))]}function x(e){var t=e.actions,a=e.setActions,n=e.actionManager;return r.a.createElement("div",null,r.a.createElement("ul",{className:"list-group"},t.map((function(e,i){return r.a.createElement("div",{className:"list-group-item p-0",key:i},r.a.createElement("div",{className:"input-group"},r.a.createElement("div",{className:"input-group-prepend"},r.a.createElement("button",{className:"btn btn-light",type:"button",onClick:function(){return a(t.filter((function(e,t){return i!==t})))}},r.a.createElement("i",{className:"fas fa-minus"}))),r.a.createElement("select",{className:"border-0 custom-select",value:e,onChange:function(e){var n=Object(m.a)(t);n[i]=e.nativeEvent.target.value,a(n)}},n.items().map((function(e,t){return r.a.createElement("option",{value:e.id,key:t},e.name)})))))}))),r.a.createElement("div",{className:"btn btn-light mt-1",onClick:function(){a([].concat(Object(m.a)(t),[n.items().length>0?n.items()[0].id:""]))}},r.a.createElement("i",{className:"fa fa-plus"})))}var O={channel:"time",row:-1,id:"",variable:"A"},j={name:"New Trigger",retain_for:7776e3,expression:"",variables:[O],action_ids:[],message:"",expressionMessage:"",expressionError:!1};function M(e){var t=e.variables,a=e.setVariables,n=e.sensorManager;function i(){if(0===t.length)return O;var e=Object(c.a)({},t.slice(-1)[0]);e.variable=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:5;function t(e){return e.charAt(Math.floor(Math.random()*e.length))}for(var a="aeoui",n="qwrtzipsdfghjklyxcvbnm",r="",i=0;i<e;i++)r+=t(i%2===0?n:a);return r}(3),a([].concat(Object(m.a)(t),[e]))}return[].concat(Object(m.a)(t.map((function(e,i){return r.a.createElement(S,{sensorManager:n,key:i,state:e,handleRemove:function(){a(t.filter((function(e,t){return t!==i})))},handleChange:function(e){var n=Object(m.a)(t);n[i]=e,a(n)}})}))),[r.a.createElement(k,{key:"add-button",onClick:function(){i()}})])}var w={type:"DebugAction",interval:300,name:"",url:"",retain_for:7776e3};function C(e){return r.a.createElement("li",{className:"list-group-item list-group-item-transparent list-group-item-action \n            ".concat(e.active?"active":""," ")+e.className,style:{cursor:"default"},onClick:e.onClick},r.a.createElement("span",{style:{width:"48px"}},e.iconLeft),e.children,r.a.createElement("span",{className:"float-right"},e.iconRight))}function I(e){var t=Object(n.useState)(!1),a=Object(s.a)(t,2),i=a[0],l=a[1];return[r.a.createElement("li",{className:"list-group-item list-group-item-action",onClick:function(){return l(!i)},style:{cursor:"pointer",borderBottom:"none"},key:"1"},r.a.createElement("i",{className:"fas fa-chevron-right fa-sm mr-2",style:i?{transform:"rotate(90deg)"}:{}}),r.a.createElement("span",{className:"text-monospace"},e.label),r.a.createElement("span",{className:"float-right font-weight-light"},e.value)),r.a.createElement("li",{className:"list-group-item custom-collapse ".concat(i?"show":""," py-0"),key:"2"},r.a.createElement("div",{className:"py-3"},i?e.children:null))]}var _=a(9),P=a.n(_);function A(e){if(null!==e)return(e=e.toString()).length<40?e:"".concat(e.slice(0,37),"...")}function L(e){return"".concat(Math.round(e/60*10)/10," minute").concat(60!==e?"s":"")}var U=new Proxy({elapsed:function(e){return"".concat(Math.round(1e3*e)," ms")},time:function(e){return new Date(1e3*e).toLocaleString()},percentage:function(e){return"".concat(Math.round(10*e)/10," %")},seconds:function(e){return"".concat(Math.round(e)," (").concat(Math.round(10*e/60/60/24)/10," days)")},url:function(e){return r.a.createElement("a",{href:decodeURIComponent(e),target:"_blank",rel:"noopener noreferrer"},decodeURIComponent(e))},interval:L,cooldown:L,type:function(e){return r.a.createElement("kbd",{className:"bg-light text-dark"},e)},retain_for:function(e){return"".concat(Math.round(e/24/60/60*10)/10," days")},expression:function(e){return r.a.createElement("div",{className:"text-monospace"},e)},broken:function(e){return e?r.a.createElement("span",{className:"fas fa-times text-danger"}):r.a.createElement("span",{className:"fas fa-check text-success"})},last_notify:function(e){return e<0?"never":"".concat(new Date(1e3*e).toLocaleString()," (").concat(P()(1e3*e).fromNow(),")")},queued_messages:function(e){return e.map((function(e,t){return r.a.createElement("div",{key:t},e)}))},action_ids:function(e){return e.map((function(e,t){return r.a.createElement("kbd",{key:t},e)}))}},{get:function(e,t){return t in e?e[t]:A}}),H=["last_reading","last_update","kwargs","enabled","id","name"],R=new Proxy({url:"Target URL",retain_for:"Retain readings for",last_notify:"Last notified",queued_messages:"Queued messages",api_token:"Api token",user_key:"User key",action_ids:"Actions"},{get:function(e,t){return t in e?e[t]:r.a.createElement("span",{className:"text-capitalize"},t)}});function T(e){return null==e?r.a.createElement("i",{className:"spinner-grow spinner-grow-lg text-secondary mx-auto my-4"}):Object.keys(e).map((function(t){return r.a.createElement(I,{key:t,label:t,value:U[t](e[t])},e[t])}))}function D(e){var t=e.label,a=e.children;return r.a.createElement("li",{className:"list-group-item px-0"},r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"col-3 h5 text-secondary m-0"},t),r.a.createElement("div",{className:"col-9"},a)))}function V(e){var t=e.showSpinner,a=e.className,n=Object(o.a)(e,["showSpinner","className"]);return r.a.createElement("button",Object.assign({className:"btn btn-light mr-2 "+a},n),t?r.a.createElement("i",{className:"spinner-border spinner-border-sm"}):n.children)}function F(e){var t=e.children,a=e.onClick,i=e.sureClass,l=void 0===i?"border-primary":i,c=Object(o.a)(e,["children","onClick","sureClass"]),m=Object(n.useState)(!1),u=Object(s.a)(m,2),d=u[0],f=u[1];return r.a.createElement(V,Object.assign({onClick:function(e){d&&a(e),!d&&setTimeout((function(){f(!1)}),3e3),f(!d)},className:d?l:""},c),t)}function G(e){var t=e.stateManager,a=Object(n.useState)(!1),i=Object(s.a)(a,2),l=i[0],c=i[1],m=Object(n.useState)(!1),u=Object(s.a)(m,2),d=u[0],f=u[1],v=t.state().active;return r.a.createElement("div",{className:"header-buttons float-right my-auto"},r.a.createElement(V,{showSpinner:l,onClick:function(){l||(c(!0),t.refreshItem(v).then((function(){c(!1)})).catch((function(){c(!1)})))},disabled:t.activeState().editMode},r.a.createElement("i",{className:"fa fa-sync"})),r.a.createElement(F,{showSpinner:d,onClick:function(){return function(){var e=t.item(),a=(e.last_reading,e.last_update,e.id,Object(o.a)(e,["last_reading","last_update","id"]));a.name+=" (copy)",f(!0),t.addItem(a).then((function(){f(!1)})).catch((function(){f(!1)}))}()},disabled:t.activeState().editMode},r.a.createElement("i",{className:"fa fa-copy"})),r.a.createElement(V,{onClick:function(){return t.setActiveState({editMode:!t.activeState().editMode})}},r.a.createElement("i",{className:"fa fa-edit"})),r.a.createElement(F,{sureClass:"border-danger",onClick:function(){return t.deleteItem(v)}},r.a.createElement("i",{className:"fa fa-trash text-danger"})))}function J(e){var t=e.stateManager,a=e.FormView,i=e.children,l=Object(o.a)(e,["stateManager","FormView","children"]),s=t.state().active;function m(e){t.setActiveState({formState:Object(c.a)({},t.activeState().formState,{},e)})}return Object(n.useEffect)((function(){null==t.item().last_reading&&t.updateItem(s)}),[s]),!0===t.activeState().editMode?[r.a.createElement(G,{stateManager:t,key:"Buttons"}),r.a.createElement("div",{className:"main px-3"},r.a.createElement(a,Object.assign({key:"form",state:Object(c.a)({},t.item(),{},t.activeState().formState),setState:m,editMode:!0,handleClose:function(){t.setActiveState({editMode:!1,formState:{}})}},l)))]:[r.a.createElement(G,{stateManager:t,key:"ButtonsDetail"}),r.a.createElement("div",{className:"main px-3",key:"detail"},function(e){var t={variables:function(e){return e.map((function(e,t){var a=e.id;try{a=l.sensorManager.items().find((function(t){return t.id===e.id})).name}catch(n){}return r.a.createElement("div",{className:"text-monospace text-large",key:t},r.a.createElement("code",{className:""},e.variable)," = ",r.a.createElement("kbd",null,a),".",r.a.createElement("kbd",null,e.channel),"[",r.a.createElement("kbd",null,e.row),"]")}))}};return r.a.createElement("ul",{className:"list-group list-group-flush"},Object.entries(e).map((function(e){var a=e[0],n=e[1];return null!=n&&""!==n&&!H.includes(a)&&r.a.createElement(D,{label:R[a],key:a},a in t?t[a](n):U[a](n))})))}(t.item()),i)]}var z=function(){function e(){Object(d.a)(this,e),this.subscriptions=[],this.listen()}return Object(f.a)(e,[{key:"subscribe",value:function(e){this.subscriptions.push(e)}},{key:"unsubscribe",value:function(e){var t=this.subscriptions.indexOf(e);delete this.subscriptions[t]}},{key:"handleEvent",value:function(e){this.subscriptions.forEach((function(t){try{t.eventHandler(e)}catch(a){console.log(a)}}))}},{key:"listen",value:function(){var e=this;new EventSource(v+"/events").onmessage=function(t){try{var a=JSON.parse(t.data);e.handleEvent(a)}catch(n){}}}}]),e}();function K(e){var t=e.stateManager,a=e.item;function n(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"light";return r.a.createElement("div",{className:"badge font-weight-normal badge-"+n},e,t.activeState(a.id).editMode&&r.a.createElement("i",{className:"fas fa-edit ml-2"}))}return"trigger"===t.eventHandlerItemPrefix?null==a.last_reading?null:null==a.last_reading.state?n("broken","warning"):a.last_reading.state?n("triggering","primary"):n("not triggering"):n(a.type)}function q(e){var t=e.stateManager,a=e.item,i=Object(n.useState)("initial"),l=Object(s.a)(i,2),c=l[0],o=l[1];return Object(n.useEffect)((function(){"initial"!==c?(o("flash"),setTimeout((function(){return o("")}),1e3)):o("")}),[t.activeState(a.id).lastUpdateEvent]),r.a.createElement(C,{className:c,onClick:function(){return t.setState({active:a.id})},active:t.state().active===a.id,iconRight:r.a.createElement(K,{stateManager:t,item:a})},a.name)}function B(e){var t,a=e.stateManager;return Object(n.useEffect)((function(){null==a.state().active&&null!=a.items()[0]&&a.setState({active:a.items()[0].id})}),[a.state().active,a.items()]),[r.a.createElement("li",{className:"list-group-item list-group-item-transparent list-group-item-action \n        ".concat("form"===a.state().active?"active":""),key:"button",style:{cursor:"default"},onClick:function(){return a.setState({active:"form"})}},r.a.createElement("h3",{className:"mb-1"},"New ",a.itemLabel,r.a.createElement("span",{className:"float-right"},r.a.createElement("i",{className:"fa fa-xs fa-plus"})))),r.a.createElement("input",{className:"input-group-sm list-group-item list-group-item-transparent w-100 icon-placeholder py-2",placeholder:"\uf002 Filter",value:a.state().filter,key:"Filter",onChange:function(e){return a.setState({filter:e.target.value})}}),(t=a.items().filter((function(e){var t=(a.state().filter||"").toLowerCase();return Object.keys(e).some((function(a){try{return e[a].toLowerCase().includes(t)}catch(n){return!1}}))})),null==t?null:t.map((function(e){return r.a.createElement(q,{stateManager:a,item:e,key:e.id})})))]}var Q=a(10),W=a.n(Q);a(23),r.a.memo((function(e){var t={responsive:!0,hoverMode:"index",stacked:!1,title:{display:!0,text:e.title||""},scales:{yAxes:[{type:"linear",display:!0,position:"left",id:"y-axis-1"},{type:"linear",display:!1,position:"right",id:"y-axis-2",gridLines:{drawOnChartArea:!1}}],xAxes:[{type:"time"}]},plugins:{zoom:{pan:{enabled:!1},zoom:{enabled:!0,drag:!0,mode:"x",speed:1,threshold:.1}}}},a=!1;Object(n.useEffect)((function(){a||(!function(){var a=W.a.Line(i.current,{data:(n=e.data,{labels:n.map((function(e,t){return t})),datasets:[{label:"My First dataset",borderColor:"#fa9121",backgroundColor:"#fa912111",fill:!0,data:n,hidden:!0},{label:"My Second dataset",borderColor:"#21af61",backgroundColor:"#21af61",fill:!1,data:n.map((function(e){return 1.2*e}))}]}),options:t});var n;i.current.ondblclick=function(){a.resetZoom()}}(),a=!0)}),[e.data]);var i=r.a.createRef();return r.a.createElement("canvas",{ref:i})}));function Z(e){return r.a.createElement("div",{className:"sidebar bg-night shadow-sm"},r.a.createElement("ul",{className:"list-group list-group-flush"},e.children))}function X(e){var t=e.FormView,a=e.stateManager,n=e.children,i=Object(o.a)(e,["FormView","stateManager","children"]);function l(e){a.setState({formState:Object(c.a)({},a.state().formState,{},e)})}return[r.a.createElement("div",{className:"header h2 text-dark my-auto px-3",key:"header"},a.item().name||"Create New"),"form"===a.state().active?r.a.createElement("div",{className:"main px-3"},r.a.createElement(t,Object.assign({key:"FormView",state:a.state().formState,setState:l,setActive:function(e){a.setState({active:e})}},i))):r.a.createElement(J,Object.assign({key:"DetailView",stateManager:a,FormView:t},i),n)]}var Y=new z,$={sensors:{manager:new b({eventManager:Y,itemLabel:"Sensor",eventHandlerItemPrefix:"sensor",fetchUrlPath:"/sensors"}),form:function(e){var t=e.editMode,a=void 0!==t&&t,n=e.state,i=void 0===n?N:n,l=e.setState,s=e.handleClose,c=void 0===s?function(){}:s,m=e.setActive,u=void 0===m?function(e){}:m,d=(Object(o.a)(e,["editMode","state","setState","handleClose","setActive"]),y(a,c,i,l,N,u,"sensors")),f={state:i,setState:l};return r.a.createElement("form",{onSubmit:d,className:"row"},r.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},r.a.createElement("h4",null,"Type"),r.a.createElement(g,{label:" ",type:"select",value:i.type,list:"form-add-sensor-types",name:"type",onChange:h(i,l),disabled:a},r.a.createElement("option",{value:"HTML"},"HTML - Grabs HTTP response from a URL"),r.a.createElement("option",{value:"CPUPercentage"},"CPUPercentage - Host system CPU usage"),r.a.createElement("option",{value:"RAMPercentage"},"RAMPercentage - Host system memory usage"),r.a.createElement("option",{value:"Uptime"},"Uptime - Host system uptime"))),r.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},r.a.createElement("h4",null,"Info"),r.a.createElement(p,Object.assign({},f,{label:"Name:",name:"name"})),r.a.createElement(p,Object.assign({},f,{label:"Update interval:",name:"interval",type:"number",suffix:"minutes",factor:60})),r.a.createElement(p,Object.assign({},f,{label:"Retain for:",name:"retain_for",type:"number",suffix:"days",factor:86400}))),r.a.createElement("div",{className:"col-lg-4"},r.a.createElement("h4",null,"Type Specific Info"),"HTML"===i.type?r.a.createElement(p,Object.assign({label:"Target URL:",name:"url"},f)):""),r.a.createElement(E,{handleClose:c,editMode:a,label:"Sensor"}))},moreInfo:function(e){var t=e.stateManager,a=t.state().activeDetailView||0,n=function(e){t.setState({activeDetailView:e})};return r.a.createElement("div",{className:"mt-3"},"HTML"===t.item().type&&r.a.createElement("button",{className:"btn btn-sm btn-outline-primary mb-2",onClick:function(){window.open(t.item().url).document.write(t.item().last_reading.content)}},r.a.createElement("span",{className:"fa fa-external-link-alt mr-2"}),"Open HTML content of last reading in new window"),r.a.createElement("div",{className:"btn-group mb-2 w-100"},r.a.createElement("button",{type:"button",className:"btn btn-light ".concat(0===a?"active":""),onClick:function(){n(0)}},r.a.createElement("span",{className:"fas fa-database mr-2"}),"Raw Data"),r.a.createElement("button",{type:"button",className:"btn btn-light ".concat(1===a?"active":""),onClick:function(){n(1)}},r.a.createElement("span",{className:"fas fa-chart-area mr-2"}),"History")),0===a&&r.a.createElement("div",null,r.a.createElement("ul",{className:"list-group"},T(t.item().last_reading)),r.a.createElement("span",{className:"text-muted font-weight-normal"},"data from last reading")),1===a&&r.a.createElement("div",null,"Work in progress"))}},triggers:{manager:new b({eventManager:Y,itemLabel:"Trigger",eventHandlerItemPrefix:"trigger",fetchUrlPath:"/triggers"}),form:function(e){var t=e.editMode,a=void 0!==t&&t,i=e.state,l=void 0===i?j:i,s=e.setState,o=e.handleClose,m=void 0===o?function(){}:o,u=e.setActive,d=void 0===u?function(){}:u,f=e.actionManager,b=e.sensorManager;Object(n.useEffect)((function(){""!==l.expression&&function(e,t){var a={expression:e,variables:t};fetch(v+"/evaluate",{method:"post",body:JSON.stringify(a)}).then((function(e){return e.json()})).then((function(e){s(Object(c.a)({},l,{expressionMessage:e.message,expressionError:e.error}))}))}(l.expression,l.variables)}),[l.expression,l.variables]);var h=y(a,m,l,s,j,d,"triggers"),g={state:l,setState:s};return r.a.createElement("form",{onSubmit:h},r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"col-md-6"},r.a.createElement(p,Object.assign({label:"Name:",name:"name"},g))),r.a.createElement("div",{className:"col-md-6"},r.a.createElement(p,Object.assign({label:"Retain history for:",type:"number",name:"retain_for",suffix:"days",factor:86400},g)))),r.a.createElement("hr",null),r.a.createElement("h4",null,"Variables"),r.a.createElement("div",{className:"variable-input-grid"},r.a.createElement("div",null),r.a.createElement("div",null,"Sensor:"),r.a.createElement("div",null,"Channel:"),r.a.createElement("div",null,"Index:"),r.a.createElement(M,{sensorManager:b,variables:l.variables,setVariables:function(e){s(Object(c.a)({},l,{variables:e}))}})),r.a.createElement("hr",null),r.a.createElement("h4",null,"Expression"),r.a.createElement(p,Object.assign({type:"text",className:"form-control text-monospace mb-1",placeholder:'A == 3 or "substing" in long_string',name:"expression"},g)),""===l.expression?null:r.a.createElement("div",{className:"alert ".concat(l.expressionError?"alert-danger":[!0,!1].includes(l.expressionMessage)?"alert-success":"alert-warning")},"expressionMessage"in l&&l.expressionMessage.toString()),r.a.createElement("h4",null,"Action"),r.a.createElement(x,{actionManager:f,actions:l.action_ids,setActions:function(e){s(Object(c.a)({},l,{action_ids:e}))}}),r.a.createElement(p,Object.assign({label:"Message:",name:"message"},g)),r.a.createElement(E,{label:"Trigger",handleClose:m,editMode:a}))},moreInfo:function(e){var t=e.stateManager;return r.a.createElement("div",{className:"mt-3"},r.a.createElement("h4",null,"Last Check"),r.a.createElement("ul",{className:"list-group"},T(t.item().last_reading)))}},actions:{manager:new b({eventManager:Y,itemLabel:"Action",eventHandlerItemPrefix:"action",fetchUrlPath:"/actions"}),form:function(e){var t=e.editMode,a=void 0!==t&&t,n=e.state,i=void 0===n?w:n,l=e.setState,s=e.handleClose,c=void 0===s?function(){}:s,m=e.setActive,u=void 0===m?function(e){}:m,d=(Object(o.a)(e,["editMode","state","setState","handleClose","setActive"]),y(a,c,i,l,w,u,"actions")),f={state:i,setState:l};return r.a.createElement("form",{onSubmit:d,className:"row"},r.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},r.a.createElement("h4",null,"Type"),r.a.createElement(g,{label:" ",type:"select",value:i.type,list:"form-add-sensor-types",name:"type",onChange:h(i,l),disabled:a},r.a.createElement("option",{value:"DebugAction"},"DebugAction - Debug print statement"),r.a.createElement("option",{value:"PushoverAction"},"Pushover - Sends a push notification"))),r.a.createElement("div",{className:"col-lg-4",style:{borderRight:"1px solid #dee2e6"}},r.a.createElement("h4",null,"Info"),r.a.createElement(p,Object.assign({label:"Name:",name:"name"},f)),r.a.createElement(p,Object.assign({label:"Cooldown:",name:"cooldown",type:"number",suffix:"minutes",factor:60},f)),r.a.createElement(p,Object.assign({label:"Retain for:",name:"retain_for",type:"number",suffix:"days",factor:86400},f))),r.a.createElement("div",{className:"col-lg-4"},r.a.createElement("h4",null,"Type Specific Info"),"PushoverAction"===i.type?[r.a.createElement(p,Object.assign({label:"Api token:",name:"api_token",key:"api_token"},f)),r.a.createElement(p,Object.assign({label:"User key:",name:"user_key",key:"user_key"},f)),r.a.createElement(p,Object.assign({label:"Device:",name:"device",key:"device"},f))]:""),r.a.createElement(E,{editMode:a,handleClose:c,label:"Action"}))},moreInfo:function(e){var t=e.stateManager;return r.a.createElement("div",{className:"mt-3"},r.a.createElement("h4",null,"Last Message"),r.a.createElement("ul",{className:"list-group"},T(t.item().last_reading)))}}};function ee(){var e=Object(n.useState)({}),t=Object(s.a)(e,2),a=t[0],i=t[1];function l(e){i(Object(c.a)({},a,{},e))}Object.keys($).map((function(e){$[e].manager.initializeGlobalState(a,l)}));var o=Object(n.useState)("sensors"),m=Object(s.a)(o,2),u=m[0],d=m[1];var f=$[u].manager,v=$[u].moreInfo;return r.a.createElement("div",{className:"main-grid"},r.a.createElement(Z,null,r.a.createElement("div",{className:"btn-group w-100 px-1 py-2"},function(){var e={sensors:r.a.createElement("span",{className:"fas fa-ruler-vertical mr-2"}),triggers:r.a.createElement("span",{className:"fas fa-calculator mr-2"}),actions:r.a.createElement("span",{className:"fas fa-bullseye mr-2"})};return Object.keys($).map((function(t){return r.a.createElement("button",{type:"button",className:"btn btn-outline-transparent text-white px-1 text-capitalize \n                        ".concat(u===t?"active":""),key:t,onClick:function(){d(t)}},e[t],r.a.createElement("br",null),t)}))}()),r.a.createElement(B,{stateManager:f})),r.a.createElement(X,{stateManager:f,FormView:$[u].form,sensorManager:$.sensors.manager,actionManager:$.actions.manager},r.a.createElement(v,{stateManager:f})))}l.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(ee,null)),document.getElementById("root"))}},[[14,1,2]]]);
//# sourceMappingURL=main.84183d30.chunk.js.map