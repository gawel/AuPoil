# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
%if c.new_url:
<form>
  <p>
    <label>Here is your new url</label>
    <input type="text" size="50" name="url" value="${c.new_url}" />
  </p>
</form>
%else:
<form method="GET" action="">
  %if c.error:
    <p class="error">${c.error}</p>
  %endif
  <p>
    <label>Url</label>
    <input type="text" size="50" name="url" value="${c.url}" />
    <label>Alias</label>
    <input type="text" size="10" maxsize="25" name="alias" />
    <br />
    <input class="button" type="submit" />
  </p>
</form>
%endif
