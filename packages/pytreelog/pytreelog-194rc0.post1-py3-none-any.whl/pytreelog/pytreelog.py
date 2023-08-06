# -*- coding: utf-8 -*-

# pytreelog - tree-like logging tool for python 

########################################################
####                   Header                       ####
########################################################
import re, sys, os, random, inspect, pprint, datetime, functools, traceback
import gc, collections
from os import path 

__references__=[
  {'title' :'pytreelog'
  ,'desc' :'Hierarchical logging system for python'
  ,'url'  :'https://bitbucket.org/runsun/TreeLog'
  ,'author':'Runsun Pan, PhD'
  ,'date':'201903'
  }
]

# The 1st PATH_TO_README is pytreelog-pkg/pytreelog/README.md (when pytreelog is installed with setup.py)
# The 2nd PATH_TO_README is pytreelog-pkg/README.md (when pytreelog.py is run in its dev folder)
PATH_TO_README = path.join( path.split(path.realpath( __file__ ))[0],'README.md')
PATH_TO_README = ((path.exists( PATH_TO_README ) and PATH_TO_README )
                 or path.join( path.split(path.split(PATH_TO_README)[0])[0],'README.md'))
BR = '\n' ##os.linesep

########################################################
####                    Para                        ####
########################################################

#SAVE_HTM_PATH = r'c:\t\panpylog.htm'
#SAVE_TXT_PATH = r'c:\t\panpylog.txt'
#HTM_BLOCK_STYLE= '''margin:5px;font-family:courier new;'''+ \
#          '''padding:5px;border:2px inset;background-color:%(bgc)s'''
#HTM_BLOCK_JS='''onmouseover="onMover(this)"''' \
#            +''' onmouseout="onMout(this)"'''
#
#btn='''<button style="padding:0px;border:1px;margin:0px;" ''' +\
#     '''onclick="toggleNext(this)">&gt;</button>'''
#HTM_BLOCK_HEAD= '<div style="%s"'%HTM_BLOCK_STYLE+ \
#                ' %s'%HTM_BLOCK_JS #+ btn
#HTM_BLOCK_TAIL = '</div>'

########################################################
####                    Tool                        ####
########################################################
     
def quotify(s):
    '''
    by FMc
    http://stackoverflow.com/questions/3584005/how-to-properly-add-quotes-to-a-string-using-python
    
     # Test data in original question.
    >>> quotify('')
    '""'
    >>> quotify('a')
    '"a"'
    >>> quotify('"a"')  # No change
    '"a"'
    >>> quotify('""a" b"')  # No change
    '""a" b"'
    >>> quotify('"a" b')
    '""a" b"'
    >>> quotify('"a" "b"')
    '""a" "b""'
    >>> quotify('a "b" c')
    '"a "b" c"'
    
    # Test data in latest edits.
    >>> quotify('type')    # Quote these
    '"type"'
    >>> quotify('"type" /?')
    '""type" /?"'
    >>> quotify('"type" "/?"')
    '""type" "/?""'
    >>> quotify('type "a a" b')
    '"type "a a" b"'
    >>> quotify('type "" b')
    '"type "" b"'
    >>> quotify('"type"')   # Don't quote
    '"type"'
    >>> quotify('""type" /?"')
    '""type" /?"'
    
    # Some more tests.
    
    >>> quotify('"a b" "c d"')
    '""a b" "c d""'
    >>> quotify('" a " foo " b "')
    '"" a " foo " b ""'
    
    '''
    Q = '"'
    re_quoted_items = re.compile(r'" \s* [^"\s] [^"]* \"', re.VERBOSE)

    # The orig string w/o the internally quoted items.
    woqi = re_quoted_items.sub('', s)
    if len(s) == 0:
            orig_quoted = Q + s + Q
    elif len(woqi) > 0 and not (woqi[0] == Q and woqi[-1] == Q):
            orig_quoted = Q + s + Q    
    else:
            orig_quoted = s
    return orig_quoted 
        
