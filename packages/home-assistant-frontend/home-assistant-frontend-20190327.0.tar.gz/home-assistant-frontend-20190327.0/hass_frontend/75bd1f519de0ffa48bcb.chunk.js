/*! For license information please see 75bd1f519de0ffa48bcb.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[100],{113:function(t,i,n){"use strict";n(2);const e={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,i){for(var n in i)t[n]=i[n]},_cloneConfig:function(t){var i={isClone:!0};return this._copyProperties(i,t),i},_getAnimationConfigRecursive:function(t,i,n){var e;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(e=t?this.animationConfig[t]:this.animationConfig,Array.isArray(e)||(e=[e]),e)for(var o,a=0;o=e[a];a++)if(o.animatable)o.animatable._getAnimationConfigRecursive(o.type||t,i,n);else if(o.id){var s=i[o.id];s?(s.isClone||(i[o.id]=this._cloneConfig(s),s=i[o.id]),this._copyProperties(s,o)):i[o.id]=o}else n.push(o)},getAnimationConfig:function(t){var i={},n=[];for(var e in this._getAnimationConfigRecursive(t,i,n),i)n.push(i[e]);return n}};n.d(i,"a",function(){return o});const o=[e,{_configureAnimations:function(t){var i=[],n=[];if(t.length>0)for(let i,e=0;i=t[e];e++){let t=document.createElement(i.name);if(t.isNeonAnimation){let e=null;t.configure||(t.configure=function(t){return null}),e=t.configure(i),n.push({result:e,config:i,neonAnimation:t})}else console.warn(this.is+":",i.name,"not found!")}for(var e=0;e<n.length;e++){let t=n[e].result,o=n[e].config,a=n[e].neonAnimation;try{"function"!=typeof t.cancel&&(t=document.timeline.play(t))}catch(i){t=null,console.warn("Couldnt play","(",o.name,").",i)}t&&i.push({neonAnimation:a,config:o,animation:t})}return i},_shouldComplete:function(t){for(var i=!0,n=0;n<t.length;n++)if("finished"!=t[n].animation.playState){i=!1;break}return i},_complete:function(t){for(var i=0;i<t.length;i++)t[i].neonAnimation.complete(t[i].config);for(i=0;i<t.length;i++)t[i].animation.cancel()},playAnimation:function(t,i){var n=this.getAnimationConfig(t);if(n){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var e=this._configureAnimations(n);if(0!=e.length){this._active[t]=e;for(var o=0;o<e.length;o++)e[o].animation.onfinish=function(){this._shouldComplete(e)&&(this._complete(e),delete this._active[t],this.fire("neon-animation-finish",i,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",i,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var i=this._active[t];for(var n in i)i[n].animation.cancel()}this._active={}}}]},178:function(t,i,n){"use strict";n.d(i,"b",function(){return a}),n.d(i,"a",function(){return s});n(2);var e=n(77),o=n(0);const a={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,i){i&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var i=Object(o.b)(t).path,n=0,e=i.indexOf(this);n<e;n++){var a=i[n];if(a.hasAttribute&&(a.hasAttribute("dialog-dismiss")||a.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(a.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},s=[e.a,a]},186:function(t,i,n){"use strict";n(2),n(187);var e=n(113),o=n(178),a=n(4),s=n(3);Object(a.a)({_template:s.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[o.a,e.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},187:function(t,i,n){"use strict";n(2),n(40),n(41),n(50),n(76);const e=document.createElement("template");e.setAttribute("style","display: none;"),e.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(e.content)},196:function(t,i,n){"use strict";n(2),n(40),n(41);var e=n(178),o=n(4),a=n(3);Object(o.a)({_template:a.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(e.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},764:function(t,i,n){"use strict";n.r(i);var e=n(5),o=(n(186),n(196),n(52));customElements.define("dialog-system-log-detail",class extends e.a{constructor(...t){super(...t),this._params=void 0}static get properties(){return{_params:{}}}async showDialog(t){this._params=t,await this.updateComplete}render(){if(!this._params)return e.e``;const t=this._params.item;return e.e`
      <paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>Log Details (${t.level})</h2>
        <paper-dialog-scrollable>
          <p>${new Date(1e3*t.timestamp)}</p>
          ${t.message?e.e`
                <pre>${t.message}</pre>
              `:e.e``}
          ${t.exception?e.e`
                <pre>${t.exception}</pre>
              `:e.e``}
        </paper-dialog-scrollable>
      </paper-dialog>
    `}_openedChanged(t){t.detail.value||(this._params=void 0)}static get styles(){return[o.b,e.c`
        paper-dialog {
          direction: ltr;
        }
      `]}})}}]);
//# sourceMappingURL=75bd1f519de0ffa48bcb.chunk.js.map