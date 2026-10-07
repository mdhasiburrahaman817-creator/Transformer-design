# transformer design Assignment

import math
import sys

# Input Section
rating = float(input("Enter the KVA ratings of the transformer: "))
frequency = float(input("Enter the frequency of the transformer: "))
hv_voltage = float(input("Enter the voltage of High voltage winding: "))
lv_voltage = float(input("Enter the voltage of Low voltage windings: "))
Bmax = float(input("Maximum Flux Density (Tesla): "))
current_density = float(input("Current Density (A/mm²): "))
ki = 0.88
ks = 0.92
hv_connection = input("HV Connection (Star/Delta): ").strip().lower()
lv_connection = input("LV Connection (Star/Delta): ").strip().lower()
kw = float(input("Enter the value of Window space factor kw: "))
layer_in_lv = int(input("Enter number of layer for LV: "))
HV_layer = int(input("Enter the number of layer in HV winding: "))
Clearance = float(input("Assume clearance to yoke: "))
insulation = int(input("Enter insulation between HV and LV: "))
height_clearance = int(input("Enter height clearance between coils and core: "))
tube_dia = float(input("Enter the diameter of the tube(in meter): "))
tube_thickness = float(input("Enter the thickness of the tube(in meter): "))
temp = float(input("Enter temperature in Celcius: "))

if hv_connection == "star":
        hv_Vpp = hv_voltage / math.sqrt(3)
elif hv_connection == "delta":
        hv_Vpp = hv_voltage
if lv_connection == "star":
        lv_VPP = lv_voltage / math.sqrt(3)
elif lv_connection == "delta":
        lv_VPP = lv_voltage

# Calculation Section
turns_ratio = round((hv_Vpp / lv_VPP),2)
Et = (1 / 40) * math.sqrt((rating * 1000) / 3)
Et = round(Et,2)
print(f"Voltage Per turn {Et} V")
# Core area and core Diameter
def net_core_area(Et, Bmax, frequency):
    Ai = (Et * 1e6) / (4.44 * Bmax * frequency)
    return round(Ai,2)
def core_diameter(Ai, Ki, Ks):
    d = math.sqrt((4 * Ai) / (Ki * Ks * math.pi))
    return round(d,2)
def actual_core_area(d, Ki, Ks):
    Ai = Ki * Ks * math.pi * d**2 / 4
    return round(Ai, 4)
def actual_flux_density(Et, Ai_actual, frequency):
    Bmax = (Et * 1e6) / (4.44 * frequency * Ai_actual)
    return round(Bmax, 3)

Ai = net_core_area(Et, Bmax, frequency)
d = core_diameter(Ai, ki, ks)
print(f"\nYour Calculated Core Diameter = {d} mm")
assumed_diameter = float(input("Enter the assumed core diameter (mm): "))

Ai_actual = actual_core_area(assumed_diameter, ki, ks)
Bmax_actual = actual_flux_density(Et, Ai_actual, frequency)
print(f"Actual Core Area      = {Ai_actual:.3f} mm²")
print(f"Final Flux Density    = {Bmax_actual:.3f} Tesla")
core_loss_per_kg = float(input("Enter core loss per Kg form (loss vs Bmax) graph: "))
VA_per_kg = float(input("Enter Volt-Ampere per kg form VA vs Bmax graph: "))
# Window area calculation
Aw = (rating * 1e9) / (3.33 * Bmax_actual * frequency * current_density * kw * Ai_actual)
print(f"Your window area is {Aw:.3f} mm²")

def assume_window_dimension(Aw):

    while True:

        Ww = float(input("Enter Window Width (mm): "))
        Wh = Aw / Ww
        ratio = Wh / Ww
        print(f"\nCalculated Window Height = {Wh:.2f} mm")
        print(f"Height/Width Ratio = {ratio:.2f}")
        choice = input("\nKeep this height? (Y/N): ").upper()
        if choice == "Y":
            final_height = Wh
        elif choice == "N":
                final_height = float(input("Enter New Window Height (mm): "))
        final_ratio = final_height/Ww
        final_window_area = Ww * final_height
        return Ww, final_height, final_window_area,final_ratio

Ww, Wh, Aw,ratio = assume_window_dimension(Aw)
print(f"Final Window Width  = {Ww:.2f} mm")
print(f"Final Window Height = {Wh:.2f} mm")
print(f"Final Window Area   = {Aw:.2f} mm²")
print(f"Final ratio   = {ratio:.2f} mm²")

# Window dimension 
L_D = 0.95 * assumed_diameter
adj_limb = Ww + L_D
H_total = Wh + 2* L_D
W_total = 2* adj_limb + L_D
H_with_clearance = Wh + 2* Clearance
print(f"Largest diameter of the core is {L_D} mm")
print(f"Distance between the centre of the adjacent limbs {adj_limb} mm")
print(f"Total height with clearance {H_with_clearance} mm")
print(f"Total height  {H_total} mm")
print(f"Total Width {W_total} mm")

