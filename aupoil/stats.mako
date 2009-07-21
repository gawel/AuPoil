# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<h1>Stats for ${c.url.alias} - <a href="${c.url.url}">${c.url.url}</a></h1>
<table>
<%
count = 0
%>
%for item in c.results:
<%
count += item[2]
%>
%if '//' in item[1]:
<tr><td><a href="${item[1]}">${item[1]}</a></td><td>${item[2]}</td></tr>
%else:
<tr><td>${item[1]}</td><td>${item[2]}</td></tr>
%endif
%endfor
<tr><td>Total</td><td>${count}</td></tr>
</table>
