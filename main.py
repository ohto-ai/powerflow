# -*- coding: utf-8 -*-

import pandapower as pp
import pandapower.plotting as ppp

net = pp.create_empty_network(f_hz=50.0, sn_mva=100.)

# 母线节点参数
GEN1 = pp.create_bus(net, vn_kv=16.5, name="GEN 1", geodata=(0,0))
GEN2 = pp.create_bus(net, vn_kv=18.0, name="GEN 2", geodata=(6,0))
GEN3 = pp.create_bus(net, vn_kv=13.8, name="GEN 3", geodata=(3,-5))
BUS1 = pp.create_bus(net, vn_kv=230., name="BUS 1", geodata=(1,0))
BUS2 = pp.create_bus(net, vn_kv=230., name="BUS 2", geodata=(5,0))
BUS3 = pp.create_bus(net, vn_kv=230., name="BUS 3", geodata=(3,-4))
BUSA = pp.create_bus(net, vn_kv=230., name="BUS A", geodata=(3,0))
BUSB = pp.create_bus(net, vn_kv=230., name="BUS B", geodata=(2,-2))
BUSC = pp.create_bus(net, vn_kv=230., name="BUS C", geodata=(4,-2))

# 发电机参数
pp.create_ext_grid(net, bus=GEN1, vm_pu=1.01, name="Gen 1")  # Slack
pp.create_gen(net, bus=GEN2, p_mw=163, vm_pu=1.01)    # PV
pp.create_gen(net, bus=GEN3, p_mw=85, vm_pu=1.01)     # PV

# 负荷参数
pp.create_load(net, bus=BUSA, p_mw=125, q_mvar=70, name="Load 1")
pp.create_load(net, bus=BUS2, p_mw=35, q_mvar=10, name="Load 2")
pp.create_load(net, bus=BUSB, p_mw=90, q_mvar=40, name="Load 3")
pp.create_load(net, bus=BUSC, p_mw=100, q_mvar=55, name="Load 4")

# 并联导纳无功负荷
pp.create_shunt(net, BUSA, q_mvar=-20)
pp.create_shunt(net, BUSB, q_mvar=-10)
pp.create_shunt(net, BUSC, q_mvar=-20)

# 变压器参数
T1 = pp.create_transformer_from_parameters(net, sn_mva=100,
                                            hv_bus=BUS1, lv_bus=GEN1,
                                            vn_hv_kv=230, vn_lv_kv=16.5,
                                            vk_percent=5.67, vkr_percent=0,
                                            i0_percent=0, pfe_kw=0,
                                            tap_side='hv', tap_pos=3, tap_neutral=0,
                                            tap_step_percent=1.74,
                                            name="Trafo 1")

T2 = pp.create_transformer_from_parameters(net, sn_mva=100,
                                            hv_bus=BUS2, lv_bus=GEN2,
                                            vn_hv_kv=230, vn_lv_kv=18,
                                            vk_percent=6.25, vkr_percent=0,
                                            i0_percent=0, pfe_kw=0,
                                            tap_side='hv', tap_pos=3, tap_neutral=0,
                                            tap_step_percent=1.74,
                                            name="Trafo 2")

T3 = pp.create_transformer_from_parameters(net, sn_mva=100,
                                            hv_bus=BUS3, lv_bus=GEN3,
                                            vn_hv_kv=230, vn_lv_kv=13.8,
                                            vk_percent=5.86, vkr_percent=0,
                                            i0_percent=0, pfe_kw=0,
                                            tap_side='hv', tap_pos=3, tap_neutral=0, 
                                            tap_step_percent=1.74,
                                            name="Trafo 3")

# 线路参数
L1A = pp.create_line_from_parameters(net, from_bus=BUS1, to_bus=BUSA, length_km=1,
                               r_ohm_per_km=5.29, x_ohm_per_km=44.965,
                               c_nf_per_km=530, max_i_ka=1, name="Line 1A",
                               geodata=[[1,0],[3,0]])

L1B = pp.create_line_from_parameters(net, from_bus=BUS1, to_bus=BUSB, length_km=1,
                               r_ohm_per_km=8.993, x_ohm_per_km=48.668,
                               c_nf_per_km=475, max_i_ka=1, name="Line 1B",
                               geodata=[[1,0],[1,-1],[2,-1],[2,-2]])

L2A = pp.create_line_from_parameters(net, from_bus=BUS2, to_bus=BUSA, length_km=1,
                               r_ohm_per_km=16.928, x_ohm_per_km=85.169,
                               c_nf_per_km=921, max_i_ka=1, name="Line 2A",
                               geodata=[[5,0],[3,0]])

L2C = pp.create_line_from_parameters(net, from_bus=BUS2, to_bus=BUSC, length_km=1,
                               r_ohm_per_km=4.4965, x_ohm_per_km=38.088,
                               c_nf_per_km=448, max_i_ka=1, name="Line 2C",
                               geodata=[[5,0],[5,-1],[4,-1],[4,-2]])

L3B = pp.create_line_from_parameters(net, from_bus=BUS3, to_bus=BUSB, length_km=1,
                               r_ohm_per_km=20.631, x_ohm_per_km=89.93,
                               c_nf_per_km=1077, max_i_ka=1, name="Line 3B",
                               geodata=[[3,-4],[2,-4],[2,-2]])

L3C = pp.create_line_from_parameters(net, from_bus=BUS3, to_bus=BUSC, length_km=1,
                               r_ohm_per_km=6.2951, x_ohm_per_km=53.3232,
                               c_nf_per_km=628, max_i_ka=1, name="Line 3C",
                               geodata=[[3,-4],[4,-4],[4,-2]])

# 其它：开关
pp.create_switch(net, bus=GEN1, element=T1, et='t', closed=True, type='CB')
pp.create_switch(net, bus=GEN2, element=T2, et='t', closed=True, type='CB')
pp.create_switch(net, bus=GEN3, element=T3, et='t', closed=True, type='CB')
pp.create_switch(net, bus=BUS1, element=T1, et='t', closed=True, type='CB')
pp.create_switch(net, bus=BUS1, element=L1A, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUS1, element=L1B, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUS2, element=T2, et='t', closed=True, type='CB')
pp.create_switch(net, bus=BUS2, element=L2A, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUS2, element=L2C, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUS3, element=T3, et='t', closed=True, type='CB')
pp.create_switch(net, bus=BUS3, element=L3B, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUS3, element=L3C, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSA, element=L1A, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSA, element=L2A, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSB, element=L1B, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSB, element=L3B, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSC, element=L2C, et='l', closed=True, type='CB')
pp.create_switch(net, bus=BUSC, element=L3C, et='l', closed=True, type='CB')

pp.runpp(net, max_iteration=15)
ppp.simple_plot(net, plot_line_switches=True)
pp.to_excel(net, "IEEE9.xlsx")
