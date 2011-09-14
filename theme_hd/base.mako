# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      body { font-family: helvetica;}
      #content, #header {
        width:400px;
        margin:auto;
      }
      #header { margin-bottom: 1em; text-align: center; }
      label {
        display: block;
        width:100px;
        font-weight: bold;
        margin-top: 0.7em;
      }
    </style>
  </head>
  <body>
    <div id="header">
      <img src="/_static/hd.png" />
    </div>
    <div id="content">
      ${self.body()}
    </div>
  </body>
</html>

