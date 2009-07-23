<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
<script language="javascript" src="http://www.google.com/jsapi"></script>
<script language="javascript">
  google.load("jquery", "1");
</script>
<meta name="Description" content="A tiny url like." />
<meta name="Keywords" content="tinyurl like" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="Distribution" content="Global" />
<meta name="Author" content="Gael Pasgrimaud - gael@gawel.org" />
<meta name="Robots" content="index,follow" />		
<link href="/_static/images/favicon.ico" rel="shortcut icon"/>
<link rel="stylesheet" href="/_static/images/CitrusIsland.css" type="text/css" />
%if c.plugin:
<link rel="stylesheet" href="/_static/images/ff.css" type="text/css" />
%endif
<title>a.pwal.fr</title>
</head>
<body>
<div id="wrap"><!-- wrap starts here -->
	<div id="header">
		<h1 id="logo">a.<span>pwal</span>.fr</h1> 
    <h2 id="slogan">parce que m&ecirc;me les URLs sont plus jolies nues...</h2>
	</div>

	<div id="menu">
		<ul>
      <li>
        a.pwal.fr is a tinyurl like which allows you to make URLs shorter
			</li>			
		</ul>		
	</div>					
	
	<div id="sidebar" >	
      <div>&nbsp;</div>
	</div>
		
	<div id="main">
    ${self.body()}

    <h1 id="help">Lost ? Get some <a href="/help.html">help</a> !</h1>
	</div>	
	
	<div id="rightbar">
	</div>		
</div>
	
<div id="footer">
  <div id="footer-content">
  <div>
    &copy; Copyright 2009 <a href="http://www.gawel.org/">Gael Pasgrimaud</a> |
    Powered by: <a href="#">AuPoil</a> | 
    Hosted by: <a href="http://www.toonux.org">Toonux</a> |
    Design by: <a href="http://www.styleshout.com/">styleshout</a> |
    Valid <a href="http://validator.w3.org/check/referer">XHTML</a> |
    <a href="http://jigsaw.w3.org/css-validator/check/referer">CSS</a> <br/>
    Go <a href="/">Home</a> |
    Try our Firefox <a href="/firefox">extension</a>
  </div>
  </div>	
</div>

<script language="javascript" src="/_static/bookmarkify.js"></script>
<script language="javascript">
  google.setOnLoadCallback(function() {
    $('#result').focus().select()
    if ($('#plugin').length) {
      if ($('#result').length) {
        $('#aupoil_form').hide();
      } else if ($('#url').val()) {
        $('#alias').focus().select();
      }
    }
    $('.bookmarkify').showBookmarksLinks();
  });
</script>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-1563403-3");
pageTracker._trackPageview();
} catch(err) {}</script>
</body>
</html>
