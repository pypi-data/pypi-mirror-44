/*! For license information please see 5e267d411f631890d3f9.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[73,127,128],{111:function(e,t,i){"use strict";i.d(t,"a",function(){return o});i(2);var a=i(51),n=i(32);const o=[a.a,n.a,{hostAttributes:{role:"option",tabindex:"0"}}]},131:function(e,t,i){"use strict";i(2),i(40),i(132);var a=i(4),n=i(3),o=i(111);Object(a.a)({_template:n.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[o.a]})},132:function(e,t,i){"use strict";i(40),i(54),i(41),i(50);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(a.content)},134:function(e,t,i){"use strict";i(2),i(30),i(100),i(85),i(138),i(102),i(41),i(136),i(137);var a=i(51),n=i(32),o=i(57),r=i(58),s=i(4),l=i(0),c=i(33),p=i(3);Object(s.a)({_template:p.a`
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
`,is:"paper-dropdown-menu",behaviors:[a.a,n.a,o.a,r.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.b)(this.$.content).getDistributedNodes(),t=0,i=e.length;t<i;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},136:function(e,t,i){"use strict";i(78);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<iron-iconset-svg name="paper-dropdown-menu" size="24">\n<svg><defs>\n<g id="arrow-drop-down"><path d="M7 10l5 5 5-5z"></path></g>\n</defs></svg>\n</iron-iconset-svg>',document.head.appendChild(a.content)},137:function(e,t,i){"use strict";i(41);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<dom-module id="paper-dropdown-menu-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        text-align: left;\n\n        /* NOTE(cdata): Both values are needed, since some phones require the\n         * value to be `transparent`.\n         */\n        -webkit-tap-highlight-color: rgba(0,0,0,0);\n        -webkit-tap-highlight-color: transparent;\n\n        --paper-input-container-input: {\n          overflow: hidden;\n          white-space: nowrap;\n          text-overflow: ellipsis;\n          max-width: 100%;\n          box-sizing: border-box;\n          cursor: pointer;\n        };\n\n        @apply --paper-dropdown-menu;\n      }\n\n      :host([disabled]) {\n        @apply --paper-dropdown-menu-disabled;\n      }\n\n      :host([noink]) paper-ripple {\n        display: none;\n      }\n\n      :host([no-label-float]) paper-ripple {\n        top: 8px;\n      }\n\n      paper-ripple {\n        top: 12px;\n        left: 0px;\n        bottom: 8px;\n        right: 0px;\n\n        @apply --paper-dropdown-menu-ripple;\n      }\n\n      paper-menu-button {\n        display: block;\n        padding: 0;\n\n        @apply --paper-dropdown-menu-button;\n      }\n\n      paper-input {\n        @apply --paper-dropdown-menu-input;\n      }\n\n      iron-icon {\n        color: var(--disabled-text-color);\n\n        @apply --paper-dropdown-menu-icon;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(a.content)},165:function(e,t,i){"use strict";var a=i(183);t.a=(e=>void 0===e.attributes.friendly_name?Object(a.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||"")},166:function(e,t,i){"use strict";i(2),i(40),i(175),i(174),i(41);var a=i(4),n=i(3);Object(a.a)({_template:n.a`
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
`;a.setAttribute("style","display: none;"),document.head.appendChild(a.content)},168:function(e,t,i){"use strict";i.d(t,"a",function(){return o});var a=i(112);const n={alert:"hass:alert",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weblink:"hass:open-in-new"};function o(e,t){if(e in n)return n[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),a.a}}},169:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var a=i(171);function n(e){return Object(a.a)(e.entity_id)}},170:function(e,t,i){"use strict";i.d(t,"a",function(){return o});i(100);const a=customElements.get("iron-icon");let n=!1;class o extends a{constructor(...e){super(...e),this._iconsetName=void 0}listen(e,t,a){super.listen(e,t,a),n||"mdi"!==this._iconsetName||(n=!0,i.e(60).then(i.bind(null,210)))}}customElements.define("ha-icon",o)},171:function(e,t,i){"use strict";function a(e){return e.substr(0,e.indexOf("."))}i.d(t,"a",function(){return a})},172:function(e,t,i){"use strict";i(2),i(40),i(41),i(50);var a=i(4),n=i(3);Object(a.a)({_template:n.a`
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
`,is:"iron-image",properties:{src:{type:String,value:""},alt:{type:String,value:null},crossorigin:{type:String,value:null},preventLoad:{type:Boolean,value:!1},sizing:{type:String,value:null,reflectToAttribute:!0},position:{type:String,value:"center"},preload:{type:Boolean,value:!1},placeholder:{type:String,value:null,observer:"_placeholderChanged"},fade:{type:Boolean,value:!1},loaded:{notify:!0,readOnly:!0,type:Boolean,value:!1},loading:{notify:!0,readOnly:!0,type:Boolean,value:!1},error:{notify:!0,readOnly:!0,type:Boolean,value:!1},width:{observer:"_widthChanged",type:Number,value:null},height:{observer:"_heightChanged",type:Number,value:null}},observers:["_transformChanged(sizing, position)","_loadStateObserver(src, preventLoad)"],created:function(){this._resolvedSrc=""},_imgOnLoad:function(){this.$.img.src===this._resolveSrc(this.src)&&(this._setLoading(!1),this._setLoaded(!0),this._setError(!1))},_imgOnError:function(){this.$.img.src===this._resolveSrc(this.src)&&(this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",this._setLoading(!1),this._setLoaded(!1),this._setError(!0))},_computePlaceholderHidden:function(){return!this.preload||!this.fade&&!this.loading&&this.loaded},_computePlaceholderClassName:function(){return this.preload&&this.fade&&!this.loading&&this.loaded?"faded-out":""},_computeImgDivHidden:function(){return!this.sizing},_computeImgDivARIAHidden:function(){return""===this.alt?"true":void 0},_computeImgDivARIALabel:function(){return null!==this.alt?this.alt:""===this.src?"":this._resolveSrc(this.src).replace(/[?|#].*/g,"").split("/").pop()},_computeImgHidden:function(){return!!this.sizing},_widthChanged:function(){this.style.width=isNaN(this.width)?this.width:this.width+"px"},_heightChanged:function(){this.style.height=isNaN(this.height)?this.height:this.height+"px"},_loadStateObserver:function(e,t){var i=this._resolveSrc(e);i!==this._resolvedSrc&&(this._resolvedSrc="",this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",""===e||t?(this._setLoading(!1),this._setLoaded(!1),this._setError(!1)):(this._resolvedSrc=i,this.$.img.src=this._resolvedSrc,this.$.sizedImgDiv.style.backgroundImage='url("'+this._resolvedSrc+'")',this._setLoading(!0),this._setLoaded(!1),this._setError(!1)))},_placeholderChanged:function(){this.$.placeholder.style.backgroundImage=this.placeholder?'url("'+this.placeholder+'")':""},_transformChanged:function(){var e=this.$.sizedImgDiv.style,t=this.$.placeholder.style;e.backgroundSize=t.backgroundSize=this.sizing,e.backgroundPosition=t.backgroundPosition=this.sizing?this.position:"",e.backgroundRepeat=t.backgroundRepeat=this.sizing?"no-repeat":""},_resolveSrc:function(e){var t=Object(o.c)(e,this.$.baseURIAnchor.href);return"/"===t[0]&&(t=(location.origin||location.protocol+"//"+location.host)+t),t}})},179:function(e,t,i){"use strict";i(2),i(40),i(50),i(132);var a=i(4),n=i(3),o=i(111);Object(a.a)({_template:n.a`
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
`,is:"paper-icon-item",behaviors:[o.a]})},180:function(e,t,i){"use strict";var a=i(5),n=(i(170),i(169)),o=i(184);function r(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let u=function(e,t,i,a){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(a){t.forEach(function(t){var n=t.placement;if(t.kind===a&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!l(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)},this),!t)return{elements:i,finishers:a};var o=this.decorateConstructor(i,t);return a.push.apply(a,o.finishers),o.finishers=a,o},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],n=e.decorators,o=n.length-1;o>=0;o--){var r=t[e.placement];r.splice(r.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var c=l.extras;if(c){for(var p=0;p<c.length;p++)this.addElementPlacement(c[p],t);i.push.apply(i,c)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[a])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var r=0;r<e.length-1;r++)for(var s=r+1;s<e.length;s++)if(e[r].key===e[s].key&&e[r].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[r].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:a,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=p(e,"finisher"),a=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:a}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher"),a=this.toElementDescriptors(e.elements);return{elements:a,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(a)for(var o=0;o<a.length;o++)n=a[o](n);var u=t(function(e){n.initializeInstanceElements(e,m.elements)},i),m=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},a=0;a<e.length;a++){var n,o=e[a];if("method"===o.kind&&(n=t.find(i)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(u.d.map(r)),e);return n.initializeClassElements(u.F,m.elements),n.runClassFinishers(u.F,m.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(a.f)()],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(a.f)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[Object(a.g)("ha-icon")],key:"_icon",value:void 0},{kind:"method",key:"render",value:function(){const e=this.stateObj;return e?a.e`
      <ha-icon
        id="icon"
        data-domain=${Object(n.a)(e)}
        data-state=${e.state}
        .icon=${this.overrideIcon||Object(o.a)(e)}
      ></ha-icon>
    `:a.e``}},{kind:"method",key:"updated",value:function(e){if(!e.has("stateObj")||!this.stateObj)return;const t=this.stateObj,i={color:"",filter:""},a={backgroundImage:""};if(t)if(t.attributes.entity_picture&&!this.overrideIcon)a.backgroundImage="url("+t.attributes.entity_picture+")",i.display="none";else{if(t.attributes.hs_color){const e=t.attributes.hs_color[0],a=t.attributes.hs_color[1];a>10&&(i.color=`hsl(${e}, 100%, ${100-a/2}%)`)}if(t.attributes.brightness){const e=t.attributes.brightness;if("number"!=typeof e){const i=`Type error: state-badge expected number, but type of ${t.entity_id}.attributes.brightness is ${typeof e} (${e})`;console.warn(i)}i.filter=`brightness(${(e+245)/5}%)`}}Object.assign(this._icon.style,i),Object.assign(this.style,a)}},{kind:"get",static:!0,key:"styles",value:function(){return a.c`
      :host {
        position: relative;
        display: inline-block;
        width: 40px;
        color: var(--paper-item-icon-color, #44739e);
        border-radius: 50%;
        height: 40px;
        text-align: center;
        background-size: cover;
        line-height: 40px;
      }

      ha-icon {
        transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
      }

      /* Color the icon if light or sun is on */
      ha-icon[data-domain="light"][data-state="on"],
      ha-icon[data-domain="switch"][data-state="on"],
      ha-icon[data-domain="binary_sensor"][data-state="on"],
      ha-icon[data-domain="fan"][data-state="on"],
      ha-icon[data-domain="sun"][data-state="above_horizon"] {
        color: var(--paper-item-icon-active-color, #fdd835);
      }

      /* Color the icon if unavailable */
      ha-icon[data-state="unavailable"] {
        color: var(--state-icon-unavailable-color);
      }
    `}}]}},a.a);customElements.define("state-badge",u)},183:function(e,t,i){"use strict";function a(e){return e.substr(e.indexOf(".")+1)}i.d(t,"a",function(){return a})},184:function(e,t,i){"use strict";var a=i(112),n=i(171),o=i(168);const r={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge"};i.d(t,"a",function(){return l});const s={binary_sensor:function(e){const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:function(e){const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";default:return Object(o.a)("cover",e.state)}},sensor:function(e){const t=e.attributes.device_class;if(t&&t in r)return r[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const i=10*Math.round(t/10);return i>=100?"hass:battery":i<=0?"hass:battery-alert":`hass:battery-${i}`}const i=e.attributes.unit_of_measurement;return i===a.j||i===a.k?"hass:thermometer":Object(o.a)("sensor")},input_datetime:function(e){return e.attributes.has_date?e.attributes.has_time?Object(o.a)("input_datetime"):"hass:calendar":"hass:clock"}};function l(e){if(!e)return a.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(n.a)(e.entity_id);return t in s?s[t](e):Object(o.a)(t,e.state)}},188:function(e,t,i){"use strict";var a=i(3),n=i(20);i(86);customElements.define("ha-config-section",class extends n.a{static get template(){return a.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},209:function(e,t,i){"use strict";var a=i(6),n=i(71);t.a=Object(a.a)(e=>(class extends e{navigate(...e){Object(n.a)(this,...e)}}))},225:function(e,t,i){"use strict";i(100);var a=i(170);customElements.define("ha-icon-next",class extends a.a{connectedCallback(){this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left",super.connectedCallback()}})},226:function(e,t,i){"use strict";t.a=((e,t)=>e<t?-1:e>t?1:0)},250:function(e,t,i){"use strict";i(2);var a=i(4),n=i(0),o=i(3);Object(a.a)({_template:o.a`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var e=Object(n.b)(this).parentNode,t=Object(n.b)(this).getOwnerRoot();return this.for?Object(n.b)(t).querySelector("#"+this.for):e.nodeType==Node.DOCUMENT_FRAGMENT_NODE?t.host:e},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(e){"entry"===e?this.show():"exit"===e&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Object(n.b)(this).textContent.trim()){for(var e=!0,t=Object(n.b)(this).getEffectiveChildNodes(),i=0;i<t.length;i++)if(""!==t[i].textContent.trim()){e=!1;break}if(e)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var e=this.offset;14!=this.marginTop&&14==this.offset&&(e=this.marginTop);var t,i,a=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),r=(n.width-o.width)/2,s=(n.height-o.height)/2,l=n.left-a.left,c=n.top-a.top;switch(this.position){case"top":t=l+r,i=c-o.height-e;break;case"bottom":t=l+r,i=c+n.height+e;break;case"left":t=l-o.width-e,i=c+s;break;case"right":t=l+n.width+e,i=c+s}this.fitToVisibleBounds?(a.left+t+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,t)+"px",this.style.right="auto"),a.top+i+o.height>window.innerHeight?(this.style.bottom=a.height-c+e+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,i)+"px",this.style.bottom="auto")):(this.style.left=t+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(e){500!==e&&this.updateStyles({"--paper-tooltip-delay-in":e+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(e){if("entry"===e&&""!==this.animationEntry)return this.animationEntry;if("exit"===e&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[e]&&"string"==typeof this.animationConfig[e][0].name){if(this.animationConfig[e][0].timing&&this.animationConfig[e][0].timing.delay&&0!==this.animationConfig[e][0].timing.delay){var t=this.animationConfig[e][0].timing.delay;"entry"===e?this.updateStyles({"--paper-tooltip-delay-in":t+"ms"}):"exit"===e&&this.updateStyles({"--paper-tooltip-delay-out":t+"ms"})}return this.animationConfig[e][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},252:function(e,t,i){"use strict";i.d(t,"c",function(){return a}),i.d(t,"a",function(){return n}),i.d(t,"d",function(){return o}),i.d(t,"b",function(){return r});const a=e=>e.callWS({type:"config/area_registry/list"}),n=(e,t)=>e.callWS(Object.assign({type:"config/area_registry/create"},t)),o=(e,t,i)=>e.callWS(Object.assign({type:"config/area_registry/update",area_id:t},i)),r=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t})},278:function(e,t,i){"use strict";i.d(t,"a",function(){return a}),i.d(t,"b",function(){return n});const a=e=>e.callWS({type:"config/device_registry/list"}),n=(e,t,i)=>e.callWS(Object.assign({type:"config/device_registry/update",device_id:t},i))},316:function(e,t,i){"use strict";i.d(t,"a",function(){return n}),i.d(t,"b",function(){return o}),i.d(t,"d",function(){return r}),i.d(t,"c",function(){return s});var a=i(165);const n=(e,t)=>{if(t.name)return t.name;const i=e.states[t.entity_id];return i?Object(a.a)(i):null},o=e=>e.callWS({type:"config/entity_registry/list"}),r=(e,t,i)=>e.callWS(Object.assign({type:"config/entity_registry/update",entity_id:t},i)),s=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t})},392:function(e,t,i){"use strict";var a=i(3),n=i(20),o=(i(170),i(184));customElements.define("ha-state-icon",class extends n.a{static get template(){return a.a`
      <ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>
    `}static get properties(){return{stateObj:{type:Object}}}computeIcon(e){return Object(o.a)(e)}})},739:function(e,t,i){"use strict";i.r(t);i(148);var a=i(3),n=i(20),o=i(19),r=i(11),s=(i(167),i(250),i(75),i(166),i(100),i(131),i(172),i(392),i(142),i(86),i(225),i(188),i(70)),l=i(110),c=i(165),p=i(42);const d=()=>Promise.all([i.e(7),i.e(102),i.e(21)]).then(i.bind(null,796)),u=(e,t)=>{Object(p.a)(e,"show-dialog",{dialogTag:"dialog-config-flow",dialogImport:d,dialogParams:t})};customElements.define("ha-config-entries-dashboard",class extends(Object(l.a)(Object(s.a)(n.a))){static get template(){return a.a`
      <style include="iron-flex ha-style">
        mwc-button {
          top: 3px;
          margin-right: -0.57em;
        }
        paper-card:last-child {
          margin-top: 12px;
        }
        .config-entry-row {
          display: flex;
          padding: 0 16px;
        }
        ha-state-icon {
          cursor: pointer;
        }
        .configured a {
          color: var(--primary-text-color);
          text-decoration: none;
        }
      </style>

      <hass-subpage
        header="[[localize('ui.panel.config.integrations.caption')]]"
      >
        <template is="dom-if" if="[[progress.length]]">
          <ha-config-section>
            <span slot="header"
              >[[localize('ui.panel.config.integrations.discovered')]]</span
            >
            <paper-card>
              <template is="dom-repeat" items="[[progress]]">
                <div class="config-entry-row">
                  <paper-item-body>
                    [[_computeIntegrationTitle(localize, item.handler)]]
                  </paper-item-body>
                  <mwc-button on-click="_continueFlow"
                    >[[localize('ui.panel.config.integrations.configure')]]</mwc-button
                  >
                </div>
              </template>
            </paper-card>
          </ha-config-section>
        </template>

        <ha-config-section class="configured">
          <span slot="header"
            >[[localize('ui.panel.config.integrations.configured')]]</span
          >
          <paper-card>
            <template is="dom-if" if="[[!entries.length]]">
              <div class="config-entry-row">
                <paper-item-body two-line>
                  <div>[[localize('ui.panel.config.integrations.none')]]</div>
                </paper-item-body>
              </div>
            </template>
            <template is="dom-repeat" items="[[entries]]">
              <a href="/config/integrations/[[item.entry_id]]">
                <paper-item>
                  <paper-item-body two-line>
                    <div>
                      [[_computeIntegrationTitle(localize, item.domain)]]:
                      [[item.title]]
                    </div>
                    <div secondary>
                      <template
                        is="dom-repeat"
                        items="[[_computeConfigEntryEntities(hass, item, entities)]]"
                      >
                        <span>
                          <ha-state-icon
                            state-obj="[[item]]"
                            on-click="_handleMoreInfo"
                          ></ha-state-icon>
                          <paper-tooltip position="bottom"
                            >[[_computeStateName(item)]]</paper-tooltip
                          >
                        </span>
                      </template>
                    </div>
                  </paper-item-body>
                  <ha-icon-next></ha-icon-next>
                </paper-item>
              </a>
            </template>
          </paper-card>
        </ha-config-section>

        <ha-config-section>
          <span slot="header"
            >[[localize('ui.panel.config.integrations.new')]]</span
          >
          <paper-card>
            <template is="dom-repeat" items="[[handlers]]">
              <div class="config-entry-row">
                <paper-item-body>
                  [[_computeIntegrationTitle(localize, item)]]
                </paper-item-body>
                <mwc-button on-click="_createFlow"
                  >[[localize('ui.panel.config.integrations.configure')]]</mwc-button
                >
              </div>
            </template>
          </paper-card>
        </ha-config-section>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,entries:Array,entities:Array,progress:Array,handlers:Array}}connectedCallback(){super.connectedCallback(),d()}_createFlow(e){u(this,{hass:this.hass,newFlowForHandler:e.model.item,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_continueFlow(e){u(this,{hass:this.hass,continueFlowId:e.model.item.flow_id,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_computeIntegrationTitle(e,t){return e(`component.${t}.config.title`)}_computeConfigEntryEntities(e,t,i){if(!i)return[];const a=[];return i.forEach(i=>{i.config_entry_id===t.entry_id&&i.entity_id in e.states&&a.push(e.states[i.entity_id])}),a}_computeStateName(e){return Object(c.a)(e)}_handleMoreInfo(e){this.fire("hass-more-info",{entityId:e.model.item.entity_id})}});i(180);var m=i(226),h=(i(179),i(134),i(133),i(278));function f(e,t){if(t.name)return t.name;const i=e.states[t.entity_id];return i?Object(c.a)(i):null}customElements.define("ha-device-card",class extends(Object(s.a)(Object(l.a)(n.a))){static get template(){return a.a`
      <style>
        :host(:not([narrow])) .device-entities {
          max-height: 225px;
          overflow: auto;
        }
        paper-card {
          flex: 1 0 100%;
          padding-bottom: 10px;
          min-width: 0;
        }
        .device {
          width: 30%;
        }
        .device .name {
          font-weight: bold;
        }
        .device .model,
        .device .manuf {
          color: var(--secondary-text-color);
        }
        .extra-info {
          margin-top: 8px;
        }
        paper-icon-item {
          cursor: pointer;
          padding-top: 4px;
          padding-bottom: 4px;
        }
        .manuf,
        .entity-id {
          color: var(--secondary-text-color);
        }
      </style>
      <paper-card heading="[[device.name]]">
        <div class="card-content">
          <!--
            <h1>[[configEntry.title]] ([[_computeIntegrationTitle(localize, configEntry.domain)]])</h1>
          -->
          <div class="info">
            <div class="model">[[device.model]]</div>
            <div class="manuf">
              [[localize('ui.panel.config.integrations.config_entry.manuf',
              'manufacturer', device.manufacturer)]]
            </div>
            <div class="area">
              <paper-dropdown-menu
                selected-item-label="{{selectedArea}}"
                label="Area"
              >
                <paper-listbox
                  slot="dropdown-content"
                  selected="[[_computeSelectedArea(areas, device)]]"
                >
                  <paper-item>
                    [[localize('ui.panel.config.integrations.config_entry.no_area')]]
                  </paper-item>
                  <template is="dom-repeat" items="[[areas]]">
                    <paper-item area="[[item]]">[[item.name]]</paper-item>
                  </template>
                </paper-listbox>
              </paper-dropdown-menu>
            </div>
          </div>
          <template is="dom-if" if="[[device.hub_device_id]]">
            <div class="extra-info">
              [[localize('ui.panel.config.integrations.config_entry.hub')]]
              <span class="hub"
                >[[_computeDeviceName(devices, device.hub_device_id)]]</span
              >
            </div>
          </template>
          <template is="dom-if" if="[[device.sw_version]]">
            <div class="extra-info">
              [[localize('ui.panel.config.integrations.config_entry.firmware',
              'version', device.sw_version)]]
            </div>
          </template>
        </div>

        <div class="device-entities">
          <template
            is="dom-repeat"
            items="[[_computeDeviceEntities(hass, device, entities)]]"
            as="entity"
          >
            <paper-icon-item on-click="_openMoreInfo">
              <state-badge
                state-obj="[[_computeStateObj(entity, hass)]]"
                slot="item-icon"
              ></state-badge>
              <paper-item-body>
                <div class="name">[[_computeEntityName(entity, hass)]]</div>
                <div class="secondary entity-id">[[entity.entity_id]]</div>
              </paper-item-body>
            </paper-icon-item>
          </template>
        </div>
      </paper-card>
    `}static get properties(){return{device:Object,devices:Array,areas:Array,entities:Array,hass:Object,narrow:{type:Boolean,reflectToAttribute:!0},_childDevices:{type:Array,computed:"_computeChildDevices(device, devices)"},selectedArea:{type:String,observer:"_selectedAreaChanged"}}}_computeSelectedArea(e,t){return e&&t&&t.area_id?e.findIndex(e=>e.area_id===t.area_id)+1:0}async _selectedAreaChanged(e){if(""===e||!this.device||!this.areas)return;const t="No Area"===e?void 0:this.areas.find(t=>t.name===e);!t&&!this.device.area_id||t&&t.area_id===this.device.area_id||await Object(h.b)(this.hass,this.device.id,{area_id:t?t.area_id:null})}_computeChildDevices(e,t){return t.filter(t=>t.hub_device_id===e.id).sort((e,t)=>Object(m.a)(e.name,t.name))}_computeDeviceEntities(e,t,i){return i.filter(e=>e.device_id===t.id).sort((t,i)=>Object(m.a)(f(e,t)||`zzz${t.entity_id}`,f(e,i)||`zzz${i.entity_id}`))}_computeStateObj(e,t){return t.states[e.entity_id]}_computeEntityName(e,t){return f(t,e)||`(${this.localize("ui.panel.config.integrations.config_entry.entity_unavailable")})`}_computeDeviceName(e,t){const i=e.find(e=>e.id===t);return i?i.name:`(${this.localize("ui.panel.config.integrations.config_entry.device_unavailable")})`}_openMoreInfo(e){this.fire("hass-more-info",{entityId:e.model.entity.entity_id})}});var y=i(316);customElements.define("ha-ce-entities-card",class extends(Object(l.a)(Object(s.a)(n.a))){static get template(){return a.a`
      <style>
        paper-card {
          flex: 1 0 100%;
          padding-bottom: 8px;
        }
        paper-icon-item {
          cursor: pointer;
          padding-top: 4px;
          padding-bottom: 4px;
        }
      </style>
      <paper-card heading="[[heading]]">
        <template is="dom-repeat" items="[[entities]]" as="entity">
          <paper-icon-item on-click="_openMoreInfo">
            <state-badge
              state-obj="[[_computeStateObj(entity, hass)]]"
              slot="item-icon"
            ></state-badge>
            <paper-item-body>
              <div class="name">[[_computeEntityName(entity, hass)]]</div>
              <div class="secondary entity-id">[[entity.entity_id]]</div>
            </paper-item-body>
          </paper-icon-item>
        </template>
      </paper-card>
    `}static get properties(){return{heading:String,entities:Array,hass:Object}}_computeStateObj(e,t){return t.states[e.entity_id]}_computeEntityName(e,t){return Object(y.a)(t,e)||`(${this.localize("ui.panel.config.integrations.config_entry.entity_unavailable")})`}_openMoreInfo(e){this.fire("hass-more-info",{entityId:e.model.entity.entity_id})}});var g=i(209);customElements.define("ha-config-entry-page",class extends(Object(g.a)(Object(s.a)(Object(l.a)(n.a)))){static get template(){return a.a`
      <style>
        .content {
          display: flex;
          flex-wrap: wrap;
          padding: 4px;
          justify-content: center;
        }
        .card {
          box-sizing: border-box;
          display: flex;
          flex: 1 0 300px;
          min-width: 0;
          max-width: 500px;
          padding: 8px;
        }
      </style>
      <hass-subpage header="[[configEntry.title]]">
        <paper-icon-button
          slot="toolbar-icon"
          icon="hass:delete"
          on-click="_removeEntry"
        ></paper-icon-button>
        <div class="content">
          <template
            is="dom-if"
            if="[[_computeIsEmpty(_configEntryDevices, _noDeviceEntities)]]"
          >
            <p>
              [[localize('ui.panel.config.integrations.config_entry.no_devices')]]
            </p>
          </template>
          <template is="dom-repeat" items="[[_configEntryDevices]]" as="device">
            <ha-device-card
              class="card"
              hass="[[hass]]"
              areas="[[areas]]"
              devices="[[devices]]"
              device="[[device]]"
              entities="[[entities]]"
              narrow="[[narrow]]"
            ></ha-device-card>
          </template>
          <template is="dom-if" if="[[_noDeviceEntities.length]]">
            <ha-ce-entities-card
              class="card"
              heading="[[localize('ui.panel.config.integrations.config_entry.no_device')]]"
              entities="[[_noDeviceEntities]]"
              hass="[[hass]]"
              narrow="[[narrow]]"
            ></ha-ce-entities-card>
          </template>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,configEntry:{type:Object,value:null},_configEntryDevices:{type:Array,computed:"_computeConfigEntryDevices(configEntry, devices)"},_noDeviceEntities:{type:Array,computed:"_computeNoDeviceEntities(configEntry, entities)"},areas:Array,devices:Array,entries:Array,entities:Array}}_computeConfigEntryDevices(e,t){return t?t.filter(t=>t.config_entries.includes(e.entry_id)).sort((e,t)=>!!e.hub_device_id-!!t.hub_device_id||Object(m.a)(e.name,t.name)):[]}_computeNoDeviceEntities(e,t){return t?t.filter(t=>!t.device_id&&t.config_entry_id===e.entry_id):[]}_computeIsEmpty(e,t){return 0===e.length&&0===t.length}_removeEntry(){if(!confirm(this.localize("ui.panel.config.integrations.config_entry.delete_confirm")))return;const e=this.configEntry.entry_id;this.hass.callApi("delete",`config/config_entries/entry/${e}`).then(e=>{this.fire("hass-reload-entries"),e.require_restart&&alert(this.localize("ui.panel.config.integrations.config_entry.restart_confirm")),this.navigate("/config/integrations/dashboard",!0)})}});var v=i(252);customElements.define("ha-config-integrations",class extends(Object(g.a)(n.a)){static get template(){return a.a`
      <app-route
        route="[[route]]"
        pattern="/:page"
        data="{{_routeData}}"
        tail="{{_routeTail}}"
      ></app-route>

      <template is="dom-if" if="[[_configEntry]]">
        <ha-config-entry-page
          hass="[[hass]]"
          config-entry="[[_configEntry]]"
          areas="[[_areas]]"
          entries="[[_entries]]"
          entities="[[_entities]]"
          devices="[[_devices]]"
          narrow="[[narrow]]"
        ></ha-config-entry-page>
      </template>
      <template is="dom-if" if="[[!_configEntry]]">
        <ha-config-entries-dashboard
          hass="[[hass]]"
          entries="[[_entries]]"
          entities="[[_entities]]"
          handlers="[[_handlers]]"
          progress="[[_progress]]"
        ></ha-config-entries-dashboard>
      </template>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,route:Object,_configEntry:{type:Object,computed:"_computeConfigEntry(_routeData, _entries)"},_entries:Array,_entities:Array,_devices:Array,_areas:Array,_progress:Array,_handlers:Array,_routeData:Object,_routeTail:Object}}ready(){super.ready(),this.addEventListener("hass-reload-entries",()=>this._loadData())}connectedCallback(){super.connectedCallback(),this._loadData(),this.hass.connection.subscribeEvents(()=>{this._debouncer=o.a.debounce(this._debouncer,r.d.after(500),()=>this._loadData())},"config_entry_discovered").then(e=>{this._unsubEvents=e})}disconnectedCallback(){super.disconnectedCallback(),this._unsubEvents&&this._unsubEvents()}_loadData(){this.hass.callApi("get","config/config_entries/entry").then(e=>{this._entries=e.sort((e,t)=>Object(m.a)(e.title,t.title))}),this.hass.callApi("get","config/config_entries/flow").then(e=>{this._progress=e}),this.hass.callApi("get","config/config_entries/flow_handlers").then(e=>{this._handlers=e}),this.hass.callWS({type:"config/entity_registry/list"}).then(e=>{this._entities=e}),this.hass.callWS({type:"config/device_registry/list"}).then(e=>{this._devices=e}),Object(v.c)(this.hass).then(e=>{this._areas=e.sort((e,t)=>Object(m.a)(e.name,t.name))})}_computeConfigEntry(e,t){return!!t&&!!e&&t.find(t=>t.entry_id===e.page)}})}}]);
//# sourceMappingURL=5e267d411f631890d3f9.chunk.js.map