#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice
from random import randint
from clint.textui import colored
from pyfiglet import Figlet
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from datetime import datetime
from threading import Thread
from typing import Union
from requests import get
from os import system
import datetime as dt
import platform
import random
import string
import time

def intervaloMinutos(horaCompra, horaAtual) -> None:
	horaCompra = dt.datetime.strptime(horaCompra, "%H:%M:%S")
	horaAtual = dt.datetime.strptime(horaAtual, "%H:%M:%S")
	intervalo = relativedelta(horaCompra, horaAtual)
	return int(intervalo.minutes)

def checkHora(hora):
	try:
		hora = dt.datetime.strptime(hora, "%H:%M:%S")
		return True
	except:
		return False 

class AutoComprar:
	def __init__(self, emailAliExpress, senhaAliExpress, linkCarrinho, cupomTentativa, cupomCompra, horaAbrir, horaCompra):
		print(self.tipo_mensagem("alerta", u"Aguardando a hora de acessar o AliExpress para comprar o produto!\n"))
		while True:
			horaAtual = str(datetime.now().strftime('%H:%M:%S'))
			if horaAtual >= horaAbrir:
				firefox_options = Options()
				firefox_options.add_argument('--headless')
				firefox_options.add_argument("--no-sandbox")
				firefox_options.add_argument("--mute-audio")
				firefox_options.add_argument("--log-level=3")
				firefox_options.add_argument("--ignore-certificate-errors")
				firefox_options.add_argument('--disable-gpu')
				firefox_options.add_argument('--disable-extensions')
				firefox_options.add_argument('--disable-default-apps')
				firefox_options.add_argument("--disable-dev-shm-usage")
				profile = webdriver.FirefoxProfile() 
				profile.executable_path = r'./geckodriver.exe'
				self.browser = webdriver.Firefox(profile, options=firefox_options, service_log_path="C:\\Windows\\Temp\\geckodriver.log")
				self.browser.get(linkCarrinho)
				self.bot(emailAliExpress, senhaAliExpress, cupomTentativa, cupomCompra, horaAbrir, horaCompra)
				break
			system("title "+ f"AutoComprar AliExpress - Versão 0.9 By Nícolas Pastorello - Hora Atual : "+horaAtual)
			time.sleep(1)

	def autenticar(self, emailAliExpress, senhaAliExpress):
		try:
			print(self.tipo_mensagem("alerta", u"Logando em sua conta do AliExpress."))
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//input[@id='fm-login-id' or @name='fm-login-id']"))).send_keys(emailAliExpress)
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//input[@id='fm-login-password' or @name='fm-login-password']"))).send_keys(senhaAliExpress)
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//button[@class='fm-button']"))).click()
			try:
				WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, r"//button[@ae_button_type='place_order']")))
				print(self.tipo_mensagem("sucesso", u"Logado em sua conta do AliExpress."))
			except:
				print(self.tipo_mensagem("erro", u"O e-mail ou senha que você inseriu está incorreta."))
				time.sleep(5)
				self.browser.close()
				self.browser.quit()
		except:
			print(self.tipo_mensagem("erro", u"Não foi possivel realizar login no AliExpress."))
			time.sleep(5)
			self.browser.close()
			self.browser.quit()

	def alterarPagamento(self):
		try:
			print(self.tipo_mensagem("alerta", u"Alterando forma de pagamento para Boleto."))
			try:
				WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, r"//span[text()='selecione o método de pagamento']"))).click() 
			except:
				WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, r"//button[text()='Mudar']"))).click() 
			
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//div[text()='Boleto']"))).click()
			time.sleep(2)
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//button[text()='Confirmar']"))).click()
			print(self.tipo_mensagem("sucesso", u"Alterado forma de pagamento para Boleto."))
		except:
			print(self.tipo_mensagem("erro", u"Não foi possivel mudar a forma de pagamento para Boleto."))
			time.sleep(5)
			self.browser.close()
			self.browser.quit()

	def aplicarCupom(self, cupomTentativa, cupomCompra):
		try:
			print(self.tipo_mensagem("alerta", u"Aplicando cupom de desconto."))
			tentativa = 0
			while True:
				WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//input[@id='code' or @name='code']"))).send_keys(cupomCompra)
				WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//button[@ae_button_type='coupon_code']"))).click()
				time.sleep(0.5)
				WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//div[@id='root']"))).click()
				time.sleep(0.5)
				validarCupom = WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//button[@ae_button_type='coupon_code']"))).text
				if validarCupom == "Remover":
					self.horaDeComprar()
					break
				else:
					tentativa += 1
					if tentativa >= int(cupomTentativa):
						print(self.tipo_mensagem("erro", u"Cupom foi aplicado {} vezes mas não foi alterado o valor. Cupom deve estar com problema.".format(tentativa)))
						break
		except:
			print(self.tipo_mensagem("erro", u"Não foi possivel definir o cupom."))
			time.sleep(5)
			self.browser.close()
			self.browser.quit()
				
	def horaDeComprar(self):
		try:
			valorComprado = WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//div[@class='total-price']"))).text
			WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, r"//button[@ae_button_type='place_order']"))).click()
			print(self.tipo_mensagem("sucesso", u"Cupom aplicado e clicado para comprar com sucesso pelo valor de {}.".format(valorComprado.replace("Total\n",""))))
		except:
			print(self.tipo_mensagem("erro", u"Não foi possivel compra."))
			time.sleep(5)
			self.browser.close()
			self.browser.quit()

	def tipo_mensagem(self, tipo, mensagem):
		if tipo == "sucesso":
			return colored.green("[+] Sucesso: "+mensagem)
		elif tipo == "alerta":
			return colored.yellow("[!] Alerta: "+mensagem)
		elif tipo == "erro":
			return colored.red("[-] Erro: "+mensagem)

	def bot(self, emailAliExpress, senhaAliExpress, cupomTentativa, cupomCompra, horaAbrir, horaCompra):
		try:
			self.autenticar(emailAliExpress, senhaAliExpress)
			self.alterarPagamento()
			print("\n")
			print(self.tipo_mensagem("alerta", u"Aguardando a hora de aplicar o seu cupom!"))
			while True:
				horaAtual = str(datetime.now().strftime('%H:%M:%S'))
				if horaAtual >= horaCompra:
					self.aplicarCupom(cupomTentativa, cupomCompra)
					break
				system("title "+ f"AutoComprar AliExpress - Versão 0.9 By Nícolas Pastorello - Hora Atual : "+horaAtual)
				time.sleep(1)
		except:
			print(self.tipo_mensagem("erro", u"Não foi possivel executar o Bot."))
			self.browser.close()
			self.browser.quit()

