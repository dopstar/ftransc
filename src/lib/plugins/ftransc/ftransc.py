# __init__.py
#
# Copyright (C) 2012 - Mkhanyisi Madlavana
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# The Rhythmbox authors hereby grant permission for non-GPL compatible
# GStreamer plugins to be used and distributed together with GStreamer
# and Rhythmbox. This permission is above and beyond the permissions granted
# by the GPL license by which Rhythmbox is covered. If you modify this code
# you may extend this exception to your version of the code, but you are not
# obligated to do so. If you do not wish to do so, delete this exception
# statement from your version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import rb
from gi.repository import Gio, GObject, GLib, Peas
from gi.repository import RB

import shlex
import gettext
gettext.install('rhythmbox', RB.locale_dir())

ui_definition = """
<ui>
    <popup name="BrowserSourceViewPopup">
        <menuitem name="ConvertFilesLibraryPopup" action="ConvertFiles" />
    </popup>

    <popup name="PlaylistViewPopup">
        <menuitem name="ConvertFilesPlaylistPopup" action="ConvertFiles" />
    </popup>

    <popup name="QueuePlaylistViewPopup">
        <menuitem name="ConvertFilesQueuePlaylistPopup" action="ConvertFiles" />
    </popup>
</ui>"""

class ConvertFilesPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'ConvertFilesPlugin'

    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(ConvertFilesPlugin, self).__init__()

    def do_activate(self):
        self.__action = Gio.SimpleAction(name='ConvertFiles')
        self.__action.connect('activate', self.convert_files)
        
        app = Gio.Application.get_default()
        app.add_action(self.__action)
        
        item = Gio.MenuItem()
        item.set_label(_("Convert Songs (ftransc)"))
        item.set_detailed_action('app.ConvertFiles')
        app.add_plugin_menu_item('edit', 'ConvertFiles', item)
        app.add_plugin_menu_item('browser-popup', 'ConvertFiles', item)
        app.add_plugin_menu_item('playlist-popup', 'ConvertFiles', item)
        app.add_plugin_menu_item('queue-popup', 'ConvertFiles', item)

    def do_deactivate(self):
        shell = self.object
        app = Gio.Application.get_default()
        app.remove_action('ConvertFiles')
        app.remove_plugin_menu_item('edit', 'ConvertFiles')
        app.remove_plugin_menu_item('browser-popup', 'ConvertFiles')
        app.remove_plugin_menu_item('playlist-popup', 'ConvertFiles')
        app.remove_plugin_menu_item('queue-popup', 'ConvertFiles')
        del self.__action

    def convert_files(self, action, data):
        shell = self.object
        page = shell.props.selected_page
        if not hasattr(page, "get_entry_view"):
            return
        entries = page.get_entry_view().get_selected_entries()
        cmdline = 'ftransc_qt ' + " ".join(shlex.quote(entry.get_playback_uri()) for entry in entries)
        GLib.spawn_command_line_async(cmdline)
