# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
%if c.url:
${c.url}
%else:
<form method="POST" action="">
  <p>
    <label>Url</label>
    <input type="text" size="50" name="url" />
    <label>Alias</label>
    <input type="text" size="10" maxsize="25" name="alias" />
    <br />
    <input class="button" type="submit" />
  </p>
</form>
%endif
