/*! For license information please see 8ef413e96faeca8ea66b.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[132],{105:function(e,t,n){"use strict";n(2);var i=n(87),a=n(58),o=n(4),r=n(0),s=n(3);Object(o.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[a.a],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){i.a.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=Object(r.b)(this).observeNodes(function(e){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(Object(r.b)(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var e;if(this.allowedPattern)e=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":e=/[0-9.,e-]/}return e},_bindValueChanged:function(e,t){t&&(void 0===e?t.value=null:e!==t.value&&(this.inputElement.value=e),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:e}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(e){var t=8==e.keyCode||9==e.keyCode||13==e.keyCode||27==e.keyCode,n=19==e.keyCode||20==e.keyCode||45==e.keyCode||46==e.keyCode||144==e.keyCode||145==e.keyCode||e.keyCode>32&&e.keyCode<41||e.keyCode>111&&e.keyCode<124;return!(t||0==e.charCode&&n)},_onKeypress:function(e){if(this.allowedPattern||"number"===this.inputElement.type){var t=this._patternRegExp;if(t&&!(e.metaKey||e.ctrlKey||e.altKey)){this._patternAlreadyChecked=!0;var n=String.fromCharCode(e.charCode);this._isPrintable(e)&&!t.test(n)&&(e.preventDefault(),this._announceInvalidCharacter("Invalid character "+n+" not entered."))}}},_checkPatternValidity:function(){var e=this._patternRegExp;if(!e)return!0;for(var t=0;t<this.inputElement.value.length;t++)if(!e.test(this.inputElement.value[t]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var e=this.inputElement.checkValidity();return e&&(this.required&&""===this.bindValue?e=!1:this.hasValidator()&&(e=a.a.validate.call(this,this.bindValue))),this.invalid=!e,this.fire("iron-input-validate"),e},_announceInvalidCharacter:function(e){this.fire("iron-announce",{text:e})},_computeValue:function(e){return e}})},111:function(e,t,n){"use strict";n.d(t,"a",function(){return o});n(2);var i=n(51),a=n(32);const o=[i.a,a.a,{hostAttributes:{role:"option",tabindex:"0"}}]},132:function(e,t,n){"use strict";n(40),n(54),n(41),n(50);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(i.content)},167:function(e,t,n){"use strict";n(2);const i=n(3).a`
/* Most common used flex styles*/
<dom-module id="iron-flex">
  <template>
    <style>
      .layout.horizontal,
      .layout.vertical {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.inline {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      }

      .layout.horizontal {
        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      }

      .layout.vertical {
        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      }

      .layout.wrap {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      .layout.no-wrap {
        -ms-flex-wrap: nowrap;
        -webkit-flex-wrap: nowrap;
        flex-wrap: nowrap;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .flex {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-auto {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      }

      .flex-none {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      }
    </style>
  </template>
</dom-module>
/* Basic flexbox reverse styles */
<dom-module id="iron-flex-reverse">
  <template>
    <style>
      .layout.horizontal-reverse,
      .layout.vertical-reverse {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.horizontal-reverse {
        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      }

      .layout.vertical-reverse {
        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      }

      .layout.wrap-reverse {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      }
    </style>
  </template>
</dom-module>
/* Flexbox alignment */
<dom-module id="iron-flex-alignment">
  <template>
    <style>
      /**
       * Alignment in cross axis.
       */
      .layout.start {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.end {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      }

      .layout.baseline {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      }

      /**
       * Alignment in main axis.
       */
      .layout.start-justified {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .layout.end-justified {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      }

      .layout.around-justified {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      }

      .layout.justified {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      }

      /**
       * Self alignment.
       */
      .self-start {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      }

      .self-center {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      }

      .self-end {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      }

      .self-stretch {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      }

      .self-baseline {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      }

      /**
       * multi-line alignment in main axis.
       */
      .layout.start-aligned {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      }

      .layout.end-aligned {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      }

      .layout.center-aligned {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      }

      .layout.between-aligned {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      }

      .layout.around-aligned {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      }
    </style>
  </template>
</dom-module>
/* Non-flexbox positioning helper styles */
<dom-module id="iron-flex-factors">
  <template>
    <style>
      .flex,
      .flex-1 {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-2 {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      }

      .flex-3 {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      }

      .flex-4 {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      }

      .flex-5 {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      }

      .flex-6 {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      }

      .flex-7 {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      }

      .flex-8 {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      }

      .flex-9 {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      }

      .flex-10 {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      }

      .flex-11 {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      }

      .flex-12 {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      }
    </style>
  </template>
</dom-module>
<dom-module id="iron-positioning">
  <template>
    <style>
      .block {
        display: block;
      }

      [hidden] {
        display: none !important;
      }

      .invisible {
        visibility: hidden !important;
      }

      .relative {
        position: relative;
      }

      .fit {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      }

      body.fullbleed {
        margin: 0;
        height: 100vh;
      }

      .scroll {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      }

      /* fixed position */
      .fixed-bottom,
      .fixed-left,
      .fixed-right,
      .fixed-top {
        position: fixed;
      }

      .fixed-top {
        top: 0;
        left: 0;
        right: 0;
      }

      .fixed-right {
        top: 0;
        right: 0;
        bottom: 0;
      }

      .fixed-bottom {
        right: 0;
        bottom: 0;
        left: 0;
      }

      .fixed-left {
        top: 0;
        bottom: 0;
        left: 0;
      }
    </style>
  </template>
</dom-module>
`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},172:function(e,t,n){"use strict";n(2),n(40),n(41),n(50);var i=n(4),a=n(3);Object(i.a)({_template:a.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},176:function(e,t,n){"use strict";n(2),n(54),n(141);var i=n(4),a=n(3),o=n(116);const r=a.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>
  </div>
`;r.setAttribute("strip-whitespace",""),Object(i.a)({_template:r,is:"paper-spinner",behaviors:[o.a]})},179:function(e,t,n){"use strict";n(2),n(40),n(50),n(132);var i=n(4),a=n(3),o=n(111);Object(i.a)({_template:a.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[o.a]})},190:function(e,t,n){"use strict";var i={},a=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,o="[^\\s]+",r=/\[([^]*?)\]/gm,s=function(){};function l(e,t){for(var n=[],i=0,a=e.length;i<a;i++)n.push(e[i].substr(0,t));return n}function d(e){return function(t,n,i){var a=i[e].indexOf(n.charAt(0).toUpperCase()+n.substr(1).toLowerCase());~a&&(t.month=a)}}function c(e,t){for(e=String(e),t=t||2;e.length<t;)e="0"+e;return e}var u=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],h=["January","February","March","April","May","June","July","August","September","October","November","December"],p=l(h,3),m=l(u,3);i.i18n={dayNamesShort:m,dayNames:u,monthNamesShort:p,monthNames:h,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10)*e%10]}};var f={D:function(e){return e.getDate()},DD:function(e){return c(e.getDate())},Do:function(e,t){return t.DoFn(e.getDate())},d:function(e){return e.getDay()},dd:function(e){return c(e.getDay())},ddd:function(e,t){return t.dayNamesShort[e.getDay()]},dddd:function(e,t){return t.dayNames[e.getDay()]},M:function(e){return e.getMonth()+1},MM:function(e){return c(e.getMonth()+1)},MMM:function(e,t){return t.monthNamesShort[e.getMonth()]},MMMM:function(e,t){return t.monthNames[e.getMonth()]},YY:function(e){return c(String(e.getFullYear()),4).substr(2)},YYYY:function(e){return c(e.getFullYear(),4)},h:function(e){return e.getHours()%12||12},hh:function(e){return c(e.getHours()%12||12)},H:function(e){return e.getHours()},HH:function(e){return c(e.getHours())},m:function(e){return e.getMinutes()},mm:function(e){return c(e.getMinutes())},s:function(e){return e.getSeconds()},ss:function(e){return c(e.getSeconds())},S:function(e){return Math.round(e.getMilliseconds()/100)},SS:function(e){return c(Math.round(e.getMilliseconds()/10),2)},SSS:function(e){return c(e.getMilliseconds(),3)},a:function(e,t){return e.getHours()<12?t.amPm[0]:t.amPm[1]},A:function(e,t){return e.getHours()<12?t.amPm[0].toUpperCase():t.amPm[1].toUpperCase()},ZZ:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+c(100*Math.floor(Math.abs(t)/60)+Math.abs(t)%60,4)}},v={D:["\\d\\d?",function(e,t){e.day=t}],Do:["\\d\\d?"+o,function(e,t){e.day=parseInt(t,10)}],M:["\\d\\d?",function(e,t){e.month=t-1}],YY:["\\d\\d?",function(e,t){var n=+(""+(new Date).getFullYear()).substr(0,2);e.year=""+(t>68?n-1:n)+t}],h:["\\d\\d?",function(e,t){e.hour=t}],m:["\\d\\d?",function(e,t){e.minute=t}],s:["\\d\\d?",function(e,t){e.second=t}],YYYY:["\\d{4}",function(e,t){e.year=t}],S:["\\d",function(e,t){e.millisecond=100*t}],SS:["\\d{2}",function(e,t){e.millisecond=10*t}],SSS:["\\d{3}",function(e,t){e.millisecond=t}],d:["\\d\\d?",s],ddd:[o,s],MMM:[o,d("monthNamesShort")],MMMM:[o,d("monthNames")],a:[o,function(e,t,n){var i=t.toLowerCase();i===n.amPm[0]?e.isPm=!1:i===n.amPm[1]&&(e.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(e,t){var n,i=(t+"").match(/([+-]|\d\d)/gi);i&&(n=60*i[1]+parseInt(i[2],10),e.timezoneOffset="+"===i[0]?n:-n)}]};v.dd=v.d,v.dddd=v.ddd,v.DD=v.D,v.mm=v.m,v.hh=v.H=v.HH=v.h,v.MM=v.M,v.ss=v.s,v.A=v.a,i.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},i.format=function(e,t,n){var o=n||i.i18n;if("number"==typeof e&&(e=new Date(e)),"[object Date]"!==Object.prototype.toString.call(e)||isNaN(e.getTime()))throw new Error("Invalid Date in fecha.format");t=i.masks[t]||t||i.masks.default;var s=[];return(t=(t=t.replace(r,function(e,t){return s.push(t),"??"})).replace(a,function(t){return t in f?f[t](e,o):t.slice(1,t.length-1)})).replace(/\?\?/g,function(){return s.shift()})},i.parse=function(e,t,n){var o=n||i.i18n;if("string"!=typeof t)throw new Error("Invalid format in fecha.parse");if(t=i.masks[t]||t,e.length>1e3)return null;var r,s={},l=[],d=(r=t,r.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(a,function(e){if(v[e]){var t=v[e];return l.push(t[1]),"("+t[0]+")"}return e}),c=e.match(new RegExp(d,"i"));if(!c)return null;for(var u=1;u<c.length;u++)l[u-1](s,c[u],o);var h,p=new Date;return!0===s.isPm&&null!=s.hour&&12!=+s.hour?s.hour=+s.hour+12:!1===s.isPm&&12==+s.hour&&(s.hour=0),null!=s.timezoneOffset?(s.minute=+(s.minute||0)-+s.timezoneOffset,h=new Date(Date.UTC(s.year||p.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0))):h=new Date(s.year||p.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0),h},t.a=i},324:function(e,t,n){"use strict";n(211),n(207),n(340);var i=n(3);const a=i.a`<dom-module id="lumo-date-picker-overlay" theme-for="vaadin-date-picker-overlay">
  <template>
    <style include="lumo-menu-overlay">
      [part="overlay"] {
        /*
        Width:
            date cell widths
          + month calendar side padding
          + year scroller width
        */
        width:
          calc(
              var(--lumo-size-m) * 7
            + var(--lumo-space-xs) * 2
            + 57px
          );
        height: 100%;
        max-height: calc(var(--lumo-size-m) * 14);
        overflow: hidden;
        -webkit-tap-highlight-color: transparent;
      }

      [part="content"] {
        padding: 0;
        height: 100%;
        overflow: hidden;
        -webkit-mask-image: none;
        mask-image: none;
      }

      @media (max-width: 420px), (max-height: 420px) {
        [part="overlay"] {
          width: 100vw;
          height: 70vh;
          max-height: 70vh;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(a.content);n(217),n(216),n(223);const o=document.createElement("template");o.innerHTML='<dom-module id="lumo-button" theme-for="vaadin-button">\n  <template>\n    <style>\n      :host {\n        /* Sizing */\n        --lumo-button-size: var(--lumo-size-m);\n        min-width: calc(var(--lumo-button-size) * 2);\n        height: var(--lumo-button-size);\n        padding: 0 calc(var(--lumo-button-size) / 3 + var(--lumo-border-radius) / 2);\n        margin: var(--lumo-space-xs) 0;\n        box-sizing: border-box;\n        /* Style */\n        font-family: var(--lumo-font-family);\n        font-size: var(--lumo-font-size-m);\n        font-weight: 500;\n        color: var(--lumo-primary-text-color);\n        background-color: var(--lumo-contrast-5pct);\n        border-radius: var(--lumo-border-radius);\n        cursor: default;\n        -webkit-tap-highlight-color: transparent;\n        -webkit-font-smoothing: antialiased;\n        -moz-osx-font-smoothing: grayscale;\n      }\n\n      /* Set only for the internal parts so we don’t affect the host vertical alignment */\n      [part="label"],\n      [part="prefix"],\n      [part="suffix"] {\n        line-height: var(--lumo-line-height-xs);\n      }\n\n      [part="label"] {\n        padding: calc(var(--lumo-button-size) / 6) 0;\n      }\n\n      :host([theme~="small"]) {\n        font-size: var(--lumo-font-size-s);\n        --lumo-button-size: var(--lumo-size-s);\n      }\n\n      :host([theme~="large"]) {\n        font-size: var(--lumo-font-size-l);\n        --lumo-button-size: var(--lumo-size-l);\n      }\n\n      /* This needs to be the last selector for it to take priority */\n      :host([disabled][disabled]) {\n        pointer-events: none;\n        color: var(--lumo-disabled-text-color);\n        background-color: var(--lumo-contrast-5pct);\n      }\n\n      /* For interaction states */\n      :host::before,\n      :host::after {\n        content: "";\n        /* We rely on the host always being relative */\n        position: absolute;\n        z-index: 1;\n        top: 0;\n        right: 0;\n        bottom: 0;\n        left: 0;\n        background-color: currentColor;\n        border-radius: inherit;\n        opacity: 0;\n        transition: opacity 0.2s;\n        pointer-events: none;\n      }\n\n      /* Hover */\n\n      :host(:hover)::before {\n        opacity: 0.05;\n      }\n\n      /* Disable hover for touch devices */\n      @media (pointer: coarse) {\n        :host(:not([active]):hover)::before {\n          opacity: 0;\n        }\n      }\n\n      /* Active */\n\n      :host::after {\n        transition: opacity 1.4s, transform 0.1s;\n        filter: blur(8px);\n      }\n\n      :host([active])::before {\n        opacity: 0.1;\n        transition-duration: 0s;\n      }\n\n      :host([active])::after {\n        opacity: 0.1;\n        transition-duration: 0s, 0s;\n        transform: scale(0);\n      }\n\n      /* Keyboard focus */\n\n      :host([focus-ring]) {\n        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);\n      }\n\n      /* Types (primary, tertiary, tertiary-inline */\n\n      :host([theme~="tertiary"]),\n      :host([theme~="tertiary-inline"]) {\n        background-color: transparent !important;\n        transition: opacity 0.2s;\n        min-width: 0;\n      }\n\n      :host([theme~="tertiary"])::before,\n      :host([theme~="tertiary-inline"])::before {\n        display: none;\n      }\n\n      :host([theme~="tertiary"]) {\n        padding: 0 calc(var(--lumo-button-size) / 6);\n      }\n\n      @media (hover: hover) {\n        :host([theme*="tertiary"]:not([active]):hover) {\n          opacity: 0.8;\n        }\n      }\n\n      :host([theme~="tertiary"][active]),\n      :host([theme~="tertiary-inline"][active]) {\n        opacity: 0.5;\n        transition-duration: 0s;\n      }\n\n      :host([theme~="tertiary-inline"]) {\n        margin: 0;\n        height: auto;\n        padding: 0;\n        line-height: inherit;\n        font-size: inherit;\n      }\n\n      :host([theme~="tertiary-inline"]) [part="label"] {\n        padding: 0;\n        line-height: inherit;\n      }\n\n      :host([theme~="primary"]) {\n        background-color: var(--lumo-primary-color);\n        color: var(--lumo-primary-contrast-color);\n        font-weight: 600;\n        min-width: calc(var(--lumo-button-size) * 2.5);\n      }\n\n      :host([theme~="primary"]:hover)::before {\n        opacity: 0.1;\n      }\n\n      :host([theme~="primary"][active])::before {\n        background-color: var(--lumo-shade-20pct);\n      }\n\n      @media (pointer: coarse) {\n        :host([theme~="primary"][active])::before {\n          background-color: var(--lumo-shade-60pct);\n        }\n\n        :host([theme~="primary"]:not([active]):hover)::before {\n          opacity: 0;\n        }\n      }\n\n      :host([theme~="primary"][active])::after {\n        opacity: 0.2;\n      }\n\n      /* Colors (success, error, contrast) */\n\n      :host([theme~="success"]) {\n        color: var(--lumo-success-text-color);\n      }\n\n      :host([theme~="success"][theme~="primary"]) {\n        background-color: var(--lumo-success-color);\n        color: var(--lumo-success-contrast-color);\n      }\n\n      :host([theme~="error"]) {\n        color: var(--lumo-error-text-color);\n      }\n\n      :host([theme~="error"][theme~="primary"]) {\n        background-color: var(--lumo-error-color);\n        color: var(--lumo-error-contrast-color);\n      }\n\n      :host([theme~="contrast"]) {\n        color: var(--lumo-contrast);\n      }\n\n      :host([theme~="contrast"][theme~="primary"]) {\n        background-color: var(--lumo-contrast);\n        color: var(--lumo-base-color);\n      }\n\n      /* Icons */\n\n      [part] ::slotted(iron-icon) {\n        display: inline-block;\n        width: var(--lumo-icon-size-m);\n        height: var(--lumo-icon-size-m);\n      }\n\n      /* Vaadin icons are based on a 16x16 grid (unlike Lumo and Material icons with 24x24), so they look too big by default */\n      [part] ::slotted(iron-icon[icon^="vaadin:"]) {\n        padding: 0.25em;\n        box-sizing: border-box !important;\n      }\n\n      [part="prefix"] {\n        margin-left: -0.25em;\n        margin-right: 0.25em;\n      }\n\n      [part="suffix"] {\n        margin-left: 0.25em;\n        margin-right: -0.25em;\n      }\n\n      /* Icon-only */\n\n      :host([theme~="icon"]) {\n        min-width: var(--lumo-button-size);\n        padding-left: calc(var(--lumo-button-size) / 4);\n        padding-right: calc(var(--lumo-button-size) / 4);\n      }\n\n      :host([theme~="icon"]) [part="prefix"],\n      :host([theme~="icon"]) [part="suffix"] {\n        margin-left: 0;\n        margin-right: 0;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(o.content);var r=n(20),s=n(45),l=n(204);const d=e=>(class extends((e=>(class extends e{static get properties(){var e={tabindex:{type:Number,value:0,reflectToAttribute:!0,observer:"_tabindexChanged"}};return window.ShadyDOM&&(e.tabIndex=e.tabindex),e}}))(e)){static get properties(){return{autofocus:{type:Boolean},_previousTabIndex:{type:Number},disabled:{type:Boolean,observer:"_disabledChanged",reflectToAttribute:!0},_isShiftTabbing:{type:Boolean}}}ready(){this.addEventListener("focusin",e=>{e.composedPath()[0]===this?this._focus(e):-1===e.composedPath().indexOf(this.focusElement)||this.disabled||this._setFocused(!0)}),this.addEventListener("focusout",e=>this._setFocused(!1)),super.ready();const e=e=>{e.composed||e.target.dispatchEvent(new CustomEvent(e.type,{bubbles:!0,composed:!0,cancelable:!1}))};this.shadowRoot.addEventListener("focusin",e),this.shadowRoot.addEventListener("focusout",e),this.addEventListener("keydown",e=>{!e.defaultPrevented&&e.shiftKey&&9===e.keyCode&&(this._isShiftTabbing=!0,HTMLElement.prototype.focus.apply(this),this._setFocused(!1),setTimeout(()=>this._isShiftTabbing=!1,0))}),!this.autofocus||this.focused||this.disabled||window.requestAnimationFrame(()=>{this._focus(),this._setFocused(!0),this.setAttribute("focus-ring","")}),this._boundKeydownListener=this._bodyKeydownListener.bind(this),this._boundKeyupListener=this._bodyKeyupListener.bind(this)}connectedCallback(){super.connectedCallback(),document.body.addEventListener("keydown",this._boundKeydownListener,!0),document.body.addEventListener("keyup",this._boundKeyupListener,!0)}disconnectedCallback(){super.disconnectedCallback(),document.body.removeEventListener("keydown",this._boundKeydownListener,!0),document.body.removeEventListener("keyup",this._boundKeyupListener,!0),this.hasAttribute("focused")&&this._setFocused(!1)}_setFocused(e){e?this.setAttribute("focused",""):this.removeAttribute("focused"),e&&this._tabPressed?this.setAttribute("focus-ring",""):this.removeAttribute("focus-ring")}_bodyKeydownListener(e){this._tabPressed=9===e.keyCode}_bodyKeyupListener(){this._tabPressed=!1}get focusElement(){return window.console.warn(`Please implement the 'focusElement' property in <${this.localName}>`),this}_focus(e){this._isShiftTabbing||(this.focusElement.focus(),this._setFocused(!0))}focus(){this.disabled||(this.focusElement.focus(),this._setFocused(!0))}blur(){this.focusElement.blur(),this._setFocused(!1)}_disabledChanged(e){this.focusElement.disabled=e,e?(this.blur(),this._previousTabIndex=this.tabindex,this.tabindex=-1,this.setAttribute("aria-disabled","true")):(void 0!==this._previousTabIndex&&(this.tabindex=this._previousTabIndex),this.removeAttribute("aria-disabled"))}_tabindexChanged(e){void 0!==e&&(this.focusElement.tabIndex=e),this.disabled&&this.tabindex&&(-1!==this.tabindex&&(this._previousTabIndex=this.tabindex),this.tabindex=e=void 0),window.ShadyDOM&&this.setProperties({tabIndex:e,tabindex:e})}});var c=n(11),u=n(19),h=n(24);const p=/\/\*\*\s+vaadin-dev-mode:start([\s\S]*)vaadin-dev-mode:end\s+\*\*\//i;function m(e,t){if("function"!=typeof e)return;const n=p.exec(e.toString());if(n)try{e=new Function(n[1])}catch(e){console.log("vaadin-development-mode-detector: uncommentAndRun() failed",e)}return e(t)}window.Vaadin=window.Vaadin||{};const f=function(e,t){if(window.Vaadin.developmentMode)return m(e,t)};function v(){}void 0===window.Vaadin.developmentMode&&(window.Vaadin.developmentMode=function(){try{return localStorage.getItem("vaadin.developmentmode.force")||["localhost","127.0.0.1"].indexOf(window.location.hostname)>=0&&!m(function(){return!0})&&!function(){if(window.Vaadin&&window.Vaadin.Flow&&window.Vaadin.Flow.clients){const e=Object.keys(window.Vaadin.Flow.clients).map(e=>window.Vaadin.Flow.clients[e]).filter(e=>e.productionMode);if(e.length>0)return!0}return!1}()}catch(e){return!1}}());const A=function(){return f(v)};let b;window.Vaadin||(window.Vaadin={}),window.Vaadin.registrations=window.Vaadin.registrations||[],window.Vaadin.developmentModeCallback=window.Vaadin.developmentModeCallback||{},window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]=function(){A&&A()};const y=e=>(class extends e{static _finalizeClass(){super._finalizeClass(),this.is&&(window.Vaadin.registrations.push(this),window.Vaadin.developmentModeCallback&&(b=u.a.debounce(b,c.b,()=>{window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]()}),Object(h.a)(b)))}ready(){super.ready(),null===document.doctype&&console.warn('Vaadin components require the "standards mode" declaration. Please add <!DOCTYPE html> to the HTML document.')}});var g=n(33);class _ extends(y(d(Object(l.a)(Object(s.a)(r.a))))){static get template(){return i.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        outline: none;
        white-space: nowrap;
      }

      :host([hidden]) {
        display: none !important;
      }

      /* Ensure the button is always aligned on the baseline */
      .vaadin-button-container::before {
        content: "\\2003";
        display: inline-block;
        width: 0;
      }

      .vaadin-button-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        height: 100%;
        min-height: inherit;
        text-shadow: inherit;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      [part="prefix"],
      [part="suffix"] {
        flex: none;
      }

      [part="label"] {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      #button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: inherit;
      }
    </style>
    <div class="vaadin-button-container">
      <div part="prefix">
        <slot name="prefix"></slot>
      </div>
      <div part="label">
        <slot></slot>
      </div>
      <div part="suffix">
        <slot name="suffix"></slot>
      </div>
    </div>
    <button id="button" type="button"></button>
`}static get is(){return"vaadin-button"}static get version(){return"2.1.0"}ready(){super.ready(),this.setAttribute("role","button"),this.$.button.setAttribute("role","presentation"),this._addActiveListeners()}disconnectedCallback(){super.disconnectedCallback(),this.hasAttribute("active")&&this.removeAttribute("active")}_addActiveListeners(){Object(g.b)(this,"down",()=>!this.disabled&&this.setAttribute("active","")),Object(g.b)(this,"up",()=>this.removeAttribute("active")),this.addEventListener("keydown",e=>!this.disabled&&[13,32].indexOf(e.keyCode)>=0&&this.setAttribute("active","")),this.addEventListener("keyup",()=>this.removeAttribute("active")),this.addEventListener("blur",()=>this.removeAttribute("active"))}get focusElement(){return this.$.button}}customElements.define(_.is,_);const w=i.a`<dom-module id="lumo-date-picker-overlay-content" theme-for="vaadin-date-picker-overlay-content">
  <template>
    <style>
      :host {
        position: relative;
        background-color: transparent;
        /* Background for the year scroller, placed here as we are using a mask image on the actual years part */
        background-image: linear-gradient(var(--lumo-shade-5pct), var(--lumo-shade-5pct));
        background-size: 57px 100%;
        background-position: top right;
        background-repeat: no-repeat;
        cursor: default;
      }

      /* Month scroller */

      [part="months"] {
        /* Month calendar height:
              header height + margin-bottom
            + weekdays height + margin-bottom
            + date cell heights
            + small margin between month calendars
        */
        --vaadin-infinite-scroller-item-height:
          calc(
              var(--lumo-font-size-l) + var(--lumo-space-m)
            + var(--lumo-font-size-xs) + var(--lumo-space-s)
            + var(--lumo-size-m) * 6
            + var(--lumo-space-s)
          );
        --vaadin-infinite-scroller-buffer-offset: 20%;
        -webkit-mask-image: linear-gradient(transparent, #000 10%, #000 85%, transparent);
        mask-image: linear-gradient(transparent, #000 10%, #000 85%, transparent);
        position: relative;
        margin-right: 57px;
      }

      /* Year scroller */

      [part="years"] {
        /* TODO get rid of fixed magic number */
        --vaadin-infinite-scroller-buffer-width: 97px;
        width: 57px;
        height: auto;
        top: 0;
        bottom: 0;
        font-size: var(--lumo-font-size-s);
        box-shadow: inset 2px 0 4px 0 var(--lumo-shade-5pct);
        -webkit-mask-image: linear-gradient(transparent, #000 35%, #000 65%, transparent);
        mask-image: linear-gradient(transparent, #000 35%, #000 65%, transparent);
      }

      [part="year-number"],
      [part="year-separator"] {
        opacity: 0.5;
        transition: 0.2s opacity;
      }

      [part="years"]:hover [part="year-number"],
      [part="years"]:hover [part="year-separator"] {
        opacity: 1;
      }

      /* TODO unsupported selector */
      #scrollers {
        position: static;
        display: block;
      }

      /* TODO unsupported selector, should fix this in vaadin-date-picker that it adapts to the
       * width of the year scroller */
      #scrollers[desktop] [part="months"] {
        right: auto;
      }

      /* Year scroller position indicator */
      [part="years"]::before {
        border: none;
        width: 1em;
        height: 1em;
        background-color: var(--lumo-base-color);
        background-image: linear-gradient(var(--lumo-tint-5pct), var(--lumo-tint-5pct));
        transform: translate(-75%, -50%) rotate(45deg);
        border-top-right-radius: calc(var(--lumo-border-radius) / 2);
        box-shadow: 2px -2px 6px 0 var(--lumo-shade-5pct);
        z-index: 1;
      }

      [part="year-number"],
      [part="year-separator"] {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50%;
        transform: translateY(-50%);
      }

      [part="years"] [part="year-separator"]::after {
        color: var(--lumo-disabled-text-color);
        content: "•";
      }

      /* Current year */

      [part="years"] [part="year-number"][current] {
        color: var(--lumo-primary-text-color);
      }

      /* Toolbar (footer) */

      [part="toolbar"] {
        padding: var(--lumo-space-s);
        box-shadow: 0 -1px 0 0 var(--lumo-contrast-10pct);
        border-bottom-left-radius: var(--lumo-border-radius);
        margin-right: 57px;
      }

      @supports (mask-image: linear-gradient(#000, #000)) or (-webkit-mask-image: linear-gradient(#000, #000)) {
        [part="toolbar"] {
          box-shadow: none;
        }
      }

      /* Today and Cancel buttons */

      /* TODO: Would be great if I could apply the "tertiary" theme from here instead of copying those styles */
      [part="toolbar"] [part\$="button"] {
        background-color: transparent;
        margin: 0;
        min-width: 0;
        padding: 0 0.75em;
      }

      /* Narrow viewport mode (fullscreen) */

      :host([fullscreen]) [part="toolbar"] {
        order: -1;
        background-color: var(--lumo-base-color);
      }

      :host([fullscreen]) [part="overlay-header"] {
        order: -2;
        height: var(--lumo-size-m);
        padding: var(--lumo-space-s);
        position: absolute;
        left: 0;
        right: 0;
        justify-content: center;
      }

      :host([fullscreen]) [part="toggle-button"],
      :host([fullscreen]) [part="clear-button"],
      [part="overlay-header"] [part="label"] {
        display: none;
      }

      /* Very narrow screen (year scroller initially hidden) */

      [part="years-toggle-button"] {
        position: relative;
        right: auto;
        display: flex;
        align-items: center;
        height: var(--lumo-size-s);
        padding: 0 0.5em;
        border-radius: var(--lumo-border-radius);
        z-index: 3;
        color: var(--lumo-primary-text-color);
        font-weight: 500;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      :host([years-visible]) [part="years-toggle-button"] {
        background-color: var(--lumo-primary-color);
        color: var(--lumo-primary-contrast-color);
      }

      [part="years-toggle-button"]::before {
        content: none;
      }

      /* TODO magic number (same as used for iron-media-query in vaadin-date-picker-overlay-content) */
      @media screen and (max-width: 374px) {
        :host {
          background-image: none;
        }

        [part="years"] {
          background-color: var(--lumo-shade-5pct);
        }

        [part="toolbar"],
        [part="months"] {
          margin-right: 0;
        }

        /* TODO make date-picker adapt to the width of the years part */
        [part="years"] {
          --vaadin-infinite-scroller-buffer-width: 90px;
          width: 50px;
        }

        :host([years-visible]) [part="months"] {
          padding-left: 50px;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(w.content);const x=i.a`<dom-module id="lumo-month-calendar" theme-for="vaadin-month-calendar">
  <template>
    <style>
      :host {
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        -webkit-tap-highlight-color: transparent;
        user-select: none;
        font-size: var(--lumo-font-size-m);
        color: var(--lumo-body-text-color);
        text-align: center;
        padding: 0 var(--lumo-space-xs);
      }

      /* Month header */

      [part="month-header"] {
        color: var(--lumo-header-text-color);
        font-size: var(--lumo-font-size-l);
        line-height: 1;
        font-weight: 500;
        margin-bottom: var(--lumo-space-m);
      }

      /* Week days and numbers */

      [part="weekdays"],
      [part="weekday"],
      [part="week-numbers"] {
        font-size: var(--lumo-font-size-xs);
        line-height: 1;
        color: var(--lumo-tertiary-text-color);
      }

      [part="weekdays"] {
        margin-bottom: var(--lumo-space-s);
      }

      /* TODO should have part="week-number" for the cell in weekdays-container */
      [part="weekday"]:empty,
      [part="week-numbers"] {
        width: var(--lumo-size-xs);
      }

      /* Date and week number cells */

      [part="date"],
      [part="week-number"] {
        box-sizing: border-box;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: var(--lumo-size-m);
        position: relative;
      }

      [part="date"] {
        transition: color 0.1s;
      }

      /* Today date */

      [part="date"][today] {
        color: var(--lumo-primary-text-color);
      }

      /* Focused date */

      [part="date"]::before {
        content: "";
        position: absolute;
        z-index: -1;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        min-width: 2em;
        min-height: 2em;
        width: 80%;
        height: 80%;
        max-height: 100%;
        max-width: 100%;
        border-radius: var(--lumo-border-radius);
      }

      [part="date"][focused]::before {
        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);
      }

      :host(:not([focused])) [part="date"][focused]::before {
        animation: vaadin-date-picker-month-calendar-focus-date 1.4s infinite;
      }

      @keyframes vaadin-date-picker-month-calendar-focus-date {
        50% {
          box-shadow: 0 0 0 2px transparent;
        }
      }

      /* TODO should not rely on the role attribute */
      [part="date"][role="button"]:not([disabled]):not([selected]):hover::before {
        background-color: var(--lumo-primary-color-10pct);
      }

      [part="date"][selected] {
        color: var(--lumo-primary-contrast-color);
      }

      [part="date"][selected]::before {
        background-color: var(--lumo-primary-color);
      }

      [part="date"][disabled] {
        color: var(--lumo-disabled-text-color);
      }

      @media (pointer: coarse) {
        [part="date"]:hover:not([selected])::before,
        [part="date"][focused]:not([selected])::before {
          display: none;
        }

        [part="date"][role="button"]:not([disabled]):active::before {
          display: block;
        }

        [part="date"][selected]::before {
          box-shadow: none;
        }
      }

      /* Disabled */

      :host([disabled]) * {
        color: var(--lumo-disabled-text-color) !important;
      }
    </style>
  </template>
</dom-module><custom-style>
  <style>
    @keyframes vaadin-date-picker-month-calendar-focus-date {
      50% {
        box-shadow: 0 0 0 2px transparent;
      }
    }
  </style>
</custom-style>`;document.head.appendChild(x.content);n(269);const k=document.createElement("template");k.innerHTML='<dom-module id="lumo-field-button">\n  <template>\n    <style>\n      [part$="button"] {\n        flex: none;\n        width: 1em;\n        height: 1em;\n        line-height: 1;\n        font-size: var(--lumo-icon-size-m);\n        text-align: center;\n        color: var(--lumo-contrast-60pct);\n        transition: 0.2s color;\n        cursor: default;\n      }\n\n      :host(:not([readonly])) [part$="button"]:hover {\n        color: var(--lumo-contrast-90pct);\n      }\n\n      :host([disabled]) [part$="button"],\n      :host([readonly]) [part$="button"] {\n        color: var(--lumo-contrast-20pct);\n      }\n\n      [part$="button"]::before {\n        font-family: "lumo-icons";\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(k.content);const D=document.createElement("template");D.innerHTML='<dom-module id="lumo-text-field" theme-for="vaadin-text-field">\n  <template>\n    <style>\n      :host {\n        --lumo-text-field-size: var(--lumo-size-m);\n        color: var(--lumo-body-text-color);\n        font-size: var(--lumo-font-size-m);\n        font-family: var(--lumo-font-family);\n        -webkit-font-smoothing: antialiased;\n        -moz-osx-font-smoothing: grayscale;\n        -webkit-tap-highlight-color: transparent;\n        padding: var(--lumo-space-xs) 0;\n      }\n\n      :host::before {\n        height: var(--lumo-text-field-size);\n        box-sizing: border-box;\n        display: inline-flex;\n        align-items: center;\n      }\n\n      [part="label"] {\n        align-self: flex-start;\n        color: var(--lumo-secondary-text-color);\n        font-weight: 500;\n        font-size: var(--lumo-font-size-s);\n        margin-left: calc(var(--lumo-border-radius) / 4);\n        transition: color 0.2s;\n        line-height: 1;\n        padding-bottom: 0.5em;\n        overflow: hidden;\n        white-space: nowrap;\n        text-overflow: ellipsis;\n        position: relative;\n        max-width: 100%;\n        box-sizing: border-box;\n      }\n\n      :host([has-label])::before {\n        /* Label height + margin */\n        margin-top: calc(var(--lumo-font-size-s) * 1.5);\n      }\n\n      :host([has-label]) {\n        padding-top: var(--lumo-space-m);\n      }\n\n      :host([focused]:not([readonly])) [part="label"] {\n        color: var(--lumo-primary-text-color);\n      }\n\n      :host([required]) [part="label"] {\n        padding-right: 1em;\n      }\n\n      /* Used for required and invalid indicators */\n      [part="label"]::after {\n        content: var(--lumo-required-field-indicator, "•");\n        transition: opacity 0.2s;\n        opacity: 0;\n        color: var(--lumo-primary-text-color);\n        position: absolute;\n        right: 0;\n        width: 1em;\n        text-align: center;\n      }\n\n      [part="value"],\n      [part="input-field"] ::slotted([part="value"]) {\n        cursor: inherit;\n        min-height: var(--lumo-text-field-size);\n        padding: 0 0.25em;\n        --_lumo-text-field-overflow-mask-image: linear-gradient(to left, transparent, #000 1.25em);\n        -webkit-mask-image: var(--_lumo-text-field-overflow-mask-image);\n      }\n\n      [part="value"]:focus {\n        -webkit-mask-image: none;\n        mask-image: none;\n      }\n\n      /*\n        TODO: CSS custom property in `mask-image` causes crash in Edge\n        see https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/15415089/\n      */\n      @-moz-document url-prefix() {\n        [part="value"],\n        [part="input-field"] ::slotted([part="value"]) {\n          mask-image: var(--_lumo-text-field-overflow-mask-image);\n        }\n      }\n\n      [part="value"]::-webkit-input-placeholder {\n        color: inherit;\n        transition: opacity 0.175s 0.05s;\n        opacity: 0.5;\n      }\n\n      [part="value"]:-ms-input-placeholder {\n        color: inherit;\n        opacity: 0.5;\n      }\n\n      [part="value"]::-moz-placeholder {\n        color: inherit;\n        transition: opacity 0.175s 0.05s;\n        opacity: 0.5;\n      }\n\n      [part="value"]::placeholder {\n        color: inherit;\n        transition: opacity 0.175s 0.1s;\n        opacity: 0.5;\n      }\n\n      [part="input-field"] {\n        border-radius: var(--lumo-border-radius);\n        background-color: var(--lumo-contrast-10pct);\n        padding: 0 calc(0.375em + var(--lumo-border-radius) / 4 - 1px);\n        font-weight: 500;\n        line-height: 1;\n        position: relative;\n        cursor: text;\n        box-sizing: border-box;\n      }\n\n      /* Used for hover and activation effects */\n      [part="input-field"]::after {\n        content: "";\n        position: absolute;\n        top: 0;\n        right: 0;\n        bottom: 0;\n        left: 0;\n        border-radius: inherit;\n        pointer-events: none;\n        background-color: var(--lumo-contrast-50pct);\n        opacity: 0;\n        transition: transform 0.15s, opacity 0.2s;\n        transform-origin: 100% 0;\n      }\n\n      /* Hover */\n\n      :host(:hover:not([readonly]):not([focused])) [part="label"] {\n        color: var(--lumo-body-text-color);\n      }\n\n      :host(:hover:not([readonly]):not([focused])) [part="input-field"]::after {\n        opacity: 0.1;\n      }\n\n      /* Touch device adjustment */\n      @media (pointer: coarse) {\n        :host(:hover:not([readonly]):not([focused])) [part="label"] {\n          color: var(--lumo-secondary-text-color);\n        }\n\n        :host(:hover:not([readonly]):not([focused])) [part="input-field"]::after {\n          opacity: 0;\n        }\n\n        :host(:active:not([readonly]):not([focused])) [part="input-field"]::after {\n          opacity: 0.2;\n        }\n      }\n\n      /* Trigger when not focusing using the keyboard */\n      :host([focused]:not([focus-ring]):not([readonly])) [part="input-field"]::after {\n        transform: scaleX(0);\n        transition-duration: 0.15s, 1s;\n      }\n\n      /* Focus-ring */\n\n      :host([focus-ring]) [part="input-field"] {\n        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);\n      }\n\n      /* Read-only and disabled */\n      :host([readonly]) [part="value"]::-webkit-input-placeholder,\n      :host([disabled]) [part="value"]::-webkit-input-placeholder {\n        opacity: 0;\n      }\n\n      :host([readonly]) [part="value"]:-ms-input-placeholder,\n      :host([disabled]) [part="value"]:-ms-input-placeholder {\n        opacity: 0;\n      }\n\n      :host([readonly]) [part="value"]::-moz-placeholder,\n      :host([disabled]) [part="value"]::-moz-placeholder {\n        opacity: 0;\n      }\n\n      :host([readonly]) [part="value"]::placeholder,\n      :host([disabled]) [part="value"]::placeholder {\n        opacity: 0;\n      }\n\n      /* Read-only */\n\n      :host([readonly]) [part="input-field"] {\n        color: var(--lumo-secondary-text-color);\n        background-color: transparent;\n        cursor: default;\n      }\n\n      :host([readonly]) [part="input-field"]::after {\n        background-color: transparent;\n        opacity: 1;\n        border: 1px dashed var(--lumo-contrast-30pct);\n      }\n\n      /* Disabled style */\n\n      :host([disabled]) {\n        pointer-events: none;\n      }\n\n      :host([disabled]) [part="input-field"] {\n        background-color: var(--lumo-contrast-5pct);\n      }\n\n      :host([disabled]) [part="label"],\n      :host([disabled]) [part="value"],\n      :host([disabled]) [part="input-field"] ::slotted(*) {\n        color: var(--lumo-disabled-text-color);\n        -webkit-text-fill-color: var(--lumo-disabled-text-color);\n      }\n\n      /* Required field style */\n\n      :host([required]:not([has-value])) [part="label"]::after {\n        opacity: 1;\n      }\n\n      /* Invalid style */\n\n      :host([invalid]) [part="label"]::after {\n        color: var(--lumo-error-text-color);\n      }\n\n      :host([invalid]) [part="input-field"] {\n        background-color: var(--lumo-error-color-10pct);\n      }\n\n      :host([invalid]) [part="input-field"]::after {\n        background-color: var(--lumo-error-color-50pct);\n      }\n\n      :host([invalid][focus-ring]) [part="input-field"] {\n        box-shadow: 0 0 0 2px var(--lumo-error-color-50pct);\n      }\n\n      /* Error message */\n\n      [part="error-message"] {\n        margin-left: calc(var(--lumo-border-radius) / 4);\n        font-size: var(--lumo-font-size-xs);\n        line-height: var(--lumo-line-height-xs);\n        color: var(--lumo-error-text-color);\n        will-change: max-height;\n        transition: 0.4s max-height;\n        max-height: 5em;\n      }\n\n      /* Margin that doesn’t reserve space when there’s no error message */\n      [part="error-message"]:not(:empty)::before,\n      [part="error-message"]:not(:empty)::after {\n        content: "";\n        display: block;\n        height: 0.4em;\n      }\n\n      :host(:not([invalid])) [part="error-message"] {\n        max-height: 0;\n        overflow: hidden;\n      }\n\n      /* Small theme */\n\n      :host([theme~="small"]) {\n        font-size: var(--lumo-font-size-s);\n        --lumo-text-field-size: var(--lumo-size-s);\n      }\n\n      :host([theme~="small"][has-label]) [part="label"] {\n        font-size: var(--lumo-font-size-xs);\n      }\n\n      :host([theme~="small"][has-label]) [part="error-message"] {\n        font-size: var(--lumo-font-size-xxs);\n      }\n\n      /* Text align */\n\n      :host([theme~="align-center"]) [part="value"] {\n        text-align: center;\n        --_lumo-text-field-overflow-mask-image: none;\n      }\n\n      :host([theme~="align-right"]) [part="value"] {\n        text-align: right;\n        --_lumo-text-field-overflow-mask-image: none;\n      }\n\n      @-moz-document url-prefix() {\n        /* Firefox is smart enough to align overflowing text to right */\n        :host([theme~="align-right"]) [part="value"] {\n          --_lumo-text-field-overflow-mask-image: linear-gradient(to right, transparent 0.25em, #000 1.5em);\n        }\n      }\n\n      /* Slotted content */\n\n      [part="input-field"] ::slotted(:not([part]):not(iron-icon)) {\n        color: var(--lumo-secondary-text-color);\n        font-weight: 400;\n      }\n\n      /* Slotted icons */\n\n      [part="input-field"] ::slotted(iron-icon) {\n        color: var(--lumo-contrast-60pct);\n        width: var(--lumo-icon-size-m);\n        height: var(--lumo-icon-size-m);\n      }\n\n      /* Vaadin icons are based on a 16x16 grid (unlike Lumo and Material icons with 24x24), so they look too big by default */\n      [part="input-field"] ::slotted(iron-icon[icon^="vaadin:"]) {\n        padding: 0.25em;\n        box-sizing: border-box !important;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(D.content);const C=document.createElement("template");C.innerHTML='<dom-module id="vaadin-text-field-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-flex;\n        outline: none;\n      }\n\n      :host::before {\n        content: "\\2003";\n        width: 0;\n        display: inline-block;\n        /* Size and position this element on the same vertical position as the input-field element\n           to make vertical align for the host element work as expected */\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      .vaadin-text-field-container,\n      .vaadin-text-area-container {\n        display: flex;\n        flex-direction: column;\n        min-width: 100%;\n        max-width: 100%;\n        width: var(--vaadin-text-field-default-width, 12em);\n      }\n\n      [part="label"]:empty {\n        display: none;\n      }\n\n      [part="input-field"] {\n        display: flex;\n        align-items: center;\n        flex: auto;\n      }\n\n      /* Reset the native input styles */\n      [part="value"] {\n        -webkit-appearance: none;\n        -moz-appearance: none;\n        outline: none;\n        margin: 0;\n        padding: 0;\n        border: 0;\n        border-radius: 0;\n        min-width: 0;\n        font: inherit;\n        font-size: 1em;\n        line-height: normal;\n        color: inherit;\n        background-color: transparent;\n        /* Disable default invalid style in Firefox */\n        box-shadow: none;\n      }\n\n      [part="input-field"] ::slotted(*) {\n        flex: none;\n      }\n\n      /* Slotted by vaadin-dropdown-menu-text-field */\n      [part="value"],\n      [part="input-field"] ::slotted([part="value"]) {\n        flex: auto;\n        white-space: nowrap;\n        overflow: hidden;\n        width: 100%;\n        height: 100%;\n      }\n\n      [part="value"]::-ms-clear {\n        display: none;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(C.content);const S=e=>(class extends(d(e)){static get properties(){return{autocomplete:{type:String},autocorrect:{type:String},autocapitalize:{type:String},errorMessage:{type:String,value:""},label:{type:String,value:"",observer:"_labelChanged"},maxlength:{type:Number},minlength:{type:Number},name:{type:String},placeholder:{type:String},readonly:{type:Boolean,reflectToAttribute:!0},required:{type:Boolean,reflectToAttribute:!0},value:{type:String,value:"",observer:"_valueChanged",notify:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},preventInvalidInput:{type:Boolean},_labelId:{type:String},_errorId:{type:String}}}get focusElement(){return this.root.querySelector("[part=value]")}_onInput(e){if(this.preventInvalidInput){const e=this.focusElement;e.value.length>0&&!this.checkValidity()&&(e.value=this.value||"")}}_onChange(e){const t=new CustomEvent("change",{detail:{sourceEvent:e},bubbles:e.bubbles,cancelable:e.cancelable});this.dispatchEvent(t)}_valueChanged(e,t){""===e&&void 0===t||(this.invalid&&this.validate(),""!==e&&null!=e?this.setAttribute("has-value",""):this.removeAttribute("has-value"))}_labelChanged(e){""!==e&&null!=e?this.setAttribute("has-label",""):this.removeAttribute("has-label")}checkValidity(){return this.required||this.pattern||this.maxlength||this.minlength?this.focusElement.checkValidity():!this.invalid}ready(){super.ready(),window.ShadyCSS&&window.ShadyCSS.nativeCss||this.updateStyles();var e=S._uniqueId=1+S._uniqueId||0;this._errorId=`${this.constructor.is}-error-${e}`,this._labelId=`${this.constructor.is}-label-${e}`,navigator.userAgent.match(/Trident/)&&this._addIEListeners()}validate(){return!(this.invalid=!this.checkValidity())}_addIEListeners(){const e=t=>{t.stopImmediatePropagation(),this.focusElement.removeEventListener("input",e)},t=()=>this.placeholder&&this.focusElement.addEventListener("input",e);this.focusElement.addEventListener("focusin",t),this.focusElement.addEventListener("focusout",t),this._createPropertyObserver("placeholder",t)}_getActiveErrorId(e,t,n){return t&&e?n:void 0}_getActiveLabelId(e,t){return e?t:void 0}_getErrorMessageAriaHidden(e,t,n){return(!this._getActiveErrorId(e,t,n)).toString()}attributeChangedCallback(e,t,n){if(super.attributeChangedCallback(e,t,n),window.ShadyCSS&&window.ShadyCSS.nativeCss||!/^(focused|focus-ring|invalid|disabled|placeholder|has-value)$/.test(e)||this.updateStyles(),/^((?!chrome|android).)*safari/i.test(navigator.userAgent)&&this.root){const e="-webkit-backface-visibility";this.root.querySelectorAll("*").forEach(t=>{t.style[e]="visible",t.style[e]=""})}}});class E extends(y(S(Object(l.a)(r.a)))){static get template(){return i.a`
    <style include="vaadin-text-field-shared-styles">
      /* polymer-cli linter breaks with empty line */
    </style>

    <div class="vaadin-text-field-container">

      <label part="label" on-click="focus" id="[[_labelId]]">[[label]]</label>

      <div part="input-field">

        <slot name="prefix"></slot>

        <input part="value" autocomplete\$="[[autocomplete]]" autocorrect\$="[[autocorrect]]" autocapitalize\$="[[autocapitalize]]" autofocus\$="[[autofocus]]" disabled\$="[[disabled]]" list="[[list]]" maxlength\$="[[maxlength]]" minlength\$="[[minlength]]" pattern="[[pattern]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" aria-readonly\$="[[readonly]]" required\$="[[required]]" aria-required\$="[[required]]" value="{{value::input}}" title="[[title]]" on-blur="validate" on-input="_onInput" on-change="_onChange" aria-describedby\$="[[_getActiveErrorId(invalid, errorMessage, _errorId)]]" aria-labelledby\$="[[_getActiveLabelId(label, _labelId)]]" aria-invalid\$="[[invalid]]">

        <slot name="suffix"></slot>

      </div>

      <div part="error-message" id="[[_errorId]]" aria-live="assertive" aria-hidden\$="[[_getErrorMessageAriaHidden(invalid, errorMessage, _errorId)]]">[[errorMessage]]</div>

    </div>
`}static get is(){return"vaadin-text-field"}static get version(){return"2.1.2"}static get properties(){return{list:{type:String},pattern:{type:String},title:{type:String}}}}customElements.define(E.is,E);const M=i.a`<dom-module id="lumo-date-picker" theme-for="vaadin-date-picker">
  <template>
    <style include="lumo-field-button">
      :host {
        outline: none;
      }

      [part="toggle-button"]::before {
        content: var(--lumo-icons-calendar);
      }

      [part="clear-button"]::before {
        content: var(--lumo-icons-cross);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(M.content);n(119);var I=n(270),$=n(325);class T extends $.a{static get is(){return"vaadin-date-picker-overlay"}}customElements.define(T.is,T);var z=n(30),Y=n(87);n(80);const O=class{static _getISOWeekNumber(e){var t=e.getDay();0===t&&(t=7);var n=4-t,i=new Date(e.getTime()+24*n*3600*1e3),a=new Date(0,0);a.setFullYear(i.getFullYear());var o=i.getTime()-a.getTime(),r=Math.round(o/864e5);return Math.floor(r/7+1)}static _dateEquals(e,t){return e instanceof Date&&t instanceof Date&&e.getFullYear()===t.getFullYear()&&e.getMonth()===t.getMonth()&&e.getDate()===t.getDate()}static _dateAllowed(e,t,n){return(!t||e>=t)&&(!n||e<=n)}static _getClosestDate(e,t){return t.filter(e=>void 0!==e).reduce((t,n)=>{return n?t?Math.abs(e.getTime()-n.getTime())<Math.abs(t.getTime()-e.getTime())?n:t:n:t})}static _extractDateParts(e){return{day:e.getDate(),month:e.getMonth(),year:e.getFullYear()}}};class F extends(Object(l.a)(Object(s.a)(r.a))){static get template(){return i.a`
    <style>
      :host {
        display: block;
      }

      [part="weekdays"],
      #days {
        display: flex;
        flex-wrap: wrap;
        flex-grow: 1;
      }

      #days-container,
      #weekdays-container {
        display: flex;
      }

      [part="week-numbers"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-shrink: 0;
      }

      [part="week-numbers"][hidden],
      [part="weekday"][hidden] {
        display: none;
      }

      [part="weekday"],
      [part="date"] {
        /* Would use calc(100% / 7) but it doesn't work nice on IE */
        width: 14.285714286%;
      }

      [part="weekday"]:empty,
      [part="week-numbers"] {
        width: 12.5%;
        flex-shrink: 0;
      }
    </style>

    <div part="month-header" role="heading">[[_getTitle(month, i18n.monthNames)]]</div>
    <div id="monthGrid" on-tap="_handleTap" on-touchend="_preventDefault" on-touchstart="_onMonthGridTouchStart">
      <div id="weekdays-container">
        <div hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]" part="weekday"></div>
        <div part="weekdays">
          <template is="dom-repeat" items="[[_getWeekDayNames(i18n.weekdays, i18n.weekdaysShort, showWeekNumbers, i18n.firstDayOfWeek)]]">
            <div part="weekday" role="heading" aria-label\$="[[item.weekDay]]">[[item.weekDayShort]]</div>
          </template>
        </div>
      </div>
      <div id="days-container">
        <div part="week-numbers" hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]">
          <template is="dom-repeat" items="[[_getWeekNumbers(_days)]]">
            <div part="week-number" role="heading" aria-label\$="[[i18n.week]] [[item]]">[[item]]</div>
          </template>
        </div>
        <div id="days">
          <template is="dom-repeat" items="[[_days]]">
            <div part="date" today\$="[[_isToday(item)]]" selected\$="[[_dateEquals(item, selectedDate)]]" focused\$="[[_dateEquals(item, focusedDate)]]" date="[[item]]" disabled\$="[[!_dateAllowed(item, minDate, maxDate)]]" role\$="[[_getRole(item)]]" aria-label\$="[[_getAriaLabel(item)]]" aria-disabled\$="[[_getAriaDisabled(item, minDate, maxDate)]]">[[_getDate(item)]]</div>
          </template>
        </div>
      </div>
    </div>
`}static get is(){return"vaadin-month-calendar"}static get properties(){return{month:{type:Date,value:new Date},selectedDate:{type:Date,notify:!0},focusedDate:Date,showWeekNumbers:{type:Boolean,value:!1},i18n:{type:Object},ignoreTaps:Boolean,_notTapping:Boolean,minDate:{type:Date,value:null},maxDate:{type:Date,value:null},_days:{type:Array,computed:"_getDays(month, i18n.firstDayOfWeek, minDate, maxDate)"},disabled:{type:Boolean,reflectToAttribute:!0,computed:"_isDisabled(month, minDate, maxDate)"}}}static get observers(){return["_showWeekNumbersChanged(showWeekNumbers, i18n.firstDayOfWeek)"]}_dateEquals(e,t){return O._dateEquals(e,t)}_dateAllowed(e,t,n){return O._dateAllowed(e,t,n)}_isDisabled(e,t,n){var i=new Date(0,0);i.setFullYear(e.getFullYear()),i.setMonth(e.getMonth()),i.setDate(1);var a=new Date(0,0);return a.setFullYear(e.getFullYear()),a.setMonth(e.getMonth()+1),a.setDate(-1),!(t&&n&&t.getMonth()===n.getMonth()&&t.getMonth()===e.getMonth()&&n.getDate()-t.getDate()>=0)&&(!this._dateAllowed(i,t,n)&&!this._dateAllowed(a,t,n))}_getTitle(e,t){if(void 0!==e&&void 0!==t)return this.i18n.formatTitle(t[e.getMonth()],e.getFullYear())}_onMonthGridTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300)}_dateAdd(e,t){e.setDate(e.getDate()+t)}_applyFirstDayOfWeek(e,t){if(void 0!==e&&void 0!==t)return e.slice(t).concat(e.slice(0,t))}_getWeekDayNames(e,t,n,i){if(void 0!==e&&void 0!==t&&void 0!==n&&void 0!==i)return e=this._applyFirstDayOfWeek(e,i),t=this._applyFirstDayOfWeek(t,i),e=e.map((e,n)=>({weekDay:e,weekDayShort:t[n]}))}_getDate(e){return e?e.getDate():""}_showWeekNumbersChanged(e,t){e&&1===t?this.setAttribute("week-numbers",""):this.removeAttribute("week-numbers")}_showWeekSeparator(e,t){return e&&1===t}_isToday(e){return this._dateEquals(new Date,e)}_getDays(e,t){if(void 0!==e&&void 0!==t){var n=new Date(0,0);for(n.setFullYear(e.getFullYear()),n.setMonth(e.getMonth()),n.setDate(1);n.getDay()!==t;)this._dateAdd(n,-1);for(var i=[],a=n.getMonth(),o=e.getMonth();n.getMonth()===o||n.getMonth()===a;)i.push(n.getMonth()===o?new Date(n.getTime()):null),this._dateAdd(n,1);return i}}_getWeekNumber(e,t){if(void 0!==e&&void 0!==t)return e||(e=t.reduce((e,t)=>!e&&t?t:e)),O._getISOWeekNumber(e)}_getWeekNumbers(e){return e.map(t=>this._getWeekNumber(t,e)).filter((e,t,n)=>n.indexOf(e)===t)}_handleTap(e){this.ignoreTaps||this._notTapping||!e.target.date||e.target.hasAttribute("disabled")||(this.selectedDate=e.target.date,this.dispatchEvent(new CustomEvent("date-tap",{bubbles:!0,composed:!0})))}_preventDefault(e){e.preventDefault()}_getRole(e){return e?"button":"presentation"}_getAriaLabel(e){if(!e)return"";var t=this._getDate(e)+" "+this.i18n.monthNames[e.getMonth()]+" "+e.getFullYear()+", "+this.i18n.weekdays[e.getDay()];return this._isToday(e)&&(t+=", "+this.i18n.today),t}_getAriaDisabled(e,t,n){if(void 0!==e&&void 0!==t&&void 0!==n)return this._dateAllowed(e,t,n)?"false":"true"}}customElements.define(F.is,F);var B=n(31),V=n(59);class P extends r.a{static get template(){return i.a`
    <style>
      :host {
        display: block;
        overflow: hidden;
        height: 500px;
      }

      #scroller {
        position: relative;
        height: 100%;
        overflow: auto;
        outline: none;
        margin-right: -40px;
        -webkit-overflow-scrolling: touch;
        -ms-overflow-style: none;
        overflow-x: hidden;
      }

      #scroller.notouchscroll {
        -webkit-overflow-scrolling: auto;
      }

      #scroller::-webkit-scrollbar {
        display: none;
      }

      .buffer {
        position: absolute;
        width: var(--vaadin-infinite-scroller-buffer-width, 100%);
        box-sizing: border-box;
        padding-right: 40px;
        top: var(--vaadin-infinite-scroller-buffer-offset, 0);
        animation: fadein 0.2s;
      }

      @keyframes fadein {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    </style>

    <div id="scroller" on-scroll="_scroll">
      <div class="buffer"></div>
      <div class="buffer"></div>
      <div id="fullHeight"></div>
    </div>
`}static get is(){return"vaadin-infinite-scroller"}static get properties(){return{bufferSize:{type:Number,value:20},_initialScroll:{value:5e5},_initialIndex:{value:0},_buffers:Array,_preventScrollEvent:Boolean,_mayHaveMomentum:Boolean,_initialized:Boolean,active:{type:Boolean,observer:"_activated"}}}ready(){super.ready(),this._buffers=Array.prototype.slice.call(this.root.querySelectorAll(".buffer")),this.$.fullHeight.style.height=2*this._initialScroll+"px";var e=this.querySelector("template");this._TemplateClass=Object(B.b)(e,this,{forwardHostProp:function(e,t){"index"!==e&&this._buffers.forEach(n=>{[].forEach.call(n.children,n=>{n._itemWrapper.instance[e]=t})})}}),navigator.userAgent.toLowerCase().indexOf("firefox")>-1&&(this.$.scroller.tabIndex=-1)}_activated(e){e&&!this._initialized&&(this._createPool(),this._initialized=!0)}_finishInit(){this._initDone||(this._buffers.forEach(e=>{[].forEach.call(e.children,e=>this._ensureStampedInstance(e._itemWrapper))},this),this._buffers[0].translateY||this._reset(),this._initDone=!0)}_translateBuffer(e){var t=e?1:0;this._buffers[t].translateY=this._buffers[t?0:1].translateY+this._bufferHeight*(t?-1:1),this._buffers[t].style.transform="translate3d(0, "+this._buffers[t].translateY+"px, 0)",this._buffers[t].updated=!1,this._buffers.reverse()}_scroll(){if(!this._scrollDisabled){var e=this.$.scroller.scrollTop;(e<this._bufferHeight||e>2*this._initialScroll-this._bufferHeight)&&(this._initialIndex=~~this.position,this._reset());var t=this.root.querySelector(".buffer").offsetTop,n=e>this._buffers[1].translateY+this.itemHeight+t,i=e<this._buffers[0].translateY+this.itemHeight+t;(n||i)&&(this._translateBuffer(i),this._updateClones()),this._preventScrollEvent||(this.dispatchEvent(new CustomEvent("custom-scroll",{bubbles:!1,composed:!0})),this._mayHaveMomentum=!0),this._preventScrollEvent=!1,this._debouncerScrollFinish=u.a.debounce(this._debouncerScrollFinish,c.d.after(200),()=>{var e=this.$.scroller.getBoundingClientRect();this._isVisible(this._buffers[0],e)||this._isVisible(this._buffers[1],e)||(this.position=this.position)})}}set position(e){this._preventScrollEvent=!0,e>this._firstIndex&&e<this._firstIndex+2*this.bufferSize?this.$.scroller.scrollTop=this.itemHeight*(e-this._firstIndex)+this._buffers[0].translateY:(this._initialIndex=~~e,this._reset(),this._scrollDisabled=!0,this.$.scroller.scrollTop+=e%1*this.itemHeight,this._scrollDisabled=!1),this._mayHaveMomentum&&(this.$.scroller.classList.add("notouchscroll"),this._mayHaveMomentum=!1,setTimeout(()=>{this.$.scroller.classList.remove("notouchscroll")},10))}get position(){return(this.$.scroller.scrollTop-this._buffers[0].translateY)/this.itemHeight+this._firstIndex}get itemHeight(){if(!this._itemHeightVal){const e=window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-infinite-scroller-item-height"):getComputedStyle(this).getPropertyValue("--vaadin-infinite-scroller-item-height"),t="background-position";this.$.fullHeight.style.setProperty(t,e);const n=getComputedStyle(this.$.fullHeight).getPropertyValue(t);this.$.fullHeight.style.removeProperty(t),this._itemHeightVal=parseFloat(n)}return this._itemHeightVal}get _bufferHeight(){return this.itemHeight*this.bufferSize}_reset(){this._scrollDisabled=!0,this.$.scroller.scrollTop=this._initialScroll,this._buffers[0].translateY=this._initialScroll-this._bufferHeight,this._buffers[1].translateY=this._initialScroll,this._buffers.forEach(e=>{e.style.transform="translate3d(0, "+e.translateY+"px, 0)"}),this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones(!0),this._debouncerUpdateClones=u.a.debounce(this._debouncerUpdateClones,c.d.after(200),()=>{this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones()}),this._scrollDisabled=!1}_createPool(){var e=this.getBoundingClientRect();this._buffers.forEach(t=>{for(var n=0;n<this.bufferSize;n++){const n=document.createElement("div");n.style.height=this.itemHeight+"px",n.instance={};const i="vaadin-infinite-scroller-item-content-"+(P._contentIndex=P._contentIndex+1||0),a=document.createElement("slot");a.setAttribute("name",i),a._itemWrapper=n,t.appendChild(a),n.setAttribute("slot",i),this.appendChild(n),Object(h.b)(),setTimeout(()=>{this._isVisible(n,e)&&this._ensureStampedInstance(n)},1)}},this),setTimeout(()=>{Object(V.a)(this,this._finishInit.bind(this))},1)}_ensureStampedInstance(e){if(!e.firstElementChild){var t=e.instance;e.instance=new this._TemplateClass({}),e.appendChild(e.instance.root),Object.keys(t).forEach(n=>{e.instance.set(n,t[n])})}}_updateClones(e){this._firstIndex=~~((this._buffers[0].translateY-this._initialScroll)/this.itemHeight)+this._initialIndex;var t=e?this.$.scroller.getBoundingClientRect():void 0;this._buffers.forEach((n,i)=>{if(!n.updated){var a=this._firstIndex+this.bufferSize*i;[].forEach.call(n.children,(n,i)=>{const o=n._itemWrapper;e&&!this._isVisible(o,t)||(o.instance.index=a+i)}),n.updated=!0}},this)}_isVisible(e,t){var n=e.getBoundingClientRect();return n.bottom>t.top&&n.top<t.bottom}}customElements.define(P.is,P);n(90);const j=document.createElement("template");j.innerHTML='<custom-style>\n  <style>\n    @font-face {\n      font-family: \'vaadin-date-picker-icons\';\n      src: url(data:application/font-woff;charset=utf-8;base64,d09GRgABAAAAAAYoAAsAAAAABdwAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAABPUy8yAAABCAAAAGAAAABgDxIFqWNtYXAAAAFoAAAAVAAAAFQXVtKKZ2FzcAAAAbwAAAAIAAAACAAAABBnbHlmAAABxAAAAUAAAAFAAtWm1WhlYWQAAAMEAAAANgAAADYNRs5taGhlYQAAAzwAAAAkAAAAJAdCA8lobXR4AAADYAAAACAAAAAgFW4CxGxvY2EAAAOAAAAAEgAAABIBEgDCbWF4cAAAA5QAAAAgAAAAIAAMACNuYW1lAAADtAAAAlIAAAJSbLEfa3Bvc3QAAAYIAAAAIAAAACAAAwAAAAMDfAGQAAUAAAKZAswAAACPApkCzAAAAesAMwEJAAAAAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAAAAQAAA6QMDwP/AAEADwABAAAAAAQAAAAAAAAAAAAAAIAAAAAAAAwAAAAMAAAAcAAEAAwAAABwAAwABAAAAHAAEADgAAAAKAAgAAgACAAEAIOkD//3//wAAAAAAIOkA//3//wAB/+MXBAADAAEAAAAAAAAAAAAAAAEAAf//AA8AAQAAAAAAAAAAAAIAADc5AQAAAAABAAAAAAAAAAAAAgAANzkBAAAAAAEAAAAAAAAAAAACAAA3OQEAAAAAAQFvAKsCqwKrAAUAAAEHFwcXAQGrPMPDPAEAAqs8xMQ8AQAAAQDVAIADKwLVAAsAAAEnBycHFwcXNxc3JwMrPO/vPO/vPO/vPO8CmTzu7jzu7zzv7zzvAAMAgAArA4ADgAADABwAIAAAASMVMwMVITUjFSMiBhURFBYzITI2NRE0JisBNSMTIREhAtXV1Sr+qlUrIzIyIwJWIzIyIytVgP2qAlYBq9YCq1VVVTIk/asjMjIjAlUkMlX9AAHVAAAAAQAAAAADbgNuABMAAAEUDgIjIi4CNTQ+AjMyHgIDbkV3oFtboHdFRXegW1ugd0UBt1ugd0VFd6BbW6B3RUV3oAAAAAABAAAAAQAAvCcusV8PPPUACwQAAAAAANVURPgAAAAA1VRE+AAAAAADgAOAAAAACAACAAAAAAAAAAEAAAPA/8AAAAQAAAAAAAOAAAEAAAAAAAAAAAAAAAAAAAAIBAAAAAAAAAAAAAAAAgAAAAQAAW8EAADVBAAAgANuAAAAAAAAAAoAFAAeADAASgB+AKAAAAABAAAACAAhAAMAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAADgCuAAEAAAAAAAEAGAAAAAEAAAAAAAIABwD5AAEAAAAAAAMAGABpAAEAAAAAAAQAGAEOAAEAAAAAAAUACwBIAAEAAAAAAAYAGACxAAEAAAAAAAoAGgFWAAMAAQQJAAEAMAAYAAMAAQQJAAIADgEAAAMAAQQJAAMAMACBAAMAAQQJAAQAMAEmAAMAAQQJAAUAFgBTAAMAAQQJAAYAMADJAAMAAQQJAAoANAFwdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzVmVyc2lvbiAxLjAAVgBlAHIAcwBpAG8AbgAgADEALgAwdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzUmVndWxhcgBSAGUAZwB1AGwAYQBydmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzRm9udCBnZW5lcmF0ZWQgYnkgSWNvTW9vbi4ARgBvAG4AdAAgAGcAZQBuAGUAcgBhAHQAZQBkACAAYgB5ACAASQBjAG8ATQBvAG8AbgAuAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==) format(\'woff\');\n      font-weight: normal;\n      font-style: normal;\n    }\n  </style>\n</custom-style><dom-module id="vaadin-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">\n  <template>\n    <style>\n      :host {\n        align-items: flex-start;\n        justify-content: flex-start;\n      }\n\n      :host([bottom-aligned]) {\n        justify-content: flex-end;\n      }\n\n      :host([right-aligned]) {\n        align-items: flex-end;\n      }\n\n      [part="overlay"] {\n        display: flex;\n        flex: auto;\n      }\n\n      [part~="content"] {\n        flex: auto;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(j.content);class H extends(Object(l.a)(Object(I.a)(Object(s.a)(r.a)))){static get template(){return i.a`
    <style>
      :host {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        outline: none;
        background: #fff;
      }

      [part="overlay-header"] {
        display: flex;
        flex-shrink: 0;
        flex-wrap: nowrap;
        align-items: center;
      }

      :host(:not([fullscreen])) [part="overlay-header"] {
        display: none;
      }

      [part="label"] {
        flex-grow: 1;
      }

      [part="clear-button"],
      [part="toggle-button"],
      [part="years-toggle-button"]::before {
        font-family: 'vaadin-date-picker-icons';
      }

      [part="clear-button"]:not([showclear]) {
        display: none;
      }

      [part="clear-button"]::before {
        content: "\\e901";
      }

      [part="toggle-button"]::before {
        content: "\\e902";
      }

      [part="years-toggle-button"] {
        display: flex;
      }

      [part="years-toggle-button"][desktop] {
        display: none;
      }

      [part="years-toggle-button"]::before {
        content: "\\e900";
      }

      :host(:not([years-visible])) [part="years-toggle-button"]::before {
        transform: rotate(180deg);
      }

      #scrollers {
        display: flex;
        height: 100%;
        width: 100%;
        position: relative;
        overflow: hidden;
      }

      [part="months"],
      [part="years"] {
        height: 100%;
      }

      [part="months"] {
        --vaadin-infinite-scroller-item-height: 270px;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
      }

      #scrollers[desktop] [part="months"] {
        right: 50px;
        transform: none !important;
      }

      [part="years"] {
        --vaadin-infinite-scroller-item-height: 80px;
        width: 50px;
        position: absolute;
        right: 0;
        transform: translateX(100%);
        -webkit-tap-highlight-color: transparent;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        /* Center the year scroller position. */
        --vaadin-infinite-scroller-buffer-offset: 50%;
      }

      #scrollers[desktop] [part="years"] {
        position: absolute;
        transform: none !important;
      }

      [part="years"]::before {
        content: '';
        display: block;
        background: transparent;
        width: 0;
        height: 0;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        border-width: 6px;
        border-style: solid;
        border-color: transparent;
        border-left-color: #000;
      }

      :host(.animate) [part="months"],
      :host(.animate) [part="years"] {
        transition: all 200ms;
      }

      [part="toolbar"] {
        display: flex;
        justify-content: space-between;
        z-index: 2;
        flex-shrink: 0;
      }

      [part~="overlay-header"]:not([desktop]) {
        padding-bottom: 40px;
      }

      [part~="years-toggle-button"] {
        position: absolute;
        top: auto;
        right: 8px;
        bottom: 0;
        z-index: 1;
        padding: 8px;
      }

      #announcer {
        display: inline-block;
        position: fixed;
        clip: rect(0, 0, 0, 0);
        clip-path: inset(100%);
      }
    </style>

    <div id="announcer" role="alert" aria-live="polite">
      [[i18n.calendar]]
    </div>

    <div part="overlay-header" on-touchend="_preventDefault" desktop\$="[[_desktopMode]]" aria-hidden="true">
      <div part="label">[[_formatDisplayed(selectedDate, i18n.formatDate, label)]]</div>
      <div part="clear-button" on-tap="_clear" showclear\$="[[_showClear(selectedDate)]]"></div>
      <div part="toggle-button" on-tap="_cancel"></div>

      <div part="years-toggle-button" desktop\$="[[_desktopMode]]" on-tap="_toggleYearScroller" aria-hidden="true">
        [[_yearAfterXMonths(_visibleMonthIndex)]]
      </div>
    </div>

    <div id="scrollers" desktop\$="[[_desktopMode]]" on-track="_track">
      <vaadin-infinite-scroller id="monthScroller" on-custom-scroll="_onMonthScroll" on-touchstart="_onMonthScrollTouchStart" buffer-size="3" active="[[initialPosition]]" part="months">
        <template>
          <vaadin-month-calendar i18n="[[i18n]]" month="[[_dateAfterXMonths(index)]]" selected-date="{{selectedDate}}" focused-date="[[focusedDate]]" ignore-taps="[[_ignoreTaps]]" show-week-numbers="[[showWeekNumbers]]" min-date="[[minDate]]" max-date="[[maxDate]]" focused\$="[[_focused]]" part="month" theme\$="[[theme]]">
          </vaadin-month-calendar>
        </template>
      </vaadin-infinite-scroller>
      <vaadin-infinite-scroller id="yearScroller" on-tap="_onYearTap" on-custom-scroll="_onYearScroll" on-touchstart="_onYearScrollTouchStart" buffer-size="12" active="[[initialPosition]]" part="years">
        <template>
          <div part="year-number" role="button" current\$="[[_isCurrentYear(index)]]" selected\$="[[_isSelectedYear(index, selectedDate)]]">
            [[_yearAfterXYears(index)]]
          </div>
          <div part="year-separator" aria-hidden="true"></div>
        </template>
      </vaadin-infinite-scroller>
    </div>

    <div on-touchend="_preventDefault" role="toolbar" part="toolbar">
      <vaadin-button id="todayButton" part="today-button" disabled="[[!_isTodayAllowed(minDate, maxDate)]]" on-tap="_onTodayTap">
        [[i18n.today]]
      </vaadin-button>
      <vaadin-button id="cancelButton" part="cancel-button" on-tap="_cancel">
        [[i18n.cancel]]
      </vaadin-button>
    </div>

    <iron-media-query query="(min-width: 375px)" query-matches="{{_desktopMode}}"></iron-media-query>
