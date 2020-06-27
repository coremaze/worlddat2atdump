from struct import *
class Entry():
    def __init__(s, address, worldName, loc, length):
        s.address = address
        s.worldName = worldName
        s.location = loc
        s.length = length
    def Details(s):
        print("Address: %s\nWorld Name: %s\nLocation: %s\n" % (hex(s.address), s.worldName, hex(s.location)))

def GetEntries(nIdx, nDat, awtype):
    #read idx file
    hIdx = open(nIdx, 'rb')
    cIdx = hIdx.read()
    hIdx.close()

    hDat = open(nDat, 'rb')
    cDat = hDat.read()
    hDat.close()

    #Parse IDX header
    (IDXLength, #0
     IDXunk1, #4
     IDXEnd, #8
     IDXunk2, #C
     IDXunk3, #10
     IDXunk4, #14
     IDXunk5, #18
     IDXunk6, #1C
     IDXunk7, #20
     IDXunk8, #24
     IDXunk9, #28
     IDXunk10, #2C
     IDXunk11, #30
     IDXunk12, #34
     IDXunk13, #38
     IDXunk14, #3C  
     IDXunk15, #40
     IDXunk16, #44
     IDXStart, #48
     IDXunk18, #4C
     IDXunk19, #50
     IDXunk20, #54
     IDXunk21, #58
     IDXunk22, #5C
     IDXunk23, #60
     IDXunk24, #64
     IDXunk25, #68
     IDXunk26, #6C
     IDXunk27, #70
     IDXunk28, #74
     IDXunk29, #78
     IDXunk30 #7C
    ) = unpack('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', cIdx[0:0x80])

    lstentries = []



    if awtype == 6:
        ENTRY_LENGTH = 0x06
        IDX_OFFSET = 0x12
    elif awtype == 5:
        ENTRY_LENGTH = 0x06
        IDX_OFFSET = 0x12
    elif awtype == 4:
        ENTRY_LENGTH = 0x06
        IDX_OFFSET = 0x12
        #WORLD_ENCODING = 'utf-16'
##    elif awtype == 4:
##        ENTRY_LENGTH = 0x8
##        IDX_OFFSET = 0x12

    BlockStart = IDXStart


    #Loop at least once, and stop when next block is at 0 (end of index)
    while True:
        forward, backward, entries, entrieslength = unpack('<IIHH', cIdx[BlockStart:BlockStart+12])
        loc = BlockStart + IDX_OFFSET
        print("Reading %s index entries from index block %s" % (entries, hex(BlockStart)))

        #Get entries until entry limit
        for entrycount in range(0, entries):
            
            if awtype == 5 or awtype == 6 or awtype == 4:
                address, data1, data2 = unpack("<IBB", cIdx[loc:loc+ENTRY_LENGTH])
                worldNameLength = 0x32 - data2

            #Figure out the encoding... it somehow uses both...
            if cIdx[loc+ENTRY_LENGTH+1] == 0:
                WORLD_ENCODING = 'utf-16'
            else:
                WORLD_ENCODING = 'utf-8'

            try:
                worldName = cIdx[loc+ENTRY_LENGTH : loc+ENTRY_LENGTH+worldNameLength].decode(WORLD_ENCODING)
                #print(hex(address), hex(loc))
                length = unpack('I', cDat[address+2:address+6])[0]
            
                #Entries whose data length are 0x0E contain no data
                if length != 0x0E:
                    lstentries.append( Entry(address, worldName, loc, length) )
            except:
                print('An invalid worldname was found. Skipping entry at %s (%s)' % (hex(loc), cIdx[loc+ENTRY_LENGTH : loc+ENTRY_LENGTH+5]))

            #Advance to next entry
            loc += ENTRY_LENGTH + worldNameLength

        if forward == 0x00000000:
            break
        
        BlockStart = forward

    return lstentries