# Calculating turns in winding
turns_lv = round(lv_VPP/Et)
turns_hv = round(hv_Vpp/Et)
heigst_turns_hv = round(turns_hv + turns_hv* 5/100)
print(f"LV turns per phase = {round(turns_lv)}")
print(f"HV turns per phase normal {round(turns_hv)}")
print(f"HV turns per phase with +5% tapping {round(heigst_turns_hv)}")
print(f"HV turns per phase with -5% tapping {round(turns_hv - turns_hv* 5/100)}")
print(f"HV turns per phase with +2.5% tapping {round(turns_hv + turns_hv* 2.5/100)}")
print(f"HV turns per phase with -2.5% tapping {round(turns_hv - turns_hv* 2.5/100)}")
# LV conductor Layout calculation 
def lv_conductor(rating, lv_voltage, current_density):

    Ilv = (rating * 1000) / (math.sqrt(3) * lv_voltage)    # Current per phase
    print(f"\nCurrent per phase = {Ilv:.2f} A")

    required_area = Ilv / current_density    # Required conductor area
    print(f"Required conductor area = {required_area:.2f} mm²")
    strips = int(input("Enter number of parallel strips: "))    
    area_per_strip = required_area / strips    # Area per strip
    print(f"Area per strip = {area_per_strip:.2f} mm²")

    while True:
        thickness = float(input("Enter strip thickness (mm): "))
        width = float(input("Enter strip width (mm): "))
        actual_area = thickness * width * strips # actual conductor area
        actual_J = Ilv / actual_area   #actual current density

        print(f"\nActual conductor area = {actual_area:.2f} mm²")
        print(f"Actual current density = {actual_J:.3f} A/mm²")

        if actual_J <= current_density:
            break
        print("\nCurrent density exceeds the allowable limit!")
        print("Please choose a larger conductor size.\n")
    return round(Ilv,1), round(actual_area,3), round(actual_J,2), thickness, width, strips

Ilv,final_lv_area,actual_density,lv_thickness,lv_width,strips = lv_conductor(rating, lv_voltage, current_density)
print(f"Thickness of LV conductor {lv_thickness} mm")
print(f"Width of LV conductor {lv_width} mm")
# HV conductor Layout calculation 
def hv_conductor(rating, hv_voltage, current_density):

    Ihv = (rating * 1000) / (3 * hv_voltage)    # Current per phase
    print(f"\nCurrent per phase = {Ihv:.2f} A")
    required_area = Ihv / current_density    # Required conductor area
    print(f"Required conductor area = {required_area:.2f} mm²")
    required_diameter = math.sqrt((4 * required_area) / math.pi)
    print(f"Required conductor diameter = {required_diameter:.3f} mm")

    while True:

        assumed_diameter = float(input("Enter assumed conductor diameter (mm): "))
        actual_area = (math.pi / 4) * assumed_diameter ** 2        # Actual conductor area
        actual_J = Ihv / actual_area        # Actual current density
        print(f"\nActual conductor area = {actual_area:.3f} mm²")
        print(f"Actual current density = {actual_J:.3f} A/mm²")
        if actual_J <= current_density:
            break
        print("\nCurrent density exceeds the allowable limit!")
        print("Please choose a larger conductor diameter.\n")
    return round(Ihv,2), round(actual_area,3), round(actual_J,2), assumed_diameter

I_hv,final_hv_area,final_hv_density,final_diameter = hv_conductor(rating, hv_voltage, current_density)
print(f"Diameter of HV conductor {final_diameter} mm")

# LV winding Layout 
total_thickness = lv_thickness + 0.25  #choosing 0.25 mm paper insulation
total_width = lv_width + 0.25
total_area = total_thickness * total_width  # Area with insulation
turns_per_layer = math.ceil(turns_lv/layer_in_lv)
height_of_lv = total_width * turns_per_layer
LV_thickness = strips * total_thickness * layer_in_lv
# Choosing distance between core and LV = 3.5 mm 
inside_dia_lv = assumed_diameter + (2*3.5)
outside_dia_lv = inside_dia_lv + (2* LV_thickness)
mean_dia_lv = (inside_dia_lv + outside_dia_lv)/2
mean_turn_length_lv = round((math.pi * mean_dia_lv),1)

