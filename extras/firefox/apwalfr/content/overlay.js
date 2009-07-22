var prefManager = Components.classes["@mozilla.org/preferences-service;1"]
                                .getService(Components.interfaces.nsIPrefBranch);

var apwalfr = {
  doc: null,
  serv: 'http://a.pwal.fr',
  pref_key: 'extensions.apwalfr.',

  getPref: function(key) {
      return prefManager.getCharPref(this.pref_key+key);
  },
  setPref: function(key, value) {
      prefManager.setCharPref(this.pref_key+key, value);
  },
  setDefaultPref: function(key, value) {
      if (!this.getPref(key)) this.setPref(key, value);
  },

  addScript: function(url) {
    var doc = this.doc;
    var s = doc.createElement('script');
    s.setAttribute('src', apwalfr.serv+url);
    s.setAttribute('type', 'text/javascript');
    doc.body.appendChild(s);
  },

  onLoad: function() {
    // initialization code
    this.setDefaultPref('default_action', 'popup');

    this.initialized = true;
  },

  onShowDefault: function(obj) {
    var value = this.getPref('default_action');
    for (var child = obj.firstChild; child; child = child.nextSibling) {
        if (child.getAttribute('value') == value)
            child.setAttribute('checked', 'true');
    }
  },

  onSetDefault: function(obj) {
    this.setPref('default_action', obj.getAttribute('value'));
  },

  onMenuItemCommand: function(obj, event) {
    // load api
    var doc = window.content.document;
    this.doc = doc;

    if (jQuery('script[src="'+this.serv+'/_static/api.js"]', doc).length == 0)
        this.addScript('/_static/api.js');

    if (event.button != 0)
        return;

    var value = this.getPref('default_action');
    if (value == 'popup')
        this.onPopup(obj);
    else
        this.onQuick(obj, value);
  },

  onPopup: function() {
    var doc = this.doc;
    var url = doc.location;

    jQuery('#apwalfr', doc).remove();
    jQuery('#apwalfr_close', doc).remove();

    var close = "document.getElementById('apwalfr').style.display='none'; this.style.display='none'"
    jQuery('body', doc).prepend('' +
        '<div id="apwalfr_close" onclick="'+close+'" ' +
             'style=z-index:1000001;float:left;top:55px;left:435px;position:fixed;border:0px;display:block;">' +
          '<img style="width:20px;height:20px;border:0px;" src="'+apwalfr.serv+'/_static/images/close.png" />' +
        '</div>' +
        '<iframe src="'+apwalfr.serv+'/?p=firefox&post='+url+'" id="apwalfr"' +
                'style="z-index:1000000;float:left;top:50px;left:30px;position:fixed;border:thin solid black; width:430px; height:230px;"' +
               ' />' +
        '</iframe>'+
        '');
  },

  onQuick: function(obj, type) {
    this.addScript('/json/?callback=apwal.'+type+'Quick&url='+this.doc.location);
  },

  onShowStats: function(obj) {
    var doc = this.doc;
    jQuery('a.apwalfr_link', doc).remove();
    jQuery('a[href^="'+apwalfr.serv+'/"]', doc).each(function() {
            var link = jQuery(this);
            var id = link.attr('href').replace(apwalfr.serv+'/');
            link.after(' <a id="apwalfr_'+id+'" class="apwalfr_link" href="'+apwalfr.serv+'/stats/'+id+'" target="_blank"></a>');
            apwalfr.addScript('/json/stats/?callback=apwal.showStats&alias='+id);
    });
  }

}

window.addEventListener("load", function(e) { apwalfr.onLoad(e); }, false);
