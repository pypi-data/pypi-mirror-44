(window.webpackJsonp=window.webpackJsonp||[]).push([[62],{763:function(t,e,a){"use strict";a.r(e);var s=a(3),n=a(20),i=a(111),o=a(101);customElements.define("notification-manager",class extends(Object(i.a)(n.a)){static get template(){return s.a`
      <style>
        paper-toast {
          z-index: 1;
        }
      </style>

      <ha-toast
        id="toast"
        dir="[[_rtl]]"
        no-cancel-on-outside-click="[[_cancelOnOutsideClick]]"
      ></ha-toast>
    `}static get properties(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1},_rtl:{type:String,computed:"_computeRTLDirection(hass)"}}}ready(){super.ready(),Promise.all([a.e(1),a.e(29)]).then(a.bind(null,404))}showDialog({message:t}){this.$.toast.show(t)}_computeRTLDirection(t){return Object(o.a)(t)?"rtl":"ltr"}})}}]);