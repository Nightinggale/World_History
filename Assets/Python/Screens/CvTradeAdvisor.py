## Sid Meier's Civilization 4
## Copyright Firaxis Games 2008
## Modified By Kailric
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
# Modified by Solver for Col v1

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


# this class is shared by both the resource and technology foreign advisors

class CvTradeAdvisor:
	"Trade Advisor Screen"

	def __init__(self):
		self.WIDGET_ID = "TechnologyAdvisorWidget"
		self.LINE_ID = "TechnologyAdvisorLine"
		self.SCREEN_NAME = "TechnologyAdvisor"
		self.DEBUG_DROPDOWN_ID =  "TechnologyAdvisorDropdownWidget"
		self.BACKGROUND_ID = "TechnologyAdvisorBackground"

		self.XResolution = 0
		self.YResolution = 0
		self.TopPanelHeight = 55
		self.nWidgetTestCount = 0
		self.nWidgetCount = 0
		
	def interfaceScreen (self, iCategory):

		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		screen = self.getScreen()
		if screen.isActive():
			return
	
		
		

		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		# Set the background and exit button, and show the screen
		if gc.getDefineINT("TK_RESEARCH_SCREEN_XY") > 0:
			self.XResolution = 1024
			self.YResolution = 768
			screen.showWindowBackground( False )
			screen.setDimensions(screen.centerX(0), screen.centerY(0), 1024, 768)
		else:
			self.XResolution = self.getScreen().getXResolution()
			self.YResolution = self.getScreen().getYResolution()
			screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_SCREEN_BG").getPath(), 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("BottomPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), 0, self.YResolution - 55, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.showWindowBackground(False)
		
		self.SCREEN_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_TRADE_ADVISOR_TITLE", ()).upper() + u"</font>"
		self.SCREEN_TITLE = localText.changeTextColor(self.SCREEN_TITLE, gc.getInfoTypeForString("COLOR_FONT_CREAM"))


		self.Y_REVOLUTION = self.YResolution / 13
		self.W_REVOLUTION = self.XResolution * 2 / 5
		
		self.Y_REBEL_BAR = self.YResolution / 6
		
		self.Y_UNITS_LISTS = self.YResolution * 33 / 100
		self.X_ROYAL_UNITS = self.XResolution * 58 / 100
		self.X_COLONIAL_UNITS = self.XResolution  * 3 / 20
		
		self.BAR_SIDE_MARGIN = self.YResolution / 15
		self.BAR_END_ICON_SIZE = self.YResolution / 13
		
		#local_button_mod = gc.getNumCivicInfos()
		#if ((gc.getNumCivicInfos() - 5) > 75):
		#	local_button_mod = 75
		#			
		
		#Controls Tech Size in General
		self.ICON_BUTTON_SIZE = self.YResolution / 34
		
		
		
		
		
		self.TECH_BACKGROUND_X = self.ICON_BUTTON_SIZE * 10
		self.TECH_BACKGROUND_Y = self.ICON_BUTTON_SIZE * 3
		self.MAGNIFYING_GLASS_X = self.ICON_BUTTON_SIZE * 8
		self.MAGNIFYING_GLASS_Y = self.ICON_BUTTON_SIZE * 6
		self.MagnefyS_X = self.ICON_BUTTON_SIZE * 4
		self.MagnefyS_Y = self.ICON_BUTTON_SIZE * 4
		self.Y_EXIT = self.YResolution - 42
		self.REVOLUTION_BUTTON = 1776
		self.AMENDMENT_BUTTON = 1778
		self.CURRENT_RESEARCH = 0
		self.TEMP_RESEARCH = -1
		self.CATEGORY = 69
		self.NumCATEGORY = 4
		self.MAGNIFYING_GLASS = self.XResolution / 2
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.PLAYER_RESEARCH = player.getCurrentTradeResearch()
		
		
		self.YCATEGORY = self.YResolution * 5 / 100
		self.YMAGNIFYING_GLASS = int(self.YResolution / 2.1)
		self.BUTTON_SPACE = int((self.YResolution / 18) * 1.9)
		self.ResearchButtonDiffer = int((self.YResolution / 18) / 1.2)
		
		self.XUnknownCATEGORY = self.ICON_BUTTON_SIZE
		
		self.XCATEGORY = self.XResolution * 90 / 100
		
		self.PIXEL_INCREMENT = 8
		self.BOX_INCREMENT_WIDTH = 24 # Used to be 33 #Should be a multiple of 3...
		self.BOX_INCREMENT_HEIGHT = 9 #Should be a multiple of 3...
		self.BOX_INCREMENT_Y_SPACING = 6 #Should be a multiple of 3...
		self.BOX_INCREMENT_X_SPACING = 9 #Should be a multiple of 3...
		self.TEXTURE_SIZE = 24
		#X_START = 6
		self.X_INCREMENT = 27
		self.Y_MOD = 100
		#Y_ROW = 32
		
		ScrollPanel = "ScrollPanel"
		screen.addScrollPanel(ScrollPanel, u"", 0, 30, self.XResolution,  self.YResolution - 110, PanelStyles.PANEL_STYLE_EXTERNAL, true, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setActivation(ScrollPanel, ActivationTypes.ACTIVATE_NORMAL)
		screen.setText( "Title", ScrollPanel, self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText( "RevolutionScreenExit", ScrollPanel, u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.XResolution - 30, self.YResolution - 36, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( "RevolutionScreenExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
		
		
		# Draw Contents
		self.drawIdeasExperience()
		if gc.getDefineINT("TK_RESEARCH_SCREEN_XY") > 0:
			self.drawArrows()
			self.drawCivicsXY()
			
		else:
			self.drawCivics()
		
		return 0

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRADE_ADVISOR)
		
	def drawIdeasExperience(self):
		self.pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		screen = self.getScreen()
		szWidget = "ProlificInvetorBar"
		screen.addStackedBarGFC(szWidget, self.XResolution / 2 - ((self.XResolution / 4) / 2), self.YResolution - 36, self.XResolution / 4, 30, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
		screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
		screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
		screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
		activeTeam = gc.getTeam(self.pActivePlayer.getTeam())
		iCurrentTradePoints = activeTeam.getFatherPoints(5)
		iTradeResearch = self.pActivePlayer.getCurrentTradeResearch()
		iTradePointCost = gc.getCivicInfo(iTradeResearch).getRequiredFatherPoints(5)
		iTradePointCost = (iTradePointCost * gc.getDefineINT("TRADING_POINTS_MOD_PERCENT")) / 100
		screen.setBarPercentage(szWidget, InfoBarTypes.INFOBAR_STORED, float(iCurrentTradePoints) / float(iTradePointCost))
		screen.setLabel(szWidget + "label", "", u"<font=3>" + localText.getText("TXT_KEY_TRADE_POINTS_XP", (iCurrentTradePoints, iTradePointCost)) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY,  self.XResolution / 2, self.YResolution - 32, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					
																									
	

	def drawCivicsXY(self):
		
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		activeTeam = gc.getTeam(player.getTeam())
		BonusRow = 0
		LineReturn = 0
		ScrollPanel = "ScrollPanel"
		iCurrentTradePoints = activeTeam.getFatherPoints(5)
		iTradeResearch = player.getCurrentTradeResearch()
		iTurns = iCurrentTradePoints
		slash = "/"
		#Current Research Code
		if iTradeResearch != -1:
			if iTradeResearch != self.CURRENT_RESEARCH:
				self.CURRENT_RESEARCH = iTradeResearch
			
		if self.TEMP_RESEARCH != -1 and self.TEMP_RESEARCH != iTradeResearch:
			iValue = 0
			if iTradeResearch != -1:
				iValue = self.ResearchButtonDiffer
		
			
		#unLearned Techs
		
		bTest = False
		DisAllowedTech = []
		for iCivic in range(gc.getNumCivicInfos()):
			DisAllowedTech.append(iCivic)
			DisAllowedTech[iCivic] = False
		for iCivic in range(gc.getNumCivicInfos()):
			if (player.getIdeasResearched(iCivic) > 0):
				if (gc.getCivicInfo(iCivic).getDisallowsTech() != -1):
					Disallow = gc.getCivicInfo(iCivic).getDisallowsTech()
					DisAllowedTech[Disallow] = True
		for iCivic in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(iCivic).getCivicOptionType() == 0):
				if gc.getCivicInfo(iCivic).getInventionCategory() == -1 and iCivic == 2:
					

					
					for iListCivic in range(gc.getNumCivicInfos()):
						if (gc.getCivicInfo(iListCivic).getCivicOptionType() == 0):
							
							iCategory = gc.getCivicInfo(iListCivic).getInventionCategory()
							
							if iCategory == iCivic:
								if (bTest == False):
									
									#localy = gc.getCivicInfo(iListCivic).getY_Location()
									#localx = gc.getCivicInfo(iListCivic).getX_Location()
									
																	
									localx = 30 + ( (gc.getCivicInfo(iListCivic).getX_Location() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
									localy = ( gc.getCivicInfo(iListCivic).getY_Location() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + self.Y_MOD
									iconModSize = (self.ICON_BUTTON_SIZE * 5) / 3
									iDisplayClickTxt = 1
									szFatherTitle = gc.getCivicInfo(iListCivic).getDescription()
									ArtTechHolder = ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLDS_TECH").getPath()
									TextColor = gc.getInfoTypeForString("COLOR_FONT_GOLD")
									if (not player.canDoCivics(iListCivic)):
										TextColor = gc.getInfoTypeForString("COLOR_FONT_CREAM")
										ArtTechHolder = ArtFileMgr.getInterfaceArtInfo("INTERFACE_CATALOG_TECH").getPath()
									Magnefy_X = localx + self.MagnefyS_X 
									Magnefy_Y = localy - self.MagnefyS_Y
									iTradePointCost = gc.getCivicInfo(iListCivic).getRequiredFatherPoints(5)
									iTradePointCost = (iTradePointCost * gc.getDefineINT("TRADING_POINTS_MOD_PERCENT")) / 100
									if (self.TEMP_RESEARCH == iListCivic):
										TurnstoComplete = ""
										#iTurns = player.getCurrentResearchProgress(True, -1)
										#if (iTurns > 0):
										TurnstoComplete = " (" + str(iTurns) + slash + str(iTradePointCost) +")"
										szFatherTitle = localText.changeTextColor(szFatherTitle + TurnstoComplete, gc.getInfoTypeForString("COLOR_FONT_GOLD"))
										iDisplayClickTxt = 0
										screen.setImageButtonAt("MagnifyingTrade", ScrollPanel, ArtFileMgr.getInterfaceArtInfo("MAGNIFYING_QUILL").getPath(), self.Magnefy_X, self.Magnefy_Y, self.MAGNIFYING_GLASS_X, self.MAGNIFYING_GLASS_Y, WidgetTypes.WIDGET_GENERAL, iListCivic, 0)
										screen.moveToFront("MagnifyingTrade")
										if player.getResearchPartner() != -1:
											szButton = gc.getLeaderHeadInfo(gc.getPlayer(player.getResearchPartner()).getLeaderType()).getButton()
											screen.addDDSGFC("Partner", szButton, self.XResolution / 3, self.YResolution - 36, self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, 2, player.getResearchPartner())	
										return 0
									elif (player.getIdeasResearched(iListCivic) > 0):
										szFatherTitle = localText.changeTextColor(szFatherTitle, gc.getInfoTypeForString("COLOR_PLAYER_DARK_GREEN_TEXT"))
										szCatText = localText.getText("TXT_KEY_TK_CATALOGED", ())
										szCatText = localText.changeTextColor(szCatText, gc.getInfoTypeForString("COLOR_PLAYER_DARK_YELLOW_TEXT"))
										screen.setImageButtonAt("HoldsTech" + str(iListCivic), ScrollPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_CATALOG_TECH").getPath(), localx, localy - ((self.YCATEGORY * 14) / 100), self.TECH_BACKGROUND_X, self.TECH_BACKGROUND_Y, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON, iListCivic)
										screen.setTextAt("Cataloged" + str(iListCivic), ScrollPanel, "<font=3>" + szCatText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, localx + self.ICON_BUTTON_SIZE, localy +  int(self.ICON_BUTTON_SIZE * 2), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										
									elif (iTradeResearch == iListCivic):
										TurnstoComplete = ""
										#iTurns = player.getCurrentResearchProgress(True, -1)
										#if iTurns > 0:
										TurnstoComplete = " (" + str(iTurns) + slash + str(iTradePointCost) +")"
										szFatherTitle = localText.changeTextColor(szFatherTitle + TurnstoComplete, gc.getInfoTypeForString("COLOR_FONT_GOLD"))
										iDisplayClickTxt = 0
										screen.setImageButtonAt("HoldsTech" + str(iListCivic), ScrollPanel, ArtTechHolder, localx, localy - ((self.YCATEGORY * 14) / 100), self.TECH_BACKGROUND_X, self.TECH_BACKGROUND_Y, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON, iListCivic)
										screen.setImageButtonAt("MagnifyingTrade", ScrollPanel, ArtFileMgr.getInterfaceArtInfo("MAGNIFYING_QUILL").getPath(), Magnefy_X, Magnefy_Y, self.MAGNIFYING_GLASS_X, self.MAGNIFYING_GLASS_Y, WidgetTypes.WIDGET_GENERAL, iListCivic, 0)
										
									else:
										TurnstoComplete = ""
										if (player.canDoCivics(iListCivic)):
											#iTurns = player.getCurrentResearchProgress(True, iListCivic)
											if iTurns > 0:
												TurnstoComplete = " (" + str(iTurns) + slash + str(iTradePointCost) +")"
										szFatherTitle = localText.changeTextColor(szFatherTitle + TurnstoComplete, TextColor)
										screen.setImageButtonAt("HoldsTech" + str(iListCivic), ScrollPanel, ArtTechHolder, localx, localy - ((self.YCATEGORY * 14) / 100), self.TECH_BACKGROUND_X, self.TECH_BACKGROUND_Y, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iListCivic, 0)
									
									#!!!!!Requirements!!!!
									
									#if gc.getCivicInfo(iListCivic).getRequiredInvention2() != -1:
									#	screen.setImageButtonAt("RequiredInv2" + str(iListCivic), ScrollPanel, gc.getCivicInfo(gc.getCivicInfo(iListCivic).getRequiredInvention2()).getButton(), int(localx + self.ICON_BUTTON_SIZE * 6.3) + iNoNeedsUnit, localy + self.ICON_BUTTON_SIZE + (iconModSize / 2), iconModSize / 2, iconModSize / 2, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON + 2, gc.getCivicInfo(iListCivic).getRequiredInvention2())	
									#if gc.getCivicInfo(iListCivic).getRequiredInventionOr() != -1:
									#	screen.setImageButtonAt("RequiredInvOr" + str(iListCivic), ScrollPanel, gc.getCivicInfo(gc.getCivicInfo(iListCivic).getRequiredInventionOr()).getButton(), int(localx + self.ICON_BUTTON_SIZE * 4.7) + iNoNeedsUnit, localy + self.ICON_BUTTON_SIZE + (iconModSize / 2), iconModSize / 2, iconModSize / 2, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON + 2, gc.getCivicInfo(iListCivic).getRequiredInventionOr())
									#	szOrText = localText.getText("TXT_KEY_TK_OR", ())
									#	szOrText = localText.changeTextColor(szOrText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
									#	screen.setTextAt("OrText" + str(iListCivic), ScrollPanel, "<font=2>" + szOrText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, int(localx + self.ICON_BUTTON_SIZE * 5.5) + iNoNeedsUnit, localy + int(iconModSize * 1.4), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
									
									iNoNeedsUnit = iconModSize / 2
									screen.addDDSGFCAt("TechBox" + str(iListCivic), ScrollPanel, gc.getCivicInfo(iListCivic).getButton(), localx + self.ICON_BUTTON_SIZE, localy + int(self.ICON_BUTTON_SIZE / 3), self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE,  WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY, iListCivic, 0, false)
									if (DisAllowedTech[iListCivic] == True):
										screen.addDDSGFCAt("Disallow" + str(iListCivic), ScrollPanel, ArtFileMgr.getInterfaceArtInfo("DISALLOW_TECH").getPath(), localx + self.ICON_BUTTON_SIZE, localy + int(self.ICON_BUTTON_SIZE / 3), self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE,  WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY, iListCivic, 0, false)
									#screen.addDDSGFCAt("CategoryBox" + str(iListCivic), ScrollPanel, gc.getCivicInfo(iCivic).getButton(), localx + self.ICON_BUTTON_SIZE, localy +  int(self.ICON_BUTTON_SIZE * 1.5), self.ICON_BUTTON_SIZE - 5, self.ICON_BUTTON_SIZE - 5, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON, iCivic, false)
									screen.setTextAt("Title" + str(iListCivic), ScrollPanel, "<font=3>" + szFatherTitle + "</font>", CvUtil.FONT_LEFT_JUSTIFY, localx + (self.ICON_BUTTON_SIZE * 2 + (self.ICON_BUTTON_SIZE / 10)), localy +  int(self.ICON_BUTTON_SIZE * 0.7), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iListCivic, 0)
									if (player.getIdeasResearched(iListCivic) <= 0):
										screen.addDDSGFCAt("MaterialIcon" + str(iListCivic), ScrollPanel, ArtFileMgr.getInterfaceArtInfo("MATERIALS_NEEDED").getPath(), localx + self.ICON_BUTTON_SIZE, localy +  int(self.ICON_BUTTON_SIZE * 1.5), self.ICON_BUTTON_SIZE - 3, self.ICON_BUTTON_SIZE - 3, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON + 3, -1, false)
										szHelp = CyGameTextMgr().parseCivicInfo(iListCivic, False, False, True, True, player.getCivilizationType())
										szHelp = localText.changeTextColor(szHelp, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
										screen.setTextAt("Cost" + str(iListCivic), ScrollPanel, "<font=2>" + szHelp + "</font>", CvUtil.FONT_LEFT_JUSTIFY, localx + self.ICON_BUTTON_SIZE * 2, localy +  int(self.ICON_BUTTON_SIZE * 1.9), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY, iListCivic, 0)
										
										
										if gc.getCivicInfo(iListCivic).getRequiredUnitType() != UnitTypes.NO_UNIT:
											iRequiredUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(gc.getCivicInfo(iListCivic).getRequiredUnitType())
											iProfession = gc.getUnitInfo(iRequiredUnit).getDefaultProfession()
											if iRequiredUnit != UnitTypes.NO_UNIT:
												screen.setImageButtonAt("RequiredUnit" + str(iListCivic), ScrollPanel, gc.getUnitInfo(iRequiredUnit).getArtInfo(0, -1).getFullLengthIcon(), int(localx + self.ICON_BUTTON_SIZE * 8), localy + self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE * 2, WidgetTypes.WIDGET_GENERAL, self.AMENDMENT_BUTTON + 1, iRequiredUnit)
												iNoNeedsUnit = 0
											
									#Required Inventions	
									if (gc.getCivicInfo(iListCivic).getRequiredInventionOr() != -1):
										if gc.getCivicInfo(iListCivic).getRequiredInvention2() != -1 and gc.getCivicInfo(iListCivic).getRequiredInvention() != -1:
											screen.addDDSGFCAt("RequiredInv" + str(iListCivic), ScrollPanel, gc.getCivicInfo(gc.getCivicInfo(iListCivic).getRequiredInvention()).getButton(), int(localx + self.ICON_BUTTON_SIZE * 7.1) + iNoNeedsUnit, localy + self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE , self.ICON_BUTTON_SIZE , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY, gc.getCivicInfo(iListCivic).getRequiredInvention(), self.AMENDMENT_BUTTON + 2, false)
									elif (gc.getCivicInfo(iListCivic).getRequiredInvention2() != -1):
										screen.addDDSGFCAt("RequiredInv" + str(iListCivic), ScrollPanel, gc.getCivicInfo(gc.getCivicInfo(iListCivic).getRequiredInvention2()).getButton(), int(localx + self.ICON_BUTTON_SIZE * 7.1) + iNoNeedsUnit, localy + self.ICON_BUTTON_SIZE, self.ICON_BUTTON_SIZE , self.ICON_BUTTON_SIZE , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY, gc.getCivicInfo(iListCivic).getRequiredInvention2(), self.AMENDMENT_BUTTON + 2, false)
									#screen.show(ScrollPanel)
									
								#elif gc.getDefineINT("TK_RESEARCH_IS_HIDDEN") > 0:
									#screen.addDDSGFCAt("HidesTech" + str(iListCivic), ScrollPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIDES_TECH").getPath(), localx, localy, self.TECH_BACKGROUND_X, self.TECH_BACKGROUND_Y,  WidgetTypes.WIDGET_GENERAL, -1, -1, false)
									
									
					if iTradeResearch != -1:
							screen.moveToFront("MagnifyingTrade")					
					self.TEMP_RESEARCH = -1
		return 0

	def getNextTestWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
	def handleInput(self, inputClass):
		
					
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
			if (inputClass.getData1() == self.CATEGORY + 1 or inputClass.getData1() == self.AMENDMENT_BUTTON):
				player = gc.getPlayer(gc.getGame().getActivePlayer())
				#if player.getResearchPartner() != -1:
					#return 0
				#if player.canDoCivics(inputClass.getData2()):
				screen = self.getScreen()
				iListCivic = inputClass.getData2()
				localx = 30 + ( (gc.getCivicInfo(iListCivic).getX_Location() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
				localy = ( gc.getCivicInfo(iListCivic).getY_Location() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + self.Y_MOD
				Magnefy_X = localx + self.ICON_BUTTON_SIZE * 4
				Magnefy_Y = localy + (self.ICON_BUTTON_SIZE / 2)
				TurnstoComplete = ""
				#iTurns = player.getCurrentResearchProgress(True, iListCivic)
				if iTurns > 0:
					TurnstoComplete = " (" + str(iTurns) + slash + str(iTradePointCost) +")"
				szFatherTitle = gc.getCivicInfo(iListCivic).getDescription()
				szFatherTitle = localText.changeTextColor(szFatherTitle + TurnstoComplete, gc.getInfoTypeForString("COLOR_FONT_GOLD"))
				screen.setTextAt("Title" + str(iListCivic), "ScrollPanel", "<font=3>" + szFatherTitle + "</font>", CvUtil.FONT_LEFT_JUSTIFY, localx + (self.ICON_BUTTON_SIZE * 2 + (self.ICON_BUTTON_SIZE / 10)), localy +  int(self.ICON_BUTTON_SIZE * 0.7), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, iListCivic, 0)
				screen.setImageButtonAt("MagnifyingTrade", "ScrollPanel", ArtFileMgr.getInterfaceArtInfo("MAGNIFYING_QUILL").getPath(), Magnefy_X, Magnefy_Y, self.MAGNIFYING_GLASS_X, self.MAGNIFYING_GLASS_Y, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iListCivic, 0)
				screen.moveToFront("MagnifyingTrade")
				#self.TEMP_RESEARCH = inputClass.getData2()
				
				
			
		
			#if (inputClass.isShiftKeyDown()):
			
			##FUNCTIONS##
			#getNotifyCode()
			#getFunctionName()
			#getButtonType()
			#getData()
			#getData1()
			#getData2()
			#getFlags()
			#getID()
			#getMouseX()
			#getMouseY()
			#getOption()
			#getPythonFile()
			#isAltKeyDown()
			#isCtrlKeyDown()
			#isShiftKeyDown()
			
			#NotifyCode.NOTIFY_CHARACTER
			#NotifyCode.NOTIFY_CLICKED
			#NotifyCode.NOTIFY_CURSOR_MOVE_OFF
			#NotifyCode.NOTIFY_CURSOR_MOVE_ON
			#NotifyCode.NOTIFY_DBL_CLICKED
			#NotifyCode.NOTIFY_FLYOUT_ITEM_SELECTED
			#NotifyCode.NOTIFY_FOCUS
			#NotifyCode.NOTIFY_LINKEXECUTE
			#NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED
			#NotifyCode.NOTIFY_MOUSEMOVE
			#NotifyCode.NOTIFY_MOUSEWHEELDOWN
			#NotifyCode.NOTIFY_MOUSEWHEELUP
			#NotifyCode.NOTIFY_MOVIE_DONE
			#NotifyCode.NOTIFY_NEW_HORIZONTAL_STOP
			#NotifyCode.NOTIFY_NEW_VERTICAL_STOP
			#NotifyCode.NOTIFY_SCROLL_DOWN
			#NotifyCode.NOTIFY_SCROLL_UP
			#NotifyCode.NOTIFY_SLIDER_NEWSTOP
			#NotifyCode.NOTIFY_TABLE_HEADER_SELECTED
			#NotifyCode.NOTIFY_UNFOCUS 
			
		return 0

	def update(self, fDelta):
		return 0
		
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		if eWidgetType == WidgetTypes.WIDGET_GENERAL and iData1 == self.AMENDMENT_BUTTON:
			if gc.getCivicInfo(iData2).getInventionCategory() == -1:
				szName = gc.getCivicInfo(iData2).getDescription()
				szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
				return szColoredName
			#player = gc.getPlayer(gc.getGame().getActivePlayer())
			szHelp = CyGameTextMgr().parseCivicInfo(iData2, False, False, True, False, player.getCivilizationType())
			szName = gc.getCivicInfo(iData2).getDescription()
			szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			if player.getResearchPartner() != -1:
				locked = localText.getText("TXT_KEY_CITY_CURRENT_RESEARCH_LOCKED", ())
				return szColoredName  + szHelp + "\n" + locked
			else:
				return szColoredName  + szHelp
			#return szHelp
		elif eWidgetType == WidgetTypes.WIDGET_GENERAL and iData1 == 2:
			
			szName = gc.getLeaderHeadInfo(gc.getPlayer(player.getResearchPartner()).getLeaderType()).getDescription()
			#szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			szName = localText.getText("TXT_KEY_RESEARCH_PARTNER_NAME", (szName,))
			return szName
		elif eWidgetType == WidgetTypes.WIDGET_GENERAL and iData1 == (self.AMENDMENT_BUTTON + 1):
			szName = gc.getUnitInfo(iData2).getDescription()
			szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			szName = localText.getText("TXT_KEY_REQUIRED_UNITCLASS", (szName,))
			return szName
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY and iData2 == self.AMENDMENT_BUTTON + 2:
			szHelp = CyGameTextMgr().parseCivicInfo(iData1, False, False, True, False, player.getCivilizationType())
			szName = gc.getCivicInfo(iData1).getDescription()
			szColoredName = localText.getText("TXT_KEY_ALSO_REQUIRES", ()) + localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			return szColoredName + szHelp
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECHNOLOGY and iData2 == 0:
			szHelp = CyGameTextMgr().parseCivicInfo(iData1, False, False, False, False, player.getCivilizationType())
			#szName = gc.getCivicInfo(iData1).getDescription()
			#szColoredName = localText.getText("TXT_KEY_ALSO_REQUIRES", ()) + localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			return szHelp
		elif eWidgetType == WidgetTypes.WIDGET_GENERAL and iData1 == self.AMENDMENT_BUTTON + 3:
			szColoredName = localText.getText("TXT_KEY_MATERIALS_ICON", ())
			return szColoredName
		elif eWidgetType == WidgetTypes.WIDGET_INVENTORS_HOUSE and iData1 == self.CATEGORY:
			szHelp = CyGameTextMgr().parseCivicInfo(iData2, False, False, True, False, player.getCivilizationType())
			szName = gc.getCivicInfo(iData2).getDescription()
			player = gc.getPlayer(gc.getGame().getActivePlayer())
			szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			if player.getResearchPartner() != -1:
				locked = localText.getText("TXT_KEY_CITY_CURRENT_RESEARCH_LOCKED", ())
				return szColoredName + szHelp + "\n" + locked
			return szColoredName + szHelp
		elif eWidgetType == WidgetTypes.WIDGET_INVENTORS_HOUSE and iData1 == self.CATEGORY + 1:
			szHelp = CyGameTextMgr().parseCivicInfo(iData2, False, False, True, False, player.getCivilizationType())
			szName = gc.getCivicInfo(iData2).getDescription()
			szColoredName = localText.changeTextColor(szName, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			#return szColoredName + szHelp
			player = gc.getPlayer(gc.getGame().getActivePlayer())
			if player.getResearchPartner() != -1:
				locked = localText.getText("TXT_KEY_CITY_CURRENT_RESEARCH_LOCKED", ())
				return szColoredName + szHelp + "\n" + locked
			elif player.canDoCivics(iData2):
				return szColoredName + szHelp + localText.getText("TXT_KEY_CLICK_TO_RESEARCH_THIS", ())
			
			else:
				return szColoredName + szHelp
				
		#elif iData1 == 1000:
				#return localText.getText("TXT_KEY_SELECT_TECH", ())

		return u""
	
		#szSpecialText = CyGameTextMgr().parseCivicInfo(self.iCivic, True, False, True, False)
		
	def CivDropDown( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = self.getScreen()
			return 0
	# Will draw the arrows
	def getXStart(self):
		return ( self.BOX_INCREMENT_WIDTH * self.PIXEL_INCREMENT )
		
	def getXSpacing(self):
		return ( self.BOX_INCREMENT_X_SPACING * self.PIXEL_INCREMENT )
										
	def getYStart(self, iY):
		return int((((self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ) / 6.0) * iY) - self.PIXEL_INCREMENT )

	def getWidth(self, xDiff):
		return ( ( xDiff * self.getXSpacing() ) + ( ( xDiff - 1 ) * self.getXStart() ) )
		
	def getHeight(self, yDiff, nFactor):
		return ( ( nFactor + ( ( abs( yDiff ) - 1 ) * 6 ) ) * self.PIXEL_INCREMENT )
	def drawArrows (self):

		screen = self.getScreen()

		iLoop = 0
		self.nWidgetCount = 0
		
		ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()

		for i in range(gc.getNumCivicInfos()):

			if (gc.getCivicInfo(i).getCivicOptionType() != 0):
				continue
				
			if gc.getCivicInfo(i).getInventionCategory() == -1:
				continue
			if gc.getCivicInfo(i).getInventionCategory() != 2:
				continue
			j = 0
			#
			for j in range(2):
					
				
				
				if (j == 0):
					eTech = gc.getCivicInfo(i).getRequiredInventionOr()
				elif (j == 1):
					eTech = gc.getCivicInfo(i).getRequiredInvention()
					eTech2 = gc.getCivicInfo(i).getRequiredInvention2()
					eOrTech = gc.getCivicInfo(i).getRequiredInventionOr()
					if (eTech2 != -1 and eOrTech != -1):
						eTech = gc.getCivicInfo(i).getRequiredInvention2()
							
				
				if ( eTech > -1):
	
					iX = 30 + ( (gc.getCivicInfo(eTech).getX_Location() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
					iY = ( gc.getCivicInfo(eTech).getY_Location() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + self.Y_MOD
					#iX = gc.getCivicInfo(eTech).getX_Location()
					#iY = gc.getCivicInfo(eTech).getY_Location()
					# j is the pre-req, i is the tech...
					xDiff = gc.getCivicInfo(i).getX_Location() - gc.getCivicInfo(eTech).getX_Location()
					yDiff = gc.getCivicInfo(i).getY_Location() - gc.getCivicInfo(eTech).getY_Location()
	
					if (yDiff == 0):
						screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(3), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						#screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, 40, 40, 100, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						#screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, 40, 40, 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff < 0):
						if ( yDiff == -6 ):
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(1), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif ( yDiff == -2 and xDiff == 2 ):
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff > 0):
						if ( yDiff == 2 and xDiff == 2):
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) * 5 / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif ( yDiff == 4 and xDiff == 1):
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(5), self.getWidth(xDiff) / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), ( self.getWidth(xDiff) * 2 / 3 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "ScrollPanel", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

		return
	def getNextWidgetName(self):
		szName = "TechArrow" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	