def quotifykvlist(kvlist, maxLenOfValString=25
               , kvjoiner=lambda k,v:k+'='+v ):
    '''
    >>> data= [ ('a',3), ('b','xyz') ]
    >>> quotifykvlist( data )
    ['a=3', 'b="xyz"']
    
    '''
    out=[]
    for k,v in kvlist :
            v= type(v)==str and [quotify(v)][0] or str(v)
            if len(v)>= maxLenOfValString:
                    v= '|'+ v[:maxLenOfValString] +'..."|'
            out.append( kvjoiner(k,v) ) 
    return out


def randomcolor():
    return '#'+''.join(random.sample('BFCDEF',6))
        
def getargskv(arginfo):
    '''
        
    Given an ArgInfo, typically returned by inspect.getargvalues(frame), 
    where frame is a function, return a 2-tuple list in the order that's 
    presented in that frame function's' signature:
        
    (frame, file, lineno, name, codetext, somenumber)
        
    [ ('a','astring'), ('b',(2,3)), ('alist',(10,)), ('x',5), ('m','mv') ]
        
    >>> a= inspect.ArgInfo( 
    ...        args=['a', 'b'], 
    ...        varargs='alist', 
    ...        keywords='kws', 
    ...        locals={'a': 'a str', 'alist': (10,),
    ...                'kws': {'x': 5, 'm': 'mv'}, 
    ...                'b': (2, 3),  'd': 'xxx'} 
    ...        )
    >>> getargskv(a) 
    [('a', 'a str'), ('b', (2, 3)), ('alist', (10,)), ('x', 5), ('m', 'mv')]
        
    ''' 
    out = [(x,arginfo.locals[x]) for x in arginfo.args]
    if arginfo.varargs: 
       out.append( (arginfo.varargs, arginfo.locals[arginfo.varargs]) )
    if arginfo.keywords:
       out+= arginfo.locals[arginfo.keywords].items() 
    return out  
                
def getcallerargs(asString=False, maxLenOfValString=25):
    '''
            Return a list of runtime (arg,val) for the function in where this
            is placed.
                
            If asString, return a string including func name. 
                
                
    >>> def test(a,b=None, *alist, **kws):
    ...         d='xxx'
    ...         def g(): return getcallerargs() 
    ...         return g()
        
    >>> test(3)
    [('a', 3), ('b', None), ('alist', ())]
        
    >>> test(3, x=5)
    [('a', 3), ('b', None), ('alist', ()), ('x', 5)]
        
    >>> test('point',(2,3), 10, x=5, m="mv")
    [('a', 'point'), ('b', (2, 3)), ('alist', (10,)), ('x', 5), ('m', 'mv')]

        
    >>> def test(a,b=None, *alist, **kws):
    ...         d='xxx'
    ...         def g(): return getcallerargs(asString=True) 
    ...         return g() 
                
    >>> test(3,4, 10, x=5)
    'test(a=3, b=4, alist=(10,), x=5)'
        
    >>> test('point',(2,3), 10, x=5, m="mv")
    'test(a="point", b=(2, 3), alist=(10,), x=5, m="mv")'
        
    >>> test('This is a vary long long long string',(2,3), 10, x=5, m="mv")
    'test(a=|"This is a vary long long..."|, b=(2, 3), alist=(10,), x=5, m="mv")'
        
    Finding args when decorated
    http://stackoverflow.com/questions/3375573/finding-a-functions-parameters-in-python
    '''
    gls__f= inspect.currentframe().f_back.f_back 
    gls__arg= inspect.getargvalues(gls__f)
    ## Example:  
    ## >>> def test(a,b=None, *ars, **kars):
    ##...               d='xxx'
    ##...               return getlivesig(locals())
    ##
    ## inspect.getargvalues(gls__f) gives:
    ##
    ##  ArgInfo(
    ##    args=['a', 'b'], 
    ##    varargs='ars', 
    ##    keywords='kars',
    ##    locals={'a': 'a string', 
    ##            'kars': {'x': 5, 'm': 'mv'}, 
    ##            'ars': (10,), 
    ##            'b': (2, 3), 
    ##            'd': 'xxx'
    ##           }
    ##  )
    out = getargskv( gls__arg )
    '''out = [(x,gls__arg.locals[x]) for x in gls__arg.args]
    if gls__arg.varargs: 
            out.append( (gls__arg.varargs, gls__arg.locals[gls__arg.varargs]) )
    if gls__arg.keywords:
            out+= gls__arg.locals[gls__arg.keywords].items() 
    ''' 
    if not asString: return out         
    out= quotifykvlist( out )           
    return gls__f.f_code.co_name + '('+ ', '.join(out)+')' 

