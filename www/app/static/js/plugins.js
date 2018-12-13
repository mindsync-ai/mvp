
// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console) {
    arguments.callee = arguments.callee.caller;
    var newarr = [].slice.call(arguments);
    (typeof console.log === 'object' ? log.apply.call(console.log, console, newarr) : console.log.apply(console, newarr));
  }
};

// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());


(function()
{
  //first, checks if it isn't implemented yet
  if (!String.prototype.format)
  {
    String.prototype.format = function()
    {
      var args = arguments;

      return this.replace(/{(\d+)}/g,
        function (match, number)
        {
          return typeof args[number] != 'undefined'? args[number]: match;
        });
    };
  }

  String.prototype.capitalizeFirstLetter = function() {
      return this.charAt(0).toUpperCase() + this.slice(1);
  }
})();

// place any jQuery/helper plugins in here, instead of separate, slower script files.
(function currencyPlugin($) {
  $.fn.currencyInput = function() {
    this.each(function() {
      var wrapper = $("<div class='currency-input' />");
      $(this).wrap(wrapper);
        $(this).before("<span class='currency-symbol'></span");
      $(this).change(function()
      {
        var min = parseFloat($(this).attr("min"));
        var max = parseFloat($(this).attr("max"));
        var value = parseFloat($(this).val());
        if (isNaN(value))
        {
          $(this).val('');
          return
        }

        if(value < min)
          value = min;
        else if(value > max)
          value = max;

        $(this).val(value.toFixed(2));
      });
    });
  };
})(jQuery);
