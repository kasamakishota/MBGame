# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random
import copy
import time
import numpy as np
from MB_AI1 import *


board = 0
cboard = 0
turn = 1
AIturn = 1
mass = 0
field_size = 0
win = 3
screen = 0
gamemode = 0
end = 0

#画面の初期設定
def field_setting():
	global board, mass, field_size, screen, gamemode, win
	#ゲームモード（1:対人対戦)(2:CPU対戦）
	print "Please select field size 3 through 10"
	#画面の一辺の長さ
	mass = int(raw_input())
	field_size = 60 * mass + 1
	win = 3
	if mass >= 5:
		win = 4
	#ゲームモード（1:対人対戦)(2:CPU対戦）
	print "Please select mode 1 or 2 (1:human, 2:CPU)"
	gamemode = int(raw_input())
	#画面サイズ
	screen_size = (field_size,field_size)
	#screen_sizeの画面を作成
	screen = pygame.display.set_mode(screen_size)
	#タイトルバーの文字列
	pygame.display.set_caption("AI_MBGame")
	#盤面の状況を表すリスト
	board = [[0 for i in range(mass)] for j in range(mass)]
	#画面の背景
	screen.fill((255,255,255))
	#枠線の描写
	for line in range(0,field_size,60):
		pygame.draw.line(screen,(0,0,0),(0,line),(field_size-1,line))
		pygame.draw.line(screen,(0,0,0),(line,0),(line,field_size-1))

#盤面の状態を取得して画面出力
def board_state():
	for y in range(0,mass):
		for x in range(0,mass):
			#状態が1ならば赤〇
			if board[x][y] == 1:
				pygame.draw.circle(screen,(255,0,0),(y*60+30,x*60+30),20,5)
			#状態が-1ならば青×
			if board[x][y] == -1:
				pygame.draw.line(screen,(0,0,255),(y*60+13,x*60+13),(y*60+48,x*60+48),6)
				pygame.draw.line(screen,(0,0,255),(y*60+48,x*60+13),(y*60+13,x*60+48),6)

#どちらのターンかを左上に表示
def turn_display():
	pygame.draw.rect(screen,(255,255,255),Rect(1,1,15,15))
	sysfont = pygame.font.SysFont(None,23)
	if turn == 1:
		text = sysfont.render(u"o",False,(255,0,0))
	if turn == -1:
		text = sysfont.render(u"×",False,(0,0,255))
	screen.blit(text,(1,1))

#終了画面
def result():
	global end
	end = 1
	sysfont = pygame.font.SysFont(None,mass*10)
	if turn == -1:
		text = sysfont.render(u"o win!",False,(0,255,0))
	if turn == 1:
		text = sysfont.render(u"× win!",False,(0,255,0))
	screen.blit(text,((field_size*0.5)-(mass*10),(field_size*0.5)-(mass*3.3)))

#ユーザインターフェース
def UI(event):
	global board, turn
	yp, xp = event.pos
	xp = xp / 60
	yp = yp / 60
	if board[xp][yp] == 0:
		board[xp][yp] = turn
		turn *= -1

def AI():
	global board, turn
	x, y = MB_AI(board,turn,mass)
	board[x][y] = turn
	turn *= -1

#勝利判定プログラム
def judgement():
	#横ラインをカウント
	for y in range(0,mass):
		count = 0
		for x in range(0,mass):
			if board[x][y] == -turn:
				count += 1
			if board[x][y] != -turn:
				count = 0
			if count == win:
				result()
	#縦ラインをカウント
	for x in range(0,mass):
		count = 0
		for y in range(0,mass):
			if board[x][y] == -turn:
				count += 1
			if board[x][y] != -turn:
				count = 0
			if count == win:
				result()
	#斜めラインをカウント
	for i in range(0,mass):
		count = [0,0,0,0]
		for j in range(0,mass-i):
			#（↘）方向
			if board[i+j][j] == -turn:
				count[0] += 1
			if board[i+j][j] != -turn:
				count[0] = 0
			if board[j][i+j] == -turn:
				count[1] += 1
			if board[j][i+j] != -turn:
				count[1] = 0
			#（↙）方向
			if board[mass-i-j-1][j] == -turn:
				count[2] += 1
			if board[mass-i-j-1][j] != -turn:
				count[2] = 0
			if board[mass-j-1][j+i] == -turn:
				count[3] += 1
			if board[mass-j-1][j+i] != -turn:
				count[3] = 0			#判定
			if count[0] == win or count[1] == win or count[2] == win or count[3] == win:
				result()

#ループプログラム
def MBGame():
	global board, turn, end, AIturn
	AIturn = random.randrange(-1,2,2)
	while True:
		#CPU
		if turn == AIturn and gamemode == 2:
			AI()
		#イベント処理
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				UI(event)
				judgement()
				for out in board:
					print out
				print ""
		#画面を更新
		turn_display()
		board_state()
		pygame.display.update()
		if end == 1:
			print "GameFinish?(y/n)"
			fin = raw_input()
			if fin == "y":
				sys.exit()
			if fin == "n":
				end = 0
				for y in range(0,mass):
					for x in range(0,mass):
						board[x][y] = 0
				turn = 1
				main()

def main():
	pygame.init()
	field_setting()
	MBGame()

if __name__ == '__main__':
	main()
	