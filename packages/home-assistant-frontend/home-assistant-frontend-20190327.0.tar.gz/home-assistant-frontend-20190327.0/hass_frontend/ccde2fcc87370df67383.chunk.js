(window.webpackJsonp=window.webpackJsonp||[]).push([[74],{188:function(e,t,s){"use strict";var a=s(3),i=s(20);s(86);customElements.define("ha-config-section",class extends i.a{static get template(){return a.a`
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
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},226:function(e,t,s){"use strict";t.a=((e,t)=>e<t?-1:e>t?1:0)},319:function(e,t,s){"use strict";s.d(t,"a",function(){return a}),s.d(t,"b",function(){return i}),s.d(t,"d",function(){return n}),s.d(t,"e",function(){return o}),s.d(t,"c",function(){return r});const a="system-admin",i="system-users",n=async e=>e.callWS({type:"config/auth/list"}),o=async(e,t,s)=>e.callWS(Object.assign({},s,{type:"config/auth/update",user_id:t})),r=async(e,t)=>e.callWS({type:"config/auth/delete",user_id:t})},742:function(e,t,s){"use strict";s.r(t);var a=s(5);s(131),s(172),s(166),s(234);const i=e=>e.callWS({type:"person/list"}),n=(e,t)=>e.callWS(Object.assign({type:"person/create"},t)),o=(e,t,s)=>e.callWS(Object.assign({type:"person/update",person_id:t},s)),r=(e,t)=>e.callWS({type:"person/delete",person_id:t});s(142),s(268);var p=s(226),c=(s(188),s(42));const d=()=>Promise.all([s.e(0),s.e(1),s.e(2),s.e(3),s.e(96)]).then(s.bind(null,799)),l=(e,t)=>{Object(c.a)(e,"show-dialog",{dialogTag:"dialog-person-detail",dialogImport:d,dialogParams:t})};var h=s(319);customElements.define("ha-config-person",class extends a.a{constructor(...e){super(...e),this.hass=void 0,this.isWide=void 0,this._storageItems=void 0,this._configItems=void 0,this._usersLoad=void 0}static get properties(){return{hass:{},isWide:{},_storageItems:{},_configItems:{}}}render(){return this.hass&&void 0!==this._storageItems&&void 0!==this._configItems?a.e`
      <hass-subpage header="Persons">
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">Persons</span>
          <span slot="introduction">
            Here you can define each person of interest in Home Assistant.
            ${this._configItems.length>0?a.e`
                  <p>
                    Note: persons configured via configuration.yaml cannot be
                    edited via the UI.
                  </p>
                `:""}
          </span>
          <paper-card class="storage">
            ${this._storageItems.map(e=>a.e`
                <paper-item @click=${this._openEditEntry} .entry=${e}>
                  <paper-item-body>
                    ${e.name}
                  </paper-item-body>
                </paper-item>
              `)}
            ${0===this._storageItems.length?a.e`
                  <div class="empty">
                    Looks like you have not created any persons yet.
                    <mwc-button @click=${this._createPerson}>
                      CREATE PERSON</mwc-button
                    >
                  </div>
                `:a.e``}
          </paper-card>
          ${this._configItems.length>0?a.e`
                <paper-card heading="Configuration.yaml persons">
                  ${this._configItems.map(e=>a.e`
                      <paper-item>
                        <paper-item-body>
                          ${e.name}
                        </paper-item-body>
                      </paper-item>
                    `)}
                </paper-card>
              `:""}
        </ha-config-section>
      </hass-subpage>

      <paper-fab
        ?is-wide=${this.isWide}
        icon="hass:plus"
        title="Create Area"
        @click=${this._createPerson}
      ></paper-fab>
    `:a.e`
        <hass-loading-screen></hass-loading-screen>
      `}firstUpdated(e){super.firstUpdated(e),this._fetchData(),d()}async _fetchData(){this._usersLoad=Object(h.d)(this.hass);const e=await i(this.hass);this._storageItems=e.storage.sort((e,t)=>Object(p.a)(e.name,t.name)),this._configItems=e.config.sort((e,t)=>Object(p.a)(e.name,t.name))}_createPerson(){this._openDialog()}_openEditEntry(e){const t=e.currentTarget.entry;this._openDialog(t)}_allowedUsers(e,t){const s=new Set;for(const e of[this._configItems,this._storageItems])for(const t of e)t.user_id&&s.add(t.user_id);const a=t?t.user_id:void 0;return e.filter(e=>e.id===a||!s.has(e.id))}async _openDialog(e){const t=await this._usersLoad;l(this,{entry:e,users:this._allowedUsers(t,e),createEntry:async e=>{const t=await n(this.hass,e);this._storageItems=this._storageItems.concat(t).sort((e,t)=>Object(p.a)(e.name,t.name))},updateEntry:async t=>{const s=await o(this.hass,e.id,t);this._storageItems=this._storageItems.map(t=>t===e?s:t)},removeEntry:async()=>{if(!confirm("Are you sure you want to delete this person?\n\nAll devices belonging to this person will become unassigned."))return!1;try{return await r(this.hass,e.id),this._storageItems=this._storageItems.filter(t=>t!==e),!0}catch(e){return!1}}})}static get styles(){return a.c`
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
        padding: 8px;
      }
      paper-item {
        padding-top: 4px;
        padding-bottom: 4px;
      }
      paper-card.storage paper-item {
        cursor: pointer;
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
    `}})}}]);