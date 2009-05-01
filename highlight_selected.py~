#    Highlight Selected - Gedit plugin
#    Copyright (C) 2009 Steve Love
#    The basic structure of this plugin comes from Jonathan Walsh's multi-
#	 edit plugin and Jesse van den Kieboom's plugin example. All I really did
#	 was change the event handlers and remove the bits I didn't need.
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gedit

class WindowInstance:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin
		self._tab 	 = None
		# Tab change handler
		self._tab_event = self._window.connect('active-tab-changed', self._tab_change)
		# Load the currently active tab
		self._tab_change(self._window, self._window.get_active_tab())
		
	def deactivate(self):
		self._destroy_settings()		
		self._window.disconnect(self._tab_event)
		
	def _tab_change(self, window, tab):
		# Destroy previous tab references
		if self._tab is not None:
			self._destroy_settings()
			
		self._tab = tab
		if tab is not None:
			self._buffer = tab.get_document()
			
			# Event handlers
			self._selection_change = self._buffer.connect('notify::has-selection', self._selection_changed)
			
	def _destroy_settings(self):
		# Disconnect event handlers
		self._buffer.disconnect(self._selection_change)
		
		# Destroy references to previous tab
		del self._tab
		del self._buffer
		
	def _selection_changed(self, *args):
		if(self._buffer.get_has_selection()):
			start, end = self._buffer.get_selection_bounds()
			selected_text = self._buffer.get_text(start, end)
			self._buffer.set_search_text(selected_text, 0)
		else:
			self._buffer.set_search_text("",0)

class HighlightSelected(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self._windows = {}

	def activate(self, window):
		self._windows[window] = WindowInstance(self, window)

	def deactivate(self, window):
		self._windows[window].deactivate()
		del self._windows[window]

	def update_ui(self, window):
		pass
