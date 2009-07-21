var apwal = {
    showStats: function(data) {
        var count = data['count'];
        var title = count+' Hits for '+data['alias']+' - '+data['url'];
        var link = document.getElementById('apwalfr_'+data['alias']);
        link.innerHTML = '('+count+')';
        link.setAttribute('title', title);
    }
}
