(window.webpackJsonp=window.webpackJsonp||[]).push([[138],{791:function(e,a,o){"use strict";o.r(a);o(196),o(186);var s=o(3),l=o(20),t=(o(86),o(70));customElements.define("zwave-log-dialog",class extends(Object(t.a)(l.a)){static get template(){return s.a`
    <style include="ha-style-dialog">
    </style>
      <paper-dialog id="pwaDialog" with-backdrop="" opened="{{_opened}}">
        <h2>OpenZwave internal logfile</h2>
        <paper-dialog-scrollable>
          <pre>[[_ozwLog]]</pre>
        <paper-dialog-scrollable>
      </paper-dialog>
      `}static get properties(){return{hass:Object,_ozwLog:String,_dialogClosedCallback:Function,_opened:{type:Boolean,value:!1},_intervalId:String,_numLogLines:{type:Number}}}ready(){super.ready(),this.addEventListener("iron-overlay-closed",e=>this._dialogClosed(e))}showDialog({_ozwLog:e,hass:a,_tail:o,_numLogLines:s,dialogClosedCallback:l}){this.hass=a,this._ozwLog=e,this._opened=!0,this._dialogClosedCallback=l,this._numLogLines=s,setTimeout(()=>this.$.pwaDialog.center(),0),o&&this.setProperties({_intervalId:setInterval(()=>{this._refreshLog()},1500)})}async _refreshLog(){const e=await this.hass.callApi("GET","zwave/ozwlog?lines="+this._numLogLines);this.setProperties({_ozwLog:e})}_dialogClosed(e){if("ZWAVE-LOG-DIALOG"===e.target.nodeName){clearInterval(this._intervalId),this._opened=!1;const e=!0;this._dialogClosedCallback({closedEvent:e}),this._dialogClosedCallback=null}}})}}]);