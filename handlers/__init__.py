import os

__all__ = [ name[:-3] for name in os.listdir(os.path.dirname(__file__)) 
            if name.endswith('.py') and name != '__init__.py' ]
            
import autoPull

#for name in __all__:
#    __import__(name)

print 'all', __all__


