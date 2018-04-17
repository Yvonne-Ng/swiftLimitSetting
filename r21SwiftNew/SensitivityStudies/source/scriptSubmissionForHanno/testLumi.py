lumiSteps = [0.1,0.2,0.3,0.5,0.7]+range(1,10)+range(10,20,1)+range(20,30,2)+range(30,50,3)+range(50,100,5)+range(100,200,10)+range(200,1000,100)

massValues = [250, 300, 400]

#------------------------------------------
#loop over mass values
previousMassDiscoveryLumi = 0
discoveryThreshold = 0.1
previousLumiIndex = 0

for mass in massValues :
  print "testing mass:", mass
    
  lumiIndex = 0
  lumi = lumiSteps[lumiIndex]

  #doing 1000/fb doesn't make much sense, may as well give up?
  while lumi<(lumiSteps[-1]) :
    lumi = lumiSteps[lumiIndex]

    while (lumi < previousMassDiscoveryLumi) :
      lumiIndex = lumiIndex+1
      lumi = lumiSteps[lumiIndex]
    
    #print "lumi before checking discovery:", lumi

    discovery = 0.5-(float(lumiIndex)/(mass/2.))
    
    if discovery < discoveryThreshold :
        print "Discovered!"
        print "mass", mass, "lumi", lumi
        previousMassDiscoveryLumi = lumi
        break
    elif discovery > 0.15 :#close enough
        lumiIndex = lumiIndex+3
        #print lumiIndex
        continue
    elif discovery > 0.13 :#go a bit higher
        lumiIndex = lumiIndex+2
        #print lumiIndex
        continue
    else :
        lumiIndex = lumiIndex+1
        #print lumiIndex
        continue








#
#print lumiSteps
#
#lumi = 250
#
#if lumi < lumiSteps[0]:
#  lumi = lumiSteps[0]
#elif lumi >= lumiSteps[-1]:#make it bigger
#  lumi*=2.
#else:#step through the vector
#  for ii in xrange( len(lumiSteps)-1):
#      if lumi >= lumiSteps[ii] and lumi < lumiSteps[ii+1]:
#          lumi = lumiSteps[ii+1]
#          break
#
#print lumi