print("-------LV winding Layout---------")
print(f"Area with insulation {total_area} mm²")
print(f"Turns per layer = {turns_per_layer}mm")
print(f"Height of LV winding {height_of_lv}mm")
print(f"Thickness of LV winding {LV_thickness}mm")
print(f"Inside diameter of LV winding {inside_dia_lv}mm")
print(f"Outside diameter of LV winding {outside_dia_lv}mm")
print(f"Mean diameter of LV winding {mean_dia_lv}mm")
print(f"Mean length of turn in LV winding {mean_turn_length_lv}mm")

# HV winding Layout 
turns_per_coil = round(heigst_turns_hv / 4)
hv_turns_per_layer = math.ceil(turns_per_coil/ HV_layer)
total_hv_diameter = final_diameter + 0.25  #choosing 0.25 mm for insulation
hv_coil_thickness = HV_layer * total_hv_diameter
inside_dia_hv = outside_dia_lv + (insulation * 2)
outside_dia_hv = inside_dia_hv + (2*hv_coil_thickness)
mean_dia_hv = (inside_dia_hv + outside_dia_hv)/2
mean_turn_length_hv = round((math.pi * mean_dia_hv),1)
hv_coil_height = total_hv_diameter * hv_turns_per_layer
height_of_hv = (4 * hv_coil_height) + (3*8)  # choosing space between the coil = 8 mm
required_height = height_of_hv + (2* height_clearance)
if required_height >= H_with_clearance:
          print("Your total height is less than required height")
          sys.exit(1)

print("-------HV winding Layout---------")   
print(f"Turns per coil = {turns_per_coil} mm")
print(f"Turns per layer = {hv_turns_per_layer} mm")
print(f"Thickness of HV coil {hv_coil_thickness} mm")
print(f"Inside diameter of HV winding {inside_dia_hv} mm")
print(f"Outside diameter of HV winding {outside_dia_hv} mm")
print(f"Mean diameter of HV winding {mean_dia_hv} mm")
print(f"Mean length of turn in HV winding {mean_turn_length_hv} mm")
print(f"Height of HV coils in window {hv_coil_height} mm")
print(f"Height of HV winding {height_of_hv} mm")
print(f"Required height of HV winding with clearance {required_height} mm")

# Percentage of Reactance calculation
Avg_Lmt = (mean_turn_length_hv + mean_turn_length_lv)/2
hc = (height_of_hv + height_of_lv)/2
Amp_Turn =  Ilv * turns_lv
mean_winding_width = insulation + (hv_coil_thickness + LV_thickness)/3
numerator = 2*math.pi*frequency*4*math.pi*1e-7*Avg_Lmt*Amp_Turn*mean_winding_width*1e-3
percent_X = round(((numerator*100)/(hc*Et)),3)
print(f"Your Percentage of reactance is {percent_X}%")

#percentage of resistance calculation
rho20 = 0.01724
alpha20 = 0.00393
rho_temp = rho20 * (1+alpha20*(temp - 20))
LV_resistance = (rho_temp*mean_turn_length_lv*turns_lv)/(final_lv_area*1000)
HV_resistance = (rho_temp*mean_turn_length_hv*turns_hv)/(final_hv_area*1000)
R_eq_hv = HV_resistance + (LV_resistance * turns_ratio ** 2)
R_base = hv_Vpp / I_hv 
percent_R = round(((R_eq_hv / R_base) * 100),5)
print(f"Your Percentage of resistance is {percent_R}%")
# Percentage of impedance Calculation 
percent_imp = math.sqrt(percent_R**2 + percent_X ** 2)

if percent_imp < 3.5 or percent_imp > 4.5:
    print(f"\n✗ %Z = {percent_imp:.3f}% is outside the allowed 3.5%-4.5% range.")
    
    print("  Try again with new window dimension / change HV layer count.")
    sys.exit(1)
else:
    print(f"\n✓ %Z = {percent_imp:.3f}% is within the 3.5%-4.5% target. Design accepted.")

# Calculation of core loss 
core_volume = Ai_actual* (3*Wh + 2*W_total)
core_weight = round(((core_volume * 7.85)/ 1e6),3)
core_loss = round((core_weight * core_loss_per_kg),2)
# Weight of HV & LV winding 
Weight_lv = round(((8.89*final_lv_area*mean_turn_length_lv*turns_lv)/1e6),2)
Weight_hv = round(((8.89*final_hv_area*mean_turn_length_hv*turns_hv)/1e6),2)
total_copper_weight = 3*(Weight_lv + Weight_hv)
# Copper loss calculation
copper_loss = round((3*(I_hv**2)*R_eq_hv),2)
stray_load_loss = copper_loss * 0.07
load_loss = copper_loss + stray_load_loss
total_loss = load_loss + core_loss

# Performence Calculation
P_out = rating * 1000
E_full_load = (P_out*100)/(P_out + total_loss)
E_one_third_load = (P_out*0.75*100)/(0.75*P_out + core_loss + load_loss*0.75**2)
E_half_load = (0.5*P_out*100)/(0.5*P_out + core_loss + load_loss*0.5**2)

