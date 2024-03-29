# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
%if c.new_url:
<form onsubmit="javascript: return false;" id="aupoil_result_form">
  <p>
    <label>Here is your new url for ${c.url}</label>
    <input type="text" name="result" id="result" size="50" value="${c.new_url}" />
  </p>
</form>
<p class="icons">
<a class="bookmarkify" style="display:none;" title="${c.title}" href="${c.url}"></a>
<div class="clear">&nbsp;</div>
</p>
%endif
<form method="get" action="" id="aupoil_form">
  <input type="hidden" id="title" name="p" value="${c.title}" />
  %if c.plugin:
    <input type="hidden" id="plugin" name="p" value="${c.plugin}" />
  %endif
  %if c.error:
    <p class="error">${c.error}</p>
  %endif
  <div>
    <label>Url</label>
    <input type="text" size="50" name="url" id="url" value="${not c.new_url and c.url or ''}" />
    <label>Alias</label>
    <input type="text" size="10" maxlength="25" id="alias" name="alias" />
    <p style="text-align:center" class="submit">
      <input class="button" type="submit" />
    </p>
  </div>
</form>
