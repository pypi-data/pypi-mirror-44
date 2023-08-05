/*! For license information please see b44440c3a88c32e13e25.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[24],{113:function(i,e,n){"use strict";n(2);const t={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(i,e){for(var n in e)i[n]=e[n]},_cloneConfig:function(i){var e={isClone:!0};return this._copyProperties(e,i),e},_getAnimationConfigRecursive:function(i,e,n){var t;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(t=i?this.animationConfig[i]:this.animationConfig,Array.isArray(t)||(t=[t]),t)for(var a,o=0;a=t[o];o++)if(a.animatable)a.animatable._getAnimationConfigRecursive(a.type||i,e,n);else if(a.id){var s=e[a.id];s?(s.isClone||(e[a.id]=this._cloneConfig(s),s=e[a.id]),this._copyProperties(s,a)):e[a.id]=a}else n.push(a)},getAnimationConfig:function(i){var e={},n=[];for(var t in this._getAnimationConfigRecursive(i,e,n),e)n.push(e[t]);return n}};n.d(e,"a",function(){return a});const a=[t,{_configureAnimations:function(i){var e=[],n=[];if(i.length>0)for(let e,t=0;e=i[t];t++){let i=document.createElement(e.name);if(i.isNeonAnimation){let t=null;i.configure||(i.configure=function(i){return null}),t=i.configure(e),n.push({result:t,config:e,neonAnimation:i})}else console.warn(this.is+":",e.name,"not found!")}for(var t=0;t<n.length;t++){let i=n[t].result,a=n[t].config,o=n[t].neonAnimation;try{"function"!=typeof i.cancel&&(i=document.timeline.play(i))}catch(e){i=null,console.warn("Couldnt play","(",a.name,").",e)}i&&e.push({neonAnimation:o,config:a,animation:i})}return e},_shouldComplete:function(i){for(var e=!0,n=0;n<i.length;n++)if("finished"!=i[n].animation.playState){e=!1;break}return e},_complete:function(i){for(var e=0;e<i.length;e++)i[e].neonAnimation.complete(i[e].config);for(e=0;e<i.length;e++)i[e].animation.cancel()},playAnimation:function(i,e){var n=this.getAnimationConfig(i);if(n){this._active=this._active||{},this._active[i]&&(this._complete(this._active[i]),delete this._active[i]);var t=this._configureAnimations(n);if(0!=t.length){this._active[i]=t;for(var a=0;a<t.length;a++)t[a].animation.onfinish=function(){this._shouldComplete(t)&&(this._complete(t),delete this._active[i],this.fire("neon-animation-finish",e,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",e,{bubbles:!1})}},cancelAnimation:function(){for(var i in this._active){var e=this._active[i];for(var n in e)e[n].animation.cancel()}this._active={}}}]},176:function(i,e,n){"use strict";n(2),n(54),n(141);var t=n(4),a=n(3),o=n(116);const s=a.a`
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
`;s.setAttribute("strip-whitespace",""),Object(t.a)({_template:s,is:"paper-spinner",behaviors:[o.a]})},178:function(i,e,n){"use strict";n.d(e,"b",function(){return o}),n.d(e,"a",function(){return s});n(2);var t=n(77),a=n(0);const o={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(i,e){e&&(i?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(i){this.closingReason=this.closingReason||{},this.closingReason.confirmed=i},_onDialogClick:function(i){for(var e=Object(a.b)(i).path,n=0,t=e.indexOf(this);n<t;n++){var o=e[n];if(o.hasAttribute&&(o.hasAttribute("dialog-dismiss")||o.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(o.hasAttribute("dialog-confirm")),this.close(),i.stopPropagation();break}}}},s=[t.a,o]},186:function(i,e,n){"use strict";n(2),n(187);var t=n(113),a=n(178),o=n(4),s=n(3);Object(o.a)({_template:s.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[a.a,t.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},187:function(i,e,n){"use strict";n(2),n(40),n(41),n(50),n(76);const t=document.createElement("template");t.setAttribute("style","display: none;"),t.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(t.content)},790:function(i,e,n){"use strict";n.r(e);n(75),n(186),n(176);var t=n(3),a=n(20),o=(n(86),n(110));customElements.define("ha-dialog-add-user",class extends(Object(o.a)(a.a)){static get template(){return t.a`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        paper-dialog {
          max-width: 500px;
        }
        .username {
          margin-top: -8px;
        }
      </style>
      <paper-dialog
        id="dialog"
        with-backdrop
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>[[localize('ui.panel.config.users.add_user.caption')]]</h2>
        <div>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <paper-input
            class="name"
            label="[[localize('ui.panel.config.users.add_user.name')]]"
            value="{{_name}}"
            required
            auto-validate
            autocapitalize="on"
            error-message="Required"
            on-blur="_maybePopulateUsername"
          ></paper-input>
          <paper-input
            class="username"
            label="[[localize('ui.panel.config.users.add_user.username')]]"
            value="{{_username}}"
            required
            auto-validate
            autocapitalize="none"
            error-message="Required"
          ></paper-input>
          <paper-input
            label="[[localize('ui.panel.config.users.add_user.password')]]"
            type="password"
            value="{{_password}}"
            required
            auto-validate
            error-message="Required"
          ></paper-input>
        </div>
        <div class="buttons">
          <template is="dom-if" if="[[_loading]]">
            <div class="submit-spinner">
              <paper-spinner active></paper-spinner>
            </div>
          </template>
          <template is="dom-if" if="[[!_loading]]">
            <mwc-button on-click="_createUser"
              >[[localize('ui.panel.config.users.add_user.create')]]</mwc-button
            >
          </template>
        </div>
      </paper-dialog>
    `}static get properties(){return{_hass:Object,_dialogClosedCallback:Function,_loading:{type:Boolean,value:!1},_errorMsg:String,_opened:{type:Boolean,value:!1},_name:String,_username:String,_password:String}}ready(){super.ready(),this.addEventListener("keypress",i=>{13===i.keyCode&&this._createUser()})}showDialog({hass:i,dialogClosedCallback:e}){this.hass=i,this._dialogClosedCallback=e,this._loading=!1,this._opened=!0,setTimeout(()=>this.shadowRoot.querySelector("paper-input").focus(),0)}_maybePopulateUsername(){if(this._username)return;const i=this._name.split(" ");i.length&&(this._username=i[0].toLowerCase())}async _createUser(){if(!this._name||!this._username||!this._password)return;let i;this._loading=!0,this._errorMsg=null;try{i=(await this.hass.callWS({type:"config/auth/create",name:this._name})).user.id}catch(i){return this._loading=!1,void(this._errorMsg=i.code)}try{await this.hass.callWS({type:"config/auth_provider/homeassistant/create",user_id:i,username:this._username,password:this._password})}catch(e){return this._loading=!1,this._errorMsg=e.code,void await this.hass.callWS({type:"config/auth/delete",user_id:i})}this._dialogDone(i)}_dialogDone(i){this._dialogClosedCallback({userId:i}),this.setProperties({_errorMsg:null,_username:"",_password:"",_dialogClosedCallback:null,_opened:!1})}_equals(i,e){return i===e}_openedChanged(i){this._dialogClosedCallback&&!i.detail.value&&this._dialogDone()}})}}]);
//# sourceMappingURL=b44440c3a88c32e13e25.chunk.js.map