(window.webpackJsonp=window.webpackJsonp||[]).push([[66],{188:function(e,t,a){"use strict";var i=a(3),s=a(20);a(86);customElements.define("ha-config-section",class extends s.a{static get template(){return i.a`
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
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},226:function(e,t,a){"use strict";t.a=((e,t)=>e<t?-1:e>t?1:0)},252:function(e,t,a){"use strict";a.d(t,"c",function(){return i}),a.d(t,"a",function(){return s}),a.d(t,"d",function(){return r}),a.d(t,"b",function(){return n});const i=e=>e.callWS({type:"config/area_registry/list"}),s=(e,t)=>e.callWS(Object.assign({type:"config/area_registry/create"},t)),r=(e,t,a)=>e.callWS(Object.assign({type:"config/area_registry/update",area_id:t},a)),n=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t})},744:function(e,t,a){"use strict";a.r(t);var i=a(5),s=(a(131),a(172),a(166),a(234),a(252)),r=(a(142),a(268),a(226)),n=(a(188),a(42));const o=()=>Promise.all([a.e(0),a.e(1),a.e(101),a.e(13)]).then(a.bind(null,786)),p=(e,t)=>{Object(n.a)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:o,dialogParams:t})};var c=a(64),l=a(101);customElements.define("ha-config-area-registry",class extends i.a{constructor(...e){super(...e),this.hass=void 0,this.isWide=void 0,this._items=void 0}static get properties(){return{hass:{},isWide:{},_items:{}}}render(){return this.hass&&void 0!==this._items?i.e`
      <hass-subpage
        header="${this.hass.localize("ui.panel.config.area_registry.caption")}"
      >
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">
            ${this.hass.localize("ui.panel.config.area_registry.picker.header")}
          </span>
          <span slot="introduction">
            ${this.hass.localize("ui.panel.config.area_registry.picker.introduction")}
            <p>
              ${this.hass.localize("ui.panel.config.area_registry.picker.introduction2")}
            </p>
            <a href="/config/integrations/dashboard">
              ${this.hass.localize("ui.panel.config.area_registry.picker.integrations_page")}
            </a>
          </span>
          <paper-card>
            ${this._items.map(e=>i.e`
                <paper-item @click=${this._openEditEntry} .entry=${e}>
                  <paper-item-body>
                    ${e.name}
                  </paper-item-body>
                </paper-item>
              `)}
            ${0===this._items.length?i.e`
                  <div class="empty">
                    ${this.hass.localize("ui.panel.config.area_registry.no_areas")}
                    <mwc-button @click=${this._createArea}>
                      ${this.hass.localize("ui.panel.config.area_registry.create_area")}
                    </mwc-button>
                  </div>
                `:i.e``}
          </paper-card>
        </ha-config-section>
      </hass-subpage>

      <paper-fab
        ?is-wide=${this.isWide}
        icon="hass:plus"
        title="${this.hass.localize("ui.panel.config.area_registry.create_area")}"
        @click=${this._createArea}
        class="${Object(c.a)({rtl:Object(l.a)(this.hass)})}"
      ></paper-fab>
    `:i.e`
        <hass-loading-screen></hass-loading-screen>
      `}firstUpdated(e){super.firstUpdated(e),this._fetchData(),o()}async _fetchData(){this._items=(await Object(s.c)(this.hass)).sort((e,t)=>Object(r.a)(e.name,t.name))}_createArea(){this._openDialog()}_openEditEntry(e){const t=e.currentTarget.entry;this._openDialog(t)}_openDialog(e){p(this,{entry:e,createEntry:async e=>{const t=await Object(s.a)(this.hass,e);this._items=this._items.concat(t).sort((e,t)=>Object(r.a)(e.name,t.name))},updateEntry:async t=>{const a=await Object(s.d)(this.hass,e.area_id,t);this._items=this._items.map(t=>t===e?a:t)},removeEntry:async()=>{if(!confirm("Are you sure you want to delete this area?\n\nAll devices in this area will become unassigned."))return!1;try{return await Object(s.b)(this.hass,e.area_id),this._items=this._items.filter(t=>t!==e),!0}catch(e){return!1}}})}static get styles(){return i.c`
      a {
        color: var(--primary-color);
      }
      paper-card {
        display: block;
        max-width: 600px;
        margin: 16px auto;
      }
      .empty {
        text-align: center;
      }
      paper-item {
        cursor: pointer;
        padding-top: 4px;
        padding-bottom: 4px;
      }
      paper-fab {
        position: fixed;
        bottom: 16px;
        right: 16px;
        z-index: 1;
      }

      paper-fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }

      paper-fab.rtl {
        right: auto;
        left: 16px;
      }

      paper-fab[is-wide].rtl {
        bottom: 24px;
        right: auto;
        left: 24px;
      }
    `}})}}]);