def iscountable(x):
    try:
      len(x)
      return True 
    except:
      return False        
        
def typename(x):
    '''
    <type 'list'>(16),file_St:<type 'str'>(38),RSbm:<type 'float'>(0.163),St:<type 'list'>(1540),nSf:<type 'int'>(2),RSbt:<type 'float'>(0.999),nP:<type 'int'>(944),Sb:<type 'list'>(1538),d_FSs:<type 'collections.defaultdict'>(16),Sf:<type 'list'>(2),cjName:<type 'str'>(2),nSm:<type 'int'>(9440),d_SF:<class 'collections.Counter'>(1538),nSb:<type 'int'>(1538),file_d_StFP:<type 'str'>(47),file_d_SF:<type 'str'>(40),RSmt:<type 'float'>(6.13),file_S:<type 'str'>(37),nSt:<type 'int'>(1540),iS:<type 'int'>(2),file_d_StFP_c:<type 'str'>(47)}
    '''
    return str(type(x)).replace("'", '').split(' ')[-1][:-1]
        
                        
def getcallername():
    '''
    >>> def callee(): return getcallername()
    >>> def caller(): return callee()
    >>> caller()
    'caller'
    '''
    return inspect.currentframe().f_back.f_back.f_code.co_name 
        
def getbinderinfo(attr=None, layer=2):
    #self=this()
    
    # inspect.getouterframes returns a list of 6-tuple:
    #    (frame, file, lineno, name, codetext, somenumber)
    
    #f_locals
    frameinfo = inspect.getouterframes(inspect.currentframe())
    fs = [ x[0] for x in frameinfo ] # frames
    
    obj = attr
    out=[]
    for f in fs:
        for k,v in f.f_locals.items():
            for kk,vv in inspect.getmembers(v):
                if vv == obj:
                   out.append( k )
    return out  
    
                  
def find_obj_name(obj):
    '''
    >> class CLS():
    ...   def __init__(self):
    ...      self.instname= find_obj_name(self)
    ...   def find_obj_name(self): 
    ...      return find_obj_name(self)
    >> c,d = CLS(), CLS()
    >> c.instname
    'self'
    >> c.find_obj_name()
    'c'
    >> d.instname
    'self'
    >> d.find_obj_name()
    'd'
        
    http://pythonic.pocoo.org/2009/5/30/finding-objects-names
    '''
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
            frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
            if isinstance(referrer, dict):
                    for k, v in referrer.iteritems():
                            if v is obj:
                                    result.append(k)
    return result
                             
def find_obj_name2(obj):
    '''
    >> class CLS():
    ...   def __init__(self):
    ...      self.instname= find_obj_name(self)
    ...   def find_obj_name(self): 
    ...      return find_obj_name(self)
    >> c,d = CLS(), CLS()
    >> c.instname
    'self'
    >> c.find_obj_name()
    'c'
    >> d.instname
    'self'
    >> d.find_obj_name()
    'd'
        
    http://pythonic.pocoo.org/2009/5/30/finding-objects-names
    '''
    frame = sys._getframe()
    frame= inspect.currentframe().f_back
    frameinfo = inspect.getoutterframes(inspect.currentframe)
    for frame in iter(lambda: frame.f_back, None):
            frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
            if isinstance(referrer, dict):
                    for k, v in referrer.iteritems():
                            if v is obj:
                                    result.append(k)
    return result

def getbindernames(obj):
    '''
    >> class Cls(object):    
    ...   def aa(self): print 'i am cc'
                
    >> cl = Cls()
        
    >> getbindernames(cl.aa)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        
    http://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init
    '''
    ## inspect.getouterframes returns a list of 6-tuple:
    ##    (frame, file, lineno, name, codetext, somenumber)
    
    cf = inspect.currentframe()
    frameinfo = inspect.getouterframes(cf)
    return str( [         
                  [ (k,v) for k, v in inspect.getmembers(fi[0].f_locals.values()) ] 
                    for i, fi in enumerate(frameinfo) if i==1
                ] 
             )
                                                                     # Get the frame name
                                                                     # represents the target
    frames = [ x[0] for x in frameinfo ] 
    bns=[]
    for i, frame in enumerate(frames):
        for k,v in frame.f_locals.items():                        
            if id(v)==id(obj): bns.append(k)
    return bns

