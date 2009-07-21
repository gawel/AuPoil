# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<h1>Stats for ${c.alias} - <a href="${c.url}">${c.url}</a></h1>
<table>
<tr><th>Referer</th><th>Hits</th></tr>
<%
count = 0
%>
%for item in c.stats:
<%
referer = item.get('referer')
%>
%if '//' in referer:
<tr><td><a href="${referer}">${referer}</a></td><td>${item.get('count')}</td></tr>
%else:
<tr><td>${referer}</td><td>${item.get('count')}</td></tr>
%endif
%endfor
<tr><td>Total</td><td>${c.count}</td></tr>
</table>
