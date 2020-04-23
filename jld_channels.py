## repris de gnss_block_factory

## BIZARRE : SBAS en plein milieu (entre GPS et GAL)
evGPS_1C,evGPS_2S,evGPS_L5,evSBAS_1C,evGAL_1B,evGAL_5X, \
	evGLO_1G,evGLO_2G,evBDS_B1,evBDS_B3 = range(10)

cid = {}
cid["1C"] = evGPS_1C
cid["2S"] = evGPS_2S
cid["L5"] = evGPS_L5
cid["1B"] = evGAL_1B
cid["5X"] = evGAL_5X
cid["1G"] = evGLO_1G
cid["2G"] = evGLO_2G
cid["B1"] = evBDS_B1
cid["B3"] = evBDS_B3