########################################################
####                    Main                        ####
########################################################

class TreeLog(collections.OrderedDict): #zdict):

    '''
    Hierarchical logging utility for python debugging.
    
    See README.md for detailed doc. 
    
    from pytreelog import TreeLog
    pl = TreeLog()
    pl.l(x)  # log x
    pl(x)    # log x

    pl.b(x)  # Beging a new block. 'x' is optional. If not given, 
             # x will be assigned the function call arg values. As of
             # 2012.12.19, this can be achieved much more easily for
             # functions by the Decorator Approach described below.  
             
    pl.e(x)  # End the current block. 'x' is optional. If x not given
             # for a function that return something, it will show the
             # returned value

    pl.data    # list of lines of the logged data
    pl.text()  # returns the data as a string
    pl.reset() # reset the data and block info to start anew 

    TreeLog(  header    = '='*45+BR+'TreeLog output'+ BR+'='*45
            , _on       = True
            , block_beg = '* '
            , block_end = '* '
            , func_beg  = '> '
            , func_end  = '< '
            , indent    = 1
            , blockline = '-----------------------'
            , blocksymbols= '|:'
            , external  = None
            , logfile=''
            )
                   
    '''  
      
    def __init__(self, **kargs):
      self.header       = '='*45+BR+'TreeLog output'+ BR+'='*45
      self._on          = True
      self.block_beg = '* '
      self.block_end = '* '
      self.func_beg = '> '
      self.func_end = '< '
      self.indent       = 1
      self.blocksymbols= '|:'
      self.blockline = '-----------------------'
      self.external = None
      self.logfile=''
      self.__dict__.update(kargs)
      if self.logfile and os.path.exists(self.logfile):
              open(self.logfile,'w').write( self.header + BR)
      self.reset() 
                
    def reset(self): 
        
        self.blocks = []
        self.indentstr = ''
        self.data    = [self.header]
        self.htmdata = []
        self.blocksymb = ''
        self.current=[]
        if self.external:  # external={'data':[]} 
           self.external['data'] = self.data
        
    def on(self) : self._on = True        
    def off(self): self._on = False 
        
    def b( self, label=None, mode='block'):  # mode='block'|'func' 
        
        if label==None: label = getcallerargs(asString=True)
                
        ind = ''.join( sym+' '*self.indent  for lbl,sym in self.blocks ) 
        sym= self.blocksymbols[ divmod( len(self.blocks), 
              len(self.blocksymbols))[1]] #len(self.blocks) #self._symbgen.next()
                
        if self._on: 
           self.current= [ ind + '.'+self.blockline 
                    , ind+ sym+  (mode=='block' and self.block_beg or self.func_beg)
                                #self[ mode+'_beg'] 
                      + str(label)  ]
           self.postlog()
                        
        self.blocksymb =  sym
        self.blocks.append( [label, sym] )
                
    def e( self, label=None, mode='block', retmode='all' ): ## mode='block|func'
           
        if len(self.blocks):  ## Note: do we want to catch error if blocks empty ?
                
          b= self.blocks.pop()   ## [label, symbol ] 
          ind = ''.join( sym +' '*self.indent for lbl,sym in self.blocks ) 
                
          if self._on:
            if label:
              self.current=[ ind + self.blocksymb 
                             +  (mode=='block' and self.block_end or self.func_end)
                             + label
                           , ind + "'"+self.blockline ]
            else:
              self.current=[ ind + "'"+self.blockline ]
                        
            self.postlog()
                        
          self.blocksymb = len(self.blocks) and self.blocks[-1][1] or ''
                
    def l(self,x):
        if self._on:
           ind = ''.join( sym +' '*self.indent  for lbl,sym in self.blocks )  
           self.current= [ ind + '-'+ str(x) ]   ## 2018.3.13: change x to str(x)
           self.postlog()
                        
    def postlog(self):
        self.data+= self.current 
        if self.logfile:
           if os.path.exists(self.logfile):
              open(self.logfile,'a').write(BR.join(self.current)+BR)
           else:
              open(self.logfile,'w').write(self.text())
                                        
    '''def _getsymb(self):
            i, s = -1, self.blocksymbbols
            while 1:
                    i+=1
                    if i==len(s): i=0
                    yield s[i]
    ''' 
    def __call__(self,func=None, on=False ):
        
        if (func==None) and not on:  ## allow @log() or @log(on=False) to turn off
           return lambda f: f       ## BUT ... it can be done with #@log
                         
        elif not inspect.isfunction(func):
          self.l(func)
                        
        else:
           ## Needs functools.wraps to preserve the signature of func
           @functools.wraps(func)
           def wraper(*args, **kargs):
                                
              fn = func.__name__
                                
              ## Decide if the func is a bound method of a class
              ##
              fninfo= traceback.extract_stack()[-2]
                                
              #self( str(fninfo) )
                                
              ## ref: http://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init
              ##
              ## fninfo will be something like:
              ##
              ## (1) ('<doctest __main__.TreeLog.__call__[34]>', 1, '<module>', 'cc = Cls()')
              ## (2) ('<doctest __main__.TreeLog.__call__[26]>', 1, '<module>', 'test5(a=4)')
              ## (3) ('<doctest __main__.TreeLog.__call__[35]>', 1, '<module>', 'cc.getname()')
              ## (4) ('<doctest __main__.TreeLog.__call__[33]>', 5, '__init__', "self.setname()")
              ## (5)               ('<doctest __main__.Cj[1]>', 1, '<module>', 'len( cj.getSubs(2) )')
              ## (6) (...                                                    , 'c,d = cc1.getit(), cc2.getit()' )
              ## 
              ## (1): func is the __init__ of Cls during instantiation of cc
              ## (2): func is not bound
              ## (3): func is a bound method of instance cc
              ## (4): self.setname is called within class __init__, i.e.,
              ##         when the inistance building not yet complete. This
              ##         will show up as self.???
              ## Case 5: called within other statement
              ##
                                
              #####################################
              ## First, we try to find the binder of func.
              ## If func is a bound method, the first argument in its
              ## argument will be *self*, or any name representing the 
              ## class instance. 
                                
              bindername=''
                                
              fr= inspect.currentframe().f_back
              for k,v in fr.f_locals.items():
                      if len(args)>0 and id(args[0])== id(v):
                              bindername=k+'.'
              #self( '### Found binder = '+ bindername)               
                                
              ## When the binder is not found, it could be:
              ##
              ## (1) Not bound:
              ##     'test()', 'len(test())', 'c,d = test1(),test2()'
              ## (2) During class initiation:
              ##     'cc=Cls()', 'c,d = Cls1(), Cls2()'
              ##
              ## For (1) we just pass the func name. 
              ## For (2), it's probably impossible to get the binder name,
              ## 'cos initantiation of the binder is not yet complete.
              ## At this moment, we will just show something like 'self':
              ## 
              ##  self.__init__ .... 
                                
                                
              ##############################################
              ## Then we find the argument names and values
                                
              ## For a function 
              ##
              ##  def test(a,b, *alist, *kwds):
              ##      i,j,k = 1,2,3
              ##
              ## inspect.getargspec returns:
              ##
              ## ArgSpec(args=['a', 'b']
              ##        , varargs='alist'   # <--- name of the *args
              ##        , keywords='kwds'   # <--- name of the **kargs
              ##        , defaults=(None,))
              ##
              ## varargs and keywords will be None if not defined
              ##
              ## Note:
              ##
              ## - inspect.getargspec(func), returning a named tuple
              ##    (args, varargs, keywords, defaults), is deprecated in py3
              ##
              ## - Use inspect.getfullargspec(func) that returns a named tuple:
              ##   FullArgSpec(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) 
              ##
              ## def example(a:int ,b=1,*c,d,e=2,**f):
              ##      pass
              ##
              ## inspect.getfullargspec(example) returns:
              ##
              ## FullArgSpec( args=['a', 'b']
              ##            , varargs='c'
              ##            , varkw='f'
              ##            , defaults=(1,)
              ##            , kwonlyargs=['d', 'e']
              ##            , kwonlydefaults={'e': 2}
              ##            , annotations={'return': <class 'str'>, 'a': <class 'int'>})
              
              argspec = inspect.getfullargspec(func)  
              if fn=='__init__': bindername= argspec.args[0]+'.'
                                
              ## inspect.getcallargs returns a dict whose keys represent
              ## ALL the argnames defined in the function signature, 
              ## including those values not given at calling
              ##
              ## {'a':3, 'b':4, 'alist':(), 'kwds':{} } 
              ## 
              ## BUG:
              ## Traceback (most recent call last):
              ##        File "cj.py", line 556, in <module>
              ##              partsave_test()         
              ##        File "cj.py", line 554, in partsave_test
              ##              partsize=10000) 
              ##        File "/home/vincent/code/repos/pantools/TreeLog.py", line 1231, in wraper
              ##              callargs= inspect.getcallargs(func, *args, **kargs) 
              ##      TypeError: getcallargs() got multiple values for keyword argument 'func'
              ##
              ## Seems to happen when a funcction is defined with ...(... **ops)
              ##
              callargs= inspect.getcallargs(func, *args, **kargs) 
                                
              fn = bindername + fn
              starti = bindername and 1 or 0 
              argspec_args= argspec.args[starti:]
              out = [ (an, callargs[an]) for an in argspec_args ]
                                
              ## If a list-args is defined, and its value is given at calling:
              ##
              if argspec.varargs and len( callargs[argspec.varargs] ) >0:
                 out.append( (argspec.varargs, callargs[argspec.varargs] ) )
                                
              ## If a kargs is defined:
              ##
              ## To get the name of keyword_var in py3 (inspect.getfullargspec), use varkw
              ## (for py2, use argspec.keywords)
              #if argspec.keywords:
              #   out+= callargs[ argspec.keywords ].items()
              if argspec.varkw:  
                 out+= callargs[ argspec.varkw ].items()
                                        
              out = quotifykvlist(out) ## format the args
                                
              self.b( fn +'('+ ', '.join(out) + ')' , mode='func') 
              ret= func(*args, **kargs)
                                
              logret= ret 
              if ret!=None:
                 logret = (type(ret)==str and quotify(ret)) or str(ret)
                 if len(logret)> 25:
                    if hasattr( ret, 'keys'):
                       ret = [ k + '=' + (iscountable(v) and (type(v)!=str and typename(v) or '') or '') + 
                            (iscountable(v) and ( type(v)==str and quotify(v) or '(%s)'%len(v)) or str(v)) 
                                                                
                            for k,v in ret.items()
                          ]
                       logret = '{%s}'%', '.join(ret) 
                    else:
                       logret = '|%s...|'%(logret[:35])
              self.e( logret, mode='func')
                                
              return ret
           return wraper
                
        '''  
        # The following code works, but arguments might be printed in
        # random order, due to the fact that .getcallargs returns a dict 
        #
        @functools.wraps(func)
        def wraper(*args, **kargs):
                argdict= inspect.getcallargs(func, *args, **kargs)                  
                out= quotifykvlist( argdict.items() )       
                        
                self.b( func.__name__+'('+ ', '.join(out) + ')' ) 
                ret= func(*args, **kargs)
                self.e()
                return ret
        return wraper 
        '''
    def text(self):
            return BR.join( self.data )     
                                
    
