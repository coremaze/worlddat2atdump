from IDX import *
from struct import *
from io import BytesIO
import argparse
import os

def ReadDBString(buf, pos):
    string = buf[pos:pos+0x100]
    string = string[:string.find(b'\x00')]
    string = string.decode('latin-1')
    return string

def Read(buf, pos, kind):
    if kind in ['B', 'b', '?']:
        size = 1
    elif kind in ['H', 'h']:
        size = 2
    elif kind in ['I', 'i', 'f']:
        size = 4

    return unpack(f'<{kind}', buf[pos:pos+size])[0]

def ReadAsHex(buf, pos):
    result = []
    truncation = 0
    for i in range(pos, pos+0x100):
        val = buf[i]
        if val != 0:
            truncation = i + 1 - pos
        result.append(val)

    result = result[:truncation]
    resultString = ''.join([f'{x:02x}' for x in result])
    return resultString


def ParsVars(sectionData):
    var = {}
    var[0] = Read(sectionData, 0x30, '?')
    #var1 to 9 unretrievable
    var[1] = False
    var[2] = True
    var[3] = True
    var[4] = True
    var[5] = True
    var[6] = True
    var[7] = True
    var[8] = True
    var[9] = False
    var[10] = Read(sectionData, 0x24, 'B')
    var[11] = Read(sectionData, 0x23, 'B')
    var[12] = Read(sectionData, 0x22, 'B')
    var[13] = 1 #no 13
    var[14] = ReadDBString(sectionData, 0x9D7)
    var[15] = '' #no 15
    var[17] = '' #no 17
    var[18] = Read(sectionData, 0x89, 'f')
    var[19] = 30000 #11000 #no 19 - this is cell limit, and generally I want it higher than the limit
    var[20] = ReadDBString(sectionData, 0x17D7)
    var[21] = Read(sectionData, 0xBF, 'i')
    var[22] = Read(sectionData, 0x61, 'f')
    var[23] = Read(sectionData, 0x6D, 'f')
    var[24] = ReadDBString(sectionData, 0x14D7)
    var[25] = Read(sectionData, 0x55, 'f')
    var[26] = ReadDBString(sectionData, 0x18D7)
    var[27] = Read(sectionData, 0xC3, 'i')
    var[28] = Read(sectionData, 0x65, 'f')
    var[29] = Read(sectionData, 0x71, 'f')
    var[30] = ReadDBString(sectionData, 0x15D7)
    var[31] = Read(sectionData, 0x59, 'f')
    var[32] = ReadDBString(sectionData, 0x19D7)
    var[33] = Read(sectionData, 0xC7, 'i')
    var[34] = Read(sectionData, 0x69, 'f')
    var[35] = Read(sectionData, 0x75, 'f')
    var[36] = ReadDBString(sectionData, 0x16D7)
    var[37] = Read(sectionData, 0x5D, 'f')
    var[39] = False #no 39
    var[40] = False #no 40
    var[41] = True #no 41
    var[42] = '' #no 42
    var[43] = '' #no 43
    var[44] = Read(sectionData, 0x31, '?')
    var[45] = Read(sectionData, 0x2F, '?')
    var[46] = '' #no 46
    var[47] = ReadDBString(sectionData, 0x13D7)
    var[49] = Read(sectionData, 0x12, 'B')
    var[50] = Read(sectionData, 0x2C, '?')
    var[51] = Read(sectionData, 0x11, 'B')
    var[52] = Read(sectionData, 0x34, 'h')
    var[53] = Read(sectionData, 0x32, 'h')
    var[54] = Read(sectionData, 0x10, 'B')
    var[55] = Read(sectionData, 0x9D, 'f')
    var[56] = ReadDBString(sectionData, 0xBD7)
    var[57] = ReadDBString(sectionData, 0xDD7)
    var[58] = '' #no 58
    var[59] = Read(sectionData, 0x21, 'B')
    var[60] = Read(sectionData, 0x4F, '?')
    var[61] = Read(sectionData, 0x50, '?')
    var[62] = Read(sectionData, 0xCF, 'i')
    var[63] = Read(sectionData, 0x20, 'B')
    var[64] = ReadDBString(sectionData, 0x12D7)
    var[65] = Read(sectionData, 0x1F, 'B')
    var[66] = ReadDBString(sectionData, 0x11D7)
    var[67] = Read(sectionData, 0x13, 'f')
    var[68] = Read(sectionData, 0x17, 'f')
    var[69] = Read(sectionData, 0x1B, 'f')
    var[70] = Read(sectionData, 0x36, 'h')
    var[72] = Read(sectionData, 0x38, 'h')
    var[74] = ReadAsHex(sectionData, 0xFD7)
    var[76] = ReadDBString(sectionData, 0xCD7)
    var[77] = 10080 #no 77
    var[80] = Read(sectionData, 0x2E, '?')
    var[81] = 0 #no 81
    var[83] = ReadDBString(sectionData, 0x10D7)
    var[84] = Read(sectionData, 0x4D, 'B')
    var[85] = Read(sectionData, 0x47, 'B')
    var[86] = Read(sectionData, 0x41, 'B')
    var[87] = Read(sectionData, 0x49, 'B')
    var[88] = Read(sectionData, 0x43, 'B')
    var[89] = Read(sectionData, 0x3D, 'B')
    var[90] = Read(sectionData, 0x48, 'B')
    var[91] = Read(sectionData, 0x42, 'B')
    var[92] = Read(sectionData, 0x3C, 'B')
    var[93] = Read(sectionData, 0x4A, 'B')
    var[94] = Read(sectionData, 0x44, 'B')
    var[95] = Read(sectionData, 0x3E, 'B')
    var[96] = Read(sectionData, 0x4C, 'B')
    var[97] = Read(sectionData, 0x46, 'B')
    var[98] = Read(sectionData, 0x40, 'B')
    var[99] = Read(sectionData, 0x4B, 'B')
    var[100] = Read(sectionData, 0x45, 'B')
    var[101] = Read(sectionData, 0x3F, 'B')
    var[102] = ReadDBString(sectionData, 0x1D7)
    var[103] = ReadDBString(sectionData, 0x2D7)
    var[104] = ReadDBString(sectionData, 0x3D7)
    var[105] = '' #no 105
    var[106] = '' #no 106
    var[107] = '' #no 107
    var[108] = Read(sectionData, 0x91, 'f')
    var[109] = Read(sectionData, 0x95, 'f')
    var[110] = Read(sectionData, 0x99, 'f')
    var[112] = ReadDBString(sectionData, 0x8D7)
    var[113] = '' #no 113
    var[114] = Read(sectionData, 0x29, 'B')
    var[115] = ReadDBString(sectionData, 0x7D7)
    var[116] = ReadDBString(sectionData, 0x6D7)
    var[117] = Read(sectionData, 0x25, '?')
    var[118] = Read(sectionData, 0x28, 'B')
    var[119] = Read(sectionData, 0x85, 'f')
    var[120] = ReadDBString(sectionData, 0x5D7)
    var[121] = Read(sectionData, 0x2A, 'B')
    var[122] = Read(sectionData, 0x27, 'B')
    var[123] = Read(sectionData, 0x81, 'f')
    var[124] = Read(sectionData, 0x7D, 'f')
    var[125] = ReadDBString(sectionData, 0x4D7)
    var[126] = Read(sectionData, 0x26, '?')
    var[127] = Read(sectionData, 0xD3, 'i')
    var[128] = Read(sectionData, 0x79, 'f')
    var[129] = ReadDBString(sectionData, 0xED7)
    var[130] = False #no 130
    var[131] = ReadDBString(sectionData, 0xD7)
    var[132] = ReadDBString(sectionData, 0xAD7)
    var[133] = False #no 133
    var[134] = False #no 134
    var[135] = Read(sectionData, 0xAE, '?')
    var[136] = Read(sectionData, 0xAF, '?')
    var[137] = Read(sectionData, 0xA1, 'f')
    var[138] = Read(sectionData, 0x8D, 'f')
    var[139] = Read(sectionData, 0xA5, '?')
    var[140] = Read(sectionData, 0xA6, 'f')
    var[141] = Read(sectionData, 0xAA, 'f')
    var[142] = Read(sectionData, 0x2D, '?')
    var[143] = Read(sectionData, 0x4E, '?')
    var[144] = Read(sectionData, 0x51, 'i')
    var[145] = Read(sectionData, 0xB0, '?')
    var[146] = Read(sectionData, 0xB1, 'i')
    var[147] = Read(sectionData, 0xB5, 'i')
    var[148] = '' #no 148
    var[149] = Read(sectionData, 0xBD, '?')
    var[150] = Read(sectionData, 0xBE, '?')
    return var