`}static get is(){return"vaadin-date-picker-overlay-content"}static get properties(){return{selectedDate:{type:Date,notify:!0},focusedDate:{type:Date,notify:!0,observer:"_focusedDateChanged"},_focusedMonthDate:Number,initialPosition:{type:Date,observer:"_initialPositionChanged"},_originDate:{value:new Date},_visibleMonthIndex:Number,_desktopMode:Boolean,_translateX:{observer:"_translateXChanged"},_yearScrollerWidth:{value:50},i18n:{type:Object},showWeekNumbers:{type:Boolean},_ignoreTaps:Boolean,_notTapping:Boolean,minDate:Date,maxDate:Date,_focused:Boolean,label:String}}ready(){super.ready(),this.setAttribute("tabindex",0),this.addEventListener("keydown",this._onKeydown.bind(this)),Object(g.b)(this,"tap",this._stopPropagation),this.addEventListener("focus",this._onOverlayFocus.bind(this)),this.addEventListener("blur",this._onOverlayBlur.bind(this))}connectedCallback(){super.connectedCallback(),this._closeYearScroller(),this._toggleAnimateClass(!0),Object(g.f)(this.$.scrollers,"pan-y"),Y.a.requestAvailability()}announceFocusedDate(){var e=this._currentlyFocusedDate(),t=[];O._dateEquals(e,new Date)&&t.push(this.i18n.today),t=t.concat([this.i18n.weekdays[e.getDay()],e.getDate(),this.i18n.monthNames[e.getMonth()],e.getFullYear()]),this.showWeekNumbers&&1===this.i18n.firstDayOfWeek&&(t.push(this.i18n.week),t.push(O._getISOWeekNumber(e))),this.dispatchEvent(new CustomEvent("iron-announce",{bubbles:!0,composed:!0,detail:{text:t.join(" ")}}))}focusCancel(){this.$.cancelButton.focus()}scrollToDate(e,t){this._scrollToPosition(this._differenceInMonths(e,this._originDate),t)}_focusedDateChanged(e){this.revealDate(e)}_isCurrentYear(e){return 0===e}_isSelectedYear(e,t){if(t)return t.getFullYear()===this._originDate.getFullYear()+e}revealDate(e){if(e){var t=this._differenceInMonths(e,this._originDate),n=this.$.monthScroller.position>t,i=this.$.monthScroller.clientHeight/this.$.monthScroller.itemHeight,a=this.$.monthScroller.position+i-1<t;n?this._scrollToPosition(t,!0):a&&this._scrollToPosition(t-i+1,!0)}}_onOverlayFocus(){this._focused=!0}_onOverlayBlur(){this._focused=!1}_initialPositionChanged(e){this.scrollToDate(e)}_repositionYearScroller(){this._visibleMonthIndex=Math.floor(this.$.monthScroller.position),this.$.yearScroller.position=(this.$.monthScroller.position+this._originDate.getMonth())/12}_repositionMonthScroller(){this.$.monthScroller.position=12*this.$.yearScroller.position-this._originDate.getMonth(),this._visibleMonthIndex=Math.floor(this.$.monthScroller.position)}_onMonthScroll(){this._repositionYearScroller(),this._doIgnoreTaps()}_onYearScroll(){this._repositionMonthScroller(),this._doIgnoreTaps()}_onYearScrollTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300),this._repositionMonthScroller()}_onMonthScrollTouchStart(){this._repositionYearScroller()}_doIgnoreTaps(){this._ignoreTaps=!0,this._debouncer=u.a.debounce(this._debouncer,c.d.after(300),()=>this._ignoreTaps=!1)}_formatDisplayed(e,t,n){return e?t(O._extractDateParts(e)):n}_onTodayTap(){var e=new Date;this.$.monthScroller.position===this._differenceInMonths(e,this._originDate)?(this.selectedDate=e,this._close()):this._scrollToCurrentMonth()}_scrollToCurrentMonth(){this.focusedDate&&(this.focusedDate=new Date),this.scrollToDate(new Date,!0)}_showClear(e){return!!e}_onYearTap(e){if(!this._ignoreTaps&&!this._notTapping){var t=(e.detail.y-(this.$.yearScroller.getBoundingClientRect().top+this.$.yearScroller.clientHeight/2))/this.$.yearScroller.itemHeight;this._scrollToPosition(this.$.monthScroller.position+12*t,!0)}}_scrollToPosition(e,t){if(void 0===this._targetPosition){if(!t)return this.$.monthScroller.position=e,this._targetPosition=void 0,void this._repositionYearScroller();this._targetPosition=e;var n=t?300:0,i=0,a=this.$.monthScroller.position,o=e=>{var t=e-(i=i||e);if(t<n){var r=((e,t,n,i)=>(e/=i/2)<1?n/2*e*e+t:-n/2*(--e*(e-2)-1)+t)(t,a,this._targetPosition-a,n);this.$.monthScroller.position=r,window.requestAnimationFrame(o)}else this.dispatchEvent(new CustomEvent("scroll-animation-finished",{bubbles:!0,composed:!0,detail:{position:this._targetPosition,oldPosition:a}})),this.$.monthScroller.position=this._targetPosition,this._targetPosition=void 0;setTimeout(this._repositionYearScroller.bind(this),1)};window.requestAnimationFrame(o)}else this._targetPosition=e}_limit(e,t){return Math.min(t.max,Math.max(t.min,e))}_handleTrack(e){if(!(Math.abs(e.detail.dx)<10||Math.abs(e.detail.ddy)>10)){Math.abs(e.detail.ddx)>this._yearScrollerWidth/3&&this._toggleAnimateClass(!0);var t=this._translateX+e.detail.ddx;this._translateX=this._limit(t,{min:0,max:this._yearScrollerWidth})}}_track(e){if(!this._desktopMode)switch(e.detail.state){case"start":this._toggleAnimateClass(!1);break;case"track":this._handleTrack(e);break;case"end":this._toggleAnimateClass(!0),this._translateX>=this._yearScrollerWidth/2?this._closeYearScroller():this._openYearScroller()}}_toggleAnimateClass(e){e?this.classList.add("animate"):this.classList.remove("animate")}_toggleYearScroller(){this._isYearScrollerVisible()?this._closeYearScroller():this._openYearScroller()}_openYearScroller(){this._translateX=0,this.setAttribute("years-visible","")}_closeYearScroller(){this.removeAttribute("years-visible"),this._translateX=this._yearScrollerWidth}_isYearScrollerVisible(){return this._translateX<this._yearScrollerWidth/2}_translateXChanged(e){this._desktopMode||(this.$.monthScroller.style.transform="translateX("+(e-this._yearScrollerWidth)+"px)",this.$.yearScroller.style.transform="translateX("+e+"px)")}_yearAfterXYears(e){var t=new Date(this._originDate);return t.setFullYear(parseInt(e)+this._originDate.getFullYear()),t.getFullYear()}_yearAfterXMonths(e){return this._dateAfterXMonths(e).getFullYear()}_dateAfterXMonths(e){var t=new Date(this._originDate);return t.setDate(1),t.setMonth(parseInt(e)+this._originDate.getMonth()),t}_differenceInMonths(e,t){return 12*(e.getFullYear()-t.getFullYear())-t.getMonth()+e.getMonth()}_differenceInYears(e,t){return this._differenceInMonths(e,t)/12}_clear(){this.selectedDate=""}_close(){const e=this.getRootNode().host,t=e?e.getRootNode().host:null;t&&(t.opened=!1),this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}_cancel(){this.focusedDate=this.selectedDate,this._close()}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var t=["down","up","right","left","enter","space","home","end","pageup","pagedown","tab","esc"],n=0;n<t.length;n++){var i=t[n];if(z.a.keyboardEventMatchesKeys(e,i))return i}}_onKeydown(e){var t=this._currentlyFocusedDate();const n=e.composedPath().indexOf(this.$.todayButton)>=0,i=e.composedPath().indexOf(this.$.cancelButton)>=0,a=!n&&!i;var o=this._eventKey(e);if("tab"===o){e.stopPropagation();const t=this.hasAttribute("fullscreen"),o=e.shiftKey;t?e.preventDefault():o&&a||!o&&i?(e.preventDefault(),this.dispatchEvent(new CustomEvent("focus-input",{bubbles:!0,composed:!0}))):o&&n?(this._focused=!0,setTimeout(()=>this.revealDate(this.focusedDate),1)):this._focused=!1}else if(o)switch(e.preventDefault(),e.stopPropagation(),o){case"down":this._moveFocusByDays(7),this.focus();break;case"up":this._moveFocusByDays(-7),this.focus();break;case"right":a&&this._moveFocusByDays(1);break;case"left":a&&this._moveFocusByDays(-1);break;case"enter":a||i?this._close():n&&this._onTodayTap();break;case"space":if(i)this._close();else if(n)this._onTodayTap();else{var r=this.focusedDate;O._dateEquals(r,this.selectedDate)?(this.selectedDate="",this.focusedDate=r):this.selectedDate=r}break;case"home":this._moveFocusInsideMonth(t,"minDate");break;case"end":this._moveFocusInsideMonth(t,"maxDate");break;case"pagedown":this._moveFocusByMonths(e.shiftKey?12:1);break;case"pageup":this._moveFocusByMonths(e.shiftKey?-12:-1);break;case"esc":this._cancel()}}_currentlyFocusedDate(){return this.focusedDate||this.selectedDate||this.initialPosition||new Date}_focusDate(e){this.focusedDate=e,this._focusedMonthDate=e.getDate()}_focusClosestDate(e){this._focusDate(O._getClosestDate(e,[this.minDate,this.maxDate]))}_moveFocusByDays(e){var t=this._currentlyFocusedDate(),n=new Date(0,0);n.setFullYear(t.getFullYear()),n.setMonth(t.getMonth()),n.setDate(t.getDate()+e),this._dateAllowed(n,this.minDate,this.maxDate)?this._focusDate(n):this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusByMonths(e){var t=this._currentlyFocusedDate(),n=new Date(0,0);n.setFullYear(t.getFullYear()),n.setMonth(t.getMonth()+e);var i=n.getMonth();n.setDate(this._focusedMonthDate||(this._focusedMonthDate=t.getDate())),n.getMonth()!==i&&n.setDate(0),this._dateAllowed(n,this.minDate,this.maxDate)?this.focusedDate=n:this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusInsideMonth(e,t){var n=new Date(0,0);n.setFullYear(e.getFullYear()),"minDate"===t?(n.setMonth(e.getMonth()),n.setDate(1)):(n.setMonth(e.getMonth()+1),n.setDate(0)),this._dateAllowed(n,this.minDate,this.maxDate)?this._focusDate(n):this._dateAllowed(e,this.minDate,this.maxDate)?this._focusDate(this[t]):this._focusClosestDate(e)}_dateAllowed(e,t,n){return(!t||e>=t)&&(!n||e<=n)}_isTodayAllowed(e,t){var n=new Date,i=new Date(0,0);return i.setFullYear(n.getFullYear()),i.setMonth(n.getMonth()),i.setDate(n.getDate()),this._dateAllowed(i,e,t)}_stopPropagation(e){e.stopPropagation()}}customElements.define(H.is,H);var L=n(89),W=n(65);const Q=e=>(class extends(Object(W.b)([L.a],e)){static get properties(){return{_selectedDate:{type:Date},_focusedDate:Date,value:{type:String,observer:"_valueChanged",notify:!0,value:""},required:{type:Boolean,value:!1},name:{type:String},initialPosition:String,label:String,opened:{type:Boolean,reflectToAttribute:!0,notify:!0,observer:"_openedChanged"},showWeekNumbers:{type:Boolean},_fullscreen:{value:!1,observer:"_fullscreenChanged"},_fullscreenMediaQuery:{value:"(max-width: 420px), (max-height: 420px)"},_touchPrevented:Array,i18n:{type:Object,value:()=>({monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],weekdays:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],weekdaysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],firstDayOfWeek:0,week:"Week",calendar:"Calendar",clear:"Clear",today:"Today",cancel:"Cancel",formatDate:e=>{const t=String(e.year).replace(/\d+/,e=>"0000".substr(e.length)+e);return[e.month+1,e.day,t].join("/")},parseDate:e=>{const t=e.split("/"),n=new Date;let i,a=n.getMonth(),o=n.getFullYear();if(3===t.length?(o=parseInt(t[2]),t[2].length<3&&o>=0&&(o+=o<50?2e3:1900),a=parseInt(t[0])-1,i=parseInt(t[1])):2===t.length?(a=parseInt(t[0])-1,i=parseInt(t[1])):1===t.length&&(i=parseInt(t[0])),void 0!==i)return{day:i,month:a,year:o}},formatTitle:(e,t)=>e+" "+t})},min:{type:String,observer:"_minChanged"},max:{type:String,observer:"_maxChanged"},_minDate:{type:Date,value:""},_maxDate:{type:Date,value:""},_noInput:{type:Boolean,computed:"_isNoInput(_fullscreen, _ios, i18n, i18n.*)"},_ios:{type:Boolean,value:navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/)},_webkitOverflowScroll:{type:Boolean,value:""===document.createElement("div").style.webkitOverflowScrolling},_ignoreAnnounce:{value:!0},_focusOverlayOnOpen:Boolean}}static get observers(){return["_updateHasValue(value)","_validateInput(_selectedDate, _minDate, _maxDate)","_selectedDateChanged(_selectedDate, i18n.formatDate)","_focusedDateChanged(_focusedDate, i18n.formatDate)","_announceFocusedDate(_focusedDate, opened, _ignoreAnnounce)"]}ready(){super.ready(),this._boundOnScroll=this._onScroll.bind(this),this._boundFocus=this._focus.bind(this),this._boundUpdateAlignmentAndPosition=this._updateAlignmentAndPosition.bind(this),Object(g.b)(this,"tap",this.open),this.addEventListener("touchend",this._preventDefault.bind(this)),this.addEventListener("keydown",this._onKeydown.bind(this)),this._overlayContent.addEventListener("close",this._close.bind(this)),this._overlayContent.addEventListener("focus-input",this._focusAndSelect.bind(this)),this.addEventListener("input",this._onUserInput.bind(this)),this.addEventListener("focus",e=>this._noInput&&e.target.blur())}connectedCallback(){super.connectedCallback(),this.$.overlay.addEventListener("vaadin-overlay-escape-press",this._boundFocus)}disconnectedCallback(){super.disconnectedCallback(),this.$.overlay.removeEventListener("vaadin-overlay-escape-press",this._boundFocus),this.opened=!1}open(){this.disabled||this.readonly||(this.$.overlay.opened=!0)}_close(e){e&&e.stopPropagation(),this._focus(),this.close()}close(){this.$.overlay.close()}get _inputElement(){return this._input()}get _nativeInput(){if(this._inputElement)return this._inputElement.focusElement?this._inputElement.focusElement:this._inputElement.inputElement?this._inputElement.inputElement:window.unwrap?window.unwrap(this._inputElement):this._inputElement}_parseDate(e){var t=/^([-+]\d{1}|\d{2,4}|[-+]\d{6})-(\d{1,2})-(\d{1,2})$/.exec(e);if(t){var n=new Date(0,0);return n.setFullYear(parseInt(t[1],10)),n.setMonth(parseInt(t[2],10)-1),n.setDate(parseInt(t[3],10)),n}}_isNoInput(e,t,n){return!this._inputElement||e||t||!n.parseDate}_formatISO(e){if(!(e instanceof Date))return"";const t=(e,t="00")=>(t+e).substr((t+e).length-t.length);let n="",i="0000",a=e.getFullYear();return a<0?(a=-a,n="-",i="000000"):e.getFullYear()>=1e4&&(n="+",i="000000"),[n+t(a,i),t(e.getMonth()+1),t(e.getDate())].join("-")}_openedChanged(e){e&&this._updateAlignmentAndPosition()}_selectedDateChanged(e,t){if(void 0===e||void 0===t)return;this.__userInputOccurred&&(this.__dispatchChange=!0);const n=e&&t(O._extractDateParts(e)),i=this._formatISO(e);i!==this.value&&(this.validate(n),this.value=i),this.__userInputOccurred=!1,this.__dispatchChange=!1,this._focusedDate=e,this._inputValue=e?n:""}_focusedDateChanged(e,t){void 0!==e&&void 0!==t&&(this.__userInputOccurred=!0,this._ignoreFocusedDateChange||this._noInput||(this._inputValue=e?t(O._extractDateParts(e)):""))}_updateHasValue(e){e?this.setAttribute("has-value",""):this.removeAttribute("has-value")}_handleDateChange(e,t,n){if(t){var i=this._parseDate(t);i?O._dateEquals(this[e],i)||(this[e]=i):this.value=n}else this[e]=""}_valueChanged(e,t){this.__dispatchChange&&this.dispatchEvent(new CustomEvent("change",{bubbles:!0})),this._handleDateChange("_selectedDate",e,t)}_minChanged(e,t){this._handleDateChange("_minDate",e,t)}_maxChanged(e,t){this._handleDateChange("_maxDate",e,t)}_updateAlignmentAndPosition(){if(!this._fullscreen){const e=this._inputElement.getBoundingClientRect(),t=e.top>window.innerHeight/2;if(e.left+this.clientWidth/2>window.innerWidth/2){const t=Math.min(window.innerWidth,document.documentElement.clientWidth);this.$.overlay.setAttribute("right-aligned",""),this.$.overlay.style.removeProperty("left"),this.$.overlay.style.right=t-e.right+"px"}else this.$.overlay.removeAttribute("right-aligned"),this.$.overlay.style.removeProperty("right"),this.$.overlay.style.left=e.left+"px";if(t){const t=Math.min(window.innerHeight,document.documentElement.clientHeight);this.$.overlay.setAttribute("bottom-aligned",""),this.$.overlay.style.removeProperty("top"),this.$.overlay.style.bottom=t-e.top+"px"}else this.$.overlay.removeAttribute("bottom-aligned"),this.$.overlay.style.removeProperty("bottom"),this.$.overlay.style.top=e.bottom+"px"}this._overlayContent._repositionYearScroller()}_fullscreenChanged(){this.$.overlay.opened&&this._updateAlignmentAndPosition()}_onOverlayOpened(){this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring");var e=this._parseDate(this.initialPosition),t=this._selectedDate||this._overlayContent.initialPosition||e||new Date;e||O._dateAllowed(t,this._minDate,this._maxDate)?this._overlayContent.initialPosition=t:this._overlayContent.initialPosition=O._getClosestDate(t,[this._minDate,this._maxDate]),this._overlayContent.scrollToDate(this._overlayContent.focusedDate||this._overlayContent.initialPosition),this._ignoreFocusedDateChange=!0,this._overlayContent.focusedDate=this._overlayContent.focusedDate||this._overlayContent.initialPosition,this._ignoreFocusedDateChange=!1,window.addEventListener("scroll",this._boundOnScroll,!0),this.addEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._webkitOverflowScroll&&(this._touchPrevented=this._preventWebkitOverflowScrollingTouch(this.parentElement)),this._focusOverlayOnOpen?(this._overlayContent.focus(),this._focusOverlayOnOpen=!1):this._focus(),this._noInput&&this.focusElement&&this.focusElement.blur(),this.updateStyles(),this._ignoreAnnounce=!1}_preventWebkitOverflowScrollingTouch(e){for(var t=[];e;){if("touch"===window.getComputedStyle(e).webkitOverflowScrolling){var n=e.style.webkitOverflowScrolling;e.style.webkitOverflowScrolling="auto",t.push({element:e,oldInlineValue:n})}e=e.parentElement}return t}_onOverlayClosed(){if(this._ignoreAnnounce=!0,window.removeEventListener("scroll",this._boundOnScroll,!0),this.removeEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._touchPrevented&&(this._touchPrevented.forEach(e=>e.element.style.webkitOverflowScrolling=e.oldInlineValue),this._touchPrevented=[]),this.updateStyles(),this._ignoreFocusedDateChange=!0,this.i18n.parseDate){var e=this._inputValue||"";const t=this.i18n.parseDate(e),n=t&&this._parseDate(`${t.year}-${t.month+1}-${t.day}`);this._isValidDate(n)?this._selectedDate=n:(this._selectedDate=null,this._inputValue=e)}else this._focusedDate&&(this._selectedDate=this._focusedDate);this._ignoreFocusedDateChange=!1,this._nativeInput&&this._nativeInput.selectionStart&&(this._nativeInput.selectionStart=this._nativeInput.selectionEnd),this.validate()}validate(e){return this.invalid=!1,e=void 0!==e?e:this._inputValue,!(this.invalid=!this.checkValidity(e))}checkValidity(e){var t=!e||this._selectedDate&&e===this.i18n.formatDate(O._extractDateParts(this._selectedDate)),n=!this._selectedDate||O._dateAllowed(this._selectedDate,this._minDate,this._maxDate),i=!0;return this._inputElement&&(this._inputElement.checkValidity?i=this._inputElement.checkValidity(e):this._inputElement.validate&&(i=this._inputElement.validate(e))),t&&n&&i}_onScroll(e){e.target!==window&&this._overlayContent.contains(e.target)||this._updateAlignmentAndPosition()}_focus(){this._noInput?this._overlayContent.focus():this._inputElement.focus()}_focusAndSelect(){this._focus(),this._setSelectionRange(0,this._inputValue.length)}_setSelectionRange(e,t){this._nativeInput&&this._nativeInput.setSelectionRange&&this._nativeInput.setSelectionRange(e,t)}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var t=["down","up","enter","esc","tab"],n=0;n<t.length;n++){var i=t[n];if(z.a.keyboardEventMatchesKeys(e,i))return i}}_isValidDate(e){return e&&!isNaN(e.getTime())}_onKeydown(e){if(this._noInput){-1===[9].indexOf(e.keyCode)&&e.preventDefault()}switch(this._eventKey(e)){case"down":case"up":e.preventDefault(),this.opened?(this._overlayContent.focus(),this._overlayContent._onKeydown(e)):(this._focusOverlayOnOpen=!0,this.open());break;case"enter":this._overlayContent.focusedDate&&(this._selectedDate=this._overlayContent.focusedDate),this.close();break;case"esc":this._focusedDate=this._selectedDate,this._close();break;case"tab":this.opened&&(e.preventDefault(),this._setSelectionRange(0,0),e.shiftKey?this._overlayContent.focusCancel():(this._overlayContent.focus(),this._overlayContent.revealDate(this._focusedDate)))}}_validateInput(e,t,n){e&&(t||n)&&(this.invalid=!O._dateAllowed(e,t,n))}_onUserInput(e){this.opened||this.open(),this._userInputValueChanged()}_userInputValueChanged(e){if(this.opened&&this._inputValue){const e=this.i18n.parseDate&&this.i18n.parseDate(this._inputValue),t=e&&this._parseDate(`${e.year}-${e.month+1}-${e.day}`);this._isValidDate(t)&&(this._ignoreFocusedDateChange=!0,O._dateEquals(t,this._focusedDate)||(this._focusedDate=t),this._ignoreFocusedDateChange=!1)}}_announceFocusedDate(e,t,n){t&&!n&&this._overlayContent.announceFocusedDate()}get _overlayContent(){return this.$.overlay.content.querySelector("#overlay-content")}});class N extends(y(d(Object(l.a)(Object(I.a)(Q(Object(s.a)(r.a))))))){static get template(){return i.a`
    <style>
      :host {
        display: inline-block;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host([opened]) {
        pointer-events: auto;
      }

      [part="text-field"] {
        width: 100%;
        min-width: 0;
      }

      [part="clear-button"],
      [part="toggle-button"] {
        font-family: 'vaadin-date-picker-icons';
      }

      [part="clear-button"]::before {
        content: "\\e901";
      }

      [part="toggle-button"]::before {
        content: "\\e902";
      }

      :host([disabled]) [part="clear-button"],
      :host([readonly]) [part="clear-button"],
      :host(:not([has-value])) [part="clear-button"] {
        display: none;
      }
    </style>


    <vaadin-text-field id="input" role="application" autocomplete="off" on-focus="_focus" value="{{_userInputValue}}" invalid="[[invalid]]" label="[[label]]" name="[[name]]" placeholder="[[placeholder]]" required="[[required]]" disabled="[[disabled]]" readonly="[[readonly]]" error-message="[[errorMessage]]" aria-label\$="[[label]]" part="text-field" theme\$="[[theme]]">
      <slot name="prefix" slot="prefix"></slot>
      <div part="clear-button" slot="suffix" on-touchend="_clearTouchend" on-click="_clear" role="button" aria-label\$="[[i18n.clear]]"></div>
      <div part="toggle-button" slot="suffix" on-tap="_toggle" role="button" aria-label\$="[[i18n.calendar]]" aria-expanded\$="[[_getAriaExpanded(opened)]]"></div>
    </vaadin-text-field>

    <vaadin-date-picker-overlay id="overlay" opened="{{opened}}" fullscreen\$="[[_fullscreen]]" theme\$="[[theme]]" on-vaadin-overlay-open="_onOverlayOpened" on-vaadin-overlay-close="_onOverlayClosed">
      <template>
        <vaadin-date-picker-overlay-content id="overlay-content" i18n="[[i18n]]" fullscreen\$="[[_fullscreen]]" label="[[label]]" selected-date="{{_selectedDate}}" slot="dropdown-content" focused-date="{{_focusedDate}}" show-week-numbers="[[showWeekNumbers]]" min-date="[[_minDate]]" max-date="[[_maxDate]]" role="dialog" on-date-tap="_close" part="overlay-content" theme\$="[[theme]]">
        </vaadin-date-picker-overlay-content>
      </template>
    </vaadin-date-picker-overlay>

    <iron-media-query query="[[_fullscreenMediaQuery]]" query-matches="{{_fullscreen}}">
    </iron-media-query>
`}static get is(){return"vaadin-date-picker"}static get version(){return"3.3.1"}static get properties(){return{disabled:{type:Boolean,value:!1,reflectToAttribute:!0},errorMessage:String,placeholder:String,readonly:{type:Boolean,value:!1,reflectToAttribute:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_userInputValue:String}}static get observers(){return["_userInputValueChanged(_userInputValue)"]}ready(){super.ready(),Object(V.a)(this,()=>this._inputElement.validate=(()=>{})),this._overlayContent.addEventListener("focus",()=>this.focusElement._setFocused(!0)),this.$.overlay.addEventListener("vaadin-overlay-close",this._onVaadinOverlayClose.bind(this))}_onVaadinOverlayClose(e){this._openedWithFocusRing&&this.hasAttribute("focused")?this.focusElement.setAttribute("focus-ring",""):this.hasAttribute("focused")||this.focusElement.blur(),e.detail.sourceEvent&&-1!==e.detail.sourceEvent.composedPath().indexOf(this)&&e.preventDefault()}_clear(){this.__dispatchChange=!0,this.value="",this.validate(),this.focus(),Object(g.d)("tap"),this.__dispatchChange=!1}_clearTouchend(e){this._clear(),e.preventDefault(),Object(g.d)("tap")}_toggle(e){e.stopPropagation(),this[this.$.overlay.opened?"close":"open"]()}_input(){return this.$.input}set _inputValue(e){this._inputElement.value=e}get _inputValue(){return this._inputElement.value}_getAriaExpanded(e){return Boolean(e).toString()}get focusElement(){return this._input()||this}}customElements.define(N.is,N)},85:function(e,t,n){"use strict";n(2),n(105),n(106),n(107),n(108);var i=n(57),a=(n(38),n(4)),o=n(3),r=n(88);Object(a.a)({is:"paper-input",_template:o.a`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate\$="[[autoValidate]]" disabled\$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden\$="[[!label]]" aria-hidden="true" for\$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id\$="[[_inputId]]" maxlength\$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby\$="[[_ariaLabelledBy]]" aria-describedby\$="[[_ariaDescribedBy]]" disabled\$="[[disabled]]" title\$="[[title]]" type\$="[[type]]" pattern\$="[[pattern]]" required\$="[[required]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]" min\$="[[min]]" max\$="[[max]]" step\$="[[step]]" name\$="[[name]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" list\$="[[list]]" size\$="[[size]]" autocapitalize\$="[[autocapitalize]]" autocorrect\$="[[autocorrect]]" on-change="_onChange" tabindex\$="[[tabIndex]]" autosave\$="[[autosave]]" results\$="[[results]]" accept\$="[[accept]]" multiple\$="[[multiple]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[r.a,i.a],properties:{value:{type:String}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}})},87:function(e,t,n){"use strict";n.d(t,"a",function(){return o});n(2);var i=n(4),a=n(3);const o=Object(i.a)({_template:a.a`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live\$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){o.instance||(o.instance=this),document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(e){this._text="",this.async(function(){this._text=e},100)},_onIronAnnounce:function(e){e.detail&&e.detail.text&&this.announce(e.detail.text)}});o.instance=null,o.requestAvailability=function(){o.instance||(o.instance=document.createElement("iron-a11y-announcer")),document.body.appendChild(o.instance)}}}]);
//# sourceMappingURL=8ef413e96faeca8ea66b.chunk.js.map