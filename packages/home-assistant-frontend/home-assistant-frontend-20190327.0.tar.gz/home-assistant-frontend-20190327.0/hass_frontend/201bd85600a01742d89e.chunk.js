/*! For license information please see 201bd85600a01742d89e.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[93,127,130],{111:function(e,t,i){"use strict";i.d(t,"a",function(){return o});i(2);var a=i(51),n=i(32);const o=[a.a,n.a,{hostAttributes:{role:"option",tabindex:"0"}}]},114:function(e,t,i){"use strict";i(2);var a=i(57),n=i(58);const o={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},r=[a.a,n.a,o];var s=i(55),l=i(62);i.d(t,"a",function(){return d});const p={_checkedChanged:function(){o._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){l.a._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},d=[s.a,r,p]},131:function(e,t,i){"use strict";i(2),i(40),i(132);var a=i(4),n=i(3),o=i(111);Object(a.a)({_template:n.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[o.a]})},132:function(e,t,i){"use strict";i(40),i(54),i(41),i(50);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(a.content)},134:function(e,t,i){"use strict";i(2),i(30),i(100),i(85),i(138),i(102),i(41),i(136),i(137);var a=i(51),n=i(32),o=i(57),r=i(58),s=i(4),l=i(0),p=i(33),d=i(3);Object(s.a)({_template:d.a`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[a.a,n.a,o.a,r.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.b)(this.$.content).getDistributedNodes(),t=0,i=e.length;t<i;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},136:function(e,t,i){"use strict";i(78);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<iron-iconset-svg name="paper-dropdown-menu" size="24">\n<svg><defs>\n<g id="arrow-drop-down"><path d="M7 10l5 5 5-5z"></path></g>\n</defs></svg>\n</iron-iconset-svg>',document.head.appendChild(a.content)},137:function(e,t,i){"use strict";i(41);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<dom-module id="paper-dropdown-menu-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        text-align: left;\n\n        /* NOTE(cdata): Both values are needed, since some phones require the\n         * value to be `transparent`.\n         */\n        -webkit-tap-highlight-color: rgba(0,0,0,0);\n        -webkit-tap-highlight-color: transparent;\n\n        --paper-input-container-input: {\n          overflow: hidden;\n          white-space: nowrap;\n          text-overflow: ellipsis;\n          max-width: 100%;\n          box-sizing: border-box;\n          cursor: pointer;\n        };\n\n        @apply --paper-dropdown-menu;\n      }\n\n      :host([disabled]) {\n        @apply --paper-dropdown-menu-disabled;\n      }\n\n      :host([noink]) paper-ripple {\n        display: none;\n      }\n\n      :host([no-label-float]) paper-ripple {\n        top: 8px;\n      }\n\n      paper-ripple {\n        top: 12px;\n        left: 0px;\n        bottom: 8px;\n        right: 0px;\n\n        @apply --paper-dropdown-menu-ripple;\n      }\n\n      paper-menu-button {\n        display: block;\n        padding: 0;\n\n        @apply --paper-dropdown-menu-button;\n      }\n\n      paper-input {\n        @apply --paper-dropdown-menu-input;\n      }\n\n      iron-icon {\n        color: var(--disabled-text-color);\n\n        @apply --paper-dropdown-menu-icon;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(a.content)},166:function(e,t,i){"use strict";i(2),i(40),i(175),i(174),i(41);var a=i(4),n=i(3);Object(a.a)({_template:n.a`
    <style include="paper-material-styles">
      :host {
        display: inline-block;
        position: relative;
        box-sizing: border-box;
        background-color: var(--paper-card-background-color, var(--primary-background-color));
        border-radius: 2px;

        @apply --paper-font-common-base;
        @apply --paper-card;
      }

      /* IE 10 support for HTML5 hidden attr */
      :host([hidden]), [hidden] {
        display: none !important;
      }

      .header {
        position: relative;
        border-top-left-radius: inherit;
        border-top-right-radius: inherit;
        overflow: hidden;

        @apply --paper-card-header;
      }

      .header iron-image {
        display: block;
        width: 100%;
        --iron-image-width: 100%;
        pointer-events: none;

        @apply --paper-card-header-image;
      }

      .header .title-text {
        padding: 16px;
        font-size: 24px;
        font-weight: 400;
        color: var(--paper-card-header-color, #000);

        @apply --paper-card-header-text;
      }

      .header .title-text.over-image {
        position: absolute;
        bottom: 0px;

        @apply --paper-card-header-image-text;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
        position:relative;

        @apply --paper-card-content;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid #e8e8e8;
        padding: 5px 16px;
        position:relative;

        @apply --paper-card-actions;
      }

      :host([elevation="1"]) {
        @apply --paper-material-elevation-1;
      }

      :host([elevation="2"]) {
        @apply --paper-material-elevation-2;
      }

      :host([elevation="3"]) {
        @apply --paper-material-elevation-3;
      }

      :host([elevation="4"]) {
        @apply --paper-material-elevation-4;
      }

      :host([elevation="5"]) {
        @apply --paper-material-elevation-5;
      }
    </style>

    <div class="header">
      <iron-image hidden\$="[[!image]]" aria-hidden\$="[[_isHidden(image)]]" src="[[image]]" alt="[[alt]]" placeholder="[[placeholderImage]]" preload="[[preloadImage]]" fade="[[fadeImage]]"></iron-image>
      <div hidden\$="[[!heading]]" class\$="title-text [[_computeHeadingClass(image)]]">[[heading]]</div>
    </div>

    <slot></slot>
`,is:"paper-card",properties:{heading:{type:String,value:"",observer:"_headingChanged"},image:{type:String,value:""},alt:{type:String},preloadImage:{type:Boolean,value:!1},fadeImage:{type:Boolean,value:!1},placeholderImage:{type:String,value:null},elevation:{type:Number,value:1,reflectToAttribute:!0},animatedShadow:{type:Boolean,value:!1},animated:{type:Boolean,reflectToAttribute:!0,readOnly:!0,computed:"_computeAnimated(animatedShadow)"}},_isHidden:function(e){return e?"false":"true"},_headingChanged:function(e){var t=this.getAttribute("heading"),i=this.getAttribute("aria-label");"string"==typeof i&&i!==t||this.setAttribute("aria-label",e)},_computeHeadingClass:function(e){return e?" over-image":""},_computeAnimated:function(e){return e}})},167:function(e,t,i){"use strict";i(2);const a=i(3).a`
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
`;a.setAttribute("style","display: none;"),document.head.appendChild(a.content)},172:function(e,t,i){"use strict";i(2),i(40),i(41),i(50);var a=i(4),n=i(3);Object(a.a)({_template:n.a`
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
`,is:"paper-item-body"})},174:function(e,t,i){"use strict";i(2),i(76);const a=i(3).a`
<dom-module id="paper-material-styles">
  <template>
    <style>
      html {
        --paper-material: {
          display: block;
          position: relative;
        };
        --paper-material-elevation-1: {
          @apply --shadow-elevation-2dp;
        };
        --paper-material-elevation-2: {
          @apply --shadow-elevation-4dp;
        };
        --paper-material-elevation-3: {
          @apply --shadow-elevation-6dp;
        };
        --paper-material-elevation-4: {
          @apply --shadow-elevation-8dp;
        };
        --paper-material-elevation-5: {
          @apply --shadow-elevation-16dp;
        };
      }
      .paper-material {
        @apply --paper-material;
      }
      .paper-material[elevation="1"] {
        @apply --paper-material-elevation-1;
      }
      .paper-material[elevation="2"] {
        @apply --paper-material-elevation-2;
      }
      .paper-material[elevation="3"] {
        @apply --paper-material-elevation-3;
      }
      .paper-material[elevation="4"] {
        @apply --paper-material-elevation-4;
      }
      .paper-material[elevation="5"] {
        @apply --paper-material-elevation-5;
      }

      /* Duplicate the styles because of https://github.com/webcomponents/shadycss/issues/193 */
      :host {
        --paper-material: {
          display: block;
          position: relative;
        };
        --paper-material-elevation-1: {
          @apply --shadow-elevation-2dp;
        };
        --paper-material-elevation-2: {
          @apply --shadow-elevation-4dp;
        };
        --paper-material-elevation-3: {
          @apply --shadow-elevation-6dp;
        };
        --paper-material-elevation-4: {
          @apply --shadow-elevation-8dp;
        };
        --paper-material-elevation-5: {
          @apply --shadow-elevation-16dp;
        };
      }
      :host(.paper-material) {
        @apply --paper-material;
      }
      :host(.paper-material[elevation="1"]) {
        @apply --paper-material-elevation-1;
      }
      :host(.paper-material[elevation="2"]) {
        @apply --paper-material-elevation-2;
      }
      :host(.paper-material[elevation="3"]) {
        @apply --paper-material-elevation-3;
      }
      :host(.paper-material[elevation="4"]) {
        @apply --paper-material-elevation-4;
      }
      :host(.paper-material[elevation="5"]) {
        @apply --paper-material-elevation-5;
      }
    </style>
  </template>
</dom-module>`;a.setAttribute("style","display: none;"),document.head.appendChild(a.content)},175:function(e,t,i){"use strict";i(2);var a=i(4),n=i(3),o=i(16);Object(a.a)({_template:n.a`
    <style>
      :host {
        display: inline-block;
        overflow: hidden;
        position: relative;
      }

      #baseURIAnchor {
        display: none;
      }

      #sizedImgDiv {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        display: none;
      }

      #img {
        display: block;
        width: var(--iron-image-width, auto);
        height: var(--iron-image-height, auto);
      }

      :host([sizing]) #sizedImgDiv {
        display: block;
      }

      :host([sizing]) #img {
        display: none;
      }

      #placeholder {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        background-color: inherit;
        opacity: 1;

        @apply --iron-image-placeholder;
      }

      #placeholder.faded-out {
        transition: opacity 0.5s linear;
        opacity: 0;
      }
    </style>

    <a id="baseURIAnchor" href="#"></a>
    <div id="sizedImgDiv" role="img" hidden\$="[[_computeImgDivHidden(sizing)]]" aria-hidden\$="[[_computeImgDivARIAHidden(alt)]]" aria-label\$="[[_computeImgDivARIALabel(alt, src)]]"></div>
    <img id="img" alt\$="[[alt]]" hidden\$="[[_computeImgHidden(sizing)]]" crossorigin\$="[[crossorigin]]" on-load="_imgOnLoad" on-error="_imgOnError">
    <div id="placeholder" hidden\$="[[_computePlaceholderHidden(preload, fade, loading, loaded)]]" class\$="[[_computePlaceholderClassName(preload, fade, loading, loaded)]]"></div>
`,is:"iron-image",properties:{src:{type:String,value:""},alt:{type:String,value:null},crossorigin:{type:String,value:null},preventLoad:{type:Boolean,value:!1},sizing:{type:String,value:null,reflectToAttribute:!0},position:{type:String,value:"center"},preload:{type:Boolean,value:!1},placeholder:{type:String,value:null,observer:"_placeholderChanged"},fade:{type:Boolean,value:!1},loaded:{notify:!0,readOnly:!0,type:Boolean,value:!1},loading:{notify:!0,readOnly:!0,type:Boolean,value:!1},error:{notify:!0,readOnly:!0,type:Boolean,value:!1},width:{observer:"_widthChanged",type:Number,value:null},height:{observer:"_heightChanged",type:Number,value:null}},observers:["_transformChanged(sizing, position)","_loadStateObserver(src, preventLoad)"],created:function(){this._resolvedSrc=""},_imgOnLoad:function(){this.$.img.src===this._resolveSrc(this.src)&&(this._setLoading(!1),this._setLoaded(!0),this._setError(!1))},_imgOnError:function(){this.$.img.src===this._resolveSrc(this.src)&&(this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",this._setLoading(!1),this._setLoaded(!1),this._setError(!0))},_computePlaceholderHidden:function(){return!this.preload||!this.fade&&!this.loading&&this.loaded},_computePlaceholderClassName:function(){return this.preload&&this.fade&&!this.loading&&this.loaded?"faded-out":""},_computeImgDivHidden:function(){return!this.sizing},_computeImgDivARIAHidden:function(){return""===this.alt?"true":void 0},_computeImgDivARIALabel:function(){return null!==this.alt?this.alt:""===this.src?"":this._resolveSrc(this.src).replace(/[?|#].*/g,"").split("/").pop()},_computeImgHidden:function(){return!!this.sizing},_widthChanged:function(){this.style.width=isNaN(this.width)?this.width:this.width+"px"},_heightChanged:function(){this.style.height=isNaN(this.height)?this.height:this.height+"px"},_loadStateObserver:function(e,t){var i=this._resolveSrc(e);i!==this._resolvedSrc&&(this._resolvedSrc="",this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",""===e||t?(this._setLoading(!1),this._setLoaded(!1),this._setError(!1)):(this._resolvedSrc=i,this.$.img.src=this._resolvedSrc,this.$.sizedImgDiv.style.backgroundImage='url("'+this._resolvedSrc+'")',this._setLoading(!0),this._setLoaded(!1),this._setError(!1)))},_placeholderChanged:function(){this.$.placeholder.style.backgroundImage=this.placeholder?'url("'+this.placeholder+'")':""},_transformChanged:function(){var e=this.$.sizedImgDiv.style,t=this.$.placeholder.style;e.backgroundSize=t.backgroundSize=this.sizing,e.backgroundPosition=t.backgroundPosition=this.sizing?this.position:"",e.backgroundRepeat=t.backgroundRepeat=this.sizing?"no-repeat":""},_resolveSrc:function(e){var t=Object(o.c)(e,this.$.baseURIAnchor.href);return"/"===t[0]&&(t=(location.origin||location.protocol+"//"+location.host)+t),t}})},176:function(e,t,i){"use strict";i(2),i(54),i(141);var a=i(4),n=i(3),o=i(116);const r=n.a`
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
`;r.setAttribute("strip-whitespace",""),Object(a.a)({_template:r,is:"paper-spinner",behaviors:[o.a]})},178:function(e,t,i){"use strict";i.d(t,"b",function(){return o}),i.d(t,"a",function(){return r});i(2);var a=i(77),n=i(0);const o={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=Object(n.b)(e).path,i=0,a=t.indexOf(this);i<a;i++){var o=t[i];if(o.hasAttribute&&(o.hasAttribute("dialog-dismiss")||o.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(o.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},r=[a.a,o]},182:function(e,t,i){"use strict";i(104);var a=i(5),n=i(42);function o(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function r(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,i,a){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(a){t.forEach(function(t){var n=t.placement;if(t.kind===a&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!s(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)},this),!t)return{elements:i,finishers:a};var o=this.decorateConstructor(i,t);return a.push.apply(a,o.finishers),o.finishers=a,o},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],n=e.decorators,o=n.length-1;o>=0;o--){var r=t[e.placement];r.splice(r.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var p=l.extras;if(p){for(var d=0;d<p.length;d++)this.addElementPlacement(p[d],t);i.push.apply(i,p)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[a])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var r=0;r<e.length-1;r++)for(var s=r+1;s<e.length;s++)if(e[r].key===e[s].key&&e[r].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[r].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:a,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=p(e,"finisher"),a=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:a}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher"),a=this.toElementDescriptors(e.elements);return{elements:a,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(a)for(var c=0;c<a.length;c++)n=a[c](n);var h=t(function(e){n.initializeInstanceElements(e,u.elements)},i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},a=0;a<e.length;a++){var n,o=e[a];if("method"===o.kind&&(n=t.find(i)))if(l(o.descriptor)||l(n.descriptor)){if(s(o)||s(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(s(o)){if(s(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}r(o,n)}else t.push(o)}return t}(h.d.map(o)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([Object(a.d)("ha-menu-button")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(a.f)({type:Boolean})],key:"hassio",value:()=>!1},{kind:"method",key:"render",value:function(){return a.e`
      <paper-icon-button
        .icon=${this.hassio?"hassio:menu":"hass:menu"}
        @click=${this._toggleMenu}
      ></paper-icon-button>
    `}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"_toggleMenu",value:function(){Object(n.a)(this,"hass-toggle-menu")}}]}},a.a)},186:function(e,t,i){"use strict";i(2),i(187);var a=i(113),n=i(178),o=i(4),r=i(3);Object(o.a)({_template:r.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[n.a,a.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},187:function(e,t,i){"use strict";i(2),i(40),i(41),i(50),i(76);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(a.content)},190:function(e,t,i){"use strict";var a={},n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,o="[^\\s]+",r=/\[([^]*?)\]/gm,s=function(){};function l(e,t){for(var i=[],a=0,n=e.length;a<n;a++)i.push(e[a].substr(0,t));return i}function p(e){return function(t,i,a){var n=a[e].indexOf(i.charAt(0).toUpperCase()+i.substr(1).toLowerCase());~n&&(t.month=n)}}function d(e,t){for(e=String(e),t=t||2;e.length<t;)e="0"+e;return e}var c=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],h=["January","February","March","April","May","June","July","August","September","October","November","December"],u=l(h,3),m=l(c,3);a.i18n={dayNamesShort:m,dayNames:c,monthNamesShort:u,monthNames:h,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10)*e%10]}};var f={D:function(e){return e.getDate()},DD:function(e){return d(e.getDate())},Do:function(e,t){return t.DoFn(e.getDate())},d:function(e){return e.getDay()},dd:function(e){return d(e.getDay())},ddd:function(e,t){return t.dayNamesShort[e.getDay()]},dddd:function(e,t){return t.dayNames[e.getDay()]},M:function(e){return e.getMonth()+1},MM:function(e){return d(e.getMonth()+1)},MMM:function(e,t){return t.monthNamesShort[e.getMonth()]},MMMM:function(e,t){return t.monthNames[e.getMonth()]},YY:function(e){return d(String(e.getFullYear()),4).substr(2)},YYYY:function(e){return d(e.getFullYear(),4)},h:function(e){return e.getHours()%12||12},hh:function(e){return d(e.getHours()%12||12)},H:function(e){return e.getHours()},HH:function(e){return d(e.getHours())},m:function(e){return e.getMinutes()},mm:function(e){return d(e.getMinutes())},s:function(e){return e.getSeconds()},ss:function(e){return d(e.getSeconds())},S:function(e){return Math.round(e.getMilliseconds()/100)},SS:function(e){return d(Math.round(e.getMilliseconds()/10),2)},SSS:function(e){return d(e.getMilliseconds(),3)},a:function(e,t){return e.getHours()<12?t.amPm[0]:t.amPm[1]},A:function(e,t){return e.getHours()<12?t.amPm[0].toUpperCase():t.amPm[1].toUpperCase()},ZZ:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+d(100*Math.floor(Math.abs(t)/60)+Math.abs(t)%60,4)}},g={D:["\\d\\d?",function(e,t){e.day=t}],Do:["\\d\\d?"+o,function(e,t){e.day=parseInt(t,10)}],M:["\\d\\d?",function(e,t){e.month=t-1}],YY:["\\d\\d?",function(e,t){var i=+(""+(new Date).getFullYear()).substr(0,2);e.year=""+(t>68?i-1:i)+t}],h:["\\d\\d?",function(e,t){e.hour=t}],m:["\\d\\d?",function(e,t){e.minute=t}],s:["\\d\\d?",function(e,t){e.second=t}],YYYY:["\\d{4}",function(e,t){e.year=t}],S:["\\d",function(e,t){e.millisecond=100*t}],SS:["\\d{2}",function(e,t){e.millisecond=10*t}],SSS:["\\d{3}",function(e,t){e.millisecond=t}],d:["\\d\\d?",s],ddd:[o,s],MMM:[o,p("monthNamesShort")],MMMM:[o,p("monthNames")],a:[o,function(e,t,i){var a=t.toLowerCase();a===i.amPm[0]?e.isPm=!1:a===i.amPm[1]&&(e.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(e,t){var i,a=(t+"").match(/([+-]|\d\d)/gi);a&&(i=60*a[1]+parseInt(a[2],10),e.timezoneOffset="+"===a[0]?i:-i)}]};g.dd=g.d,g.dddd=g.ddd,g.DD=g.D,g.mm=g.m,g.hh=g.H=g.HH=g.h,g.MM=g.M,g.ss=g.s,g.A=g.a,a.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},a.format=function(e,t,i){var o=i||a.i18n;if("number"==typeof e&&(e=new Date(e)),"[object Date]"!==Object.prototype.toString.call(e)||isNaN(e.getTime()))throw new Error("Invalid Date in fecha.format");t=a.masks[t]||t||a.masks.default;var s=[];return(t=(t=t.replace(r,function(e,t){return s.push(t),"??"})).replace(n,function(t){return t in f?f[t](e,o):t.slice(1,t.length-1)})).replace(/\?\?/g,function(){return s.shift()})},a.parse=function(e,t,i){var o=i||a.i18n;if("string"!=typeof t)throw new Error("Invalid format in fecha.parse");if(t=a.masks[t]||t,e.length>1e3)return null;var r,s={},l=[],p=(r=t,r.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(n,function(e){if(g[e]){var t=g[e];return l.push(t[1]),"("+t[0]+")"}return e}),d=e.match(new RegExp(p,"i"));if(!d)return null;for(var c=1;c<d.length;c++)l[c-1](s,d[c],o);var h,u=new Date;return!0===s.isPm&&null!=s.hour&&12!=+s.hour?s.hour=+s.hour+12:!1===s.isPm&&12==+s.hour&&(s.hour=0),null!=s.timezoneOffset?(s.minute=+(s.minute||0)-+s.timezoneOffset,h=new Date(Date.UTC(s.year||u.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0))):h=new Date(s.year||u.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0),h},t.a=a},193:function(e,t,i){"use strict";var a=i(190);t.a=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>a.a.format(e,"haDateTime")},200:function(e,t,i){"use strict";i(2),i(40),i(54),i(41);var a=i(114),n=i(62),o=i(4),r=i(33),s=i(3),l=i(59);const p=s.a`

    <style>
      :host {
        display: inline-block;
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-common-base;
      }

      :host([disabled]) {
        pointer-events: none;
      }

      :host(:focus) {
        outline:none;
      }

      .toggle-bar {
        position: absolute;
        height: 100%;
        width: 100%;
        border-radius: 8px;
        pointer-events: none;
        opacity: 0.4;
        transition: background-color linear .08s;
        background-color: var(--paper-toggle-button-unchecked-bar-color, #000000);

        @apply --paper-toggle-button-unchecked-bar;
      }

      .toggle-button {
        position: absolute;
        top: -3px;
        left: 0;
        height: 20px;
        width: 20px;
        border-radius: 50%;
        box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.6);
        transition: -webkit-transform linear .08s, background-color linear .08s;
        transition: transform linear .08s, background-color linear .08s;
        will-change: transform;
        background-color: var(--paper-toggle-button-unchecked-button-color, var(--paper-grey-50));

        @apply --paper-toggle-button-unchecked-button;
      }

      .toggle-button.dragging {
        -webkit-transition: none;
        transition: none;
      }

      :host([checked]:not([disabled])) .toggle-bar {
        opacity: 0.5;
        background-color: var(--paper-toggle-button-checked-bar-color, var(--primary-color));

        @apply --paper-toggle-button-checked-bar;
      }

      :host([disabled]) .toggle-bar {
        background-color: #000;
        opacity: 0.12;
      }

      :host([checked]) .toggle-button {
        -webkit-transform: translate(16px, 0);
        transform: translate(16px, 0);
      }

      :host([checked]:not([disabled])) .toggle-button {
        background-color: var(--paper-toggle-button-checked-button-color, var(--primary-color));

        @apply --paper-toggle-button-checked-button;
      }

      :host([disabled]) .toggle-button {
        background-color: #bdbdbd;
        opacity: 1;
      }

      .toggle-ink {
        position: absolute;
        top: -14px;
        left: -14px;
        right: auto;
        bottom: auto;
        width: 48px;
        height: 48px;
        opacity: 0.5;
        pointer-events: none;
        color: var(--paper-toggle-button-unchecked-ink-color, var(--primary-text-color));

        @apply --paper-toggle-button-unchecked-ink;
      }

      :host([checked]) .toggle-ink {
        color: var(--paper-toggle-button-checked-ink-color, var(--primary-color));

        @apply --paper-toggle-button-checked-ink;
      }

      .toggle-container {
        display: inline-block;
        position: relative;
        width: 36px;
        height: 14px;
        /* The toggle button has an absolute position of -3px; The extra 1px
        /* accounts for the toggle button shadow box. */
        margin: 4px 1px;
      }

      .toggle-label {
        position: relative;
        display: inline-block;
        vertical-align: middle;
        padding-left: var(--paper-toggle-button-label-spacing, 8px);
        pointer-events: none;
        color: var(--paper-toggle-button-label-color, var(--primary-text-color));
      }

      /* invalid state */
      :host([invalid]) .toggle-bar {
        background-color: var(--paper-toggle-button-invalid-bar-color, var(--error-color));
      }

      :host([invalid]) .toggle-button {
        background-color: var(--paper-toggle-button-invalid-button-color, var(--error-color));
      }

      :host([invalid]) .toggle-ink {
        color: var(--paper-toggle-button-invalid-ink-color, var(--error-color));
      }
    </style>

    <div class="toggle-container">
      <div id="toggleBar" class="toggle-bar"></div>
      <div id="toggleButton" class="toggle-button"></div>
    </div>

    <div class="toggle-label"><slot></slot></div>

  `;p.setAttribute("strip-whitespace",""),Object(o.a)({_template:p,is:"paper-toggle-button",behaviors:[a.a],hostAttributes:{role:"button","aria-pressed":"false",tabindex:0},properties:{},listeners:{track:"_ontrack"},attached:function(){Object(l.a)(this,function(){Object(r.f)(this,"pan-y")})},_ontrack:function(e){var t=e.detail;"start"===t.state?this._trackStart(t):"track"===t.state?this._trackMove(t):"end"===t.state&&this._trackEnd(t)},_trackStart:function(e){this._width=this.$.toggleBar.offsetWidth/2,this._trackChecked=this.checked,this.$.toggleButton.classList.add("dragging")},_trackMove:function(e){var t=e.dx;this._x=Math.min(this._width,Math.max(0,this._trackChecked?this._width+t:t)),this.translate3d(this._x+"px",0,0,this.$.toggleButton),this._userActivate(this._x>this._width/2)},_trackEnd:function(e){this.$.toggleButton.classList.remove("dragging"),this.transform("",this.$.toggleButton)},_createRipple:function(){this._rippleContainer=this.$.toggleButton;var e=n.a._createRipple();return e.id="ink",e.setAttribute("recenters",""),e.classList.add("circle","toggle-ink"),e}})},206:function(e,t,i){"use strict";function a(e,t){return e&&-1!==e.config.components.indexOf(t)}i.d(t,"a",function(){return a})},250:function(e,t,i){"use strict";i(2);var a=i(4),n=i(0),o=i(3);Object(a.a)({_template:o.a`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var e=Object(n.b)(this).parentNode,t=Object(n.b)(this).getOwnerRoot();return this.for?Object(n.b)(t).querySelector("#"+this.for):e.nodeType==Node.DOCUMENT_FRAGMENT_NODE?t.host:e},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(e){"entry"===e?this.show():"exit"===e&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Object(n.b)(this).textContent.trim()){for(var e=!0,t=Object(n.b)(this).getEffectiveChildNodes(),i=0;i<t.length;i++)if(""!==t[i].textContent.trim()){e=!1;break}if(e)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var e=this.offset;14!=this.marginTop&&14==this.offset&&(e=this.marginTop);var t,i,a=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),r=(n.width-o.width)/2,s=(n.height-o.height)/2,l=n.left-a.left,p=n.top-a.top;switch(this.position){case"top":t=l+r,i=p-o.height-e;break;case"bottom":t=l+r,i=p+n.height+e;break;case"left":t=l-o.width-e,i=p+s;break;case"right":t=l+n.width+e,i=p+s}this.fitToVisibleBounds?(a.left+t+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,t)+"px",this.style.right="auto"),a.top+i+o.height>window.innerHeight?(this.style.bottom=a.height-p+e+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,i)+"px",this.style.bottom="auto")):(this.style.left=t+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(e){500!==e&&this.updateStyles({"--paper-tooltip-delay-in":e+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(e){if("entry"===e&&""!==this.animationEntry)return this.animationEntry;if("exit"===e&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[e]&&"string"==typeof this.animationConfig[e][0].name){if(this.animationConfig[e][0].timing&&this.animationConfig[e][0].timing.delay&&0!==this.animationConfig[e][0].timing.delay){var t=this.animationConfig[e][0].timing.delay;"entry"===e?this.updateStyles({"--paper-tooltip-delay-in":t+"ms"}):"exit"===e&&this.updateStyles({"--paper-tooltip-delay-out":t+"ms"})}return this.animationConfig[e][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},795:function(e,t,i){"use strict";i.r(t);i(140),i(139),i(166),i(172),i(131),i(75),i(135);var a=i(3),n=i(20),o=(i(182),i(86),i(70)),r=i(110);i(186),i(176);customElements.define("ha-change-password-card",class extends(Object(r.a)(n.a)){static get template(){return a.a`
      <style include="ha-style">
        .error {
          color: red;
        }
        .status {
          color: var(--primary-color);
        }
        .error,
        .status {
          position: absolute;
          top: -4px;
        }
        paper-card {
          display: block;
        }
        .currentPassword {
          margin-top: -4px;
        }
      </style>
      <div>
        <paper-card
          heading="[[localize('ui.panel.profile.change_password.header')]]"
        >
          <div class="card-content">
            <template is="dom-if" if="[[_errorMsg]]">
              <div class="error">[[_errorMsg]]</div>
            </template>
            <template is="dom-if" if="[[_statusMsg]]">
              <div class="status">[[_statusMsg]]</div>
            </template>
            <paper-input
              class="currentPassword"
              label="[[localize('ui.panel.profile.change_password.current_password')]]"
              type="password"
              value="{{_currentPassword}}"
              required
              auto-validate
              error-message="[[localize('ui.panel.profile.change_password.error_required')]]"
            ></paper-input>
            <template is="dom-if" if="[[_currentPassword]]">
              <paper-input
                label="[[localize('ui.panel.profile.change_password.new_password')]]"
                type="password"
                value="{{_password1}}"
                required
                auto-validate
                error-message="[[localize('ui.panel.profile.change_password.error_required')]]"
              ></paper-input>
              <paper-input
                label="[[localize('ui.panel.profile.change_password.confirm_new_password')]]"
                type="password"
                value="{{_password2}}"
                required
                auto-validate
                error-message="[[localize('ui.panel.profile.change_password.error_required')]]"
              ></paper-input>
            </template>
          </div>
          <div class="card-actions">
            <template is="dom-if" if="[[_loading]]">
              <div><paper-spinner active></paper-spinner></div>
            </template>
            <template is="dom-if" if="[[!_loading]]">
              <mwc-button on-click="_changePassword"
                >[[localize('ui.panel.profile.change_password.submit')]]</mwc-button
              >
            </template>
          </div>
        </paper-card>
      </div>
    `}static get properties(){return{hass:Object,_loading:{type:Boolean,value:!1},_statusMsg:String,_errorMsg:String,_currentPassword:String,_password1:String,_password2:String}}ready(){super.ready(),this.addEventListener("keypress",e=>{this._statusMsg=null,13===e.keyCode&&this._changePassword()})}async _changePassword(){if(this._statusMsg=null,this._currentPassword&&this._password1&&this._password2)if(this._password1===this._password2)if(this._currentPassword!==this._password1){this._loading=!0,this._errorMsg=null;try{await this.hass.callWS({type:"config/auth_provider/homeassistant/change_password",current_password:this._currentPassword,new_password:this._password1}),this.setProperties({_statusMsg:"Password changed successfully",_currentPassword:null,_password1:null,_password2:null})}catch(e){this._errorMsg=e.message}this._loading=!1}else this._errorMsg="New password must be different than current password";else this._errorMsg="New password confirmation doesn't match"}});let s=!1;customElements.define("ha-mfa-modules-card",class extends(Object(o.a)(Object(r.a)(n.a))){static get template(){return a.a`
      <style include="iron-flex ha-style">
        .error {
          color: red;
        }
        .status {
          color: var(--primary-color);
        }
        .error,
        .status {
          position: absolute;
          top: -4px;
        }
        paper-card {
          display: block;
          max-width: 600px;
          margin: 16px auto;
        }
        mwc-button {
          margin-right: -0.57em;
        }
      </style>
      <paper-card heading="[[localize('ui.panel.profile.mfa.header')]]">
        <template is="dom-repeat" items="[[mfaModules]]" as="module">
          <paper-item>
            <paper-item-body two-line="">
              <div>[[module.name]]</div>
              <div secondary="">[[module.id]]</div>
            </paper-item-body>
            <template is="dom-if" if="[[module.enabled]]">
              <mwc-button on-click="_disable"
                >[[localize('ui.panel.profile.mfa.disable')]]</mwc-button
              >
            </template>
            <template is="dom-if" if="[[!module.enabled]]">
              <mwc-button on-click="_enable"
                >[[localize('ui.panel.profile.mfa.enable')]]</mwc-button
              >
            </template>
          </paper-item>
        </template>
      </paper-card>
    `}static get properties(){return{hass:Object,_loading:{type:Boolean,value:!1},_statusMsg:String,_errorMsg:String,mfaModules:Array}}connectedCallback(){super.connectedCallback(),s||(s=!0,this.fire("register-dialog",{dialogShowEvent:"show-mfa-module-setup-flow",dialogTag:"ha-mfa-module-setup-flow",dialogImport:()=>Promise.all([i.e(7),i.e(26)]).then(i.bind(null,784))}))}_enable(e){this.fire("show-mfa-module-setup-flow",{hass:this.hass,mfaModuleId:e.model.module.id,dialogClosedCallback:()=>this._refreshCurrentUser()})}_disable(e){if(!confirm(this.localize("ui.panel.profile.mfa.confirm_disable","name",e.model.module.name)))return;const t=e.model.module.id;this.hass.callWS({type:"auth/depose_mfa",mfa_module_id:t}).then(()=>{this._refreshCurrentUser()})}_refreshCurrentUser(){this.fire("hass-refresh-current-user")}});i(104),i(250);var l=i(193);customElements.define("ha-settings-row",class extends n.a{static get template(){return a.a`
      <style>
        :host {
          display: flex;
          padding: 0 16px;
          align-content: normal;
          align-self: auto;
          align-items: center;
        }
        :host([narrow]) {
          align-items: normal;
          flex-direction: column;
          border-top: 1px solid var(--divider-color);
          padding-bottom: 8px;
        }
        paper-item-body {
          padding-right: 16px;
        }
      </style>
      <paper-item-body two-line$="[[!threeLine]]" three-line$="[[threeLine]]">
        <slot name="heading"></slot>
        <div secondary><slot name="description"></slot></div>
      </paper-item-body>
      <slot></slot>
    `}static get properties(){return{narrow:{type:Boolean,reflectToAttribute:!0},threeLine:{type:Boolean,value:!1}}}});customElements.define("ha-refresh-tokens-card",class extends(Object(r.a)(Object(o.a)(n.a))){static get template(){return a.a`
      <style>
        paper-card {
          display: block;
        }
        paper-icon-button {
          color: var(--primary-text-color);
        }
        paper-icon-button[disabled] {
          color: var(--disabled-text-color);
        }
      </style>
      <paper-card
        heading="[[localize('ui.panel.profile.refresh_tokens.header')]]"
      >
        <div class="card-content">
          [[localize('ui.panel.profile.refresh_tokens.description')]]
        </div>
        <template is="dom-repeat" items="[[_computeTokens(refreshTokens)]]">
          <ha-settings-row three-line>
            <span slot="heading">[[_formatTitle(item.client_id)]]</span>
            <div slot="description">[[_formatCreatedAt(item.created_at)]]</div>
            <div slot="description">[[_formatLastUsed(item)]]</div>
            <div>
              <template is="dom-if" if="[[item.is_current]]">
                <paper-tooltip position="left"
                  >[[localize('ui.panel.profile.refresh_tokens.current_token_tooltip')]]</paper-tooltip
                >
              </template>
              <paper-icon-button
                icon="hass:delete"
                on-click="_handleDelete"
                disabled="[[item.is_current]]"
              ></paper-icon-button>
            </div>
          </ha-settings-row>
        </template>
      </paper-card>
    `}static get properties(){return{hass:Object,refreshTokens:Array}}_computeTokens(e){return e.filter(e=>"normal"===e.type).reverse()}_formatTitle(e){return this.localize("ui.panel.profile.refresh_tokens.token_title","clientId",e)}_formatCreatedAt(e){return this.localize("ui.panel.profile.refresh_tokens.created_at","date",Object(l.a)(new Date(e),this.hass.language))}_formatLastUsed(e){return e.last_used_at?this.localize("ui.panel.profile.refresh_tokens.last_used","date",Object(l.a)(new Date(e.last_used_at),this.hass.language),"location",e.last_used_ip):this.localize("ui.panel.profile.refresh_tokens.not_used")}async _handleDelete(e){if(confirm(this.localize("ui.panel.profile.refresh_tokens.confirm_delete","name",e.model.item.client_id)))try{await this.hass.callWS({type:"auth/delete_refresh_token",refresh_token_id:e.model.item.id}),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.refresh_tokens.delete_failed"))}}});customElements.define("ha-long-lived-access-tokens-card",class extends(Object(r.a)(Object(o.a)(n.a))){static get template(){return a.a`
      <style include="ha-style">
        paper-card {
          display: block;
        }
        .card-content {
          margin: -1em 0;
        }
        a {
          color: var(--primary-color);
        }
        paper-icon-button {
          color: var(--primary-text-color);
        }
      </style>
      <paper-card
        heading="[[localize('ui.panel.profile.long_lived_access_tokens.header')]]"
      >
        <div class="card-content">
          <p>
            [[localize('ui.panel.profile.long_lived_access_tokens.description')]]
            <a
              href="https://developers.home-assistant.io/docs/en/auth_api.html#making-authenticated-requests"
              target="_blank"
            >
              [[localize('ui.panel.profile.long_lived_access_tokens.learn_auth_requests')]]
            </a>
          </p>
          <template is="dom-if" if="[[!_tokens.length]]">
            <p>
              [[localize('ui.panel.profile.long_lived_access_tokens.empty_state')]]
            </p>
          </template>
        </div>
        <template is="dom-repeat" items="[[_tokens]]">
          <ha-settings-row two-line>
            <span slot="heading">[[item.client_name]]</span>
            <div slot="description">[[_formatCreatedAt(item.created_at)]]</div>
            <paper-icon-button
              icon="hass:delete"
              on-click="_handleDelete"
            ></paper-icon-button>
          </ha-settings-row>
        </template>
        <div class="card-actions">
          <mwc-button on-click="_handleCreate">
            [[localize('ui.panel.profile.long_lived_access_tokens.create')]]
          </mwc-button>
        </div>
      </paper-card>
    `}static get properties(){return{hass:Object,refreshTokens:Array,_tokens:{type:Array,computed:"_computeTokens(refreshTokens)"}}}_computeTokens(e){return e.filter(e=>"long_lived_access_token"===e.type).reverse()}_formatTitle(e){return this.localize("ui.panel.profile.long_lived_access_tokens.token_title","name",e)}_formatCreatedAt(e){return this.localize("ui.panel.profile.long_lived_access_tokens.created_at","date",Object(l.a)(new Date(e),this.hass.language))}async _handleCreate(){const e=prompt(this.localize("ui.panel.profile.long_lived_access_tokens.prompt_name"));if(e)try{const t=await this.hass.callWS({type:"auth/long_lived_access_token",lifespan:3650,client_name:e});prompt(this.localize("ui.panel.profile.long_lived_access_tokens.prompt_copy_token"),t),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.long_lived_access_tokens.create_failed"))}}async _handleDelete(e){if(confirm(this.localize("ui.panel.profile.long_lived_access_tokens.confirm_delete","name",e.model.item.client_name)))try{await this.hass.callWS({type:"auth/delete_refresh_token",refresh_token_id:e.model.item.id}),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.long_lived_access_tokens.delete_failed"))}}});i(134),i(133);customElements.define("ha-pick-language-row",class extends(Object(r.a)(Object(o.a)(n.a))){static get template(){return a.a`
      <style>
        a {
          color: var(--primary-color);
        }
        paper-item {
          direction: ltr;
        }
        paper-item[is-rtl] {
          direction: rtl;
        }
      </style>
      <ha-settings-row narrow="[[narrow]]">
        <span slot="heading"
          >[[localize('ui.panel.profile.language.header')]]</span
        >
        <span slot="description">
          <a
            href="https://developers.home-assistant.io/docs/en/internationalization_translation.html"
            target="_blank"
            >[[localize('ui.panel.profile.language.link_promo')]]</a
          >
        </span>
        <paper-dropdown-menu
          label="[[localize('ui.panel.profile.language.dropdown_label')]]"
          dynamic-align=""
        >
          <paper-listbox
            slot="dropdown-content"
            attr-for-selected="language-tag"
            selected="{{languageSelection}}"
          >
            <template is="dom-repeat" items="[[languages]]">
              <paper-item language-tag$="[[item.key]]" is-rtl$="[[item.isRTL]]">
                [[item.nativeName]]
              </paper-item>
            </template>
          </paper-listbox>
        </paper-dropdown-menu>
      </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,languageSelection:{type:String,observer:"languageSelectionChanged"},languages:{type:Array,computed:"computeLanguages(hass)"}}}static get observers(){return["setLanguageSelection(language)"]}computeLanguages(e){if(!e||!e.translationMetadata)return[];const t=e.translationMetadata.translations;return Object.keys(t).map(e=>Object.assign({key:e},t[e]))}setLanguageSelection(e){this.languageSelection=e}languageSelectionChanged(e){e!==this.hass.language&&this.fire("hass-language-select",{language:e})}ready(){super.ready(),this.hass&&this.hass.language&&this.setLanguageSelection(this.hass.language)}});customElements.define("ha-pick-theme-row",class extends(Object(r.a)(Object(o.a)(n.a))){static get template(){return a.a`
      <style>
        a {
          color: var(--primary-color);
        }
      </style>
      <ha-settings-row narrow="[[narrow]]">
        <span slot="heading"
          >[[localize('ui.panel.profile.themes.header')]]</span
        >
        <span slot="description">
          <template is="dom-if" if="[[!_hasThemes]]">
            [[localize('ui.panel.profile.themes.error_no_theme')]]
          </template>
          <a
            href="https://www.home-assistant.io/components/frontend/#defining-themes"
            target="_blank"
            >[[localize('ui.panel.profile.themes.link_promo')]]</a
          >
        </span>
        <paper-dropdown-menu
          label="[[localize('ui.panel.profile.themes.dropdown_label')]]"
          dynamic-align
          disabled="[[!_hasThemes]]"
        >
          <paper-listbox slot="dropdown-content" selected="{{selectedTheme}}">
            <template is="dom-repeat" items="[[themes]]" as="theme">
              <paper-item>[[theme]]</paper-item>
            </template>
          </paper-listbox>
        </paper-dropdown-menu>
      </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,_hasThemes:{type:Boolean,computed:"_compHasThemes(hass)"},themes:{type:Array,computed:"_computeThemes(hass)"},selectedTheme:{type:Number}}}static get observers(){return["selectionChanged(hass, selectedTheme)"]}_compHasThemes(e){return e.themes&&e.themes.themes&&Object.keys(e.themes.themes).length}ready(){super.ready(),this.hass.selectedTheme&&this.themes.indexOf(this.hass.selectedTheme)>0?this.selectedTheme=this.themes.indexOf(this.hass.selectedTheme):this.hass.selectedTheme||(this.selectedTheme=0)}_computeThemes(e){return e?["Backend-selected","default"].concat(Object.keys(e.themes.themes).sort()):[]}selectionChanged(e,t){t>0&&t<this.themes.length?e.selectedTheme!==this.themes[t]&&this.fire("settheme",this.themes[t]):0===t&&""!==e.selectedTheme&&this.fire("settheme","")}});i(167),i(2);var p=i(4),d=i(0);const c=Object(p.a)({is:"iron-label",listeners:{tap:"_tapHandler"},properties:{for:{type:String,value:"",reflectToAttribute:!0,observer:"_forChanged"},_forElement:Object},attached:function(){this._forChanged()},ready:function(){this._generateLabelId()},_generateLabelId:function(){if(!this.id){var e="iron-label-"+c._labelNumber++;Object(d.b)(this).setAttribute("id",e)}},_findTarget:function(){if(this.for){var e=Object(d.b)(this).getOwnerRoot();return Object(d.b)(e).querySelector("#"+this.for)}var t=Object(d.b)(this).querySelector("[iron-label-target]");return t||(t=Object(d.b)(this).firstElementChild),t},_tapHandler:function(e){this._forElement&&(Object(d.b)(e).localTarget!==this._forElement&&(this._forElement.focus(),this._forElement.click()))},_applyLabelledBy:function(){this._forElement&&Object(d.b)(this._forElement).setAttribute("aria-labelledby",this.id)},_forChanged:function(){this._forElement&&Object(d.b)(this._forElement).removeAttribute("aria-labelledby"),this._forElement=this._findTarget(),this._applyLabelledBy()}});c._labelNumber=0;var h=i(206);i(200);const u=async e=>{const t=await e.callWS({type:"notify/html5/appkey"});return t?function(e){const t=(e+"=".repeat((4-e.length%4)%4)).replace(/-/g,"+").replace(/_/g,"/"),i=window.atob(t),a=new Uint8Array(i.length);for(let e=0;e<i.length;++e)a[e]=i.charCodeAt(e);return a}(t):null},m="serviceWorker"in navigator&&"PushManager"in window&&("https:"===document.location.protocol||"localhost"===document.location.hostname||"127.0.0.1"===document.location.hostname);customElements.define("ha-push-notifications-toggle",class extends(Object(o.a)(n.a)){static get template(){return a.a`
      <paper-toggle-button
        disabled="[[_compDisabled(disabled, loading)]]"
        checked="{{pushChecked}}"
        on-change="handlePushChange"
      ></paper-toggle-button>
    `}static get properties(){return{hass:{type:Object,value:null},disabled:{type:Boolean,value:!1},pushChecked:{type:Boolean,value:"Notification"in window&&"granted"===Notification.permission},loading:{type:Boolean,value:!0}}}async connectedCallback(){if(super.connectedCallback(),m)try{const e=await navigator.serviceWorker.ready;if(!e.pushManager)return;e.pushManager.getSubscription().then(e=>{this.loading=!1,this.pushChecked=!!e})}catch(e){}}handlePushChange(e){m&&(e.target.checked?this.subscribePushNotifications():this.unsubscribePushNotifications())}async subscribePushNotifications(){const e=await navigator.serviceWorker.ready;let t;try{let i;i=navigator.userAgent.toLowerCase().indexOf("firefox")>-1?"firefox":"chrome";const a=prompt("What should this device be called ?");if(null==a)return void(this.pushChecked=!1);let n;try{n=await u(this.hass)}catch(e){n=null}t=n?await e.pushManager.subscribe({userVisibleOnly:!0,applicationServerKey:n}):await e.pushManager.subscribe({userVisibleOnly:!0}),await this.hass.callApi("POST","notify.html5",{subscription:t,browser:i,name:a})}catch(e){const i=e.message||"Notification registration failed.";t&&await t.unsubscribe(),console.error(e),this.fire("hass-notification",{message:i}),this.pushChecked=!1}}async unsubscribePushNotifications(){const e=await navigator.serviceWorker.ready;try{const t=await e.pushManager.getSubscription();if(!t)return;await this.hass.callApi("DELETE","notify.html5",{subscription:t}),await t.unsubscribe()}catch(e){const t=e.message||"Failed unsubscribing for push notifications.";console.error("Error in unsub push",e),this.fire("hass-notification",{message:t}),this.pushChecked=!0}}_compDisabled(e,t){return e||t}});customElements.define("ha-push-notifications-row",class extends(Object(r.a)(n.a)){static get template(){return a.a`
      <style>
        a {
          color: var(--primary-color);
        }
      </style>
      <ha-settings-row narrow="[[narrow]]">
        <span slot="heading"
          >[[localize('ui.panel.profile.push_notifications.header')]]</span
        >
        <span slot="description">
          [[_description(_platformLoaded, _pushSupported)]]
          <a
            href="https://www.home-assistant.io/components/notify.html5/"
            target="_blank"
            >[[localize('ui.panel.profile.push_notifications.link_promo')]]</a
          >
        </span>
        <ha-push-notifications-toggle
          hass="[[hass]]"
          disabled="[[_error]]"
        ></ha-push-notifications-toggle>
      </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,_platformLoaded:{type:Boolean,computed:"_compPlatformLoaded(hass)"},_pushSupported:{type:Boolean,value:m},_error:{type:Boolean,computed:"_compError(_platformLoaded, _pushSupported)"}}}_compPlatformLoaded(e){return Object(h.a)(e,"notify.html5")}_compError(e,t){return!e||!t}_description(e,t){let i;return i=t?e?"description":"error_load_platform":"error_use_https",this.localize(`ui.panel.profile.push_notifications.${i}`)}});customElements.define("ha-panel-profile",class extends(Object(o.a)(Object(r.a)(n.a))){static get template(){return a.a`
      <style include="ha-style">
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .content {
          display: block;
          max-width: 600px;
          margin: 0 auto;
        }

        .content > * {
          display: block;
          margin: 24px 0;
        }
      </style>

      <app-header-layout has-scrolling-region>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button></ha-menu-button>
            <div main-title>[[localize('panel.profile')]]</div>
          </app-toolbar>
        </app-header>

        <div class="content">
          <paper-card heading="[[hass.user.name]]">
            <div class="card-content">
              [[localize('ui.panel.profile.current_user', 'fullName',
              hass.user.name)]]
              <template is="dom-if" if="[[hass.user.is_owner]]"
                >[[localize('ui.panel.profile.is_owner')]]</template
              >
            </div>

            <hello-world hass="[[hass]]"></hello-world>

            <ha-pick-language-row
              narrow="[[narrow]]"
              hass="[[hass]]"
            ></ha-pick-language-row>
            <ha-pick-theme-row
              narrow="[[narrow]]"
              hass="[[hass]]"
            ></ha-pick-theme-row>
            <ha-push-notifications-row
              narrow="[[narrow]]"
              hass="[[hass]]"
            ></ha-push-notifications-row>

            <div class="card-actions">
              <mwc-button class="warning" on-click="_handleLogOut"
                >[[localize('ui.panel.profile.logout')]]</mwc-button
              >
            </div>
          </paper-card>

          <template is="dom-if" if="[[_canChangePassword(hass.user)]]">
            <ha-change-password-card hass="[[hass]]"></ha-change-password-card>
          </template>

          <ha-mfa-modules-card
            hass="[[hass]]"
            mfa-modules="[[hass.user.mfa_modules]]"
          ></ha-mfa-modules-card>

          <ha-refresh-tokens-card
            hass="[[hass]]"
            refresh-tokens="[[_refreshTokens]]"
            on-hass-refresh-tokens="_refreshRefreshTokens"
          ></ha-refresh-tokens-card>

          <ha-long-lived-access-tokens-card
            hass="[[hass]]"
            refresh-tokens="[[_refreshTokens]]"
            on-hass-refresh-tokens="_refreshRefreshTokens"
          ></ha-long-lived-access-tokens-card>
        </div>
      </app-header-layout>
    `}static get properties(){return{hass:Object,narrow:Boolean,_refreshTokens:Array}}connectedCallback(){super.connectedCallback(),this._refreshRefreshTokens()}async _refreshRefreshTokens(){this._refreshTokens=await this.hass.callWS({type:"auth/refresh_tokens"})}_handleLogOut(){this.fire("hass-logout")}_canChangePassword(e){return e.credentials.some(e=>"homeassistant"===e.auth_provider_type)}})}}]);
//# sourceMappingURL=201bd85600a01742d89e.chunk.js.map