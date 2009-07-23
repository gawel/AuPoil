var prefManager = Components.classes["@mozilla.org/preferences-service;1"]
                                .getService(Components.interfaces.nsIPrefBranch);

var apwalfr = {
  doc: null,
  pref_key: 'extensions.apwalfr.',
  sites: [
    ["del.icio.us", "Save to del.icio.us", "http://del.icio.us/post?url=$u&title=$t", "delicious.png", 204, 0],
    ["Digg", "Digg It!", "http://digg.com/submit?phase=2&url=$u&title=$t", "digg.png", 221, 0],
    ["Facebook", "Save to Facebook", "http://www.facebook.com/share.php?u=$u", "facebook.png", 306, 0],
    ["Google", "Save to Google Bookmarks", "http://www.google.com/bookmarks/mark?op=edit&output=popup&bkmk=$u&title=$t", "google.png", 425, 0],
    ["LinkedIn", "Share on LinkedIn", "http://www.linkedin.com/shareArticle?mini=true&url=$u&title=$t", "linkedin.png", 1155, 0],
    ["MySpace", "Save to MySpace", "http://www.myspace.com/Modules/PostTo/Pages/?c=$u&t=$t", "myspace.png", 595, 0],
    ["OnlyWire", "Save to OnlyWire", "http://www.onlywire.com/submit?u=$u&gt=$t", "onlywire.png", 1071, 0],
    ["Reddit", "Reddit", "http://reddit.com/submit?url=$u&title=$t", "reddit.png", 714, 0],
    ["Slashdot", "Slashdot It!", "http://slashdot.org/bookmark.pl?url=$u&title=$t", "slashdot.png", 799, 0],
    ["Technorati", "Add to my Technorati Favorites", "http://technorati.com/faves?add=$u", "technorati.png", 901, 0],
    ["Twitter", "Save to Twitter", "http://twitter.com/home/?status=$t+$u", "twitter.png", 1105, 0],
    ["Windows Live", "Save to Windows Live", "https://favorites.live.com/quickadd.aspx?mkt=en-us&url=$u&title=$t", "windowslive.png", 952, 0],
    ["Yahoo!", "Save to Yahoo! Bookmarks", "http://bookmarks.yahoo.com/toolbar/savebm?opener=tb&u=$u&t=$t", "yahoo.png", 969, 0]
  ],

  getPref: function(key) {
      return prefManager.getCharPref(this.pref_key+key);
  },
  setPref: function(key, value) {
      prefManager.setCharPref(this.pref_key+key, value);
  },
  setDefaultPref: function(key, value) {
      try {this.getPref(key);} catch(e) {this.setPref(key, value);}
  },

  addScript: function(url) {
    var doc = this.doc;
    var s = doc.createElement('script');
    s.setAttribute('src', this.getPref('server')+url);
    s.setAttribute('type', 'text/javascript');
    doc.body.appendChild(s);
  },

  createMenuItem: function(site, name, command) {
    const XUL_NS = "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul";
    var item = document.createElementNS(XUL_NS, "menuitem");
    item.setAttribute("image", this.getPref('server') + '/_static/images/bookmarkify/'+site[3]);
    item.setAttribute("label", site[1]);
    item.setAttribute("value", site[0]);
    item.setAttribute("oncommand", command)
    item.setAttribute("name", name);
    item.setAttribute("type", "radio");
    return item
  },

  onLoad: function() {
    // initialization code
    var klass = this;

    this.setDefaultPref('default_action', 'popup');
    this.setDefaultPref('server', 'http://a.pwal.fr');

    document.getElementById('popup-apwalfr').setAttribute("image", klass.getPref('server')+'/_static/images/favicon.ico')

    var menu = document.getElementById("menu-apwalfr");
    var separator = document.getElementById("bookmark-sep-apwalfr");
    jQuery(klass.sites).each(function() {
       var item = klass.createMenuItem(this, "apwalfr_quick", "apwalfr.onQuick(this)");
       menu.appendChild(item);
       menu.insertBefore(item, separator);
    });

    var value = klass.getPref('default_action');
    menu = document.getElementById("action-apwalfr");
    menu.firstChild.setAttribute("image", klass.getPref('server')+'/_static/images/favicon.ico')
    jQuery(klass.sites).each(function() {
       var item = klass.createMenuItem(this, "apwalfr_action", "apwalfr.onSetDefault(this)");
       if (item.getAttribute("value") == value) {
            item.setAttribute('checked', 'true');
            document.getElementById("default-action-apwalfr").setAttribute('label', 'Default action: '+item.getAttribute("label"));
       }
       menu.appendChild(item);
    });

    this.initialized = true;
  },

  onShowDefault: function(obj) {
    var klass = this;

    var value = klass.getPref('default_action');
    for (var item = obj.firstitem; item; item = item.nextSibling) {
        if (item.getAttribute('value') == value) {
            item.setAttribute('checked', 'true');
            document.getElementById("default-action-apwalfr").setAttribute('label', 'Default action: '+item.getAttribute("label"));
        }
    }
  },

  onSetDefault: function(obj) {
    this.setPref('default_action', obj.getAttribute('value'));
    document.getElementById("default-action-apwalfr").setAttribute('label', 'Default action: '+obj.getAttribute("label"));
  },

  onMenuItemCommand: function(obj, event) {
    // load api
    var doc = window.content.document;
    var server = this.getPref('server');
    this.doc = doc;

    if (jQuery('script[src="'+server+'/_static/api.js"]', doc).length == 0)
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
    var server = this.getPref('server');
    var url = doc.location;

    jQuery('#apwalfr', doc).remove();
    jQuery('#apwalfr_close', doc).remove();

    var close = "document.getElementById('apwalfr').style.display='none'; this.style.display='none'"
    jQuery('body', doc).prepend('' +
        '<div id="apwalfr_close" onclick="'+close+'" ' +
             'style=z-index:1000001;float:left;top:55px;left:435px;position:fixed;border:0px;display:block;">' +
          '<img style="width:20px;height:20px;border:0px;" src="'+server+'/_static/images/close.png" />' +
        '</div>' +
        '<iframe src="'+server+'/?p=firefox&post='+url+'" id="apwalfr"' +
                'style="z-index:1000000;float:left;top:50px;left:30px;position:fixed;border:thin solid black; width:430px; height:230px;"' +
               ' />' +
        '</iframe>'+
        '');
  },

  onQuick: function(obj, type) {
    if (!type)
       type = obj.getAttribute("value");
    var url = null;
    jQuery.each(this.sites, function() {
        if (this[0] == type) url = this[2];
    });
    this.addScript('/json/?callback=apwal.quickPost&arg='+encodeURIComponent(url)+'&url='+encodeURIComponent(this.doc.location.href));
  },

  onShowStats: function(obj) {
    var klass = this;
    var doc = this.doc;
    var server = this.getPref('server');
    jQuery('a.apwalfr_link', doc).remove();
    jQuery('a[href^="'+server+'/"]', doc).each(function() {
            var link = jQuery(this);
            var id = link.attr('href').replace(server+'/', '');
            link.after(' <a id="apwalfr_'+id+'" class="apwalfr_link" href="'+server+'/stats/'+id+'" target="_blank"></a>');
            klass.addScript('/json/stats/?callback=apwal.showStats&alias='+id);
    });
  }

}

window.addEventListener("load", function(e) { apwalfr.onLoad(e); }, false);
