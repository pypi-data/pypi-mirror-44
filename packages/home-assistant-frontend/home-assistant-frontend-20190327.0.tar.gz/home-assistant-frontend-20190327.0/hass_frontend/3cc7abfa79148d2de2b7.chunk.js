(window.webpackJsonp=window.webpackJsonp||[]).push([[13],{786:function(a,e,i){"use strict";i.r(e);var t=i(5),r=(i(186),i(196),i(85),i(52));customElements.define("dialog-area-registry-detail",class extends t.a{constructor(...a){super(...a),this.hass=void 0,this._name=void 0,this._error=void 0,this._params=void 0,this._submitting=void 0}static get properties(){return{_error:{},_name:{},_params:{}}}async showDialog(a){this._params=a,this._error=void 0,this._name=this._params.entry?this._params.entry.name:"",await this.updateComplete}render(){if(!this._params)return t.e``;const a=this._params.entry,e=""===this._name.trim();return t.e`
      <paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>
          ${a?a.name:this.hass.localize("ui.panel.config.area_registry.editor.default_name")}
        </h2>
        <paper-dialog-scrollable>
          ${this._error?t.e`
                <div class="error">${this._error}</div>
              `:""}
          <div class="form">
            ${a?t.e`
                  <div>Area ID: ${a.area_id}</div>
                `:""}

            <paper-input
              .value=${this._name}
              @value-changed=${this._nameChanged}
              label="Name"
              error-message="Name is required"
              .invalid=${e}
            ></paper-input>
          </div>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          ${a?t.e`
                <mwc-button
                  class="warning"
                  @click="${this._deleteEntry}"
                  .disabled=${this._submitting}
                >
                  ${this.hass.localize("ui.panel.config.area_registry.editor.delete")}
                </mwc-button>
              `:t.e``}
          <mwc-button
            @click="${this._updateEntry}"
            .disabled=${e||this._submitting}
          >
            ${a?this.hass.localize("ui.panel.config.area_registry.editor.update"):this.hass.localize("ui.panel.config.area_registry.editor.create")}
          </mwc-button>
        </div>
      </paper-dialog>
    `}_nameChanged(a){this._error=void 0,this._name=a.detail.value}async _updateEntry(){this._submitting=!0;try{const a={name:this._name.trim()};this._params.entry?await this._params.updateEntry(a):await this._params.createEntry(a),this._params=void 0}catch(a){this._error=a.message||"Unknown error"}finally{this._submitting=!1}}async _deleteEntry(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}_openedChanged(a){a.detail.value||(this._params=void 0)}static get styles(){return[r.b,t.c`
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