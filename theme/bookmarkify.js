
jQuery.fn.extend({
    redirectBookmark: function() {
        var clicked = $(this);
        var self = $('a.bookmarkInfo', clicked.parents('div.bookmarkify'));
        var server = self.attr('alt');
        var href = self.attr('href');
        var title = self.attr('title');
        var alias = self.text();
        var url = clicked.attr('alt');
        $.getJSON(server+'/json/?callback=?&url='+href+'&alias='+alias, function(data) {
            var url = clicked.attr('alt').replace('$u', data['new_url']).replace('$t', title);
            alert(url);
            window.location.href = url;
        });
        return false;
    },
    showBookmarksLinks: function(options) {

        var defaults = {
            server: 'http://a.pwal.fr',
            sites: [
["Ask", "Save to Ask", "http://myjeeves.ask.com/mysearch/BookmarkIt?v=1.2&amp;t=webpages&amp;url=$u&amp;title=$t", "ask.png", 0, 0],
["backflip", "Save to backflip", "http://www.backflip.com/add_page_pop.ihtml?url=$u&amp;title=$t", "backflip.png", 17, 0],
["blinklist", "Save to blinklist", "http://blinklist.com/index.php?Action=Blink/addblink.php&amp;Url=$u&amp;Title=$t", "blinklist.png", 34, 0],
["BlogBookmark", "Save to BlogBookmark", "http://www.blogbookmark.com/submit.php?url=$u", "blogbookmark.png", 51, 0],
["Bloglines", "Save to Bloglines", "http://www.bloglines.com/sub/$u", "bloglines.png", 68, 0],
["BlogMarks", "Save to BlogMarks", "http://blogmarks.net/my/new.php?mini=1&amp;simple=1&amp;url=$u&amp;title=$t", "blogmarks.png", 85, 0],
["Blogsvine", "Save to Blogsvine", "http://www.blogsvine.com/submit.php?url=$u", "blogsvine.png", 102, 0],
["BuddyMarks", "BuddyMark It", "http://www.buddymarks.com/add_bookmark.php?bookmark_title=$t&amp;bookmark_url=$u", "buddymarks.png", 119, 0],
["BUMPzee!", "Save to BUMPzee!", "http://www.bumpzee.com/bump.php?u=$u", "bumpzee.png", 136, 0],
["CiteULike", "Save to CiteULike", "http://www.citeulike.org/posturl?url=$u&amp;title=$t", "citeulike.png", 153, 0],
["co.mments", "Save to co.mments.com", "http://co.mments.com/track?url=$u&amp;title=$t", "comments.png", 170, 0],
["Connotea", "Save to Connotea", "http://www.connotea.org/addpopup?continue=confirm&amp;uri=$u&amp;title=$t", "connotea.png", 187, 0],
["del.icio.us", "Save to del.icio.us", "http://del.icio.us/post?url=$u&amp;title=$t", "delicious.png", 204, 0],
["Digg", "Digg It!", "http://digg.com/submit?phase=2&amp;url=$u&amp;title=$t", "digg.png", 221, 0],
["diigo", "Save to diigo", "http://www.diigo.com/post?url=$u&amp;title=$t", "diigo.png", 238, 0],
["DotNetKicks", "Save to DotNetKicks", "http://www.dotnetkicks.com/kick/?url=$u&amp;title=$t", "dotnetkicks.png", 255, 0],
["DropJack", "Save to DropJack", "http://www.dropjack.com/submit.php?url=$u", "dropjack.png", 272, 0],
["dzone", "Save to dzone", "http://www.dzone.com/links/add.html?description=$t&amp;url=$u&amp;title=$t", "dzone.png", 289, 0],
["Facebook", "Save to Facebook", "http://www.facebook.com/share.php?u=$u", "facebook.png", 306, 0],
["Fark", "FarkIt!", "http://cgi.fark.com/cgi/fark/farkit.pl?u=$u&amp;h=$t", "fark.png", 323, 0],
["Faves", "Save to Faves", "http://faves.com/Authoring.aspx?u=$u&amp;t=$t", "faves.png", 340, 0],
["Feed Me Links", "Save to Feed Me Links", "http://feedmelinks.com/categorize?from=toolbar&amp;op=submit&amp;name=$t&amp;url=$u", "feedmelinks.png", 357, 0],
["folkd.com", "Save to folkd.com", "http://www.folkd.com/submit/$u", "folkd.png", 374, 0],
["Furl", "Save to Furl", "http://www.furl.net/storeIt.jsp?u=$u&amp;t=$t", "furl.png", 408, 0],
["Google", "Save to Google Bookmarks", "http://www.google.com/bookmarks/mark?op=edit&amp;output=popup&amp;bkmk=$u&amp;title=$t", "google.png", 425, 0],
["Hugg", "Save to Hugg", "http://www.hugg.com/node/add/storylink?edit[title]=$t&amp;edit[url]=$u", "hugg.png", 442, 0],
["Jamespot", "Spot It!", "http://www.jamespot.com/?action=spotit&url=$u", "jamespot.png", 1122, 0],
["Jeqq", "Save to Jeqq", "http://www.jeqq.com/submit.php?url==$u&amp;title=$t", "jeqq.png", 459, 0],
["Kaboodle", "Save to Kaboodle", "http://www.kaboodle.com/za/selectpage?p_pop=false&amp;pa=url&amp;u=$u", "kaboodle.png", 476, 0],
["kirtsy", "Save to kirtsy", "http://www.kirtsy.com/submit.php?url=$u", "kirtsy.png", 493, 0],
["linkaGoGo", "Save to linkaGoGo", "http://www.linkagogo.com/go/AddNoPopup?url=$u&amp;title=$t", "linkagogo.png", 510, 0],
["LinkedIn", "Share on LinkedIn", "http://www.linkedin.com/shareArticle?mini=true&url=$u&title=$t", "linkedin.png", 1155, 0],
["LinksMarker", "Save to LinksMarker", "http://www.linksmarker.com/submit.php?url=$u&amp;title=$t", "linksmarker.png", 527, 0],
["Mister Wong", "Save to Mister Wong", "http://www.mister-wong.com/index.php?action=addurl&amp;bm_url=$u&amp;bm_description=$t", "misterwong.png", 561, 0],
["Mixx", "Save to Mixx", "http://www.mixx.com/submit?page_url=$u", "mixx.png", 578, 0],
["MySpace", "Save to MySpace", "http://www.myspace.com/Modules/PostTo/Pages/?c=$u&amp;t=$t", "myspace.png", 595, 0],
["MyWeb", "Save to My Web", "http://myweb.yahoo.com/myweb/save?t=$t&amp;u=$u", "myweb.png", 612, 0],
["Netvouz", "Save to Netvouz", "http://www.netvouz.com/action/submitBookmark?url=$u&amp;title=$t&amp;popup=no", "netvouz.png", 629, 0],
["Newsvine", "Seed Newsvine", "http://www.newsvine.com/_tools/seed?popoff=0&amp;u=$u", "newsvine.png", 646, 0],
["oneview", "Save to oneview", "http://www.oneview.com/quickadd/neu/addBookmark.jsf?URL=$u&amp;title=$t", "oneview.png", 1054, 0],
["OnlyWire", "Save to OnlyWire", "http://www.onlywire.com/submit?u=$u&amp;t=$t", "onlywire.png", 1071, 0],
["PlugIM", "Promote on PlugIM", "http://www.plugim.com/submit?url=$u&amp;title=$t", "plugim.png", 663, 0],
["Propeller", "Submit to Propeller", "http://www.propeller.com/submit/?U=$u&amp;T=$t", "propeller.png", 697, 0],
["Reddit", "Reddit", "http://reddit.com/submit?url=$u&amp;title=$t", "reddit.png", 714, 0],
["Rojo", "Save to Rojo", "http://www.rojo.com/add-subscription/?resource=$u", "rojo.png", 731, 0],
["Segnalo", "Save to Segnalo", "http://segnalo.com/post.html.php?url=$u&amp;title=$t", "segnalo.png", 748, 0],
["Shoutwire", "Shout It!", "http://www.shoutwire.com/?p=submit&amp;link=$u", "shoutwire.png", 765, 0],
["Simpy", "Save to Simpy", "http://www.simpy.com/simpy/LinkAdd.do?href=$u&amp;title=$t", "simpy.png", 782, 0],
["Slashdot", "Slashdot It!", "http://slashdot.org/bookmark.pl?url=$u&amp;title=$t", "slashdot.png", 799, 0],
["Sphere", "Sphere It", "http://www.sphere.com/search?q=sphereit:$u&amp;title=$t", "sphere.png", 816, 0],
["Spurl", "Save to Spurl", "http://www.spurl.net/spurl.php?url=$u&amp;title=$t", "spurl.png", 850, 0],
["Squidoo", "Save to Squidoo", "http://www.squidoo.com/lensmaster/bookmark?$u", "squidoo.png", 867, 0],
["StumbleUpon", "Stumble It!", "http://www.stumbleupon.com/submit?url=$u&amp;title=$t", "stumbleupon.png", 884, 0],
["Technorati", "Add to my Technorati Favorites", "http://technorati.com/faves?add=$u", "technorati.png", 901, 0],
["ThisNext", "Save to ThisNext", "http://www.thisnext.com/pick/new/submit/sociable/?url=$u&amp;name=$t", "thisnext.png", 918, 0],
["Twitter", "Save to Twitter", "http://twitter.com/home/?status=$t+$u", "twitter.png", 1105, 0],
["Webride", "Discuss on Webride", "http://webride.org/discuss/split.php?uri=$u&amp;title=$t", "webride.png", 935, 0],
["Windows Live", "Save to Windows Live", "https://favorites.live.com/quickadd.aspx?mkt=en-us&amp;url=$u&amp;title=$t", "windowslive.png", 952, 0],
["Worlds Movies", "Save to Worlds Movies", "http://www.worldsmovies.net/member/uservideo.php?url=$u", "worldsmovies.png", 1139, 0],
["Yahoo!", "Save to Yahoo! Bookmarks", "http://bookmarks.yahoo.com/toolbar/savebm?opener=tb&amp;u=$u&amp;t=$t", "yahoo.png", 969, 0]
]
            }

        if (options)
            $.extend(defaults, options);

        return this.each(function() {
            var self = $(this);
            self.hide();
            self.addClass('bookmarkInfo');
            self.attr('alt', defaults.server);
            var target = $('<div class="bookmarkify"></div>');
            target.append(self.clone());
            $(defaults.sites).each(function() {
                var link = $('' +
                    '<a href="#" alt="'+this[2]+'" title="'+this[0]+'" onclick="jQuery(this).redirectBookmark()">' +
                    '  <img alt="'+this[0]+'" src="'+defaults.server+'/_static/images/bookmarkify/'+this[3]+'" />' +
                    '</a>');
                target.append(link);
            });
            self.after(target);
            self.remove()
        });
    }
});

