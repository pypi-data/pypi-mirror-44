(window.webpackJsonp=window.webpackJsonp||[]).push([[22],{789:function(t,i,e){"use strict";e.r(i);var a=e(5),s=(e(186),e(196),e(85),e(52)),n=e(171),r=e(165);customElements.define("dialog-entity-registry-detail",class extends a.a{constructor(...t){super(...t),this.hass=void 0,this._name=void 0,this._entityId=void 0,this._error=void 0,this._params=void 0,this._submitting=void 0}static get properties(){return{_error:{},_name:{},_entityId:{},_params:{}}}async showDialog(t){this._params=t,this._error=void 0,this._name=this._params.entry.name||"",this._entityId=this._params.entry.entity_id,await this.updateComplete}render(){if(!this._params)return a.e``;const t=this._params.entry,i=this.hass.states[t.entity_id],e=Object(n.a)(this._entityId.trim())!==Object(n.a)(this._params.entry.entity_id);return a.e`
      <paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>${t.entity_id}</h2>
        <paper-dialog-scrollable>
          ${i?"":a.e`
                <div>
                  ${this.hass.localize("ui.panel.config.entity_registry.editor.unavailable")}
                </div>
              `}
          ${this._error?a.e`
                <div class="error">${this._error}</div>
              `:""}
          <div class="form">
            <paper-input
              .value=${this._name}
              @value-changed=${this._nameChanged}
              .label=${this.hass.localize("ui.dialogs.more_info_settings.name")}
              .placeholder=${i?Object(r.a)(i):""}
              .disabled=${this._submitting}
            ></paper-input>
            <paper-input
              .value=${this._entityId}
              @value-changed=${this._entityIdChanged}
              .label=${this.hass.localize("ui.dialogs.more_info_settings.entity_id")}
              error-message="Domain needs to stay the same"
              .invalid=${e}
              .disabled=${this._submitting}
            ></paper-input>
          </div>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <mwc-button
            class="warning"
            @click="${this._deleteEntry}"
            .disabled=${this._submitting}
          >
            ${this.hass.localize("ui.panel.config.entity_registry.editor.delete")}
          </mwc-button>
          <mwc-button
            @click="${this._updateEntry}"
            .disabled=${e||this._submitting}
          >
            ${this.hass.localize("ui.panel.config.entity_registry.editor.update")}
          </mwc-button>
        </div>
      </paper-dialog>
    `}_nameChanged(t){this._error=void 0,this._name=t.detail.value}_entityIdChanged(t){this._error=void 0,this._entityId=t.detail.value}async _updateEntry(){this._submitting=!0;try{await this._params.updateEntry({name:this._name.trim()||null,new_entity_id:this._entityId.trim()}),this._params=void 0}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}async _deleteEntry(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}_openedChanged(t){t.detail.value||(this._params=void 0)}static get styles(){return[s.b,a.c`
        paper-dialog {
          min-width: 400px;
        }
        .form {
          padding-bottom: 24px;
        }
        mwc-button.warning {
          margin-right: auto;
        }
        .error {
          color: var(--google-red-500);
        }
      `]}})}}]);