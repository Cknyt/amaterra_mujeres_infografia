# -*- coding: utf-8 -*-
"""
Script to fill ATP and No_ATP_(+0,5) sheets with dynamic Excel formulas.
Uses universal Excel formula syntax for decimals: ">="&0.5 so that
Excel parses 0.5 correctly regardless of whether the system locale uses comma or dot!
"""
import openpyxl

def apply_formulas(file_path, output_path):
    wb = openpyxl.load_workbook(file_path)
    # Ensure Excel recalculates all formulas on load
    wb.calculation.fullCalcOnLoad = True
    
    # -------------------------------------------------------------
    # 1. PESTAÑA: ATP
    # -------------------------------------------------------------
    ws_atp = wb['ATP']
    
    # Tabla 1: Total ATP (Filas 5-8)
    ws_atp['E6'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre")'
    ws_atp['E7'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer")'
    ws_atp['E8'] = '=SUM(E6:E7)'
    ws_atp['F6'] = '=SUM(E6/E8)*100'
    ws_atp['F7'] = '=SUM(E7/E8)*100'
    ws_atp['F8'] = '=SUM(E8/E8)*100'
    # % de ATP sobre los fines de mercado
    ws_atp['H7'] = "=SUM(E8/'No_ATP_(+0,5)'!E12)*100"
    
    # Tabla 2: Mujeres ATP por subsectores (Filas 11-27)
    atp_subsectors = [
        (12, 'EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN CRIA Y CARNE'),
        (13, 'EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN LECHE'),
        (14, 'EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS EN INVERNADERO'),
        (15, 'EXPLOTACIONES DE AVES PONEDORAS ESPECIALIZADAS'),
        (16, 'EXPLOTACIONES DE OVINOS ESPECIALIZADAS'),
        (17, 'EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS AL AIRE LIBRE'),
        (18, 'EXPLOTACIONES FRUTÍCOLAS ESPECIALIZADAS'),
        (19, 'EXPLOTACIONES ESPECIALIZADAS EN VITICULTURA'),
        (20, 'EXPLOTACIONES NO CLASIFICADAS'),
        (21, 'EXPLOTACIONES DE CAPRINOS ESPECIALIZADAS'),
        (22, 'EXPLOTACIONES DE AVES DE CORRAL DE CARNE ESPECIALIZADAS'),
        (23, 'EXPLOTACIONES DE HERBÍVOROS'),
        (24, 'EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES EN INVERNADERO'),
        (25, 'EXPLOTACIONES QUE COMBINAN LA CRÍA Y ENGORDE DE PORCINOS'),
        (26, 'EXPLOTACIONES APÍCOLAS')
    ]
    
    for r, sub_name in atp_subsectors:
        ws_atp.cell(r, 4, sub_name)
        ws_atp.cell(r, 5, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$I$2:$I$12651, D{r})')
        ws_atp.cell(r, 6, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$I$2:$I$12651, D{r})')
        ws_atp.cell(r, 7, f'=SUM(E{r}/$E$8)*100')
        ws_atp.cell(r, 8, f'=SUM(F{r}/$E$8)*100')
        ws_atp.cell(r, 9, f'=SUM(F{r}/$F$27)*100')
        ws_atp.cell(r, 10, f'=SUM(E{r}/$E$27)*100')
        ws_atp.cell(r, 14, f'=E{r}')
        ws_atp.cell(r, 15, f'=F{r}')
        ws_atp.cell(r, 16, f'=SUM(N{r}:O{r})')
        ws_atp.cell(r, 17, f'=IF(P{r}>0, SUM(N{r}/P{r})*100, 0)')
        ws_atp.cell(r, 18, f'=IF(P{r}>0, SUM(O{r}/P{r})*100, 0)')
        
    # Totales subsectores fila 27
    ws_atp['E27'] = '=SUM(E12:E26)'
    ws_atp['F27'] = '=SUM(F12:F26)'
    ws_atp['G27'] = '=SUM(E27/$E$8)*100'
    ws_atp['H27'] = '=SUM(F27/$E$8)*100'
    ws_atp['I27'] = '=SUM(F27/$F$27)*100'
    ws_atp['J27'] = '=SUM(E27/$E$27)*100'
    ws_atp['N27'] = '=SUM(N12:N26)'
    ws_atp['O27'] = '=SUM(O12:O26)'
    ws_atp['P27'] = '=SUM(P12:P26)'
    ws_atp['Q27'] = '=SUM(N27/P27)*100'
    ws_atp['R27'] = '=SUM(O27/P27)*100'
    
    # Tabla 3: Edad ATP (Filas 29-37)
    ws_atp['D30'] = '=ROUND(AVERAGEIFS(Hoja1!$L$2:$L$12651, Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer"), 0)'
    
    # Tramos edad
    # 18-40
    ws_atp['Q30'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$L$2:$L$12651, ">=18", Hoja1!$L$2:$L$12651, "<=40")'
    ws_atp['R30'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">=18", Hoja1!$L$2:$L$12651, "<=40")'
    ws_atp['S30'] = '=SUM(Q30/$Q$33)*100'
    ws_atp['T30'] = '=SUM(R30/$R$33)*100'
    
    # 41-65
    ws_atp['Q31'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$L$2:$L$12651, ">=41", Hoja1!$L$2:$L$12651, "<=65")'
    ws_atp['R31'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">=41", Hoja1!$L$2:$L$12651, "<=65")'
    ws_atp['S31'] = '=SUM(Q31/$Q$33)*100'
    ws_atp['T31'] = '=SUM(R31/$R$33)*100'
    
    # Mayor de 65
    ws_atp['Q32'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$L$2:$L$12651, ">65")'
    ws_atp['R32'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">65")'
    ws_atp['S32'] = '=SUM(Q32/$Q$33)*100'
    ws_atp['T32'] = '=SUM(R32/$R$33)*100'
    
    # Total edad
    ws_atp['Q33'] = '=SUM(Q30:Q32)'
    ws_atp['R33'] = '=SUM(R30:R32)'
    ws_atp['S33'] = '=SUM(Q33/$Q$33)*100'
    ws_atp['T33'] = '=SUM(R33/$R$33)*100'
    
    # Edad x Comarcas para mujeres (W a AC)
    comarcas_atp = [
        ('W', 'ENKARTERRIALDE'),
        ('X', 'JATAONDO'),
        ('Y', 'GORBEIALDE'),
        ('Z', 'URKIOLA'),
        ('AA', 'URREMENDI'),
        ('AB', 'LEA ARTIBAI')
    ]
    # Fila 30: 18-40
    for col_letter, adr_name in comarcas_atp:
        ws_atp[f'{col_letter}30'] = f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">=18", Hoja1!$L$2:$L$12651, "<=40", Hoja1!$S$2:$S$12651, "{adr_name}")'
        ws_atp[f'{col_letter}31'] = f'=SUM({col_letter}30/$AC$30)*100'
    ws_atp['AC30'] = '=SUM(W30:AB30)'
    ws_atp['AC31'] = '=SUM(AC30/$AC$30)*100'
    
    # Fila 32: 41-65
    for col_letter, adr_name in comarcas_atp:
        ws_atp[f'{col_letter}32'] = f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">=41", Hoja1!$L$2:$L$12651, "<=65", Hoja1!$S$2:$S$12651, "{adr_name}")'
        ws_atp[f'{col_letter}33'] = f'=SUM({col_letter}32/$AC$32)*100'
    ws_atp['AC32'] = '=SUM(W32:AB32)'
    ws_atp['AC33'] = '=SUM(AC32/$AC$32)*100'
    
    # Fila 34: Mayor de 65
    for col_letter, adr_name in comarcas_atp:
        ws_atp[f'{col_letter}34'] = f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$L$2:$L$12651, ">65", Hoja1!$S$2:$S$12651, "{adr_name}")'
        ws_atp[f'{col_letter}35'] = f'=SUM({col_letter}34/$AC$34)*100'
    ws_atp['AC34'] = '=SUM(W34:AB34)'
    ws_atp['AC35'] = '=SUM(AC34/$AC$34)*100'
    
    # Tabla 4: Superficie ATP (Filas 32-37)
    # 33: Muy pequeña: 0,5 - 5 ha
    ws_atp['E33'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$O$2:$O$12651, "<=5")'
    ws_atp['F33'] = '=SUM(E33/$E$8)*100'
    ws_atp['G33'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$O$2:$O$12651, "<=5")'
    ws_atp['H33'] = '=SUM(G33/$E$8)*100'
    ws_atp['I33'] = '=SUM(G33/$G$37)*100'
    ws_atp['J33'] = '=SUM(E33/$E$37)*100'
    
    # 34: Pequeña: 5-20 ha
    ws_atp['E34'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$O$2:$O$12651, ">5", Hoja1!$O$2:$O$12651, "<=20")'
    ws_atp['F34'] = '=SUM(E34/$E$8)*100'
    ws_atp['G34'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$O$2:$O$12651, ">5", Hoja1!$O$2:$O$12651, "<=20")'
    ws_atp['H34'] = '=SUM(G34/$E$8)*100'
    ws_atp['I34'] = '=SUM(G34/$G$37)*100'
    ws_atp['J34'] = '=SUM(E34/$E$37)*100'
    
    # 35: Mediana: 20-50 ha
    ws_atp['E35'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$O$2:$O$12651, ">20", Hoja1!$O$2:$O$12651, "<=50")'
    ws_atp['F35'] = '=SUM(E35/$E$8)*100'
    ws_atp['G35'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$O$2:$O$12651, ">20", Hoja1!$O$2:$O$12651, "<=50")'
    ws_atp['H35'] = '=SUM(G35/$E$8)*100'
    ws_atp['I35'] = '=SUM(G35/$G$37)*100'
    ws_atp['J35'] = '=SUM(E35/$E$37)*100'
    
    # 36: Grande: > 50 ha
    ws_atp['E36'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$O$2:$O$12651, ">50")'
    ws_atp['F36'] = '=SUM(E36/$E$8)*100'
    ws_atp['G36'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$O$2:$O$12651, ">50")'
    ws_atp['H36'] = '=SUM(G36/$E$8)*100'
    ws_atp['I36'] = '=SUM(G36/$G$37)*100'
    ws_atp['J36'] = '=SUM(E36/$E$37)*100'
    
    # 37: Total
    ws_atp['E37'] = '=SUM(E33:E36)'
    ws_atp['F37'] = '=SUM(E37/$E$8)*100'
    ws_atp['G37'] = '=SUM(G33:G36)'
    ws_atp['H37'] = '=SUM(G37/$E$8)*100'
    ws_atp['I37'] = '=SUM(G37/$G$37)*100'
    ws_atp['J37'] = '=SUM(E37/$E$37)*100'
    
    # Tabla 5: Eco ATP (Filas 39-41)
    ws_atp['L39'] = '=SUM(E40, G40)'
    ws_atp['E40'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$T$2:$T$12651, "<>")'
    ws_atp['F40'] = '=SUM(E40/$E$8)*100'
    ws_atp['G40'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$T$2:$T$12651, "<>")'
    ws_atp['H40'] = '=SUM(G40/$E$7)*100'
    ws_atp['F41'] = '=SUM(E40/L39)*100'
    ws_atp['H41'] = '=SUM(G40/L39)*100'
    
    # Tabla 6: Comarca ATP (Filas 44-51)
    comarcas_table_atp = [
        (45, 'Enkarterrialde', 'ENKARTERRIALDE'),
        (46, 'Jata Ondo', 'JATAONDO'),
        (47, 'Gorbeialde', 'GORBEIALDE'),
        (48, 'Urkiola', 'URKIOLA'),
        (49, 'Urremendi', 'URREMENDI'),
        (50, 'Lea-Artibai', 'LEA ARTIBAI')
    ]
    for r, name_lbl, adr_val in comarcas_table_atp:
        ws_atp.cell(r, 4, name_lbl)
        ws_atp.cell(r, 5, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$S$2:$S$12651, "{adr_val}")')
        ws_atp.cell(r, 6, f'=SUM(E{r}/$E$51)*100')
        ws_atp.cell(r, 7, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$S$2:$S$12651, "{adr_val}")')
        ws_atp.cell(r, 8, f'=SUM(G{r}/$G$51)*100')
        ws_atp.cell(r, 13, f'=E{r}')
        ws_atp.cell(r, 14, f'=G{r}')
        ws_atp.cell(r, 15, f'=SUM(M{r}:N{r})')
        ws_atp.cell(r, 16, f'=SUM(M{r}/O{r})*100')
        ws_atp.cell(r, 17, f'=SUM(N{r}/O{r})*100')
        
    ws_atp['E51'] = '=SUM(E45:E50)'
    ws_atp['F51'] = '=SUM(E51/$E$51)*100'
    ws_atp['G51'] = '=SUM(G45:G50)'
    ws_atp['H51'] = '=SUM(G51/$G$51)*100'
    ws_atp['M51'] = '=SUM(M45:M50)'
    ws_atp['N51'] = '=SUM(N45:N50)'
    ws_atp['O51'] = '=SUM(O45:O50)'
    ws_atp['P51'] = '=SUM(M51/O51)*100'
    ws_atp['Q51'] = '=SUM(N51/O51)*100'
    
    # Tabla 7: Condición jurídica ATP (Filas 54-63)
    juridica_table = [
        (55, 'Persona física', 'PERSONA FISICA'),
        (56, 'Comunidad de bienes', 'COMUNIDAD DE BIENES'),
        (57, 'Sociedad civil', 'SOCIEDAD CIVIL'),
        (58, 'Titularidad compartida', 'ENTIDAD DE TITULARIDAD COMPARTIDA'),
        (59, 'Sociedad limitada', 'SOCIEDAD LIMITADA'),
        (60, 'Asociaciones', 'ASOCIACIONES'),
        (61, 'Sociedad agraria de transformación', 'SOCIEDAD AGRARIA DE TRANSFORMACION'),
        (62, 'Cooperativa', 'SOCIEDADES COOPERATIVAS')
    ]
    for r, name_lbl, jur_val in juridica_table:
        ws_atp.cell(r, 4, name_lbl)
        ws_atp.cell(r, 5, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$G$2:$G$12651, "{jur_val}")')
        ws_atp.cell(r, 6, f'=SUM(E{r}/$E$8)*100')
        ws_atp.cell(r, 7, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Bai/Si", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$G$2:$G$12651, "{jur_val}")')
        ws_atp.cell(r, 8, f'=SUM(G{r}/$E$8)*100')
        
    ws_atp['E63'] = '=SUM(E55:E62)'
    ws_atp['F63'] = '=SUM(E63/$E$8)*100'
    ws_atp['G63'] = '=SUM(G55:G62)'
    ws_atp['H63'] = '=SUM(G63/$E$8)*100'
    
    # -------------------------------------------------------------
    # 2. PESTAÑA: No_ATP_(+0,5)
    # -------------------------------------------------------------
    ws_no = wb['No_ATP_(+0,5)']
    
    # Tabla 1: Marco general (Filas 3-6)
    ws_no['E4'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "<>OTRA", Hoja1!$C$2:$C$12651, "<>", Hoja1!$M$2:$M$12651, "hombre")'
    ws_no['E5'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "<>OTRA", Hoja1!$C$2:$C$12651, "<>", Hoja1!$M$2:$M$12651, "mujer")'
    ws_no['E6'] = '=SUM(E4:E5)'
    ws_no['F4'] = '=SUM(E4/E6)*100'
    ws_no['F5'] = '=SUM(E5/E6)*100'
    ws_no['F6'] = '=SUM(E6/E6)*100'
    ws_no['G4'] = '=ATP!E6'
    ws_no['G5'] = '=ATP!E7'
    ws_no['G6'] = '=SUM(G4:G5)'
    ws_no['H4'] = '=SUM(G4/$E$6)*100'
    ws_no['H5'] = '=SUM(G5/$E$6)*100'
    ws_no['H6'] = '=SUM(G6/$E$6)*100'
    
    # Tabla 2: Autoconsumo vs Fines de Mercado (Filas 9-12)
    ws_no['D10'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "AUTOCONSUMO", Hoja1!$M$2:$M$12651, "hombre")'
    ws_no['E10'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre")'
    ws_no['F10'] = '=SUM(D10/$E$6)*100'
    ws_no['G10'] = '=SUM(E10/$E$6)*100'
    
    ws_no['D11'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "AUTOCONSUMO", Hoja1!$M$2:$M$12651, "mujer")'
    ws_no['E11'] = '=COUNTIFS(Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer")'
    ws_no['F11'] = '=SUM(D11/$E$6)*100'
    ws_no['G11'] = '=SUM(E11/$E$6)*100'
    
    ws_no['D12'] = '=SUM(D10:D11)'
    ws_no['E12'] = '=SUM(E10:E11)'
    ws_no['F12'] = '=SUM(D12/$E$6)*100'
    ws_no['G12'] = '=SUM(E12/$E$6)*100'
    
    # Tabla 3: No ATP + F.M (UTAS >= 0.5) (Filas 15-16)
    # NOTA: Usamos ">="&0.5 para que Excel lo evalúe perfectamente con comas (0,5) o puntos (0.5) según el idioma
    ws_no['D16'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5)'
    ws_no['E16'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5)'
    ws_no['F16'] = '=SUM(D16:E16)'
    
    # Tabla 4: Edad No ATP (UTAS >= 0.5) (Filas 19-26)
    # 20: 18-40
    ws_no['D20'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">=18", Hoja1!$L$2:$L$12651, "<=40")'
    ws_no['E20'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">=18", Hoja1!$L$2:$L$12651, "<=40")'
    ws_no['F20'] = '=SUM(D20/$D$23)*100'
    ws_no['G20'] = '=SUM(E20/$E$23)*100'
    
    # 21: 41-65
    ws_no['D21'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">=41", Hoja1!$L$2:$L$12651, "<=65")'
    ws_no['E21'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">=41", Hoja1!$L$2:$L$12651, "<=65")'
    ws_no['F21'] = '=SUM(D21/$D$23)*100'
    ws_no['G21'] = '=SUM(E21/$E$23)*100'
    
    # 22: Mayor de 65
    ws_no['D22'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">65")'
    ws_no['E22'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$L$2:$L$12651, ">65")'
    ws_no['F22'] = '=SUM(D22/$D$23)*100'
    ws_no['G22'] = '=SUM(E22/$E$23)*100'
    
    # 23: Total
    ws_no['D23'] = '=SUM(D20:D22)'
    ws_no['E23'] = '=SUM(E20:E22)'
    ws_no['F23'] = '=SUM(D23/$D$23)*100'
    ws_no['G23'] = '=SUM(E23/$E$23)*100'
    
    # 26: Edad media
    ws_no['D26'] = '=ROUND(AVERAGEIFS(Hoja1!$L$2:$L$12651, Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5), 0)'
    ws_no['E26'] = '=ROUND(AVERAGEIFS(Hoja1!$L$2:$L$12651, Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5), 0)'
    
    # Tabla 5: Subsectores No ATP (UTAS >= 0.5) (Filas 29-48)
    no_atp_subsectors = [
        (30, 'EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN CRIA Y CARNE'),
        (31, 'EXPLOTACIONES DE OVINOS ESPECIALIZADAS'),
        (32, 'EXPLOTACIONES NO CLASIFICADAS'),
        (33, 'EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS AL AIRE LIBRE'),
        (34, 'EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS EN INVERNADERO'),
        (35, 'EXPLOTACIONES FRUTÍCOLAS ESPECIALIZADAS'),
        (36, 'EXPLOTACIONES ESPECIALIZADAS EN VITICULTURA'),
        (37, 'EXPLOTACIONES DE HERBÍVOROS'),
        (38, 'EXPLOTACIONES DE CAPRINOS ESPECIALIZADAS'),
        (39, 'EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN LECHE'),
        (40, 'EXPLOTACIONES DE AVES PONEDORAS ESPECIALIZADAS'),
        (41, 'EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES EN INVERNADERO'),
        (42, 'EXPLOTACIONES APÍCOLAS'),
        (43, 'EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES AL AIRE LIBRE'),
        (44, 'EXPLOTACIONES QUE COMBINAN LA CRÍA Y ENGORDE DE PORCINOS'),
        (45, 'EXPLOTACIONES ESPECIALIZADAS EN CEREALICULTURA (DISTINTA DE LA DE ARROZ), EN CULTIVO DE PLANTAS OLEAGINOSAS Y PROTEAGINOSAS'),
        (46, 'EXPLOTACIONES ESPECIALIZADAS EN CULTIVO DE SETAS'),
        (47, 'EXPLOTACIONES DE AVES DE CORRAL DE CARNE ESPECIALIZADAS')
    ]
    
    for r, sub_name in no_atp_subsectors:
        ws_no.cell(r, 4, sub_name)
        ws_no.cell(r, 5, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$I$2:$I$12651, D{r})')
        ws_no.cell(r, 6, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$I$2:$I$12651, D{r})')
        ws_no.cell(r, 7, f'=SUM(E{r}/$E$48)*100')
        ws_no.cell(r, 8, f'=SUM(F{r}/$F$48)*100')
        ws_no.cell(r, 16, f'=E{r}')
        ws_no.cell(r, 17, f'=F{r}')
        ws_no.cell(r, 18, f'=SUM(P{r}:Q{r})')
        ws_no.cell(r, 19, f'=IF(R{r}>0, SUM(P{r}/R{r})*100, 0)')
        ws_no.cell(r, 20, f'=IF(R{r}>0, SUM(Q{r}/R{r})*100, 0)')
        
    ws_no['E48'] = '=SUM(E30:E47)'
    ws_no['F48'] = '=SUM(F30:F47)'
    ws_no['G48'] = '=SUM(E48/$E$48)*100'
    ws_no['H48'] = '=SUM(F48/$F$48)*100'
    ws_no['P48'] = '=SUM(P30:P47)'
    ws_no['Q48'] = '=SUM(Q30:Q47)'
    ws_no['R48'] = '=SUM(P48:Q48)'
    ws_no['S48'] = '=SUM(P48/R48)*100'
    ws_no['T48'] = '=SUM(Q48/R48)*100'
    
    # Tabla 6: Superficie No ATP (UTAS >= 0.5) (Filas 56-61)
    # 57: Muy pequeña: < 5 ha
    ws_no['E57'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, "<5")'
    ws_no['F57'] = '=SUM(E57/$E$61)*100'
    ws_no['G57'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, "<5")'
    ws_no['H57'] = '=SUM(G57/$G$61)*100'
    
    # 58: Pequeña: 5-20 ha
    ws_no['E58'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">=5", Hoja1!$O$2:$O$12651, "<=20")'
    ws_no['F58'] = '=SUM(E58/$E$61)*100'
    ws_no['G58'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">=5", Hoja1!$O$2:$O$12651, "<=20")'
    ws_no['H58'] = '=SUM(G58/$G$61)*100'
    
    # 59: Mediana: 20-50 ha
    ws_no['E59'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">20", Hoja1!$O$2:$O$12651, "<=50")'
    ws_no['F59'] = '=SUM(E59/$E$61)*100'
    ws_no['G59'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">20", Hoja1!$O$2:$O$12651, "<=50")'
    ws_no['H59'] = '=SUM(G59/$G$61)*100'
    
    # 60: Grande: > 50 ha
    ws_no['E60'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">50")'
    ws_no['F60'] = '=SUM(E60/$E$61)*100'
    ws_no['G60'] = '=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$O$2:$O$12651, ">50")'
    ws_no['H60'] = '=SUM(G60/$G$61)*100'
    
    # 61: Total
    ws_no['E61'] = '=SUM(E57:E60)'
    ws_no['F61'] = '=SUM(E61/$E$61)*100'
    ws_no['G61'] = '=SUM(G57:G60)'
    ws_no['H61'] = '=SUM(G61/$G$61)*100'
    
    # Tabla 7: Comarca No ATP (UTAS >= 0.5) (Filas 65-72)
    comarcas_table_no = [
        (66, 'Jata Ondo', 'JATAONDO'),
        (67, 'Enkarterrialde', 'ENKARTERRIALDE'),
        (68, 'Gorbeialde', 'GORBEIALDE'),
        (69, 'Urremendi', 'URREMENDI'),
        (70, 'Lea-Artibai', 'LEA ARTIBAI'),
        (71, 'Urkiola', 'URKIOLA')
    ]
    for r, name_lbl, adr_val in comarcas_table_no:
        ws_no.cell(r, 4, name_lbl)
        ws_no.cell(r, 5, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "hombre", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$S$2:$S$12651, "{adr_val}")')
        ws_no.cell(r, 6, f'=SUM(E{r}/$E$72)*100')
        ws_no.cell(r, 7, f'=COUNTIFS(Hoja1!$P$2:$P$12651, "Ez/No", Hoja1!$C$2:$C$12651, "FINES DE MERCADO", Hoja1!$M$2:$M$12651, "mujer", Hoja1!$R$2:$R$12651, ">="&0.5, Hoja1!$S$2:$S$12651, "{adr_val}")')
        ws_no.cell(r, 8, f'=SUM(G{r}/$G$72)*100')
        ws_no.cell(r, 11, f'=E{r}')
        ws_no.cell(r, 12, f'=G{r}')
        ws_no.cell(r, 13, f'=SUM(K{r}:L{r})')
        ws_no.cell(r, 14, f'=SUM(K{r}/M{r})*100')
        ws_no.cell(r, 15, f'=SUM(L{r}/M{r})*100')
        
    ws_no['E72'] = '=SUM(E66:E71)'
    ws_no['F72'] = '=SUM(E72/$E$72)*100'
    ws_no['G72'] = '=SUM(G66:G71)'
    ws_no['H72'] = '=SUM(G72/$G$72)*100'
    ws_no['K72'] = '=SUM(K66:K71)'
    ws_no['L72'] = '=SUM(L66:L71)'
    ws_no['M72'] = '=SUM(M66:M71)'
    ws_no['N72'] = '=SUM(K72/M72)*100'
    ws_no['O72'] = '=SUM(L72/M72)*100'
    
    wb.save(output_path)
    print(f"Successfully applied all formulas and saved to {output_path}")

if __name__ == '__main__':
    apply_formulas('new/30septmujeres.backup.xlsx', 'new/30septmujeres.xlsx')
