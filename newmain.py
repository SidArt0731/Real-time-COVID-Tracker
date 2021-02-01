from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from  kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.bottomnavigation import MDBottomNavigation,MDBottomNavigationItem
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
import requests
from kivy.properties import ObjectProperty,NumericProperty,StringProperty
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout


kv= """
Screen:
	MDBoxLayout:
		orientation : "vertical"
		MDToolbar:
			md_bg_color : 1 , 0 , 0 , 1
			title : "Covid Tracker"
			pos_hint : {"top" : 1}
			elevation : 11
			left_action_items: [['information', lambda x: app.show_data(object)]]
			right_action_items: [['settings', lambda x: app.show_themepicker()]]
		
			
		MDBottomNavigation:		
						
			MDBottomNavigationItem:
				text : "Live"
				name : "screen1"
				icon : "bacteria"
				MDBoxLayout:
					spacing : "2dp"
					padding : "12dp"
					orientation : "vertical"
					
					LiveCases:
						search_input: searchinput
						MDTextField:
							id: searchinput
							pos_hint : {"top" : 1, "center_x": .5}
							hint_text:'Enter a valid Country'
							helper_text:'Name of country'
							helper_text_mode:'on_focus'
							multiline: False
							required : True
							
						MDFloatingActionButton:
							icon : "magnify"
							pos_hint : {"center_y" : 0.05 , "right" : .95}
							on_release:
								self.parent.search()
									
						Image:
							source:'bacteria.png'
							pos_hint:{'top':.65,'right':1}
							size_hint: .3,.1
								
						# location
						Label:
							text: str(self.parent.location)
							pos_hint:{'top':.75,'right':1}
							size_hint: 1,.1
							font_size: 55
							color:1,0,1,1
							
						# confirmed
						Label:
							text: "Confirmed:   " + str(self.parent.confirmed)
							pos_hint:{'top':.55,'right':1}
							size_hint: 1,.1
							font_size:35
							color:0,1,1,1
								
						# deaths
						Label:
							text: "Deaths:   " + str(self.parent.deaths)
							pos_hint:{'top':.45,'right':1}
							size_hint: 1,.1
							font_size:35
							color:1,0,0,1
							
						# recovered
						Label:
							text: "Recovered:   " + str(self.parent.recovered)
							pos_hint:{'top':.35,'right':1}
							size_hint: 1,.1
							font_size:35
							color:0,1,0,1
						
			MDBottomNavigationItem:
				text : "World"
				name : "screen2"
				icon : "earth"
				MDBoxLayout:
					spacing : "2dp"
					padding : "4dp"
					WorldCases:
						
						MDRaisedButton:
							pos_hint:{'top':1,'right':1}
							size_hint: 1,.1
							text:'Search for world cases'
							on_release:
								self.parent.search_world()
							
						Label:
							text:"Search for World Cases"
							pos_hint:{'top':8,'right':1}
							size_hint: 1,.1
							font_size:35
					
						#confirmed
						Label:
							text:'Confirmed:        ' + str(self.parent.confirmed)
							pos_hint:{'top':.55,'left':1}
							size_hint: 1,.1
							font_size:35
							color:0,1,1,1
							
						Label:
							text: str(self.parent.date)
							pos_hint:{'top':.65,'left':1}
							size_hint: 1,.1
							font_size:35
							
						#deaths
						Label:
							text:'Deaths:        ' + str(self.parent.deaths)
							pos_hint:{'top':.45,'left':1}
							size_hint: 1,.1
							font_size:35
							color:1,0,0,1
						
						#Recovered
						Label:
							text:'Recovered:        ' + str(self.parent.recovered)
							pos_hint:{'top':.35,'left':1}
							size_hint: 1,.1
							font_size:35
							color:0,1,0,1
						
	Image:
		source: "bacteria.png"
		opacity : .2

"""
class WorldCases(FloatLayout):
    confirmed = NumericProperty()
    deaths = NumericProperty()
    recovered = NumericProperty()
    date = StringProperty()

    def search_world(self):
    	try:
    		api_url = 'https://covid2019-api.herokuapp.com/total'
    		result = requests.get(url=api_url).json()
    		self.confirmed = result['confirmed']
    		self.deaths = result['deaths']
    		self.recovered = result['recovered']
    		self.date = result['dt']
    		
    	except:
    		Snackbar(text='No internet connection',font_size=20).show()

class LiveCases(FloatLayout):
    search_input = ObjectProperty()
    location = StringProperty()
    confirmed = NumericProperty()
    deaths = NumericProperty()
    recovered = NumericProperty()

    def search(self):
        try:
            api_url = 'https://covid2019-api.herokuapp.com/v2/country/{}'
            result = requests.get(url=api_url.format(self.search_input.text)).json()
            self.location = result['data']['location']
            self.confirmed = result['data']['confirmed']
            self.deaths = result['data']['deaths']
            self.recovered = result['data']['recovered']
        except:
            Snackbar(text='No such country or check internet connection',font_size=20).show()




class MainApp(MDApp):
	
	def __init__(self,**kwargs):
		self.theme_cls = ThemeManager()
		self.theme_cls.primary_palette = 'Blue'
		self.theme_cls.theme_style = 'Dark'
		super().__init__(**kwargs)
	
	def build(self):
		 
		return Builder.load_string(kv)
		
	def show_data(self , obj):
		
		about_us = "This app tracks covid rate.\nCreated by Siddharth Soni.\nContact: sidsoni0731@gmail.com"
		
		close_button = MDFlatButton(text = "close", on_release = self.close_dialog)
		self.dialog = MDDialog(title = "COVID Tracker", text = about_us, size_hint = (0.7 , 1), buttons = [close_button])
		
		self.dialog.open()
		
	def close_dialog(self , obj):
		self.dialog.dismiss()
		
	def show_themepicker(self):
		picker = MDThemePicker()
		picker.open()
		

MainApp().run()


		
