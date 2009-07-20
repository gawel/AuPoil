# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<h1>Stats for ${c.url.alias} - ${c.url.url}</h1>
<table>
<%
count = 0
%>
%for item in c.results:
<%
count += item[2]
%>
<tr><td>${item[1]}</td><td>${item[2]}</td></tr>
%endfor
<tr><td>Total</td><td>${count}</td></tr>
</table>
