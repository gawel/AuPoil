/* ***** BEGIN LICENSE BLOCK *****
 *   Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 * 
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is a.pwal.fr.
 *
 * The Initial Developer of the Original Code is
 * Gael Pasgrimaud.
 * Portions created by the Initial Developer are Copyright (C) 2009
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 * 
 * ***** END LICENSE BLOCK ***** */

var apwalfr = {
  onLoad: function() {
    // initialization code
    this.initialized = true;
  },

  onMenuItemCommand: function(e) {
    var doc = window.content.document;
    var url = doc.location;
    var src = 'http://localhost:5000';

    jQuery('#apwalfr', doc).remove();
    jQuery('#apwalfr_close', doc).remove();

    var close = "document.getElementById('apwalfr').style.display='none'; this.style.display='none'"
    jQuery('body', doc).prepend('' +
        '<div id="apwalfr_close" onclick="'+close+'" ' +
             'style=z-index:1000001;float:left;top:55px;left:435px;position:fixed;display:block;">' +
          '<img style="width:20px;height:20px" src="'+src+'/_static/images/close.png" />' +
        '</div>' +
        '<iframe src="'+src+'/?p=firefox&post='+url+'" id="apwalfr"' +
                'style="z-index:1000000;float:left;top:50px;left:30px;position:fixed;border:thin solid black; width:430px; height:230px;"' +
               ' />' +
        '</iframe>'+
        '');
  }

};
window.addEventListener("load", function(e) { apwalfr.onLoad(e); }, false);