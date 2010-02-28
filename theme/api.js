var apwal = {
    showStats: function(data) {
        var count = data['count'];
        var title = count+' Hits for '+data['alias']+' - '+data['url'];
        var link = document.getElementById('apwalfr_'+data['alias']);
        link.innerHTML = '('+count+')';
        link.setAttribute('title', title);
    },
    quickPost: function(url, data) {
        if (data['new_url']) {
            url = url.replace('$t', encodeURIComponent(document.title)).replace('$u', encodeURIComponent(data['new_url']));
            window.top.location = url;
        } else {
            alert(data['error']);
        }
    },
    twitterQuick: function(data) {
        if (data['new_url'])
            window.top.location = "http://twitter.com/home?status="+data['new_url'];
        else
            alert(data['error']);
    },
    fbQuick: function(data) {
        if (data['new_url'])
            window.top.location = "http://www.facebook.com/share.php?u="+data['new_url'];
        else
            alert(data['error']);
    }
}
