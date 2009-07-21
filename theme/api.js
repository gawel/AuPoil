var apwal = {
    showStats: function(data) {
        var count = data['count'];
        var title = count+' Hits for '+data['alias']+' - '+data['url'];
        var link = document.getElementById('apwalfr_'+data['alias']);
        link.innerHTML = '('+count+')';
        link.setAttribute('title', title);
    },
    twitterQuick: function(data) {
        if (!data['error'])
            window.location = "http://twitter.com/home?status="+data['url'];
        else
            alert(data['error']);
    },
    fbQuick: function(data) {
        if (!data['error'])
            window.location = "http://www.facebook.com/share.php?u="+data['url'];
        else
            alert(data['error']);
    }
}
