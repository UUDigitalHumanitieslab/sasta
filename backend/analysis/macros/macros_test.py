import pytest
from .macros import expandmacros, get_macros_dict
import os.path as op

TESTSTRINGS = ['b  = """number(@begin)"""', 'e = """number(@end)"""',
               'single_name = """( @ntype = "eigen" or @postag="SPEC(deeleigen)"  )"""',
               'multi_name =  """( @cat=''mwu'' and node[@rel=''mwp'' and %single_name%] ) """',
               'name =        """( %single_name% or %multi_name% )"""',
               'name_phrase=  """( %name% or node[@rel="hd"  and %name%]  )"""']
TESTQUERIES = [('//node[%b%="3"]', '//node[number(@begin)="3"]'),
               ('//node[%single_name%]',
                "//node[( @ntype = 'eigen' or @postag='SPEC(deeleigen)'  )]"),
               ("//node[%multi_name%]",
                "//node[( @cat='mwu' and node[@rel='mwp' and ( @ntype = 'eigen' or @postag='SPEC(deeleigen)'  )] ) ]"),
               ("//node[%fout%]", "//node[%fout%]")]

MACROFILENAMES = ['sastamacros1.txt',
                  'sastamacros2.txt']
HERE = op.dirname(op.abspath(__file__))
MACROFILENAMES = [op.join(HERE, fn) for fn in MACROFILENAMES]


@pytest.mark.parametrize('short, long', TESTQUERIES)
def test_macro_expansion(short, long):
    macrodict = get_macros_dict(MACROFILENAMES)
    for (short, long) in TESTQUERIES:
        expansion = expandmacros(short, macrodict)
        assert expansion == long