def SaveVars(var, fileName):
    print(f'Saving {fileName}...')
    with open(fileName, 'w') as f:
        f.write('atdump version 4\n')
        for i, e in var.items():
            val = e
            if type(e) == bool:
                val = ('N', 'Y')[e]
            if type(e) == float:
                val = f'{e:06f}'
            f.write(f'{i} {val}\n')

def ParseNumber(string):
    if string.startswith('0x'):
        return int(string[2:], base=16)
    else:
        return int(string)

parser = argparse.ArgumentParser(description='Converts world databases to atdumps.')
parser.add_argument('database', type=str, help='Path to database, without extension')
parser.add_argument('--output', type=str, help='Path to write the results to', default='')
parser.add_argument('--address', type=str, help='Address to manually search for a world at (Hint: subtract 0xCD7 from the start of the object path). Can be used to recover corrupted worlds.')
args = parser.parse_args()

nDat = args.database+'.dat'
nIdx = args.database+'.idx'

with open(nDat, 'rb') as f:
    cDat = f.read()

if args.address is None:
    entries = GetEntries(nIdx, nDat, 4)
    for e in entries:
        e.Details()
        if not e.worldName.isascii():
            print(f'Skipping {e.worldName}...')
            continue

        reader = BytesIO(cDat[e.address:])
        length, = unpack('<I', reader.read(4))
        sectionData = reader.read(length)
        var = ParsVars(sectionData)
        SaveVars(var, os.path.join(args.output, f'atdump-result-{e.worldName}.txt'))
else:
    addr = ParseNumber(args.address)
    sectionData = cDat[addr:]
    var = ParsVars(sectionData)
    SaveVars(var, os.path.join(args.output, f'atdump-result-{args.address}.txt'))


        
    
    
    




