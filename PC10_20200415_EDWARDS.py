#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:17:33 2020

@author: summeredwards
"""
#==============================

# PC10 - API IN THE SKY

# SUMMER EDWARDS

# 04/15/2020

#

# Code uses a weather API to display a summary of the weather forecast. Code will 
# show a text summary of what the forecast is for a specific time of day. It also shows how high 
# the temperature is, and whether it is currently daytime or nighttime. The bubbles on the right 
# hand side represent the temperature: the bigger the bubble, the higher the temperature; color also corresponds. 
# If the bubble is really light blue, then it is freezing temperatures. The warmer and darker the color, 
# the warmer it is outside. If it is currently dayttime outside, the code will illustrate a sun at the bottom
# of the screen. If it is nighttime, it will show a moon at the bottom of the screen. 

#==============================


#import modules 
import pygame
import json 
import requests

pygame.init()

#set globals 
screen = pygame.display.set_mode((1400,600)) 
screen.fill((0,0,0))

#import data
URL = 'https://api.weather.gov/gridpoints/BOU/53,74/forecast'

#create class
class getWeather:
  def __init__(self,screen,location=[50,100],locationCirc=[1325,100],color=(0,0,0)): 
    #set main attributes
    self.data=[] 
    self.numCirc=6 #number of circles to draw
    self.radius= self.tempData() #store the temp data to self.radius
    self.Time= self.timeData()
    self.location= location
    self.locationCirc= locationCirc
    self.color= color
    self.screen= screen

  def tempData(self, URL=URL):
    '''Pulls temperature data from URL (API)'''
    #pull data from URL
    self.data = requests.get(URL).json() 
    
    temp=[]
    for i in range(self.numCirc):
      temp.append(self.data['properties']['periods'][i]['temperature']) 
      
    #return the temp list to be stored as self.radius
    return temp
  #function modified from Dr. Z's function she made in class ^^
  
  def timeData(self, URL=URL):
      '''Pulls time-of-day data from the URL (API)'''
      #pull data from URL
      self.data = requests.get(URL).json() 
        
      Daytime=[]
      for i in range(self.numCirc):
          Daytime.append(self.data['properties']['periods'][i]['isDaytime']) 
          
      #return the Daytime list to be stored as self.Time
      return Daytime

  def textData(self,idx,loc,xoffset=0, yoffset=0, fontsize = 30,fontcolor=(255,255,255),background=(0,0,0)):
      '''Adds text to describe data. Gets called when circles are drawn.'''

      font = font = pygame.font.Font('freesansbold.ttf', fontsize) 
      
      label=self.data['properties']['periods'][idx]['shortForecast'] 
      label2 = self.data['properties']['periods'][idx]['name']
      #Add text from: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
      text = font.render(label2+': '+label, True, fontcolor) 

      #create a text surface object 
      textRect = text.get_rect()  
      
      #set the center of the text surface object 
      textRect.center = (loc[0]+xoffset // 2, loc[1]+yoffset // 2)  
      screen.blit(text, textRect) 
  #function modified from Dr. Z's function she made in class ^^
  
  def drawCirc(self,text=True):
    '''Draws circles with radii based on temperature data.'''
    circList = []
    for i in range(self.numCirc):
        loc = (self.location[0], int(self.location[1] + i*60))
        loc2 = (self.locationCirc[0], int(self.locationCirc[1] + i*60))
        
        if self.radius[i] <= 32:
            self.color = (232,247,255) #really light blue for freezing temps
        if 33 <= self.radius[i] <= 45:
            self.color = (128,168,255) #light-ish blue for cold temps
        if 46 <= self.radius[i] <= 65:
            self.color = (229,158,255) #light-ish purple for mild temps
        if 66 <= self.radius[i] <= 75:
            self.color = (250,135,189) #light pink for warm temps
        if 76 <= self.radius[i] <= 85:
            self.color = (255,89,128) #dark pink for warmer temps
        if self.radius[i] >= 86:
            self.color = (255,84,84) #bright red for hot temps 
        
        #draw circles
        circList.append(pygame.draw.circle(self.screen,self.color,loc2,int(self.radius[i]/2)))
        
        #add labels
        if text:
          self.textData(i,loc,xoffset=1150,yoffset=0) 
  #used Dr. Z's function as guidance to create this one ^^ 
  
  def drawSky(self):
      '''Draws a sun when it is currently daytime, and draws a moon when it is currently nighttime.'''
      #draw sun
      if self.Time[0] == True:
          pygame.draw.circle(self.screen,(250,240,175),(625,500),50)
          pygame.draw.circle(self.screen,(242,187,104),(625,500),52,4)
      #draw moon     
      if self.Time[0] == False:
          pygame.draw.circle(self.screen,(255,255,255),(625,500),50)
          pygame.draw.circle(self.screen,(201,201,201),(625,500),52,3)
             
          pygame.draw.circle(self.screen,(201,201,201),(650,525),13)
          pygame.draw.circle(self.screen,(148,148,148),(650,525),15,1)
             
          pygame.draw.circle(self.screen,(201,201,201),(590,485),8)
          pygame.draw.circle(self.screen,(148,148,148),(590,485),10,1)
             
          pygame.draw.circle(self.screen,(201,201,201),(640,465),10)
          pygame.draw.circle(self.screen,(148,148,148),(640,465),12,1)
             
          pygame.draw.circle(self.screen,(201,201,201),(625,500),4)
          pygame.draw.circle(self.screen,(148,148,148),(625,500),6,1)
             
          pygame.draw.circle(self.screen,(201,201,201),(605,535),4)
          pygame.draw.circle(self.screen,(148,148,148),(605,535),6,1)
             
          pygame.draw.circle(self.screen,(148,148,148),(615,485),3)
          pygame.draw.circle(self.screen,(148,148,148),(590,515),3)
          pygame.draw.circle(self.screen,(148,148,148),(655,495),3)

#create object
weather = getWeather(screen) 

#create game loop
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
   
    screen.fill((56,56,56))
    weather.drawCirc()
    weather.drawSky()
    
    pygame.display.update()
    
pygame.quit()
    
# got RGB colors from https://www.google.com/search?q=color+picker

