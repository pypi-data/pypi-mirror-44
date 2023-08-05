/*! For license information please see ef784bc6be92bfd5bd5e.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[85],{176:function(e,t,r){"use strict";r(2),r(54),r(141);var i=r(4),a=r(3),n=r(116);const o=a.a`
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
`;o.setAttribute("strip-whitespace",""),Object(i.a)({_template:o,is:"paper-spinner",behaviors:[n.a]})},182:function(e,t,r){"use strict";r(104);var i=r(5),a=r(42);function n(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function o(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,r,i){var a=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var a=t.placement;if(t.kind===i&&("static"===a||"prototype"===a)){var n="static"===a?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],a={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,a)},this),e.forEach(function(e){if(!s(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],a=e.decorators,n=a.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var p=l.extras;if(p){for(var d=0;d<p.length;d++)this.addElementPlacement(p[d],t);r.push.apply(r,p)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var a=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(a)||a);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=p(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var c=0;c<i.length;c++)a=i[c](a);var u=t(function(e){a.initializeInstanceElements(e,h.elements)},r),h=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var a,n=e[i];if("method"===n.kind&&(a=t.find(r)))if(l(n.descriptor)||l(a.descriptor)){if(s(n)||s(a))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");a.descriptor=n.descriptor}else{if(s(n)){if(s(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");a.decorators=n.decorators}o(n,a)}else t.push(n)}return t}(u.d.map(n)),e);a.initializeClassElements(u.F,h.elements),a.runClassFinishers(u.F,h.finishers)}([Object(i.d)("ha-menu-button")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.f)({type:Boolean})],key:"hassio",value:()=>!1},{kind:"method",key:"render",value:function(){return i.e`
      <paper-icon-button
        .icon=${this.hassio?"hassio:menu":"hass:menu"}
        @click=${this._toggleMenu}
      ></paper-icon-button>
    `}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"_toggleMenu",value:function(){Object(a.a)(this,"hass-toggle-menu")}}]}},i.a)},201:function(e,t,r){"use strict";r(2),r(40);var i=r(32),a=r(58),n=r(4),o=r(0),s=r(3);Object(n.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[a.a,i.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=a.a.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=Object(o.b)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});r(106),r(107),r(108);var l=r(57),p=r(88);Object(n.a)({_template:s.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float\$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate\$="[[autoValidate]]" disabled\$="[[disabled]]" invalid="[[invalid]]">

      <label hidden\$="[[!label]]" aria-hidden="true" for\$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id\$="[[_inputId]]" aria-labelledby\$="[[_ariaLabelledBy]]" aria-describedby\$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator\$="[[validator]]" disabled\$="[[disabled]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" name\$="[[name]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]" autocapitalize\$="[[autocapitalize]]" rows\$="[[rows]]" max-rows\$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[p.a,l.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},753:function(e,t,r){"use strict";r.r(t);r(140),r(139),r(135),r(201),r(176);var i=r(11),a=r(19),n=r(3),o=r(20);r(182),r(86);customElements.define("ha-panel-dev-template",class extends o.a{static get template(){return n.a`
      <style include="ha-style iron-flex iron-positioning"></style>
      <style>
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .content {
          padding: 16px;
          direction: ltr;
        }

        .edit-pane {
          margin-right: 16px;
        }

        .edit-pane a {
          color: var(--dark-primary-color);
        }

        .horizontal .edit-pane {
          max-width: 50%;
        }

        .render-pane {
          position: relative;
          max-width: 50%;
        }

        .render-spinner {
          position: absolute;
          top: 8px;
          right: 8px;
        }

        paper-textarea {
          --paper-input-container-input: {
            @apply --paper-font-code1;
          }
        }

        .rendered {
          @apply --paper-font-code1;
          clear: both;
          white-space: pre-wrap;
        }

        .rendered.error {
          color: red;
        }
      </style>

      <app-header-layout has-scrolling-region>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button></ha-menu-button>
            <div main-title>Templates</div>
          </app-toolbar>
        </app-header>

        <div class$="[[computeFormClasses(narrow)]]">
          <div class="edit-pane">
            <p>
              Templates are rendered using the Jinja2 template engine with some
              Home Assistant specific extensions.
            </p>
            <ul>
              <li>
                <a
                  href="http://jinja.pocoo.org/docs/dev/templates/"
                  target="_blank"
                  >Jinja2 template documentation</a
                >
              </li>
              <li>
                <a
                  href="https://home-assistant.io/docs/configuration/templating/"
                  target="_blank"
                  >Home Assistant template extensions</a
                >
              </li>
            </ul>
            <paper-textarea
              label="Template editor"
              value="{{template}}"
              autofocus
            ></paper-textarea>
          </div>

          <div class="render-pane">
            <paper-spinner
              class="render-spinner"
              active="[[rendering]]"
            ></paper-spinner>
            <pre class$="[[computeRenderedClasses(error)]]">[[processed]]</pre>
          </div>
        </div>
      </app-header-layout>
    `}static get properties(){return{hass:{type:Object},error:{type:Boolean,value:!1},rendering:{type:Boolean,value:!1},template:{type:String,value:'Imitate available variables:\n{% set my_test_json = {\n  "temperature": 25,\n  "unit": "°C"\n} %}\n\nThe temperature is {{ my_test_json.temperature }} {{ my_test_json.unit }}.\n\n{% if is_state("device_tracker.paulus", "home") and\n      is_state("device_tracker.anne_therese", "home") -%}\n  You are both home, you silly\n{%- else -%}\n  Anne Therese is at {{ states("device_tracker.anne_therese") }}\n  Paulus is at {{ states("device_tracker.paulus") }}\n{%- endif %}\n\nFor loop example:\n{% for state in states.sensor -%}\n  {%- if loop.first %}The {% elif loop.last %} and the {% else %}, the {% endif -%}\n  {{ state.name | lower }} is {{state.state_with_unit}}\n{%- endfor %}.',observer:"templateChanged"},processed:{type:String,value:""}}}computeFormClasses(e){return e?"content fit":"content fit layout horizontal"}computeRenderedClasses(e){return e?"error rendered":"rendered"}templateChanged(){this.error&&(this.error=!1),this._debouncer=a.a.debounce(this._debouncer,i.d.after(500),()=>{this.renderTemplate()})}renderTemplate(){this.rendering=!0,this.hass.callApi("POST","template",{template:this.template}).then(function(e){this.processed=e,this.rendering=!1}.bind(this),function(e){this.processed=e&&e.body&&e.body.message||"Unknown error rendering template",this.error=!0,this.rendering=!1}.bind(this))}})}}]);
//# sourceMappingURL=ef784bc6be92bfd5bd5e.chunk.js.map