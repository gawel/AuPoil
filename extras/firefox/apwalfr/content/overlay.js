var apwalfr = {
  _doc: null,
  serv: 'http://a.pwal.fr',

  onLoad: function() {
    // initialization code
    this.initialized = true;
  },

  addScript: function(url) {
    var doc = apwalfr._doc;
    var s = doc.createElement('script');
    s.setAttribute('src', apwalfr.serv+url);
    s.setAttribute('type', 'text/javascript');
    doc.body.appendChild(s);
  },    

  onMenuItemCommand: function(event) {
    // load api
    var doc = window.content.document;
    apwalfr._doc = doc;
    if (jQuery('script#apwal-api').length == 0) {
        apwalfr.addScript('/_static/api.js');
    }

    if (event.button != 0)
        return;
                         
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
    apwalfr.addScript('/json/?callback=apwal.'+type+'Quick&url='+apwalfr._doc.location);
  },
  onShowStats: function(obj) {
    var doc = apwalfr._doc;
    jQuery('a.apwalfr_link', doc).remove();
    jQuery('a[href^="'+apwalfr.serv+'/"]', doc).each(function() {
            var link = jQuery(this);
            var id = link.attr('href').split('/')[3];
            link.after(' <a id="apwalfr_'+id+'" class="apwalfr_link" href="'+apwalfr.serv+'/stats/'+id+'" target="_blank"></a>');
            apwalfr.addScript('/json/stats/?callback=apwal.showStats&alias='+id);
    });
  }

};
window.addEventListener("load", function(e) { apwalfr.onLoad(e); }, false);
