def get_batting_table_schema():
    # this was derived in an offline process.
    # TODO: automate this

    return {
        2: "Season",
        3: "Age",
        4: "G",
        5: "AB",
        6: "PA",
        7: "H",
        8: "1B",
        9: "2B",
        10: "3B",
        11: "HR",
        12: "R",
        13: "RBI",
        14: "BB",
        15: "IBB",
        16: "SO",
        17: "HBP",
        18: "SF",
        19: "SH",
        20: "GDP",
        21: "SB",
        22: "CS",
        23: "AVG",
        24: "GB",
        25: "FB",
        26: "LD",
        27: "IFFB",
        28: "Pitches",
        29: "Balls",
        30: "Strikes",
        31: "IFH",
        32: "BU",
        33: "BUH",
        34: "BB%",
        35: "K%",
        36: "BB/K",
        37: "OBP",
        38: "SLG",
        39: "OPS",
        40: "ISO",
        41: "BABIP",
        42: "GB/FB",
        43: "LD%",
        44: "GB%",
        45: "FB%",
        46: "IFFB%",
        47: "HR/FB",
        48: "IFH%",
        49: "BUH%",
        50: "wOBA",
        51: "wRAA",
        52: "wRC",
        53: "Bat",
        54: "Fld",
        55: "Rep",
        56: "Pos",
        57: "RAR",
        58: "WAR",
        59: "Dol",
        60: "Spd",
        61: "wRC+",
        62: "WPA",
        63: "-WPA",
        64: "+WPA",
        65: "RE24",
        66: "REW",
        67: "pLI",
        68: "phLI",
        69: "PH",
        70: "WPA/LI",
        71: "Clutch",
        72: "FB%",
        73: "FBv",
        74: "SL%",
        75: "SLv",
        76: "CT%",
        77: "CTv",
        78: "CB%",
        79: "CBv",
        80: "CH%",
        81: "CHv",
        82: "SF%",
        83: "SFv",
        84: "KN%",
        85: "KNv",
        86: "XX%",
        87: "PO%",
        88: "wFB",
        89: "wSL",
        90: "wCT",
        91: "wCB",
        92: "wCH",
        93: "wSF",
        94: "wKN",
        95: "wFB/C",
        96: "wSL/C",
        97: "wCT/C",
        98: "wCB/C",
        99: "wCH/C",
        100: "wSF/C",
        101: "wKN/C",
        102: "O-Swing%",
        103: "Z-Swing%",
        104: "Swing%",
        105: "O-Contact%",
        106: "Z-Contact%",
        107: "Contact%",
        108: "Zone%",
        109: "F-Strike%",
        110: "SwStr%",
        111: "BsR",
        112: "FA% (pfx)",
        113: "FT% (pfx)",
        114: "FC% (pfx)",
        115: "FS% (pfx)",
        116: "FO% (pfx)",
        117: "SI% (pfx)",
        118: "SL% (pfx)",
        119: "CU% (pfx)",
        120: "KC% (pfx)",
        121: "EP% (pfx)",
        122: "CH% (pfx)",
        123: "SC% (pfx)",
        124: "KN% (pfx)",
        125: "UN% (pfx)",
        126: "vFA (pfx)",
        127: "vFT (pfx)",
        128: "vFC (pfx)",
        129: "vFS (pfx)",
        130: "vFO (pfx)",
        131: "vSI (pfx)",
        132: "vSL (pfx)",
        133: "vCU (pfx)",
        134: "vKC (pfx)",
        135: "vEP (pfx)",
        136: "vCH (pfx)",
        137: "vSC (pfx)",
        138: "vKN (pfx)",
        139: "FA-X (pfx)",
        140: "FT-X (pfx)",
        141: "FC-X (pfx)",
        142: "FS-X (pfx)",
        143: "FO-X (pfx)",
        144: "SI-X (pfx)",
        145: "SL-X (pfx)",
        146: "CU-X (pfx)",
        147: "KC-X (pfx)",
        148: "EP-X (pfx)",
        149: "CH-X (pfx)",
        150: "SC-X (pfx)",
        151: "KN-X (pfx)",
        152: "FA-Z (pfx)",
        153: "FT-Z (pfx)",
        154: "FC-Z (pfx)",
        155: "FS-Z (pfx)",
        156: "FO-Z (pfx)",
        157: "SI-Z (pfx)",
        158: "SL-Z (pfx)",
        159: "CU-Z (pfx)",
        160: "KC-Z (pfx)",
        161: "EP-Z (pfx)",
        162: "CH-Z (pfx)",
        163: "SC-Z (pfx)",
        164: "KN-Z (pfx)",
        165: "wFA (pfx)",
        166: "wFT (pfx)",
        167: "wFC (pfx)",
        168: "wFS (pfx)",
        169: "wFO (pfx)",
        170: "wSI (pfx)",
        171: "wSL (pfx)",
        172: "wCU (pfx)",
        173: "wKC (pfx)",
        174: "wEP (pfx)",
        175: "wCH (pfx)",
        176: "wSC (pfx)",
        177: "wKN (pfx)",
        178: "wFA/C (pfx)",
        179: "wFT/C (pfx)",
        180: "wFC/C (pfx)",
        181: "wFS/C (pfx)",
        182: "wFO/C (pfx)",
        183: "wSI/C (pfx)",
        184: "wSL/C (pfx)",
        185: "wCU/C (pfx)",
        186: "wKC/C (pfx)",
        187: "wEP/C (pfx)",
        188: "wCH/C (pfx)",
        189: "wSC/C (pfx)",
        190: "wKN/C (pfx)",
        191: "O-Swing% (pfx)",
        192: "Z-Swing% (pfx)",
        193: "Swing% (pfx)",
        194: "O-Contact% (pfx)",
        195: "Z-Contact% (pfx)",
        196: "Contact% (pfx)",
        197: "Zone% (pfx)",
        198: "Pace",
        199: "Def",
        200: "wSB",
        201: "UBR",
        202: "Age Rng",
        203: "Off",
        204: "Lg",
        205: "wGDP",
        206: "Pull%",
        207: "Cent%",
        208: "Oppo%",
        209: "Soft%",
        210: "Med%",
        211: "Hard%",
        212: "TTO%",
        213: "CH% (pi)",
        214: "CS% (pi)",
        215: "CU% (pi)",
        216: "FA% (pi)",
        217: "FC% (pi)",
        218: "FS% (pi)",
        219: "KN% (pi)",
        220: "SB% (pi)",
        221: "SI% (pi)",
        222: "SL% (pi)",
        223: "XX% (pi)",
        224: "vCH (pi)",
        225: "vCS (pi)",
        226: "vCU (pi)",
        227: "vFA (pi)",
        228: "vFC (pi)",
        229: "vFS (pi)",
        230: "vKN (pi)",
        231: "vSB (pi)",
        232: "vSI (pi)",
        233: "vSL (pi)",
        234: "vXX (pi)",
        235: "CH-X (pi)",
        236: "CS-X (pi)",
        237: "CU-X (pi)",
        238: "FA-X (pi)",
        239: "FC-X (pi)",
        240: "FS-X (pi)",
        241: "KN-X (pi)",
        242: "SB-X (pi)",
        243: "SI-X (pi)",
        244: "SL-X (pi)",
        245: "XX-X (pi)",
        246: "CH-Z (pi)",
        247: "CS-Z (pi)",
        248: "CU-Z (pi)",
        249: "FA-Z (pi)",
        250: "FC-Z (pi)",
        251: "FS-Z (pi)",
        252: "KN-Z (pi)",
        253: "SB-Z (pi)",
        254: "SI-Z (pi)",
        255: "SL-Z (pi)",
        256: "XX-Z (pi)",
        257: "wCH (pi)",
        258: "wCS (pi)",
        259: "wCU (pi)",
        260: "wFA (pi)",
        261: "wFC (pi)",
        262: "wFS (pi)",
        263: "wKN (pi)",
        264: "wSB (pi)",
        265: "wSI (pi)",
        266: "wSL (pi)",
        267: "wXX (pi)",
        268: "wCH/C (pi)",
        269: "wCS/C (pi)",
        270: "wCU/C (pi)",
        271: "wFA/C (pi)",
        272: "wFC/C (pi)",
        273: "wFS/C (pi)",
        274: "wKN/C (pi)",
        275: "wSB/C (pi)",
        276: "wSI/C (pi)",
        277: "wSL/C (pi)",
        278: "wXX/C (pi)",
        279: "O-Swing% (pi)",
        280: "Z-Swing% (pi)",
        281: "Swing% (pi)",
        282: "O-Contact% (pi)",
        283: "Z-Contact% (pi)",
        284: "Contact% (pi)",
        285: "Zone% (pi)",
        286: "Pace (pi)",
    }