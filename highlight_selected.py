#    Highlight Selected - Gedit plugin
#    Copyright (C) 2009 Steve Love
#    The basic structure of this plugin comes from Jonathan Walsh's multi-
#    edit plugin and Jesse van den Kieboom's plugin example. All I really did
#    was change the event handlers and remove the bits I didn't need.
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
		self._start  = None
		self._end	 = None
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
			self._mark_move = self._buffer.connect('mark-set', self._mark_moved)
			
	def _destroy_settings(self):
		# Disconnect event handlers
		self._buffer.disconnect(self._selection_change)
		self._buffer.disconnect(self._mark_move)
		
		# Destroy references to previous tab
		del self._tab
		del self._buffer
	
	def _selection_changed(self, *args):
		if(self._buffer.get_has_selection()):
			start, end = self._buffer.get_selection_bounds()
			if(start.starts_word() and end.ends_word()):
				self._highlight_selected(start, end)
		else:
			self._remove_highlight()
		
	def _mark_moved(self, textbuffer, textiter, mark):
		if (mark.get_name() == 'insert'):
			pos = self._buffer.get_iter_at_mark(mark)
			if(pos.ends_word()):
				self._end = pos
				if (self._start != None and self._start != self._end):
					self._highlight_selected(self._start, self._end)
				else:
					self._start = None
					self._end   = None
		elif (mark.get_name() == 'selection_bound'):
			pos = self._buffer.get_iter_at_mark(mark)
			if (pos.starts_word()):
				self._start = pos
			elif (pos.ends_word()):
				self._end = pos
		else:
			return False
	
	def _highlight_selected(self, start, end):
		if(self._buffer.get_has_selection()):
			selected_text = self._buffer.get_text(start, end)
			self._buffer.set_search_text(selected_text, 0)
		else:
			self._remove_highlight()
	
	def _remove_highlight(self):
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
