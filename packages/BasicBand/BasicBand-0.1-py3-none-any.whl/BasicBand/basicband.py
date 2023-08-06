from __future__ import unicode_literals
__author__ = "Juan Montesinos"
__version__ = "0.1"
__maintainer__ = "Juan Montesinos"
__email__ = "juanfelipe.montesinos@upf.edu"


import json
import os
import re
import copy
__all__ = ['BasicBand']
def apply(x,f):
    #Returns true if video has to be deleted
    tmp = x[f['key']]
    args = f['p2a'](f['filter'])
    tmp = f['f'](tmp,*args)
    if tmp == True:
        x = tmp
    else:
        x[f['key']] = tmp
    return x
def greater_than(x,t):
    f = lambda X:t<X
    out = list(filter(f,x))
    if not out:
        return True
    else:
        return out
def smaller_than(x,t):
    f = lambda X:t>X
    out =  list(filter(f,x))
    if not out:
        return True
    else:
        return out
PATTERNS = {'t<\d+':{'f':smaller_than,'key':'segMS','p2a':lambda x: [int(re.findall('\d+',x)[0])]},
            't>\d+':{'f':greater_than,'key':'segMS','p2a':lambda x: [int(re.findall('\d+',x)[0])]}
            }
"""
Patterns is a variable which contains as keys re patters available for filtering
each filter consist in 4 elements:
    a 'key' which sets which video variable should be modified
    a 'p2a' pattern2 args function which maps the information contained in the user-input
    (which is an string) into a list of arguments 
    'f' is the function that does the transformation given the arguments of p2a and 
    the varible provided by 'key'
    
    All this is parsed to apply function
"""

def time2ms(time):
    # Expected format hh:mm:ss.xxx extended
    # Typicall format mm:ss
    patterns = {'mm:ss':'^\d+\W\d\d','hh:mm:ss':'^\d+\W\d\d\W\d\d',
                '.xxx':'\d\d\d'}
    key = patterns.keys()
    h=re.match(patterns['hh:mm:ss'],time)
    m=re.match(patterns['mm:ss'],time)
    if h:
        results = h.group()
        results = re.findall('\d\d',results)
        results = [int(r) for r in results]
        h = results[0]*3600*1000
        m = results[1]*60*1000
        s = results[2]*1000
    elif m:
        results = m.group()
        results = re.findall('\d+',results)
        results = [int(r) for r in results]
        h = 0
        m = results[0]*60*1000
        s = results[1]*1000
    else:
        raise Exception ('Wrong time format' )
    try:
        ms = int(re.findall(patterns['.xxx'],time)[0])
    except:
        ms = 0

    return h+m+s+ms
    
def segment2list(segment):
    start = []
    end   = []
    for s in segment:
        start.append(time2ms(s['start']))
        end.append(time2ms(s['end']))
    dur = [e-s for e,s in zip(end,start)]
    return start,end,dur
def dataset_analysis(path_to_dataset):
    """This function takes as input a directory root dataset folder with the following structure:"
    dataset---
        ---class1 (must be a folder)
            ---file1 (must not to  be a folder)
            ---file2 (must not to be a folder)
        ---class2 (must be a folder)
            ---file1 (must not to be a folder)
            ---file2 (must not to be a folder)
    Returns:
        clases: list of classes (class folder name)  eg. clases = [class1,class2]
        class_path: list of absolute paths to classes eg class_path = [absolute_path/class1, absolute_pàth/class2]
        files: python dictionary whose keys are the clases and items are class videos
                eg. files = {class1:[video1,video2,...,videoN]}
        files_path: Analogous to class_path
    """
    clases = [f for f in os.listdir(path_to_dataset)]
    class_path = [os.path.join(path_to_dataset,f) for f in os.listdir(path_to_dataset)]
    files = {}
    files_path = {}
    for clase,typ in zip(clases,class_path):
        files_ = [f for f in os.listdir(typ)]
        files_path_ = [os.path.join(typ,f) for f in os.listdir(typ)]
        files[clase]=files_
        files_path[clase] = files_path_
    return clases,class_path,files,files_path
