# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
%if c.new_url:
<form onsubmit="javascript: return false;" id="aupoil_result_form">
  <p>
    <label>Here is your new url for ${c.url}</label>
    <input type="text" name="result" size="50" value="${c.new_url}" />
  </p>
</form>
<p></p>
%endif
<form method="GET" action="" id="aupoil_form">
  %if c.error:
    <p class="error">${c.error}</p>
  %endif
  <p>
    <label>Url</label>
    <input type="text" size="50" name="url" value="${not c.new_url and c.url or ''}" />
    <label>Alias</label>
    <input type="text" size="10" maxsize="25" name="alias" />
    <br />
    <input class="button" type="submit" />
  </p>
</form>
