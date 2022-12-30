

import os

import sdl2.ext as sdl2ext
from sdl2 import (pixels, render, surface)
from sdl2.sdlttf import (TTF_OpenFont, 
						 TTF_RenderText_Shaded,
						 TTF_RenderText_Shaded_Wrapped,
						 TTF_RenderUTF8_Shaded,
						 TTF_RenderText_Blended_Wrapped,
						 TTF_GetError)


class TextSprite(sdl2ext.TextureSprite):
	def __init__(self, renderer, font = None, text = "", fontSize = 16, 
					   textColor = pixels.SDL_Color(255, 255, 255), 
					   backgroundColor = pixels.SDL_Color(0, 0, 0)):
		if isinstance(renderer, sdl2ext.Renderer):
			self.renderer = renderer.renderer
		elif isinstance(renderer, render.SDL_Renderer):
			self.renderer = renderer
		else:
			raise TypeError("unsupported renderer type")

		if font is None:
			font = os.path.join(os.environ["windir"],"Fonts","Arial.ttf")
		elif not os.path.isfile(font):
			if os.path.isfile(os.path.join(os.environ["windir"], "Fonts", font + ".ttf")):
				font = os.path.join(os.environ["windir"], "Fonts", font + ".ttf")
			else:
				raise IOError("Cannot find %s" % font)

		self.font = TTF_OpenFont(font.encode(), fontSize)
		if self.font is None:
			raise TTF_GetError()
		self._text = text
		self.fontSize = fontSize
		self.textColor = textColor
		self.backgroundColor = backgroundColor
		texture = self._createTexture()
		
		super().__init__(texture)
	
	def _createTexture(self):
		textSurface = TTF_RenderText_Blended_Wrapped(self.font, self._text.encode(), self.textColor, wrapLength=200)
		if textSurface is None:
			raise TTF_GetError()
		texture = render.SDL_CreateTextureFromSurface(self.renderer, textSurface)
		if texture is None:
			raise sdl2ext.SDLError()
		surface.SDL_FreeSurface(textSurface)
		return texture
	
	def _updateTexture(self):
		textureToDelete = self.texture
		x = self.x
		y = self.y		
		texture = self._createTexture()
		super().__init__(texture)
		self.x = x
		self.y = y

		render.SDL_DestroyTexture(textureToDelete)
	
	@property
	def text(self):
		return self._text
	
	@text.setter
	def text(self, value):
		if self._text == value:
			return
		self._text = value
		self._updateTexture()