
    // DATOS EXTRAÍDOS CON EXACTITUD MATEMÁTICA DEL EXCEL OFICIAL
    const DATA_EXCEL = {
      "No_ATP": {
        "marco_general": {
          "total_explotaciones": 12120,
          "hombres_total": 8458,
          "hombres_pct": 69.79,
          "mujeres_total": 3662,
          "mujeres_pct": 30.21,
          "autoconsumo": {
            "total": 8798,
            "hombres": 6330,
            "mujeres": 2468,
            "pct_h": 52.23,
            "pct_m": 20.36
          },
          "fines_mercado": {
            "total": 3322,
            "hombres": 2128,
            "mujeres": 1194,
            "pct_h": 17.56,
            "pct_m": 9.85
          },
          "no_atp_mercado": {
            "total": 2793,
            "hombres": 1789,
            "mujeres": 1004
          }
        },
        "edad": {
          "edad_media": {
            "hombres": 60,
            "mujeres": 66
          },
          "tramos": [
            {"tramo": "18-40", "h": 185, "m": 52, "h_pct": 6.62, "m_pct": 1.86, "m_pct_sobre_m": 5.18},
            {"tramo": "41-65", "h": 945, "m": 425, "h_pct": 33.83, "m_pct": 15.22, "m_pct_sobre_m": 42.33},
            {"tramo": "Mayor de 65", "h": 659, "m": 527, "h_pct": 23.59, "m_pct": 18.87, "m_pct_sobre_m": 52.49}
          ]
        },
        "subsectores": [
          {"nombre": "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN CRIA Y CARNE", "h": 786, "m": 448, "pct_m_de_1004": 44.62},
          {"nombre": "EXPLOTACIONES DE OVINOS ESPECIALIZADAS", "h": 216, "m": 122, "pct_m_de_1004": 12.15},
          {"nombre": "EXPLOTACIONES NO CLASIFICADAS", "h": 178, "m": 104, "pct_m_de_1004": 10.36},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS AL AIRE LIBRE", "h": 106, "m": 78, "pct_m_de_1004": 7.77},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS EN INVERNADERO", "h": 83, "m": 60, "pct_m_de_1004": 5.98},
          {"nombre": "EXPLOTACIONES FRUTÍCOLAS ESPECIALIZADAS", "h": 115, "m": 58, "pct_m_de_1004": 5.78},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN VITICULTURA", "h": 105, "m": 36, "pct_m_de_1004": 3.59},
          {"nombre": "EXPLOTACIONES DE HERBÍVOROS", "h": 68, "m": 33, "pct_m_de_1004": 3.29},
          {"nombre": "EXPLOTACIONES DE CAPRINOS ESPECIALIZADAS", "h": 36, "m": 22, "pct_m_de_1004": 2.19},
          {"nombre": "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN LECHE", "h": 17, "m": 10, "pct_m_de_1004": 1.0},
          {"nombre": "EXPLOTACIONES DE AVES PONEDORAS ESPECIALIZADAS", "h": 23, "m": 8, "pct_m_de_1004": 0.8},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES EN INVERNADERO", "h": 8, "m": 7, "pct_m_de_1004": 0.7},
          {"nombre": "EXPOTACIONES APÍCOLAS", "h": 25, "m": 7, "pct_m_de_1004": 0.7},
          {"nombre": "FLORICULTURA Y PLANTAS ORNAMENTALES AL AIRE LIBRE", "h": 6, "m": 4, "pct_m_de_1004": 0.4},
          {"nombre": "EXPLOTACIONES QUE COMBINAN LA CRÍA Y ENGORDE DE PORCINOS", "h": 6, "m": 3, "pct_m_de_1004": 0.3},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN CEREALICULTURA (DISTINTA DE LA DE ARROZ), EN CULTIVO DE PLANTAS OLEAGINOSAS Y PROTEAGINOSAS", "h": 5, "m": 2, "pct_m_de_1004": 0.2},
          {"nombre": "CULTIVO DE SETAS", "h": 3, "m": 2, "pct_m_de_1004": 0.2},
          {"nombre": "EXPLOTACIONES DE AVES DE CORRAL DE CARNE ESPECIALIZADAS", "h": 3, "m": 0, "pct_m_de_1004": 0.0}
        ],
        "superficie": [
          {"estrato": "Muy pequeña: 0,5 - 5 ha", "h": 1238, "m": 749, "pct_m_de_1004": 74.6},
          {"estrato": "Pequeña: 5–20 ha", "h": 408, "m": 199, "pct_m_de_1004": 19.82},
          {"estrato": "Mediana: 20–50 ha", "h": 116, "m": 50, "pct_m_de_1004": 4.98},
          {"estrato": "Grande: > 50 ha", "h": 28, "m": 6, "pct_m_de_1004": 0.6}
        ],
        "ecologico": [
          {"tipo": "Certificado ecológico", "h": 38, "m": 13, "pct_m_de_1004": 1.29},
          {"tipo": "Una parte de la explotación", "h": 2, "m": 2, "pct_m_de_1004": 0.2},
          {"tipo": "En proceso de certificación", "h": 5, "m": 3, "pct_m_de_1004": 0.3}
        ],
        "comarca": [
          {"comarca": "Jata Ondo", "h": 449, "m": 261, "pct_m_de_1004": 26.0},
          {"comarca": "Enkarterrialde", "h": 450, "m": 209, "pct_m_de_1004": 20.82},
          {"comarca": "Gorbeialde", "h": 285, "m": 146, "pct_m_de_1004": 14.54},
          {"comarca": "Urremendi", "h": 216, "m": 146, "pct_m_de_1004": 14.54},
          {"comarca": "Lea-Artibai", "h": 184, "m": 129, "pct_m_de_1004": 12.85},
          {"comarca": "Urkiola", "h": 206, "m": 113, "pct_m_de_1004": 11.25}
        ],
        "forma_juridica": [
          {"forma": "Persona física", "h": 1680, "m": 956, "pct_m_de_1004": 95.22},
          {"forma": "Comunidad de bienes", "h": 17, "m": 8, "pct_m_de_1004": 0.8},
          {"forma": "Sociedad civil", "h": 10, "m": 8, "pct_m_de_1004": 0.8},
          {"forma": "Sociedad limitada", "h": 66, "m": 22, "pct_m_de_1004": 2.19},
          {"forma": "Titularidad compartida", "h": 1, "m": 0, "pct_m_de_1004": 0.0},
          {"forma": "Cooperativa", "h": 11, "m": 1, "pct_m_de_1004": 0.1},
          {"forma": "Asociaciones", "h": 3, "m": 2, "pct_m_de_1004": 0.2},
          {"forma": "Otros", "h": 1, "m": 6, "pct_m_de_1004": 0.6},
          {"forma": "Sociedad anónima", "h": 1, "m": 0, "pct_m_de_1004": 0.0},
          {"forma": "Sociedad agraria de transformación", "h": 0, "m": 1, "pct_m_de_1004": 0.1}
        ]
      },
      "ATP": {
        "marco_general": {
          "total_atp": 529,
          "hombres": 339,
          "hombres_pct": 64.08,
          "mujeres": 190,
          "mujeres_pct": 35.92,
          "pct_atp_sobre_fines_mercado": 15.92
        },
        "edad": {
          "edad_media_m": 53,
          "tramos": [
            {"tramo": "18-40", "h": 80, "m": 33, "m_pct_sobre_m": 17.37},
            {"tramo": "41-65", "h": 227, "m": 131, "m_pct_sobre_m": 68.95},
            {"tramo": "Mayor de 65", "h": 23, "m": 26, "m_pct_sobre_m": 13.68}
          ]
        },
        "subsectores": [
          {"nombre": "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN CRIA Y CARNE", "h": 113, "m": 83, "pct_m_de_190": 43.68},
          {"nombre": "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN LECHE", "h": 47, "m": 25, "pct_m_de_190": 13.16},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS EN INVERNADERO", "h": 64, "m": 17, "pct_m_de_190": 8.95},
          {"nombre": "EXPLOTACIONES DE AVES PONEDORAS ESPECIALIZADAS", "h": 12, "m": 11, "pct_m_de_190": 5.79},
          {"nombre": "EXPLOTACIONES DE OVINOS ESPECIALIZADAS", "h": 24, "m": 9, "pct_m_de_190": 4.74},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS AL AIRE LIBRE", "h": 17, "m": 9, "pct_m_de_190": 4.74},
          {"nombre": "EXPLOTACIONES FRUTÍCOLAS ESPECIALIZADAS", "h": 9, "m": 9, "pct_m_de_190": 4.74},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN VITICULTURA", "h": 14, "m": 7, "pct_m_de_190": 3.68},
          {"nombre": "EXPLOTACIONES NO CLASIFICADAS", "h": 10, "m": 5, "pct_m_de_190": 2.63},
          {"nombre": "EXPLOTACIONES DE CAPRINOS ESPECIALIZADAS", "h": 2, "m": 5, "pct_m_de_190": 2.63},
          {"nombre": "EXPLOTACIONES DE AVES DE CORRAL DE CARNE ESPECIALIZADAS", "h": 6, "m": 3, "pct_m_de_190": 1.58},
          {"nombre": "EXPLOTACIONES DE HERBÍVOROS", "h": 5, "m": 3, "pct_m_de_190": 1.58},
          {"nombre": "EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES EN INVERNADERO", "h": 10, "m": 3, "pct_m_de_190": 1.58},
          {"nombre": "EXPLOTACIONES QUE COMBINAN LA CRÍA Y ENGORDE DE PORCINOS", "h": 1, "m": 1, "pct_m_de_190": 0.53},
          {"nombre": "EXPLOTACIONES APÍCOLAS", "h": 5, "m": 0, "pct_m_de_190": 0.0}
        ],
        "superficie": [
          {"estrato": "Muy pequeña: 0,5 - 5 ha", "h": 113, "m": 61, "pct_m_de_190": 32.11},
          {"estrato": "Pequeña: 5–20 ha", "h": 59, "m": 52, "pct_m_de_190": 27.37},
          {"estrato": "Mediana: 20–50 ha", "h": 85, "m": 50, "pct_m_de_190": 26.32},
          {"estrato": "Grande: > 50 ha", "h": 82, "m": 27, "pct_m_de_190": 14.21}
        ],
        "ecologico": [
          {"tipo": "Certificado ecológico", "h": 24, "m": 17, "pct_m_de_190": 8.95},
          {"tipo": "Una parte de la explotación", "h": 4, "m": 4, "pct_m_de_190": 2.11},
          {"tipo": "En proceso de certificación", "h": 4, "m": 1, "pct_m_de_190": 0.53}
        ],
        "comarca": [
          {"comarca": "Enkarterrialde", "h": 107, "m": 78, "pct_m_de_190": 41.05},
          {"comarca": "Jata Ondo", "h": 87, "m": 31, "pct_m_de_190": 16.32},
          {"comarca": "Gorbeialde", "h": 51, "m": 29, "pct_m_de_190": 15.26},
          {"comarca": "Urkiola", "h": 42, "m": 19, "pct_m_de_190": 10.0},
          {"comarca": "Urremendi", "h": 27, "m": 20, "pct_m_de_190": 10.53},
          {"comarca": "Lea-Artibai", "h": 25, "m": 13, "pct_m_de_190": 6.84}
        ],
        "forma_juridica": [
          {"forma": "Persona física", "h": 255, "m": 152, "pct_m_de_190": 80.0},
          {"forma": "Comunidad de bienes", "h": 42, "m": 18, "pct_m_de_190": 9.47},
          {"forma": "Sociedad civil", "h": 19, "m": 12, "pct_m_de_190": 6.32},
          {"forma": "Titularidad compartida", "h": 4, "m": 3, "pct_m_de_190": 1.58},
          {"forma": "Sociedad limitada", "h": 14, "m": 3, "pct_m_de_190": 1.58},
          {"forma": "Asociaciones", "h": 1, "m": 0, "pct_m_de_190": 0.0},
          {"forma": "Sociedad agraria de transformación", "h": 1, "m": 0, "pct_m_de_190": 0.0},
          {"forma": "Cooperativa", "h": 3, "m": 2, "pct_m_de_190": 1.05}
        ]
      }
    };

    const I18N = {
      "es": {
        "govBrand": "BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA",
        "printBtn": "Imprimir Informe",
        "heroBadge": "INFORME FORAL · OBSERVATORIO AGRARIO Y PERSPECTIVA DE GÉNERO · ELABORADO POR AMATERRA",
        "heroTitle": "Situación de las Mujeres en el Sector Agrario de Bizkaia",
        "heroSubtitle": "Análisis estructural diferenciado y segmentado entre las <strong>Mujeres Profesionales a Título Principal (ATP)</strong> y el colectivo de explotaciones comerciales <strong>No ATP</strong>, basado en los registros oficiales de altas forales de Bizkaia.",
        "kpi1Lbl": "Censo Total Bizkaia",
        "kpi1Desc": "3.662 Mujeres (30,2%) | 8.458 Hombres",
        "kpi2Lbl": "Fines de Mercado",
        "kpi2Desc": "1.194 Mujeres (35,9%) | 2.128 Hombres",
        "kpi3Lbl": "Universo ATP (Profesional)",
        "kpi3Val": "190 Mujeres",
        "kpi3Desc": "35,9% de los 529 ATPs de Bizkaia",
        "kpi4Lbl": "Universo NO ATP (Mercado)",
        "kpi4Val": "1.004 Mujeres",
        "kpi4Desc": "35,9% de los 2.793 No ATPs comerciales",
        "viewDual": "Comparativa Dual (Lado a Lado)",
        "viewAtp": "Solo ATP (190 mujeres)",
        "viewNoatp": "Solo NO ATP (1.004 mujeres)",
        "navChip1": "1. Subsectores",
        "navChip2": "2. Superficie",
        "navChip3": "3. Ecológico",
        "navChip4": "4. Comarcas",
        "navChip5": "5. Forma Jurídica",
        "navChip6": "6. Edad y Relevo",
        "badgeAtpPill": "ATP: 190 Mujeres",
        "badgeNoatpPill": "NO ATP: 1.004 Mujeres",
        "sec1Tag": "INDICADOR ESTRUCTURAL 1",
        "sec1Title": "Distribución por Subsectores Productivos",
        "sec1Desc": "Comparativa del <strong>% del total de mujeres por subsectores</strong>. Contraste de especializaciones productivas entre el segmento profesional ATP (190 mujeres) y el segmento No ATP (1.004 mujeres).",
        "sec1ChartTitle": "Comparativa Directa de Especialización Productiva (% de Mujeres en cada colectivo)",
        "sec1ChartBadge": "Top 8 Subsectores",
        "sec1AtpCardTitle": "Subsectores en Mujeres Profesionales",
        "sec1AtpBase": "Base: 190 Mujeres ATP (100%)",
        "sec1AtpUnit": "en Bovinos Cría y Carne (83 mujeres)",
        "sec1AtpText": "En el sector ATP destaca además una fuerte presencia en <strong>bovinos de leche (13,2%)</strong> y <strong>hortalizas de invernadero (8,9%)</strong>, sectores de alta exigencia laboral e inversión tecnológica.",
        "sec1AtpBtn": "Mostrar tabla completa de 15 subsectores ATP",
        "sec1NoatpCardTitle": "Subsectores en Explotaciones Comerciales",
        "sec1NoatpBase": "Base: 1.004 Mujeres No ATP (100%)",
        "sec1NoatpUnit": "en Bovinos Cría y Carne (448 mujeres)",
        "sec1NoatpText": "En el colectivo No ATP, el segundo y tercer puesto corresponden al <strong>ovino tradicional (12,2%)</strong> y a explotaciones <strong>no clasificadas (10,4%)</strong>, mientras que el bovino de leche apenas alcanza el 1%.",
        "sec1NoatpBtn": "Mostrar tabla completa de 18 subsectores NO ATP",
        "sec1InsightTitle": "Conclusión Analítica: Diferenciación Productiva",
        "sec1InsightText": "Aunque el <strong>bovino de carne</strong> es el pilar en ambos grupos (~44%), el perfil ATP profesional muestra una presencia decisiva en <strong>bovinos de leche (13,2% vs 1,0%)</strong> y en <strong>invernadero hortícola (8,9% vs 6,0%)</strong>, actividades con altos requerimientos de capital, tecnología y dedicación plena. En contraste, el colectivo No ATP exhibe una fuerte concentración en <strong>ovino extensivo (12,2%)</strong> y huerta al aire libre no mecanizada (7,8%).",
        "sec2Tag": "INDICADOR ESTRUCTURAL 2",
        "sec2Title": "Dimensión y Superficie de las Explotaciones",
        "sec2Desc": "Distribución del <strong>% del total de mujeres por estratos de superficie</strong> (0,5-5 ha, 5-20 ha, 20-50 ha, >50 ha). Contraste estructural entre la viabilidad territorial del ATP y el minifundismo en el modelo No ATP.",
        "sec2ChartTitle": "Contraste Dimensional: % de Mujeres según Estrato de Hectáreas",
        "sec2ChartBadge": "4 Estratos Oficiales",
        "sec2AtpCardTitle": "Superficie en Mujeres Profesionales",
        "sec2AtpBase": "Base: 190 Mujeres ATP",
        "sec2AtpUnit": "supera las 5 hectáreas (129 mujeres)",
        "sec2AtpText": "Estructura equilibrada: el <strong>40,5%</strong> de las mujeres profesionales gestiona fincas medianas o grandes (>20 ha), con un 14,2% en explotaciones de más de 50 hectáreas.",
        "sec2NoatpCardTitle": "Superficie en Explotaciones Comerciales",
        "sec2NoatpBase": "Base: 1.004 Mujeres No ATP",
        "sec2NoatpUnit": "en minifundio < 5 hectáreas (749 mujeres)",
        "sec2NoatpText": "Extrema fragmentación: <strong>3 de cada 4 mujeres</strong> no alcanzan las 5 hectáreas, y solo un <strong>0,6%</strong> (6 mujeres en todo Bizkaia) tiene más de 50 ha.",
        "sec2InsightTitle": "Conclusión Analítica: La Brecha Territorial",
        "sec2InsightText": "La brecha de superficie es el principal condicionante de rentabilidad. Mientras que el <strong>74,6% de las mujeres No ATP se encuentran atrapadas en el minifundio (&lt;5 ha)</strong> con escasa capacidad de rotación y capitalización, el <strong>67,9% de las mujeres ATP disponen de bases territoriales viables (&gt;5 ha)</strong>, permitiendo el pastoreo intensivo y la rotación forrajera indispensable para la viabilidad económica.",
        "sec3Tag": "INDICADOR ESTRUCTURAL 3",
        "sec3Title": "Sostenibilidad y Producción Ecológica Oficial",
        "sec3Desc": "Análisis del <strong>% de ecológico del total de mujeres</strong> (certificado, parcial y en proceso de certificación). El impacto catalizador de la profesionalización sobre la transición verde.",
        "sec3BannerTag": "FACTOR MULTIPLICADOR CLAVE",
        "sec3BannerTitle": "La condición ATP multiplica por 6,5 la tasa de producción ecológica femenina",
        "sec3BannerDesc": "El <strong>11,6%</strong> de las mujeres ATP son ecológicas (22 de 190), frente a solo el <strong>1,8%</strong> en No ATP (18 de 1.004).",
        "sec3BannerKpiLbl": "Tasa Eco Femenina ATP",
        "sec3AtpCardTitle": "Producción Ecológica en ATP",
        "sec3AtpBase": "Base: 190 Mujeres ATP",
        "sec3AtpUnit": "con actividad ecológica (22 mujeres)",
        "sec3AtpText": "De las 22 mujeres ecológicas ATP: <strong>17 disponen de certificado oficial</strong> (8,95%), 4 certifican una parte (2,11%) y 1 está en proceso (0,53%).",
        "sec3AtpNote": "<strong>Liderazgo femenino en el sector eco ATP:</strong> Las 22 mujeres representan el <strong>40,7% de todas las explotaciones ecológicas profesionales</strong> de Bizkaia (54 en total: 32 hombres y 22 mujeres).",
        "sec3NoatpCardTitle": "Producción Ecológica en NO ATP",
        "sec3NoatpBase": "Base: 1.004 Mujeres No ATP",
        "sec3NoatpUnit": "con actividad ecológica (18 mujeres)",
        "sec3NoatpText": "De las 1.004 mujeres comerciales No ATP: solo <strong>13 cuentan con certificado oficial</strong> (1,29%), 2 en parte (0,20%) y 3 en proceso (0,30%).",
        "sec3NoatpNote": "<strong>Peso femenino en No ATP:</strong> Las 18 mujeres representan el <strong>28,6%</strong> de los 63 ecológicos No ATP comerciales (45 hombres y 18 mujeres).",
        "sec4Tag": "INDICADOR ESTRUCTURAL 4",
        "sec4Title": "Distribución Territorial por Comarcas (ADR)",
        "sec4Desc": "Análisis del <strong>% del total de mujeres por comarca</strong> en las 6 comarcas agrarias de Bizkaia. Revela una divergencia geográfica radical en la localización del talento profesional frente a las explotaciones no ATP.",
        "sec4ChartTitle": "Distribución Comarcal Comparativa: % de Mujeres en cada Comarca",
        "sec4ChartBadge": "6 Comarcas de Bizkaia",
        "sec4InsightTitle": "Conclusión Analítica: La Polaridad Geográfica",
        "sec4InsightText": "Existe una inversión territorial asombrosa: <strong>Enkarterrialde</strong> es el bastión indiscutible del modelo profesional femenino, aglutinando por sí sola el <strong>41,05% de todas las mujeres ATP de Bizkaia</strong> (78 mujeres), debido a su relieve y vocación ganadera extensiva. En cambio, en el colectivo No ATP comercial, la mayor concentración se traslada a <strong>Jata Ondo</strong> con el <strong>26,00%</strong> (261 mujeres), impulsada por la huerta de ribera y la proximidad metropolitana.",
        "sec5Tag": "INDICADOR ESTRUCTURAL 5",
        "sec5Title": "Condición Jurídica y Modelos de Titularidad",
        "sec5Desc": "Análisis del <strong>% de forma jurídica dentro del total de mujeres</strong>. Muestra cómo la profesionalización fomenta fórmulas asociativas compartidas frente al individualismo de la persona física.",
        "sec5AtpCardTitle": "Modelos Jurídicos en ATP",
        "sec5AtpBase": "Base: 190 Mujeres ATP",
        "sec5AtpUnit": "en fórmulas societarias y asociativas (38 mujeres)",
        "sec5AtpText": "El <strong>80,0%</strong> son personas físicas individuales, pero existe una presencia destacada de <strong>Comunidades de Bienes (9,47%)</strong>, <strong>Sociedades Civiles (6,32%)</strong> y <strong>Titularidad Compartida (1,58%)</strong>.",
        "sec5NoatpCardTitle": "Modelos Jurídicos en NO ATP",
        "sec5NoatpBase": "Base: 1.004 Mujeres No ATP",
        "sec5NoatpUnit": "persona física individual (956 mujeres)",
        "sec5NoatpText": "Hegemonía casi total de la persona física aislada. Las Comunidades de Bienes apenas representan el 0,80% y <strong>no hay ninguna explotación registrada bajo Titularidad Compartida (0,0%)</strong>.",
        "sec5InsightTitle": "Conclusión Analítica: Colectivización y Protección Laboral",
        "sec5InsightText": "La profesionalización actúa como un motor de estructuración jurídica. En el segmento ATP, <strong>1 de cada 5 mujeres (20%)</strong> opta por figuras como Comunidades de Bienes, Sociedades Civiles o Titularidad Compartida (Ley 35/2011), lo que reduce el riesgo financiero individual y asegura visibilidad en las cotizaciones a la Seguridad Social agraria. En el segmento No ATP, el 95,2% opera bajo persona física tradicional con nula penetración de la cotitularidad formal.",
        "sec6Tag": "INDICADOR ESTRUCTURAL 6",
        "sec6Title": "Pirámide de Edad y Alerta de Relevo Generacional",
        "sec6Desc": "Comparativa de la <strong>edad media</strong> y la distribución de las mujeres en los tramos oficiales: 18-40 años, 41-65 años y mayores de 65 años.",
        "sec6AtpCardTitle": "Demografía Femenina Profesional",
        "sec6AtpBase": "Edad Media: 53 años",
        "sec6AtpUnit": "edad media (frente a 66 en No ATP)",
        "sec6NoatpCardTitle": "Demografía Femenina Comercial",
        "sec6NoatpBase": "Edad Media: 66 años",
        "sec6NoatpUnit": "edad media (riesgo de cese)",
        "sec6InsightTitle": "Alerta Demográfica: Riesgo Inminente de Abandono",
        "sec6InsightText": "Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>más de la mitad de las mujeres (52,5% - 527 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,2%. Sin un plan de relevo tutelado, más de 500 explotaciones corren riesgo de cese en la presente década.",
        "footerTitle": "Diputación Foral de Bizkaia · Nekazaritza Saila",
        "footerSource": "Informe Técnico y Demográfico con perspectiva de género · Fuente oficial: Diputación Foral de Bizkaia.",
        "footerAmaterra": "Elaboración técnica, análisis y visualización desarrollados por Amaterra.",
        "thSubsector": "Subsector",
        "thHombres": "Hombres",
        "thMujeres": "Mujeres",
        "thPctMujeresAtp": "% Mujeres (de 190)",
        "thPctMujeresNoatp": "% Mujeres (de 1004)",
        "ageYoung": "Jóvenes (18 - 40 años)",
        "ageMid": "Madurez Productiva (41 - 65 años)",
        "ageOld": "Mayores de 65 años",
        "ageOldAlert": "⚠️ Mayores de 65 años (Jubilación)",
        "hombresPrefix": "Hombres",
        "mujeresPrefix": "Mujeres",
        "chartAtpSeries": "Mujeres ATP (% de 190)",
        "chartNoatpSeries": "Mujeres NO ATP (% de 1.004)"
      },
      "eu": {
        "govBrand": "BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA",
        "printBtn": "Txostena Inprimatu",
        "heroBadge": "FORU TXOSTENA · NEKAZARITZA BEHATOKIA ETA GENERO IKUSPEGIA · AMATERRAK EGINA",
        "heroTitle": "Emakumeen Egoera Bizkaiko Nekazaritza Sektorean",
        "heroSubtitle": "Egitura-azterketa bereizia <strong>Nekazari Profesionalen (ATP)</strong> eta merkataritza-helburuko <strong>Ez-ATP</strong> ustiategien artean, Bizkaiko foru erregistro ofizialetan oinarritua.",
        "kpi1Lbl": "Bizkaiko Errolda Guztira",
        "kpi1Desc": "3.662 Emakume (%30,2) | 8.458 Gizon",
        "kpi2Lbl": "Merkataritza Helburuak",
        "kpi2Desc": "1.194 Emakume (%35,9) | 2.128 Gizon",
        "kpi3Lbl": "ATP Unibertsoa (Profesionala)",
        "kpi3Val": "190 Emakume",
        "kpi3Desc": "Bizkaiko 529 ATPen %35,9",
        "kpi4Lbl": "EZ-ATP Unibertsoa (Merkatua)",
        "kpi4Val": "1.004 Emakume",
        "kpi4Desc": "2.793 Ez-ATP komertzialen %35,9",
        "viewDual": "Alderaketa Duala (Ondoan)",
        "viewAtp": "ATP Bakarrik (190 emakume)",
        "viewNoatp": "EZ-ATP Bakarrik (1.004 emakume)",
        "navChip1": "1. Azpisektoreak",
        "navChip2": "2. Azalera",
        "navChip3": "3. Ekologikoa",
        "navChip4": "4. Eskualdeak",
        "navChip5": "5. Forma Juridikoa",
        "navChip6": "6. Adina eta Erreleboa",
        "badgeAtpPill": "ATP: 190 Emakume",
        "badgeNoatpPill": "EZ-ATP: 1.004 Emakume",
        "sec1Tag": "EGITURA-ADIERAZLEA 1",
        "sec1Title": "Banaketa Ekoizpen Azpisektoreen Arabera",
        "sec1Desc": "<strong>Emakumeen guztizkoaren % azpisektoreka</strong> alderaketa. Ekoizpen-espezializazioen kontrastea ATP profesionalen (190 emakume) eta Ez-ATP segmentuaren (1.004 emakume) artean.",
        "sec1ChartTitle": "Ekoizpen-espezializazioaren alderaketa zuzena (% emakumeak talde bakoitzean)",
        "sec1ChartBadge": "Top 8 Azpisektoreak",
        "sec1AtpCardTitle": "Azpisektoreak Emakume Profesionaletan",
        "sec1AtpBase": "Oinarria: 190 Emakume ATP (%100)",
        "sec1AtpUnit": "Haragitarako Behian (83 emakume)",
        "sec1AtpText": "ATP sektorean, gainera, presentzia handia dute <strong>esnetarako behiak (%13,2)</strong> eta <strong>berotegiko baratzezaintzak (%8,9)</strong>, lan-eskakizun eta inbertsio teknologiko handiko sektoreak.",
        "sec1AtpBtn": "Erakutsi 15 ATP azpisektoreen taula osoa",
        "sec1NoatpCardTitle": "Azpisektoreak Merkataritza Ustiategietan",
        "sec1NoatpBase": "Oinarria: 1.004 Emakume Ez-ATP (%100)",
        "sec1NoatpUnit": "Haragitarako Behian (448 emakume)",
        "sec1NoatpText": "Ez-ATP taldean, bigarren eta hirugarren postuak <strong>ardi tradizionalari (%12,2)</strong> eta <strong>sailkatu gabeko ustiategiei (%10,4)</strong> dagozkie; esnetarako behiak, berriz, apenas iristen den %1era.",
        "sec1NoatpBtn": "Erakutsi 18 Ez-ATP azpisektoreen taula osoa",
        "sec1InsightTitle": "Ondorio Analitikoa: Ekoizpen-Bereizketa",
        "sec1InsightText": "Haragitarako behia bi taldeetan funtsezkoa den arren (~%44), ATP profil profesionalak presentzia erabakigarria du <strong>esnetarako behian (%13,2 vs %1,0)</strong> eta <strong>berotegiko baratzezaintzan (%8,9 vs %6,0)</strong>, kapital, teknologia eta dedikazio osoa eskatzen duten jarduerak. Aitzitik, Ez-ATP taldeak kontzentrazio handia du <strong>ardi estentsiboan (%12,2)</strong> eta aire zabaleko baratze ez-mekanizatuan (%7,8).",
        "sec2Tag": "EGITURA-ADIERAZLEA 2",
        "sec2Title": "Ustiategien Dimentsioa eta Azalera",
        "sec2Desc": "<strong>Emakumeen guztizkoaren % azalera-estratuen arabera</strong> (0,5-5 ha, 5-20 ha, 20-50 ha, >50 ha). ATPren lurralde-bideragarritasunaren eta Ez-ATP ereduaren lurzoru-zatikatzearen (minifundismoaren) arteko egitura-kontrastea.",
        "sec2ChartTitle": "Dimentsio-kontrastea: Emakumeen % hektarea-estratuaren arabera",
        "sec2ChartBadge": "4 Estratu Ofizialak",
        "sec2AtpCardTitle": "Azalera Emakume Profesionaletan",
        "sec2AtpBase": "Oinarria: 190 Emakume ATP",
        "sec2AtpUnit": "5 hektarea baino gehiago ditu (129 emakume)",
        "sec2AtpText": "Egitura orekatua: emakume profesionalen <strong>%40,5ek</strong> ustiategi ertain edo handiak (>20 ha) kudeatzen ditu, eta %14,2k 50 hektareatik gorako ustiategiak.",
        "sec2NoatpCardTitle": "Azalera Merkataritza Ustiategietan",
        "sec2NoatpBase": "Oinarria: 1.004 Emakume Ez-ATP",
        "sec2NoatpUnit": "5 hektarea baino gutxiagoko lursailetan (749 emakume)",
        "sec2NoatpText": "Muturreko zatikatzea: <strong>4 emakumetik 3k</strong> ez dute 5 hektarea lortzen, eta <strong>%0,6k</strong> baino ez (6 emakume Bizkaia osoan) ditu 50 ha baino gehiago.",
        "sec2InsightTitle": "Ondorio Analitikoa: Lurralde Arrakala",
        "sec2InsightText": "Azalera-arrakala da errentagarritasunaren baldintzatzaile nagusia. <strong>Ez-ATP emakumeen %74,6 lursail txikietan (&lt;5 ha) harrapatuta</strong> dagoen bitartean, txandakatze eta kapitalizazio ahalmen txikiarekin, <strong>ATP emakumeen %67,9k lur-oinarri bideragarriak (&gt;5 ha)</strong> ditu, bideragarritasun ekonomikorako ezinbestekoa den bazka-txandaketa eta artzaintza ahalbidetuz.",
        "sec3Tag": "EGITURA-ADIERAZLEA 3",
        "sec3Title": "Iraunkortasuna eta Ekoizpen Ekologiko Ofiziala",
        "sec3Desc": "<strong>Emakumeen guztizkoaren % ekologikoan</strong> azterketa (ziurtatua, zati bat eta trantsizioan). Profesionalizazioak trantsizio berdean duen eragin bideratzailea.",
        "sec3BannerTag": "FAKTORE BIDERKATZAILE NAGUSIA",
        "sec3BannerTitle": "ATP izaerak 6,5 aldiz biderkatzen du emakumeen ekoizpen ekologikoaren tasa",
        "sec3BannerDesc": "ATP emakumeen <strong>%11,6</strong> ekologikoak dira (190tik 22), Ez-ATP-ko <strong>%1,8aren</strong> aldean (1.004tik 18).",
        "sec3BannerKpiLbl": "ATP Emakumeen Eko Tasa",
        "sec3AtpCardTitle": "Ekoizpen Ekologikoa ATPn",
        "sec3AtpBase": "Oinarria: 190 Emakume ATP",
        "sec3AtpUnit": "jarduera ekologikoarekin (22 emakume)",
        "sec3AtpText": "ATPko 22 emakume ekologikoetatik: <strong>17k ziurtagiri ofiziala dute</strong> (%8,95), 4k zati bat (%2,11) eta 1 prozesuan dago (%0,53).",
        "sec3AtpNote": "<strong>Emakumeen lidergoa ATP eko sektorean:</strong> 22 emakume horiek Bizkaiko ustiategi ekologiko profesional guztien <strong>%40,7</strong> ordezkatzen dute (54 guztira: 32 gizon eta 22 emakume).",
        "sec3NoatpCardTitle": "Ekoizpen Ekologikoa EZ-ATPn",
        "sec3NoatpBase": "Oinarria: 1.004 Emakume Ez-ATP",
        "sec3NoatpUnit": "jarduera ekologikoarekin (18 emakume)",
        "sec3NoatpText": "Ez-ATPko 1.004 emakumeetatik: <strong>13k baino ez dute ziurtagiri ofiziala</strong> (%1,29), 2k zati batean (%0,20) eta 3k prozesuan (%0,30).",
        "sec3NoatpNote": "<strong>Emakumeen pisua Ez-ATPn:</strong> 18 emakume horiek 63 ustiategi ekologiko komertzialen <strong>%28,6</strong> dira (45 gizon eta 18 emakume).",
        "sec4Tag": "EGITURA-ADIERAZLEA 4",
        "sec4Title": "Lurralde Banaketa Eskualdeka (LGE)",
        "sec4Desc": "<strong>Emakumeen guztizkoaren % eskualdeka</strong> Bizkaiko 6 nekazaritza-eskualdeetan. Dibergentzia geografiko handia erakusten du talentu profesionalaren eta Ez-ATP ustiategien artean.",
        "sec4ChartTitle": "Eskualdeetako banaketa konparatua: Emakumeen % eskualde bakoitzean",
        "sec4ChartBadge": "Bizkaiko 6 Eskualdeak",
        "sec4InsightTitle": "Ondorio Analitikoa: Polaritate Geografikoa",
        "sec4InsightText": "Lurralde-alderantzikatze harrigarria dago: <strong>Enkarterrialde</strong> da emakume profesionalen gotorleku nagusia, Bizkaiko emakume ATP guztien <strong>%41,05</strong> biltzen baitu (78 emakume), bertako erliebe eta abeltzaintza-bokazioari esker. Aitzitik, Ez-ATP talde komertzialean kontzentraziorik handiena <strong>Jata Ondora</strong> lekualdatzen da (<strong>%26,00</strong>, 261 emakume), ibai-ertzeko baratzezaintzak eta hiri-hurbiltasunak bultzatuta.",
        "sec5Tag": "EGITURA-ADIERAZLEA 5",
        "sec5Title": "Egoera Juridikoa eta Titulartasun Ereduak",
        "sec5Desc": "<strong>Forma juridikoaren % emakumeen guztizkoaren barruan</strong> azterketa. Profesionalizazioak elkartze-formulak nola sustatzen dituen erakusten du pertsona fisikoaren indibidualismoaren aurrean.",
        "sec5AtpCardTitle": "Eredu Juridikoak ATPn",
        "sec5AtpBase": "Oinarria: 190 Emakume ATP",
        "sec5AtpUnit": "sozietate eta elkartze-formuletan (38 emakume)",
        "sec5AtpText": "<strong>%80,0</strong> pertsona fisiko indibidualak dira, baina presentzia nabarmena dute <strong>Ondasun-erkidegoek (%9,47)</strong>, <strong>Sozietate Zibilek (%6,32)</strong> eta <strong>Titulartasun Partekatuak (%1,58)</strong>.",
        "sec5NoatpCardTitle": "Eredu Juridikoak EZ-ATPn",
        "sec5NoatpBase": "Oinarria: 1.004 Emakume Ez-ATP",
        "sec5NoatpUnit": "pertsona fisiko indibiduala (956 emakume)",
        "sec5NoatpText": "Pertsona fisiko isolatuaren nagusitasun ia osoa. Ondasun-erkidegoek apenas ordezkatzen duten %0,80 eta <strong>ez dago Titulartasun Partekatuan erregistratutako ustiategirik (%0,0)</strong>.",
        "sec5InsightTitle": "Ondorio Analitikoa: Kolektibizazioa eta Lan Babesa",
        "sec5InsightText": "Profesionalizazioa egituraketa juridikoaren eragile da. ATP segmentuan, <strong>5 emakumetik 1ek (%20)</strong> Ondasun-erkidegoak, Sozietate Zibilak edo Titulartasun Partekatua (35/2011 Legea) bezalako formulak hautatzen ditu; horrek finantza-arriskua murrizten du eta nekazaritza-Gizarte Segurantzako kotizazioak bermatzen ditu. Ez-ATP segmentuan, %95,2 pertsona fisiko tradizionalaren pean aritzen da, kotitulartasun formalaren sartze nulua izanik.",
        "sec6Tag": "EGITURA-ADIERAZLEA 6",
        "sec6Title": "Adin Piramidea eta Belaunaldi Erreleboaren Alerta",
        "sec6Desc": "<strong>Batez besteko adinaren</strong> eta emakumeen banaketaren konparaketa tarte ofizialetan: 18-40 urte, 41-65 urte eta 65 urtetik gorakoak.",
        "sec6AtpCardTitle": "Emakume Profesionalen Demografia",
        "sec6AtpBase": "Batez Besteko Adina: 53 urte",
        "sec6AtpUnit": "batez besteko adina (Ez-ATP-ko 66 urteen aldean)",
        "sec6NoatpCardTitle": "Merkataritza Emakumeen Demografia",
        "sec6NoatpBase": "Batez Besteko Adina: 66 urte",
        "sec6NoatpUnit": "batez besteko adina (uzteko arriskua)",
        "sec6InsightTitle": "Alerta Demografikoa: Berehalako Uzte Arriskua",
        "sec6InsightText": "Belaunaldi-arrakala handia dago, <strong>13 urteko aldearekin batez besteko adinean</strong> (53 urte ATPn eta 66 urte Ez-ATPn). Ez-ATP taldean, <strong>emakumeen erdiak baino gehiagok (%52,5 - 527 titular) erretiratzeko adin ofiziala gainditzen du</strong>; 40 urtetik beherakoak, berriz, apenas dira %5,2. Errelebo-planik gabe, 500 ustiategi baino gehiago desagertzeko arriskuan daude hamarkada honetan.",
        "footerTitle": "Bizkaiko Foru Aldundia · Nekazaritza Saila",
        "footerSource": "Foru Txosten Tekniko eta Demografikoa genero ikuspegiarekin · Iturri ofiziala: Bizkaiko Foru Aldundia.",
        "footerAmaterra": "Elaborazio teknikoa, analisia eta bistaratzea Amaterrak garatua.",
        "thSubsector": "Azpisektorea",
        "thHombres": "Gizonak",
        "thMujeres": "Emakumeak",
        "thPctMujeresAtp": "% Emakumeak (190tik)",
        "thPctMujeresNoatp": "% Emakumeak (1004tik)",
        "ageYoung": "Gazteak (18 - 40 urte)",
        "ageMid": "Helduaro Produktiboa (41 - 65 urte)",
        "ageOld": "65 urtetik gorakoak",
        "ageOldAlert": "⚠️ 65 urtetik gorakoak (Erretiratzea)",
        "hombresPrefix": "Gizonak",
        "mujeresPrefix": "Emakumeak",
        "chartAtpSeries": "Emakumeak ATP (% 190tik)",
        "chartNoatpSeries": "Emakumeak EZ-ATP (% 1.004tik)"
      }
    };

    const LOOKUP_EU = {
      "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN CRIA Y CARNE": "Haragitarako behi-aziendaren ustiategi espezializatuak",
      "EXPLOTACIONES DE BOVINOS ESPECIALIZADAS: ORIENTACIÓN LECHE": "Esnetarako behi-aziendaren ustiategi espezializatuak",
      "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS EN INVERNADERO": "Berotegiko barazkietan espezializatutako ustiategiak",
      "EXPLOTACIONES DE AVES PONEDORAS ESPECIALIZADAS": "Hegazti erruleetan espezializatutako ustiategiak",
      "EXPLOTACIONES DE OVINOS ESPECIALIZADAS": "Ardi-aziendaren ustiategi espezializatuak",
      "EXPLOTACIONES ESPECIALIZADAS EN HORTALIZAS AL AIRE LIBRE": "Aire zabaleko barazkietan espezializatutako ustiategiak",
      "EXPLOTACIONES FRUTÍCOLAS ESPECIALIZADAS": "Frutazaintzako ustiategi espezializatuak",
      "EXPLOTACIONES ESPECIALIZADAS EN VITICULTURA": "Mahastizaintzako ustiategi espezializatuak",
      "EXPLOTACIONES NO CLASIFICADAS": "Sailkatu gabeko ustiategiak",
      "EXPLOTACIONES DE CAPRINOS ESPECIALIZADAS": "Ahuntz-aziendaren ustiategi espezializatuak",
      "EXPLOTACIONES DE AVES DE CORRAL DE CARNE ESPECIALIZADAS": "Haragitarako hegaztien ustiategi espezializatuak",
      "EXPLOTACIONES DE HERBÍVOROS": "Belarjaleen ustiategiak",
      "EXPLOTACIONES ESPECIALIZADAS EN FLORICULTURA Y PLANTAS ORNAMENTALES EN INVERNADERO": "Lorezaintza eta landare apaingarriak berotegian",
      "EXPLOTACIONES QUE COMBINAN LA CRÍA Y ENGORDE DE PORCINOS": "Txerriak hazi eta gizentzeko ustiategiak",
      "EXPLOTACIONES APÍCOLAS": "Erlezaintzako ustiategiak",
      "EXPOTACIONES APÍCOLAS": "Erlezaintzako ustiategiak",
      "FLORICULTURA Y PLANTAS ORNAMENTALES AL AIRE LIBRE": "Lorezaintza eta landare apaingarriak aire zabalean",
      "EXPLOTACIONES ESPECIALIZADAS EN CEREALICULTURA (DISTINTA DE LA DE ARROZ), EN CULTIVO DE PLANTAS OLEAGINOSAS Y PROTEAGINOSAS": "Zerealak, koipetsuak eta proteaginosak",
      "CULTIVO DE SETAS": "Onddo eta perretxikoen laborantza",
      "Muy pequeña: 0,5 - 5 ha": "Oso txikia: 0,5 - 5 ha",
      "Pequeña: 5–20 ha": "Txikia: 5–20 ha",
      "Mediana: 20–50 ha": "Ertaina: 20–50 ha",
      "Grande: > 50 ha": "Handia: > 50 ha",
      "Certificado ecológico": "Ziurtagiri ekologikoa",
      "Una parte de la explotación": "Ustiategiaren zati bat",
      "En proceso de certificación": "Ziurtatze-prozesuan",
      "Persona física": "Pertsona fisikoa",
      "Comunidad de bienes": "Ondasun-erkidegoa",
      "Sociedad civil": "Sozietate zibila",
      "Titularidad compartida": "Titulartasun partekatua",
      "Sociedad limitada": "Sozietate mugatua (SM)",
      "Cooperativa": "Kooperatiba",
      "Asociaciones": "Elkarteak",
      "Otros": "Beste batzuk",
      "Sociedad anónima": "Sozietate anonimoa (SA)",
      "Sociedad agraria de transformación": "Nekazaritzako Eraldaketa Sozietatea (NES)"
    };

    let CURRENT_LANG = 'es';
    let chartSubsectoresInstance = null;
    let chartSuperficieInstance = null;
    let chartComarcasInstance = null;

    // Global View Mode Controller
    function setViewMode(mode) {
      const body = document.body;
      body.classList.remove('mode-dual', 'mode-atp-only', 'mode-noatp-only');
      
      document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));

      if (mode === 'dual') {
        body.classList.add('mode-dual');
        document.getElementById('btn-view-dual').classList.add('active');
      } else if (mode === 'atp') {
        body.classList.add('mode-atp-only');
        document.getElementById('btn-view-atp').classList.add('active');
      } else if (mode === 'noatp') {
        body.classList.add('mode-noatp-only');
        document.getElementById('btn-view-noatp').classList.add('active');
      }

      window.dispatchEvent(new Event('resize'));
    }

    // Toggle Collapsible Tables
    function toggleExpand(elementId, btn) {
      const el = document.getElementById(elementId);
      const isEu = CURRENT_LANG === 'eu';
      if (el.style.display === 'none' || el.style.display === '') {
        el.style.display = 'block';
        btn.querySelector('span').textContent = isEu ? 'Ezkutatu taula xehatua' : 'Ocultar tabla detallada';
        btn.querySelector('svg').style.transform = 'rotate(180deg)';
      } else {
        el.style.display = 'none';
        btn.querySelector('span').textContent = isEu ? 'Erakutsi taula osoa' : 'Mostrar tabla completa';
        btn.querySelector('svg').style.transform = 'rotate(0deg)';
      }
    }

    // Comprehensive Bilingual Switcher
    function setLang(lang) {
      CURRENT_LANG = lang;
      document.documentElement.lang = lang;

      document.getElementById('btn-lang-es').classList.toggle('active', lang === 'es');
      document.getElementById('btn-lang-eu').classList.toggle('active', lang === 'eu');

      const t = I18N[lang] || I18N.es;

      // Top bar & Hero
      document.getElementById('txt-gov-brand').textContent = t.govBrand;
      document.getElementById('txt-print-btn').textContent = t.printBtn;
      document.getElementById('txt-hero-badge').textContent = t.heroBadge;
      document.getElementById('txt-hero-title').textContent = t.heroTitle;
      document.getElementById('txt-hero-subtitle').innerHTML = t.heroSubtitle;

      document.getElementById('txt-kpi1-lbl').textContent = t.kpi1Lbl;
      document.getElementById('txt-kpi1-desc').textContent = t.kpi1Desc;
      document.getElementById('txt-kpi2-lbl').textContent = t.kpi2Lbl;
      document.getElementById('txt-kpi2-desc').textContent = t.kpi2Desc;
      document.getElementById('txt-kpi3-lbl').textContent = t.kpi3Lbl;
      document.getElementById('txt-kpi3-val').textContent = t.kpi3Val;
      document.getElementById('txt-kpi3-desc').textContent = t.kpi3Desc;
      document.getElementById('txt-kpi4-lbl').textContent = t.kpi4Lbl;
      document.getElementById('txt-kpi4-val').textContent = t.kpi4Val;
      document.getElementById('txt-kpi4-desc').textContent = t.kpi4Desc;

      // Nav buttons
      document.getElementById('txt-view-dual').textContent = t.viewDual;
      document.getElementById('txt-view-atp').textContent = t.viewAtp;
      document.getElementById('txt-view-noatp').textContent = t.viewNoatp;

      document.getElementById('nav-chip-1').textContent = t.navChip1;
      document.getElementById('nav-chip-2').textContent = t.navChip2;
      document.getElementById('nav-chip-3').textContent = t.navChip3;
      document.getElementById('nav-chip-4').textContent = t.navChip4;
      if (document.getElementById('nav-chip-5')) document.getElementById('nav-chip-5').textContent = t.navChip6;

      for (let i = 1; i <= 6; i++) {
        const pAtp = document.getElementById('badge-atp-pill-' + i);
        const pNo = document.getElementById('badge-noatp-pill-' + i);
        if (pAtp) pAtp.textContent = t.badgeAtpPill;
        if (pNo) pNo.textContent = t.badgeNoatpPill;
      }

      // Bloque 1
      document.getElementById('txt-sec1-tag').textContent = t.sec1Tag;
      document.getElementById('txt-sec1-title').textContent = t.sec1Title;
      document.getElementById('txt-sec1-desc').innerHTML = t.sec1Desc;
      document.getElementById('txt-sec1-chart-title').textContent = t.sec1ChartTitle;
      document.getElementById('txt-sec1-chart-badge').textContent = t.sec1ChartBadge;
      document.getElementById('txt-sec1-atp-card-title').textContent = t.sec1AtpCardTitle;
      document.getElementById('txt-sec1-atp-base').textContent = t.sec1AtpBase;
      document.getElementById('txt-sec1-atp-unit').textContent = t.sec1AtpUnit;
      document.getElementById('txt-sec1-atp-text').innerHTML = t.sec1AtpText;
      document.getElementById('txt-sec1-atp-btn').textContent = t.sec1AtpBtn;
      document.getElementById('txt-sec1-noatp-card-title').textContent = t.sec1NoatpCardTitle;
      document.getElementById('txt-sec1-noatp-base').textContent = t.sec1NoatpBase;
      document.getElementById('txt-sec1-noatp-unit').textContent = t.sec1NoatpUnit;
      document.getElementById('txt-sec1-noatp-text').innerHTML = t.sec1NoatpText;
      document.getElementById('txt-sec1-noatp-btn').textContent = t.sec1NoatpBtn;
      document.getElementById('txt-sec1-insight-title').textContent = t.sec1InsightTitle;
      document.getElementById('txt-sec1-insight-text').innerHTML = t.sec1InsightText;

      document.getElementById('th-sub-atp-name').textContent = t.thSubsector;
      document.getElementById('th-sub-atp-h').textContent = t.thHombres;
      document.getElementById('th-sub-atp-m').textContent = t.thMujeres;
      document.getElementById('th-sub-atp-pct').textContent = t.thPctMujeresAtp;
      document.getElementById('th-sub-noatp-name').textContent = t.thSubsector;
      document.getElementById('th-sub-noatp-h').textContent = t.thHombres;
      document.getElementById('th-sub-noatp-m').textContent = t.thMujeres;
      document.getElementById('th-sub-noatp-pct').textContent = t.thPctMujeresNoatp;

      // Bloque 2
      document.getElementById('txt-sec2-tag').textContent = t.sec2Tag;
      document.getElementById('txt-sec2-title').textContent = t.sec2Title;
      document.getElementById('txt-sec2-desc').innerHTML = t.sec2Desc;
      document.getElementById('txt-sec2-chart-title').textContent = t.sec2ChartTitle;
      document.getElementById('txt-sec2-chart-badge').textContent = t.sec2ChartBadge;
      document.getElementById('txt-sec2-atp-card-title').textContent = t.sec2AtpCardTitle;
      document.getElementById('txt-sec2-atp-base').textContent = t.sec2AtpBase;
      document.getElementById('txt-sec2-atp-unit').textContent = t.sec2AtpUnit;
      document.getElementById('txt-sec2-atp-text').innerHTML = t.sec2AtpText;
      document.getElementById('txt-sec2-noatp-card-title').textContent = t.sec2NoatpCardTitle;
      document.getElementById('txt-sec2-noatp-base').textContent = t.sec2NoatpBase;
      document.getElementById('txt-sec2-noatp-unit').textContent = t.sec2NoatpUnit;
      document.getElementById('txt-sec2-noatp-text').innerHTML = t.sec2NoatpText;
      document.getElementById('txt-sec2-insight-title').textContent = t.sec2InsightTitle;
      document.getElementById('txt-sec2-insight-text').innerHTML = t.sec2InsightText;

      // Bloque 3
      document.getElementById('txt-sec3-tag').textContent = t.sec3Tag;
      document.getElementById('txt-sec3-title').textContent = t.sec3Title;
      document.getElementById('txt-sec3-desc').innerHTML = t.sec3Desc;
      document.getElementById('txt-sec3-banner-tag').textContent = t.sec3BannerTag;
      document.getElementById('txt-sec3-banner-title').textContent = t.sec3BannerTitle;
      document.getElementById('txt-sec3-banner-desc').innerHTML = t.sec3BannerDesc;
      document.getElementById('txt-sec3-banner-kpi-lbl').textContent = t.sec3BannerKpiLbl;
      document.getElementById('txt-sec3-atp-card-title').textContent = t.sec3AtpCardTitle;
      document.getElementById('txt-sec3-atp-base').textContent = t.sec3AtpBase;
      document.getElementById('txt-sec3-atp-unit').textContent = t.sec3AtpUnit;
      document.getElementById('txt-sec3-atp-text').innerHTML = t.sec3AtpText;
      document.getElementById('txt-sec3-atp-note').innerHTML = t.sec3AtpNote;
      if (document.getElementById('txt-sec3-noatp-card-title')) {
        document.getElementById('txt-sec3-noatp-card-title').textContent = t.sec3NoatpCardTitle;
        document.getElementById('txt-sec3-noatp-base').textContent = t.sec3NoatpBase;
        document.getElementById('txt-sec3-noatp-unit').textContent = t.sec3NoatpUnit;
        document.getElementById('txt-sec3-noatp-text').innerHTML = t.sec3NoatpText;
        document.getElementById('txt-sec3-noatp-note').innerHTML = t.sec3NoatpNote;
      }

      // Bloque 4
      document.getElementById('txt-sec4-tag').textContent = t.sec4Tag;
      document.getElementById('txt-sec4-title').textContent = t.sec4Title;
      document.getElementById('txt-sec4-desc').innerHTML = t.sec4Desc;
      document.getElementById('txt-sec4-chart-title').textContent = t.sec4ChartTitle;
      document.getElementById('txt-sec4-chart-badge').textContent = t.sec4ChartBadge;
      document.getElementById('txt-sec4-insight-title').textContent = t.sec4InsightTitle;
      document.getElementById('txt-sec4-insight-text').innerHTML = t.sec4InsightText;

      // Bloque 5 (Condición jurídica eliminada)
      // Bloque 6
      document.getElementById('txt-sec6-tag').textContent = t.sec6Tag;
      document.getElementById('txt-sec6-title').textContent = t.sec6Title;
      document.getElementById('txt-sec6-desc').innerHTML = t.sec6Desc;
      document.getElementById('txt-sec6-atp-card-title').textContent = t.sec6AtpCardTitle;
      document.getElementById('txt-sec6-atp-base').textContent = t.sec6AtpBase;
      document.getElementById('txt-sec6-atp-unit').textContent = t.sec6AtpUnit;
      document.getElementById('txt-sec6-noatp-card-title').textContent = t.sec6NoatpCardTitle;
      document.getElementById('txt-sec6-noatp-base').textContent = t.sec6NoatpBase;
      document.getElementById('txt-sec6-noatp-unit').textContent = t.sec6NoatpUnit;
      document.getElementById('txt-sec6-insight-title').textContent = t.sec6InsightTitle;
      document.getElementById('txt-sec6-insight-text').innerHTML = t.sec6InsightText;

      // Footer
      document.getElementById('txt-footer-title').textContent = t.footerTitle;
      document.getElementById('txt-footer-source').textContent = t.footerSource;
      document.getElementById('txt-footer-amaterra').textContent = t.footerAmaterra;
      document.getElementById('txt-footer-link-1').textContent = t.navChip1.replace(/^\d+\.\s*/, '');
      document.getElementById('txt-footer-link-2').textContent = t.navChip2.replace(/^\d+\.\s*/, '');
      document.getElementById('txt-footer-link-3').textContent = t.navChip3.replace(/^\d+\.\s*/, '');
      document.getElementById('txt-footer-link-4').textContent = t.navChip4.replace(/^\d+\.\s*/, '');
      if (document.getElementById('txt-footer-link-5')) document.getElementById('txt-footer-link-5').textContent = t.navChip6.replace(/^\d+\.\s*/, '');

      // Re-render dynamic lists with translated item labels
      renderSubsectores();
      renderSuperficie();
      renderEcologico();
      renderComarcas();
      // renderFormaJuridica();
      renderEdad();

      // Update Chart.js datasets & labels
      updateChartsLanguage();
    }

    function translateName(name) {
      if (CURRENT_LANG === 'eu' && LOOKUP_EU[name]) {
        return LOOKUP_EU[name];
      }
      return name;
    }

    // 1. RENDER SUBSECTORES
    function renderSubsectores() {
      const atpList = document.getElementById('list-subsectores-atp');
      const noatpList = document.getElementById('list-subsectores-noatp');
      const atpTbody = document.getElementById('tbody-subsectores-atp');
      const noatpTbody = document.getElementById('tbody-subsectores-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = '';
      noatpList.innerHTML = '';
      atpTbody.innerHTML = '';
      noatpTbody.innerHTML = '';

      const atpSorted = [...DATA_EXCEL.ATP.subsectores].sort((a,b) => b.pct_m_de_190 - a.pct_m_de_190);
      const noatpSorted = [...DATA_EXCEL.No_ATP.subsectores].sort((a,b) => b.pct_m_de_1004 - a.pct_m_de_1004);

      atpSorted.slice(0, 5).forEach(s => {
        atpList.innerHTML += `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${translateName(s.nombre)}</span>
              <span class="segment-item-pct atp-pct">${s.pct_m_de_190}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${s.m} ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix}: ${s.h} | ${t.mujeresPrefix}: ${s.m}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: ${s.pct_m_de_190}%;"></div></div>
          </div>
        `;
      });

      noatpSorted.slice(0, 5).forEach(s => {
        noatpList.innerHTML += `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${translateName(s.nombre)}</span>
              <span class="segment-item-pct noatp-pct">${s.pct_m_de_1004}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${s.m} ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix}: ${s.h} | ${t.mujeresPrefix}: ${s.m}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: ${s.pct_m_de_1004}%;"></div></div>
          </div>
        `;
      });

      atpSorted.forEach(s => {
        atpTbody.innerHTML += `
          <tr>
            <td>${translateName(s.nombre)}</td>
            <td class="num">${s.h}</td>
            <td class="num">${s.m}</td>
            <td class="num pct-cell" style="color:var(--atp-primary);">${s.pct_m_de_190}%</td>
          </tr>
        `;
      });

      noatpSorted.forEach(s => {
        noatpTbody.innerHTML += `
          <tr>
            <td>${translateName(s.nombre)}</td>
            <td class="num">${s.h}</td>
            <td class="num">${s.m}</td>
            <td class="num pct-cell" style="color:var(--noatp-primary);">${s.pct_m_de_1004}%</td>
          </tr>
        `;
      });
    }

    // 2. RENDER SUPERFICIE
    function renderSuperficie() {
      const atpList = document.getElementById('list-superficie-atp');
      const noatpList = document.getElementById('list-superficie-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = '';
      noatpList.innerHTML = '';

      DATA_EXCEL.ATP.superficie.forEach(s => {
        atpList.innerHTML += `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${translateName(s.estrato)}</span>
              <span class="segment-item-pct atp-pct">${s.pct_m_de_190}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${s.m} ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix}: ${s.h} | ${t.mujeresPrefix}: ${s.m}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: ${s.pct_m_de_190}%;"></div></div>
          </div>
        `;
      });

      DATA_EXCEL.No_ATP.superficie.forEach(s => {
        noatpList.innerHTML += `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${translateName(s.estrato)}</span>
              <span class="segment-item-pct noatp-pct">${s.pct_m_de_1004}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${s.m} ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix}: ${s.h} | ${t.mujeresPrefix}: ${s.m}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: ${s.pct_m_de_1004}%;"></div></div>
          </div>
        `;
      });
    }

    // 3. RENDER ECOLOGICO
    function renderEcologico() {
      const atpList = document.getElementById('list-ecologico-atp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      if (atpList) {
        atpList.innerHTML = '';
        DATA_EXCEL.ATP.ecologico.forEach(e => {
          atpList.innerHTML += `
            <div class="segment-item">
              <div class="segment-item-top">
                <span class="segment-item-name">${translateName(e.tipo)}</span>
                <span class="segment-item-pct atp-pct">${e.pct_m_de_190}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${e.m} ${mLabel})</span></span>
              </div>
              <div class="segment-item-sub">${t.hombresPrefix}: ${e.h} | ${t.mujeresPrefix}: ${e.m}</div>
              <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: ${e.pct_m_de_190 * 8}%;"></div></div>
            </div>
          `;
        });
      }
    }

    // 4. RENDER COMARCAS
    function renderComarcas() {
      const grid = document.getElementById('comarca-interactive-grid');
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';
      grid.innerHTML = '';
      
      const comarcas = DATA_EXCEL.ATP.comarca.map(cAtp => {
        const cNoatp = DATA_EXCEL.No_ATP.comarca.find(cn => cn.comarca.trim().toLowerCase() === cAtp.comarca.trim().toLowerCase()) || {};
        return {
          nombre: cAtp.comarca,
          atp_m: cAtp.m,
          atp_h: cAtp.h,
          atp_pct: cAtp.pct_m_de_190,
          noatp_m: cNoatp.m || 0,
          noatp_h: cNoatp.h || 0,
          noatp_pct: cNoatp.pct_m_de_1004 || 0
        };
      });

      comarcas.forEach(c => {
        grid.innerHTML += `
          <div class="comarca-card" onclick="highlightComarca(this, '${c.nombre}')">
            <div class="comarca-name">${c.nombre}</div>
            <div class="comarca-badge-row">
              <div class="comarca-mini-metric comarca-mini-atp">
                <span>ATP (190 ${mLabel}):</span>
                <span>${c.atp_pct}% (${c.atp_m})</span>
              </div>
              <div class="comarca-mini-metric comarca-mini-noatp">
                <span>EZ-ATP (1004 ${mLabel}):</span>
                <span>${c.noatp_pct}% (${c.noatp_m})</span>
              </div>
            </div>
          </div>
        `;
      });
    }

    function highlightComarca(el, name) {
      document.querySelectorAll('.comarca-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
    }

    // 5. RENDER FORMA JURIDICA
    function renderFormaJuridica() {
      const atpList = document.getElementById('list-juridica-atp');
      const noatpList = document.getElementById('list-juridica-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = '';
      noatpList.innerHTML = '';

      const atpSorted = [...DATA_EXCEL.ATP.forma_juridica].sort((a,b) => b.pct_m_de_190 - a.pct_m_de_190);
      const noatpSorted = [...DATA_EXCEL.No_ATP.forma_juridica].sort((a,b) => b.pct_m_de_1004 - a.pct_m_de_1004);

      atpSorted.forEach(j => {
        if (j.m > 0 || j.pct_m_de_190 > 0) {
          atpList.innerHTML += `
            <div class="segment-item">
              <div class="segment-item-top">
                <span class="segment-item-name">${translateName(j.forma)}</span>
                <span class="segment-item-pct atp-pct">${j.pct_m_de_190}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${j.m} ${mLabel})</span></span>
              </div>
              <div class="segment-item-sub">${t.hombresPrefix}: ${j.h} | ${t.mujeresPrefix}: ${j.m}</div>
              <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: ${j.pct_m_de_190}%;"></div></div>
            </div>
          `;
        }
      });

      noatpSorted.forEach(j => {
        if (j.m > 0 || j.pct_m_de_1004 > 0) {
          noatpList.innerHTML += `
            <div class="segment-item">
              <div class="segment-item-top">
                <span class="segment-item-name">${translateName(j.forma)}</span>
                <span class="segment-item-pct noatp-pct">${j.pct_m_de_1004}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${j.m} ${mLabel})</span></span>
              </div>
              <div class="segment-item-sub">${t.hombresPrefix}: ${j.h} | ${t.mujeresPrefix}: ${j.m}</div>
              <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: ${j.pct_m_de_1004}%;"></div></div>
            </div>
          `;
        }
      });
    }

    // 6. RENDER EDAD
    function renderEdad() {
      const atpList = document.getElementById('list-edad-atp');
      const noatpList = document.getElementById('list-edad-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct atp-pct">17,37% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(33 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 80 (%24,24)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 17.37%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct atp-pct">68,95% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(131 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 227 (%68,79)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 68.95%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageOld}</span>
            <span class="segment-item-pct atp-pct">13,68% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(26 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 23 (%6,97)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 13.68%;"></div></div>
        </div>
      `;

      noatpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct noatp-pct">5,18% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(52 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 185 (%10,34)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 5.18%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct noatp-pct">42,33% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(425 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 945 (%52,82)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 42.33%;"></div></div>
        </div>
        <div class="segment-item" style="border-color: #FECACA; background: #FEF2F2;">
          <div class="segment-item-top">
            <span class="segment-item-name" style="color: #991B1B;">${t.ageOldAlert}</span>
            <span class="segment-item-pct" style="color: #DC2626;">52,49% <span style="font-size:11px;font-weight:500;color:#991B1B;">(527 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 659 (%36,84)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 52.49%; background: #DC2626;"></div></div>
        </div>
      `;
    }

    // 7. CHART.JS INITIALIZATION & MULTILINGUAL UPDATE
    const chartLabelsEs = {
      subsectores: ['Bovinos Cría y Carne', 'Bovinos Leche', 'Hortalizas Invernadero', 'Aves Ponedoras', 'Ovinos', 'Hortalizas Aire Libre', 'Frutícolas', 'Viticultura'],
      superficie: ['Muy pequeña (0,5 - 5 ha)', 'Pequeña (5 - 20 ha)', 'Mediana (20 - 50 ha)', 'Grande (> 50 ha)']
    };

    const chartLabelsEu = {
      subsectores: ['Haragitarako Behiak', 'Esnetarako Behiak', 'Berotegiko Barazkiak', 'Hegazti Erruleak', 'Ardiak', 'Aire Zabaleko Barazkiak', 'Frutazaintza', 'Mahastizaintza'],
      superficie: ['Oso txikia (0,5 - 5 ha)', 'Txikia (5 - 20 ha)', 'Ertaina (20 - 50 ha)', 'Handia (> 50 ha)']
    };

    function initCharts() {
      Chart.defaults.font.family = "'Inter', sans-serif";
      Chart.defaults.color = '#475569';

      const t = I18N[CURRENT_LANG] || I18N.es;
      const atpSubValues = [43.68, 13.16, 8.95, 5.79, 4.74, 4.74, 4.74, 3.68];
      const noatpSubValues = [44.62, 1.00, 5.98, 0.80, 12.15, 7.77, 5.78, 3.59];

      chartSubsectoresInstance = new Chart(document.getElementById('chartSubsectoresComp'), {
        type: 'bar',
        data: {
          labels: CURRENT_LANG === 'eu' ? chartLabelsEu.subsectores : chartLabelsEs.subsectores,
          datasets: [
            {
              label: t.chartAtpSeries,
              data: atpSubValues,
              backgroundColor: '#047857',
              borderRadius: 6,
              borderSkipped: false
            },
            {
              label: t.chartNoatpSeries,
              data: noatpSubValues,
              backgroundColor: '#D97706',
              borderRadius: 6,
              borderSkipped: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: {
              position: 'top',
              labels: { font: { weight: 600, size: 12 } }
            },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}%`
              }
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: { callback: val => val + '%' },
              grid: { color: '#E2E8F0' }
            },
            y: {
              grid: { display: false },
              ticks: { font: { weight: 600, size: 11 } }
            }
          }
        }
      });

      // 2. Superficie
      const atpSup = DATA_EXCEL.ATP.superficie.map(s => s.pct_m_de_190);
      const noatpSup = DATA_EXCEL.No_ATP.superficie.map(s => s.pct_m_de_1004);

      chartSuperficieInstance = new Chart(document.getElementById('chartSuperficieComp'), {
        type: 'bar',
        data: {
          labels: CURRENT_LANG === 'eu' ? chartLabelsEu.superficie : chartLabelsEs.superficie,
          datasets: [
            {
              label: t.chartAtpSeries,
              data: atpSup,
              backgroundColor: '#047857',
              borderRadius: 6
            },
            {
              label: t.chartNoatpSeries,
              data: noatpSup,
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { font: { weight: 600 } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}%`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: val => val + '%' },
              grid: { color: '#E2E8F0' }
            },
            x: {
              grid: { display: false },
              ticks: { font: { weight: 600, size: 12 } }
            }
          }
        }
      });

      // 3. Comarcas
      const comarcaLabels = ['Enkarterrialde', 'Jata Ondo', 'Gorbeialde', 'Urremendi', 'Urkiola', 'Lea-Artibai'];
      const atpComarcaVals = [41.05, 16.32, 15.26, 10.53, 10.00, 6.84];
      const noatpComarcaVals = [20.82, 26.00, 14.54, 14.54, 11.25, 12.85];

      chartComarcasInstance = new Chart(document.getElementById('chartComarcasComp'), {
        type: 'bar',
        data: {
          labels: comarcaLabels,
          datasets: [
            {
              label: t.chartAtpSeries,
              data: atpComarcaVals,
              backgroundColor: '#047857',
              borderRadius: 6
            },
            {
              label: t.chartNoatpSeries,
              data: noatpComarcaVals,
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { font: { weight: 600 } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}%`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: val => val + '%' },
              grid: { color: '#E2E8F0' }
            },
            x: {
              grid: { display: false },
              ticks: { font: { weight: 600, size: 12 } }
            }
          }
        }
      });
    }

    function updateChartsLanguage() {
      const t = I18N[CURRENT_LANG] || I18N.es;
      if (chartSubsectoresInstance) {
        chartSubsectoresInstance.data.labels = CURRENT_LANG === 'eu' ? chartLabelsEu.subsectores : chartLabelsEs.subsectores;
        chartSubsectoresInstance.data.datasets[0].label = t.chartAtpSeries;
        chartSubsectoresInstance.data.datasets[1].label = t.chartNoatpSeries;
        chartSubsectoresInstance.update();
      }

      if (chartSuperficieInstance) {
        chartSuperficieInstance.data.labels = CURRENT_LANG === 'eu' ? chartLabelsEu.superficie : chartLabelsEs.superficie;
        chartSuperficieInstance.data.datasets[0].label = t.chartAtpSeries;
        chartSuperficieInstance.data.datasets[1].label = t.chartNoatpSeries;
        chartSuperficieInstance.update();
      }

      if (chartComarcasInstance) {
        chartComarcasInstance.data.datasets[0].label = t.chartAtpSeries;
        chartComarcasInstance.data.datasets[1].label = t.chartNoatpSeries;
        chartComarcasInstance.update();
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderSubsectores();
      renderSuperficie();
      renderEcologico();
      renderComarcas();
      // renderFormaJuridica();
      renderEdad();
      initCharts();
    });
  