PopularBookmarks = [
["del.icio.us", "Save to del.icio.us", "http://del.icio.us/post?url=$u&amp;title=$t", "delicious.png", 204, 0],
["Digg", "Digg It!", "http://digg.com/submit?phase=2&amp;url=$u&amp;title=$t", "digg.png", 221, 0],
["Facebook", "Save to Facebook", "http://www.facebook.com/share.php?u=$u", "facebook.png", 306, 0],
["Google", "Save to Google Bookmarks", "http://www.google.com/bookmarks/mark?op=edit&amp;output=popup&amp;bkmk=$u&amp;title=$t", "google.png", 425, 0],
["LinkedIn", "Share on LinkedIn", "http://www.linkedin.com/shareArticle?mini=true&url=$u&title=$t", "linkedin.png", 1155, 0],
["MySpace", "Save to MySpace", "http://www.myspace.com/Modules/PostTo/Pages/?c=$u&amp;t=$t", "myspace.png", 595, 0],
["Reddit", "Reddit", "http://reddit.com/submit?url=$u&amp;title=$t", "reddit.png", 714, 0],
["Slashdot", "Slashdot It!", "http://slashdot.org/bookmark.pl?url=$u&amp;title=$t", "slashdot.png", 799, 0],
["Technorati", "Add to my Technorati Favorites", "http://technorati.com/faves?add=$u", "technorati.png", 901, 0],
["Twitter", "Save to Twitter", "http://twitter.com/home/?status=$t+$u", "twitter.png", 1105, 0],
["Windows Live", "Save to Windows Live", "https://favorites.live.com/quickadd.aspx?mkt=en-us&amp;url=$u&amp;title=$t", "windowslive.png", 952, 0],
["Yahoo!", "Save to Yahoo! Bookmarks", "http://bookmarks.yahoo.com/toolbar/savebm?opener=tb&amp;u=$u&amp;t=$t", "yahoo.png", 969, 0]
]