class BasicBandSubsetGather(object):
    def __new__(cls,obj,instruments):
        obj.filters.extend(instruments)
        obj.__resetiterator__()
        filters = []
        #Compares user restriction with allowed restrictions
        #If match, set of tools is parsed into a list
        for i in instruments:
            for f in PATTERNS.keys():
                if re.match(f,i):
                    PATTERNS[f].update({'filter':i})
                    filters.append(PATTERNS[f])
                    break
        #Copy to prevent error due to iterator size change
        newobj = copy.deepcopy(obj)
        for instrument,video_id,dic in obj:
            for filtro in filters:
                #apply returns the modified information of the video given a filter
                #filter has very special structure
                out = apply(dic,filtro)
                # apply returns true if for some reason the video should be deleted
                #For example, no segments accomplish with desired restrictions
                if out == True:
                    newobj.dataset[instrument].pop(video_id,None)
                else:
                    newobj.dataset[instrument][video_id] = out
        newobj.__resetiterator__()
        return newobj
class BasicBandSubsetFilter(object):
    def __new__(cls,obj,instruments):
        clases = list(obj.dataset.keys())
        [obj.dataset.pop(c,None) for c in clases if c not in instruments]
        obj.filters.extend(instruments)
        obj.__resetiterator__()
        return obj
class BasicBandSubsetExclude(object):
    def __new__(cls,obj,instruments):
        [obj.dataset.pop(c,None) for c in instruments]
        obj.filters.extend(instruments)
        obj.__resetiterator__()
        return obj