#Voltage Regulation Calculation
E_unity = math.sqrt((1 + percent_R/100)**2 + (percent_X/100)**2)
VR_unity = (E_unity - 1)* 100
#VR at 0.8 lagging p.f.
sin_phi = math.sqrt(1 - 0.8**2)
VR_lagging = (percent_R*0.8) + (percent_X*sin_phi)

# no load current 
magnetizing_VA = round((core_weight * VA_per_kg),3)
Ic = core_loss/(3*hv_Vpp)
Im = magnetizing_VA/ (3*hv_Vpp)
I_nl = math.sqrt(Ic**2 + Im**2)

print(f"Core loss is {core_loss}W")
print(f"Copper loss is {copper_loss}W")
print(f"Stray load loss is {stray_load_loss}W")
print(f"Total loss is {total_loss}W")
print(f"Efficiency on full load at unity p.f. = {E_full_load:.2f}%")
print(f"Efficiency on 75% load at unity p.f. = {E_one_third_load:.3f}%")
print(f"Efficiency on 50% load at unity p.f. = {E_half_load:.3}%")

print(f"Voltage regulation at unity power factor = {VR_unity:.3f}%")
print(f"Voltage regulation at 0.8 lagging power factor = {VR_lagging:.3f}%")

print(f"Your Magnetizing Volt ampere is {magnetizing_VA}")
print(f"Core loss current = {Ic:.4f}A")
print(f"Magnetizing current = {Im:.3f}A")
print(f"No load current = {I_nl:.4f}A")

# Design of transformer Tank
HV_coil_gap = adj_limb - outside_dia_hv
tank_L = (3*outside_dia_hv) + (2*HV_coil_gap) + 2*40 # taking end clearance = 40 mm
tank_B = outside_dia_hv + (2*60) # taking allowance for leads and taps = 60 mm
height_to_oil = H_total + 50 + 250  # taking base = 50 mm and oil margin = 250 mm
tank_H = height_to_oil + 250   # taking 250 mm for leads 

# Temperature Rise 
Dsp_surface = ((2*tank_H*tank_B)+(2*tank_L*tank_H))/1e6
print("Assuming 1m² can dissipate 12.5W heat")
temp_rise = total_loss/(12.5*Dsp_surface)
increased_area = 0
if temp_rise > 50:
     print("Temperature rise exceeds the limit you need extra cooling area")
     x = ((total_loss/(50*Dsp_surface))-3.7)/8.8
     original_area = Dsp_surface * x
     increased_area = original_area - Dsp_surface
     print(f"You need {increased_area}m² Extra cooling area.")
else:
     print("Temperature is within the limit")

# NO. of tube    
tube_len = height_to_oil - tube_dia
tube_surface = math.pi * tube_dia * tube_len * 1e-3
no_of_tube = math.ceil(increased_area/tube_surface)

# Volume of tank and Weight of oil 
vol_tank_oil = tank_L*tank_B*height_to_oil*1e-9
copper_volume = total_copper_weight/(8.89*1000)
vol_core_copper = copper_volume + (core_volume*1e-9)
Oil_volume = round((vol_tank_oil - vol_core_copper)*1000)
Oil_weight = 0.89 * Oil_volume
vol_tank = 0.005* (2*tank_L*tank_B+2*tank_L*tank_H+2*tank_B*tank_H)*1e-6 #taking thickness = 5mm
weight_tank = round((vol_tank * 7.85 * 1000),3)
vol_tube = round((math.pi*tube_dia**2*tube_len*no_of_tube)/4)
tube_oil_weight = vol_tube * 0.89
tube_weight = round((tube_surface*tube_thickness*7.85*1000*no_of_tube),3) 
total_weight = weight_tank+tube_weight+tube_oil_weight+Oil_weight+core_weight+total_copper_weight


print(f"Tank Length is {tank_L} mm")
print(f"Tank Breadth is {tank_B} mm")
print(f"Tank Height is {tank_H} mm")
print(f"No. of tube is {no_of_tube}")
print(f"Volume of Oil is {Oil_volume} litre")
print(f"weight of tank is = {weight_tank}Kg")
print(f"weight of Oil in tank is = {Oil_weight}Kg")
print(f"weight of tube is = {tube_weight}Kg")
print(f"weight of oil in tube is = {tube_oil_weight}Kg")
print(f"Weight of LV winding is: {Weight_lv} Kg")
print(f"Weight of HV winding is: {Weight_hv} Kg")
print(f"Weight of copper winding is: {total_copper_weight} Kg")
print(f"Weight of core winding is: {core_weight:.3f} Kg")
print(f"Total weight of the transformer is {total_weight:.4f}Kg")
