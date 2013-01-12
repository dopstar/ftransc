#!/usr/bin/python

import os
import sys
from subprocess import Popen, PIPE

from gi.repository import Gtk

from ftransc.utils import m3u_extract
from ftransc.utils.constants import VERSION

class Window(Gtk.Window):
    def __init__(self, cmdlinefiles=None):
        super(Window, self).__init__(title='ftransc Audio Converter v%s' % VERSION)
        self.files = cmdlinefiles or []

        self.main_pane = Gtk.Box()
        self.main_pane.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.add(self.main_pane)

        self._make_left_pane()
        self._make_right_pane()
        self.main_pane.pack_start(self.left_pane, False, False, 0)
        self.main_pane.pack_start(self.right_pane, True, True, 0)
        self.connect('destroy', Gtk.main_quit)
        self.show_all()

    def _make_left_pane(self):
        self.left_pane = Gtk.Box(False, 8)
        self.left_pane.set_orientation(Gtk.Orientation.VERTICAL)

        self.add_files_button = Gtk.Button(label='Add Files')
        self.add_files_button.connect('clicked', self.add_files)

        self.add_folder_button = Gtk.Button('Add Folder')
        self.add_folder_button.set_tooltip_text('Add folders with audio/video files on them')
        
        self.output_folder_button = Gtk.Button(label='Output Folder')
        self.output_folder_button.connect('clicked', self.add_files)

        self.output_folder_entry = Gtk.Entry()
        self.output_folder_entry.set_editable(False)

        self.browse_section = Gtk.Table(2, 2, False)
        self.browse_section.attach(self.add_files_button, 0, 1, 0, 1)
        self.browse_section.attach(self.add_folder_button, 1, 2, 0, 1)
        self.browse_section.attach(self.output_folder_button, 0, 1, 1, 2)
        self.browse_section.attach(self.output_folder_entry, 1, 2, 1, 2)

        self.presets_section = Gtk.Table(2, 2, True)
        self.format_label = Gtk.Label('Format')
        self.quality_label = Gtk.Label('Quality')

        self.left_pane.pack_start(self.browse_section, True, True, 0)

    def _make_right_pane(self):
        self.right_pane = Gtk.Box()
        self.right_pane.set_orientation(Gtk.Orientation.VERTICAL)

        self._create_media_store()
        self._create_tree_view()

    
    def _create_media_store(self):
        self.media_store = Gtk.ListStore(bool, str, str, int)
        self.media_store.clear()

        for count, songname in enumerate(self.files):
            songsize = (os.path.getsize(songname)/1024.0)/1024.0
            if songsize < 1:
                songsize = '%.2fKB' % songsize
            elif songsize < 1024:
                songsize = '%.2fMB' % songsize
            else:
                songsize = '%.2fGB' % songsize

            if count == 0:
                self.current_iter = self.media_store.append([True, songname, songsize, 0])
            else:
                self.media_store.append([True, songname, songsize, 0])

    def _create_tree_view(self):
        treeview = Gtk.TreeView(model=self.media_store)
        treeview.set_rules_hint(True)

        renderer_text = Gtk.CellRendererText()
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect('toggled', self.add_files)
        renderer_progress = Gtk.CellRendererProgress()

        enable_column = Gtk.TreeViewColumn('Enable', renderer_toggle, active=0)
        filename_column = Gtk.TreeViewColumn('Filename', renderer_text, text=1)
        filesize_column = Gtk.TreeViewColumn('Size', renderer_text, text=2)
        status_column = Gtk.TreeViewColumn('Status', renderer_progress, value=3)

        treeview.append_column(enable_column)
        treeview.append_column(filename_column)
        treeview.append_column(filesize_column)
        treeview.append_column(status_column)
        self.right_pane.pack_start(treeview, True, True, 1)


    def main(self):
        Gtk.main()

    def add_files(self):
        pass

    def browse(self):
        pass

    def convert(self):
        pass

    def createFilesTable(self):
        pass

    def createButton(self):
        pass

    def delete_items(self):
        pass

if __name__ == '__main__':
    app = Window(cmdlinefiles=m3u_extract(sys.argv[1:], mode='playlist'))
    app.main()

