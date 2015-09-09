Angular.js Hello World
-------
https://angularjs.org/

Note: `angular.min.js` is automatically downloaded if not found in your home directory under `rusthon_cache`,
see the special `source` attribute of the `script` tag below that instructs the transpiler to do the download.

```html
<html>
<head>
<link href='~/bootstrap-3.3.5-dist/css/bootstrap.css' rel='stylesheet' zip="https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip"/>
<script src="~/rusthon_cache/jquery-2.1.4.min.js" source="http://code.jquery.com/jquery-2.1.4.min.js"></script>
<script src="~/bootstrap-3.3.5-dist/js/bootstrap.min.js"></script>

<script src="~/rusthon_cache/angular.min.js" source="https://ajax.googleapis.com/ajax/libs/angularjs/1.3.9/angular.min.js"></script>

<@myscript>

</head>
<body>

<div ng-app="invoice1" ng-controller="InvoiceController as invoice">
  <b>Invoice:</b>
  <div class="well">
    Quantity: <input type="number" min="0" ng-model="invoice.qty" required >
  </div>
  <div class="well">
    Costs: <input type="number" min="0" ng-model="invoice.cost" required >
    <select ng-model="invoice.inCurr">
      <option ng-repeat="c in invoice.currencies">{{c}}</option>
    </select>
  </div>
  <div class="well">
    <b>Total:</b>
    <span ng-repeat="c in invoice.currencies">
      {{invoice.total(c) | currency:c}}
    </span>
    <button class="btn" ng-click="invoice.pay()">Pay</button>
  </div>
</div>

</body>
</html>
```
Above a special syntax is used `@myscript` this tells Rusthon where to insert the output of scripts it translates using the javascript backend.

rusthon
-------
Below `@myscript` is given on the line just before the fenced rusthon code block.  This allows you to insert multiple scripts into your html, in the head or body.

@myscript
```rusthon
#backend:javascript
from runtime import *

module = angular.module('invoice1', [])

def invoice_controller():
	this.qty = 1
	this.cost = 2
	this.inCurr = 'EUR'
	this.currencies = ['USD', 'EUR', 'CNY']
	this.usdToForeignRates = {
		'USD': 1,
		'EUR': 0.74,
		'CNY': 6.09
	}

	def total(outCurr):
		return this.convertCurrency(this.qty * this.cost, this.inCurr, outCurr)
	def convertCurrency(amount, inCurr, outCurr):
		return amount * this.usdToForeignRates[outCurr] / this.usdToForeignRates[inCurr]
	def pay():
		window.alert("Thanks!")

	this.pay = pay
	this.total = total
	this.convertCurrency = convertCurrency

module.controller('InvoiceController', invoice_controller)
```
