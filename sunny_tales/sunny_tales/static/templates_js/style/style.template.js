(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['style.template'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [2,'>= 1.0.0-rc.3'];
helpers = helpers || Handlebars.helpers; data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n            <tr>\n                <td>";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.name; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n                <td>";
  options = {hash:{},data:data};
  stack2 = ((stack1 = helpers.f_displayStyle),stack1 ? stack1.call(depth0, depth0.input_type, options) : helperMissing.call(depth0, "f_displayStyle", depth0.input_type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "</td>\n            </tr>\n        ";
  return buffer;
  }

  buffer += "<table id=";
  if (stack1 = helpers.elementId) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.elementId; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " class='table table-hover' data-target_id=";
  if (stack1 = helpers.targetId) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.targetId; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + ">\n    <thead>\n        <tr>\n            <th>Property</th>\n            <th>Value</th>\n        </tr>\n    </thead>\n    <tbody>\n        ";
  stack1 = helpers.each.call(depth0, depth0.styles, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </tbody>\n</table>";
  return buffer;
  });
})();