def test():   
    import doctest 
    print('--- Loading "{}" for doctest:'.format(PATH_TO_README))
    #print( os.path.split( os.path.realpath(sys.argv[0])) )
    doc = ''.join( open(PATH_TO_README, 'r').readlines() )
    TreeLog.__doc__ = doc
    doctest.testmod()  
    print('--- Tests done.')
     
    ## The following is the original way to run doctest from 
    ## the TreeLog.__doc__. It is abandoned 'cos it forces us 
    ## to maintain 2 copies of test examples (in TreeLog.__doc__
    ## and in README.md )
    # print('--- Running doctest.testmod() for TreeLog module:')
    # doctest.testmod()
    # print('--- Test done.')
                    
class panlog_old(list):
    
    def __init__(self, savepath=r'c:\t', append=True):
        #pl.b()
        self._on = False
        self.layer = 0 
        self.block_beg = '> '
        self.block_end = '< '
        self.indent = ' |'
        self.block_indent = ' '
        self.blocks=[]  # [(head,tail), (head,tail) ...]
        
        self.txtfile = SAVE_TXT_PATH
        self.htmfile = SAVE_HTM_PATH
        self.block_style= HTM_BLOCK_STYLE
        self.block_mover_style= HTM_BLOCK_STYLE
        self.block_head = HTM_BLOCK_HEAD  
        self.block_tail = HTM_BLOCK_TAIL
        
        self.header='='*45+BR+'TreeLog output'+ BR+'='*45
        self.data = [self.header]
        self.js='''<script language=javascript>
        function toggleNext(tag){
          //alert(tag)
          //alert(tag.nextSibling)
          //alert(tag.nextSibling.nextSibling)
          
          nts = tag.nextSibling.nextSibling.style
          nts.display = nts.display=='block'?'none':'block'
        
         
        }        

        function onMover(tag){

           tag.oldcolor = tag.style.backgroundColor
           try{
            var e = window.event;
            e.cancelBubble = true;
            if (e.stopPropagation) e.stopPropagation();
           }catch(e){this.stopPropagation()}
           
           //tag.style.borderStyle='inset'
           //tag.style.borderColor='red'
           tag.style.backgroundColor = 'yellow' 
            
        }        
        function onMout(tag){
           try{
           var e = window.event;
           e.cancelBubble = true;
           if (e.stopPropagation) e.stopPropagation();
           }catch(e){}

            //tag.style.borderStyle='outset'
            //tag.style.borderColor = ''
            tag.style.backgroundColor = tag.oldcolor
        }        
        </script>
        '''
        self.htmdata=[self.js, self.header.replace(BR,'<br/>')]
        
        #pl.e()
    
    def reset(self):
        self.data = [self.header]
        self.htmdata=[self.header.replace(BR,'<br/>')]
        
    def on(self) : self._on = True        
    def off(self): self._on = False 
                
    def b(self,label=None):
        if label==None: label = getcallername() 
        self.layer+=1
        self.add( '<blk>\n'+ self.block_beg+ str(label))
        
    def e(self,label=None):
        if label==None: label = getcallername() 
        self.add( self.block_end+ label+BR+'</blk>'  )
        self.layer-=1
        
    def fb(self,arg='',label=''):
        fn= getcallername() 
        self.layer+=1
        try:
          if arg!='': arg = arg.__repr__()
        except: pass
        self.add( '<blk>'+BR+'%s%s(%s) %s'%(self.block_beg,
                  '<b style="background-color:darkblue;color:lightblue;"'
                  +'>%s</b>'%fn, arg,label))

    def fe(self,arg='',label=''):
        try:
          fn = getcaller().__name__
        except:
          fn= ''
        try:
          if arg!='': arg = arg.__repr__()
        except: pass
          
        self.add( '%s%s(%s) %s'%(self.block_end,
                fn,arg,label)+BR+'</blk>')
        self.layer-=1

    
    def l(self,x):
        self.add( self.block_indent+ x)
    
    def add(self,x): 
        if not self._on: return None
        ind = self.indent*self.layer 
        
        line = '+---------------------'
        txt = str(x).replace('<blk>',line).replace('</blk>',line).split(BR)
        txt = [(y!=line and ind+y or ind[:-1]+y) for y in txt]
        self.data+=txt

        htmhead = HTM_BLOCK_HEAD%({'bgc':randomcolor()
                                  ,'new_bgc':randomcolor()})
        htm = str(x).replace('<blk>'+BR,htmhead).replace('</blk>',
            HTM_BLOCK_TAIL).split(BR)
        self.htmdata+=htm
        
        self.save()
        
    def save(self, append=False):
        '''  
         disable it for now during the transition to the new TreeLog class
        
        try:
          mode = append and 'a' or 'w'
          open(self.txtfile, mode).write(self.out())
          open(self.htmfile, mode).write(self.out(True))
        except:
          open(self.txtfile, 'w').write(self.out())
          open(self.htmfile, 'w').write(self.out(True))
        '''  
 
    def out(self, htm=False):
        if htm:
            s=BR+'div style="font-family:courier new">%s</div>'+BR
            return s%('\n<br/>'.join( self.htmdata )).replace('</div>'+BR+'<br/>','</div>')
        else: return BR.join(self.data)

if __name__ == "__main__":
  test()
    