system("title "+ f"AutoComprar AliExpress - Versão 0.9 By Nícolas Pastorello")
Graph = Figlet(font="slant")
GraphRender = Graph.renderText("AutoComprar AliExpress")
system("cls")
print("%s" % (colored.yellow(GraphRender)))
print(colored.cyan("Automatização de compras no AliExpress definido por horario.\nNão me responsabilizo por problemas relacionadas a sua conta.\nBy Nícolas Pastorello\n"))
print(colored.green("https://github.com/opastorello/AliExpressAutoCompra\n"))

try:
	
	while True:
	    emailAliExpress = input(colored.yellow('[!] Insira seu e-mail do AliExpress: '))
	    try:
	        emailAliExpress = emailAliExpress
	    except:
	        continue
	    if len(emailAliExpress) < 1:
	        continue
	    break

	while True:
	    senhaAliExpress = input(colored.yellow('[!] Insira sua senha do AliExpress: '))
	    try:
	        senhaAliExpress = senhaAliExpress
	    except:
	        continue
	    if len(senhaAliExpress) < 1:
	        continue
	    break

	while True:
	    linkCarrinho = input(colored.yellow('[!] Insira o link do carrinho do produto desejado: '))
	    try:
	        linkCarrinho = linkCarrinho
	    except:
	        continue
	    if 'https://shoppingcart.aliexpress.com/' not in linkCarrinho:
	        continue
	    break

	while True:
	    cupomCompra = input(colored.yellow('[!] Informe o cupom de desconto: '))
	    try:
	        cupomCompra = cupomCompra
	    except:
	        continue
	    if len(cupomCompra) < 2:
	        continue
	    break

	while True:
	    cupomTentativa = input(colored.yellow('[!] Informe a quantidade de tentativas de aplicar o cupom de desconto (1~10): '))
	    try:
	        cupomTentativa = cupomTentativa
	    except:
	        continue
	    if cupomTentativa.isdigit() == False:
	    	continue
	    if len(cupomTentativa) < 1:
	        continue
	    if int(cupomTentativa) < 1:
	        continue
	    if int(cupomTentativa) > 10:
	        continue
	    break

	while True:
	    horaAbrir = input(colored.yellow('[!] Informe a hora de acessar o AliExpress para comprar o produto (Exemplo 20:50:00): '))
	    try:
	        horaAbrir = horaAbrir
	    except:
	        continue
	    if len(horaAbrir) < 8:
	        continue
	    if checkHora(horaAbrir) == False:
	        continue
	    if horaAbrir <= str(datetime.now().strftime('%H:%M:%S')):
	    	continue
	    break

	while True:
		horaCompra = input(colored.yellow('[!] Informe a hora de aplicar o cupom de desconto (Exemplo 21:00:00): '))
		try:
			horaCompra = horaCompra
		except:
			continue
		if len(horaCompra) < 8:
			continue
		if checkHora(horaCompra) == False:
			continue
		if intervaloMinutos(horaCompra, horaAbrir) < 1:
			continue
		break

	print("\n")

	AutoComprar(emailAliExpress, senhaAliExpress, linkCarrinho, cupomTentativa, cupomCompra, horaAbrir, horaCompra)
except (KeyboardInterrupt):
	pass