class BasicBandDownloader(object):
    def __new__(cls,obj,dataset_dir):
        import youtube_dl
        outtmpl = '%(id)s.%(ext)s'
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': outtmpl,
            """
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            """
            'logger': None
        }
        for instrument,video_id,_ in obj:
            ydl_opts['outtmpl'] = os.path.join(dataset_dir, instrument, outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                if not os.path.exists(os.path.join(dataset_dir, instrument)):
                    os.makedirs(os.path.join(dataset_dir, instrument))
                try:
                    ydl.download(['https://www.youtube.com/watch?v=%s' % video_id])
                    del obj.dataset[instrument][video_id]
                except:
                    ydl.download(['https://www.youtube.com/watch?v=%s' % video_id])
        return obj 
class BasicBand(object):
    """
        inputs:
                dataset (str / dict): Path to json file or dictionary already opened from that file
                dataset_path (str): Path to root folder of dataset (which contains videos)
                            If provided it will compare json file against existing videos and
                            provide for each video the path in which it's saved.
    """
    def __init__(self,dataset,dataset_path = None):
        #if dataset is a path to json file
        if isinstance(dataset,str):
            self.json_path  = dataset
            self.dataset = json.load(open(self.json_path))
        #If dataset has been already loaded as dict
        elif isinstance(dataset,dict):
            self.dataset = dataset
        else:
        #Any other case
            raise AssertionError
        
        # Variable for the iterator (iterator through instruments)
        self.ds_key_iter = iter(dataset.keys())
        #Constrains applied to dataset, intially none
        self.filters = []
        #Reserved attributes to set iterator
        self.res_iter_attributes = ['ds_key_iter','is_iter','inst']
        self.root = dataset_path
        
        #Convert the segment structure which is natively 
        #[{'start':str,'end':str}1 ... {'start':str,'end':str}N] into 3 lists
        #of same length containing starting point, end point and duration in ms
        for instrument,video_id,dic in self:
            start,end,dur = segment2list(dic['Segments'])
            self.dataset[instrument][video_id].update({'segMS':dur,'segS':start,'segE':end})
        
        #Performs comparison between json file and root folder which contains videos
        if dataset_path is not None:
            self.jsonvsfolder(dataset_path)
    def __iter__(self):
        return self
    def __next__(self):
        # If iterator has been initilized, is_iter should be defined
        # is_iter iterates through videos for a given instrument
        if not hasattr(self, 'is_iter'):
            self.inst = next(self.ds_key_iter)
            self.is_iter = iter(self.dataset[self.inst])
        try:
            # If can get next video for an instrument, continue
            key = next(self.is_iter)            
        except StopIteration:
            #If video_id iterator is exhausted load next instrument
            try:
                self.inst = next(self.ds_key_iter)
                self.is_iter = iter(self.dataset[self.inst])
            # If next instrument is exhausted reset iterator    
            except StopIteration:
                self.ds_key_iter = iter(self.dataset.keys())
                del self.is_iter
                del self.inst
                raise StopIteration
            key =  next(self.is_iter)
        return self.inst,key,self.dataset[self.inst][key]
    def __repr__(self):
        inst_list = list(self.dataset.keys())
        inst = ''
        for i in inst_list: inst += str(i) +','
        filters = ''
        for i in self.filters: filters += str(i) +','
        string = 'BasicBand Dataset, 2019 \n'
        string += 'Instruments: \n \t' + inst + '\n'
        string += 'Filters: \n \t' + filters
        
        return string
    def __str__(self):
        return self.__repr__()    
    def __resetiterator__(self):
        """Reset interator method aimed to be used when composing a subset"""
        for attribute in self.res_iter_attributes:
            if hasattr(self, attribute):
                delattr(self,attribute)
        self.ds_key_iter = iter(self.dataset.keys())
    def gather(self,*args):
        """
        Gathering method to filter videos given some video-level restrictions
        Example
        db = db.gather('t>3000') Gathers videos larger than 3s
        db = db.gather('t>3000','t<5000') Gathers videos larger than 3s and shorter than 5s
        It is equivalent to 
        db = db.gather('t>3000').gather('t<5000')
        """
        return BasicBandSubsetGather(self,args)
    def filter(self,*args):
        """
        Filter out dataset given video class/es
        db =db.filter('violin','cello') Only those instruments remain
        This method deletes everything but input instruments
        """
        return BasicBandSubsetFilter(self,args)
    def exclude(self,*args):
        """
        Filter out dataset given video class/es
        db =db.exclude('violin','cello') Everything but those instruments remains
        This method deletes input instrument
        """
        return BasicBandSubsetExclude(self,args)

    def download(self,dst_path,dst_log,*args):
        """
        Dataset downloader which allows pre-composition
        input:
            dst_path (str): path to save the dataset
            dst_log (str): path to save a backup json which allows to resume downloading
            args are aimed to be used for filter out instruments before downloading
            in the command line version
        returns:
            dict with a backup containing those videos which have not been downloaded
            It's possible to resume downloading instantiating the class with that json file
        """
        #TODO test
        if args[0] == 'exclude':
            f = self.exclude
        elif args[0] == 'filter':
            f = self.filter
        del args[0]
        self = f(*args)
        obj =  BasicBandDownloader(self,dst_path)
        obj.save_json(dst_log)
        return obj
    def save_json(self,path):
        """
        Saves the dataset as json file
        """
        with open(path, 'w') as dst_file:
            json.dump(self.dataset, dst_file)        
    def as_dict(self,key = None):
        if key is None:
            return self.dataset
        else:
            return self.dataset[key]
    def instruments(self):
        return self.dataset.keys()
    
    def jsonvsfolder(self,path):
        instruments,instrument_paths, \
            videos,video_paths = dataset_analysis(path)
        self.missing_instruments = [f for f in instruments if f not in self.instruments()]
        [self.dataset.pop(f,None) for f in self.missing_instruments]
        self.__resetiterator__()
        for instrument in self.instruments():
            video_ids = [os.path.splitext(f)[0] for f in videos[instrument]]
            for video_id,path in zip(video_ids,video_paths[instrument]):
                try:
                    #Try except to deal with key error generated by videos filtered out
                    #such that they exist in the folder but not in the json
                    #TODO remove those videos which exist in dataset but not in folder
                    #remove_residual expects to do that
                    self.dataset[instrument][video_id].update({'path':path})
                except KeyError:
                    pass
    def remove_residual(self,path):
        #TODO testing
        residual = BasicBand(path)
        for instrument,video_id,_ in residual:
            self.dataset[instrument].pop(video_id,None)
    def file_list(self):
        return list(iter(object))
            
#dataset={'piano':{'hola':5,'adios':7},'viola':{'bien':{'mas':-1},'tu':8}}
#dataset = json.load(open('/home/jfm/Downloads/violin.json'))
#db = BasicBand(dataset)
#db.jsonvsfolder('/media/jfm/Slave/BasicBand25')
#for i in iter(db): print(i)
#db.__repr__()
#if __name__ == '__main__':
#    _fire.Fire(BasicBand)