import math
import ctypes
import pymem                   
import pymem.process  
from math import sqrt, pi, atan
import requests             
from threading import Thread   
import keyboard                
import time                  

print('>>> Запускаем чит...')

if keyboard.is_pressed("end"):
    exit(0)

pm = pymem.Pymem('csgo.exe')

user32 = ctypes.windll.user32

client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

print('')
print('>>> Получение оффсетов...')

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwEntityList = int(response["signatures"]["dwEntityList"])
dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwForceJump = int(response["signatures"]["dwForceJump"])
m_fFlags = int(response["netvars"]["m_fFlags"])
dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_bDormant = int(response["signatures"]["m_bDormant"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
m_iItemDefinitionIndex = int(response["netvars"]["m_iItemDefinitionIndex"])
m_OriginalOwnerXuidLow = int(response["netvars"]["m_OriginalOwnerXuidLow"])
m_iItemIDHigh = int(response["netvars"]["m_iItemIDHigh"])
m_nFallbackPaintKit = int(response["netvars"]["m_nFallbackPaintKit"])
m_iAccountID = int(response["netvars"]["m_iAccountID"])
m_nFallbackStatTrak = int(response["netvars"]["m_nFallbackStatTrak"])
m_nFallbackSeed = int(response["netvars"]["m_nFallbackSeed"])
m_flFallbackWear = int(response["netvars"]["m_flFallbackWear"])
m_hMyWeapons = int(response['netvars']['m_hMyWeapons'])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_clrRender = int(response["netvars"]["m_clrRender"])

rgbT = [255, 51, 0]
rgbCT = [0, 51, 255]

def glowesp():
    while True:
        glow = pm.read_uint(client + dwGlowObjectManager)

        for i in range(0, 32):
            entity =  pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                entity_team_id = pm.read_uint(entity + m_iTeamNum)
                entityglowing = pm.read_uint(entity + m_iGlowIndex)

                if entity_team_id == 2:
                    pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))
                    pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                    pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
                    

                elif entity_team_id == 3:
                    pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))
                    pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                    pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)

def chamsesp():
    try:
        time.sleep(0.001)
        for i in range (0, 32):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)
            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)

                if entity_team_id == 2:
                    pm.write_int(entity + m_clrRender, (rgbT[0]))
                    pm.write_int(entity + m_clrRender + 0x1, (rgbT[1]))
                    pm.write_int(entity + m_clrRender + 0x2, (rgbT[2]))

                elif entity_team_id == 3:
                    pm.write_int(entity + m_clrRender, (rgbCT[0]))
                    pm.write_int(entity + m_clrRender + 0x1, (rgbCT[1]))
                    pm.write_int(entity + m_clrRender + 0x2, (rgbCT[2]))

            else: 
                pass

    except Exception as e:
        print(e)

def triggerbot():
     while True:
        localPlayer = pm.read_int(client + dwLocalPlayer)
        crosshairID = pm.read_int(localPlayer + m_iCrosshairId)
        getTeam = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
        localTeam = pm.read_int(localPlayer + m_iTeamNum)
        crosshairTeam = pm.read_int(getTeam + m_iTeamNum)

        if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam:
            pm.write_int(client + dwForceAttack, 6)


def BunnyHop():
    while True:
        if pm.read_int(client + dwLocalPlayer):
            player = pm.read_int(client + dwLocalPlayer)
            force_jump = client + dwForceJump
            on_ground = pm.read_int(player + m_fFlags)

            if keyboard.is_pressed("space"):
                if on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.17)
                    pm.write_int(force_jump, 4)

print ('')
print ('>>> Запуск BunnyHop...')

Thread(target=BunnyHop).start()

print ('')
print ('>>> BunnyHop запущен.')

print ('')
print ('>>> Запуск Chams...')

Thread(target=chamsesp).start()

print ('')
print ('>>> Chams запущен.')

print ('')
print ('>>> Запуск GlowESP...')
    
Thread(target=glowesp).start()
    
print ('')
print ('>>> GlowESP запущен.')

print ('')
print ('>>> Запуск Triggerbot...')

Thread(target=triggerbot).start()

print ('')
print ('>>> Triggerbot запущен.')

def main():
    chamsesp()
    glowesp()
    triggerbot()
   
if __name__ == '__main__':
    main()
