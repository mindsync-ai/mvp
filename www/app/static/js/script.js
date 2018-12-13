function toHumanReadableSize(sz) {
  var Kb = 1024;
  var Mb = Kb * Kb;
  var Gb = Mb * Kb;

  if (sz < Kb)
  {
    return sz + " Bytes";
  } else if (sz >= Kb && sz < Mb) {
    return (sz / Kb).toFixed(2) + " Kbytes"
  } else if (sz >= Mb && sz < Gb) {
    return (sz / Mb).toFixed(2) + " Mbytes"
  } else {
    return (sz / Gb).toFixed(2) + " Gbytes"
  }
}

function urlify(text)
{
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a target="_blank" href="' + url + '">' + url + '</a>';
    })
}





















