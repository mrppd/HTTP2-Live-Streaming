import imageio
class VideoStream:
    def __init__(self, filename, ext):
        self.filename_50 = filename+'_50.'+ext
        self.filename_150 = filename+'_150.'+ext
        self.filename_300 = filename+'_300.'+ext
        self.filename_600 = filename+'_600.'+ext
        self.filename_1200 = filename+'_1200.'+ext
        self.filename_2500 = filename+'_2500.'+ext
        self.filename_4000 = filename+'_4000.'+ext
        try:
            #self.file = open(filename)
            self.file_50 = imageio.get_reader(self.filename_50)
            self.file_150 = imageio.get_reader(self.filename_150)
            self.file_300 = imageio.get_reader(self.filename_300)
            self.file_600 = imageio.get_reader(self.filename_600)
            self.file_1200 = imageio.get_reader(self.filename_1200)
            self.file_2500 = imageio.get_reader(self.filename_2500)
            self.file_4000 = imageio.get_reader(self.filename_4000)
        except:
            raise IOError
        self.frameNum = 0

        
    def openFile(self, filename, ext):
        self.filename_50 = filename+'_50.'+ext
        self.filename_150 = filename+'_150.'+ext
        self.filename_300 = filename+'_300.'+ext
        self.filename_600 = filename+'_600.'+ext
        self.filename_1200 = filename+'_1200.'+ext
        self.filename_2500 = filename+'_2500.'+ext
        self.filename_4000 = filename+'_4000.'+ext
        try:
            #self.file = open(filename)
            self.file_50 = imageio.get_reader(self.filename_50)
            self.file_150 = imageio.get_reader(self.filename_150)
            self.file_300 = imageio.get_reader(self.filename_300)
            self.file_600 = imageio.get_reader(self.filename_600)
            self.file_1200 = imageio.get_reader(self.filename_1200)
            self.file_2500 = imageio.get_reader(self.filename_2500)
            self.file_4000 = imageio.get_reader(self.filename_4000)
        except:
            raise IOError
        self.frameNum = 0
        
        
    def nextFrame(self, typeReturn='serial'):
        """Get next frame."""
        data = self.file_600.get_next_data() # Get the framelength from the first 5 bits
        #if data: 
        # r=serialize the data
        sdata = imageio.imwrite(imageio.RETURN_BYTES, data, format='jpg')
        self.frameNum += 1
        
        if(typeReturn=='serial'):
            return sdata
        elif(typeReturn=='ndarray'):
            return data
        elif(typeReturn=='both'):
            return [sdata, data]
        else:
            print("Error occured!")
            return 0
	
    
    def getFrame(self, index, quality=3, typeReturn='serial'):	
        """Get next frame."""
        data = []
        if(quality==1):
            data = self.file_50.get_data(index) # Get the frame
        elif(quality==2):
            data = self.file_150.get_data(index) 
        elif(quality==3):
            data = self.file_300.get_data(index) 
        elif(quality==4):
            data = self.file_600.get_data(index) 
        elif(quality==5):
            data = self.file_1200.get_data(index)
        elif(quality==6):
            data = self.file_2500.get_data(index)
        elif(quality==7):
            data = self.file_4000.get_data(index)
        #if data: 
        # r=serialize the data
        sdata = imageio.imwrite(imageio.RETURN_BYTES, data, format='jpg')
        self.frameNum += 1
        
        if(typeReturn=='serial'):
            return sdata
        elif(typeReturn=='ndarray'):
            return data
        elif(typeReturn=='both'):
            return [sdata, data]
        else:
            print("Error occured!")
            return 0
        
    def frameReduce(self):
        self.frameNum -= 1
    
    def frameIncrease(self):
        self.frameNum += 1
        
    def frameNbr(self):
        #Get frame number.
        return self.frameNum
   
    def closeFile(self):
        #Get frame number.
        self.file.close()
        return 0
	
	