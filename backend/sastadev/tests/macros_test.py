from sastadev.macros import expandmacros

teststrings = ['b  = """number(@begin)"""', 'e = """number(@end)"""', 'single_name = """( @ntype = "eigen" or @postag="SPEC(deeleigen)"  )"""',
               'multi_name =  """( @cat=''mwu'' and node[@rel=''mwp'' and %single_name%] ) """', 'name =        """( %single_name% or %multi_name% )"""',
               'name_phrase=  """( %name% or node[@rel="hd"  and %name%]  )"""']


testqueries = [('//node[%b%="3"]', '//node[number(@begin)="3"]'), ('//node[%single_name%]', "//node[( @ntype = 'eigen' or @postag='SPEC(deeleigen)'  )]"),
               ("//node[%multi_name%]", "//node[( @cat='mwu' and node[@rel='mwp' and ( @ntype = 'eigen' or @postag='SPEC(deeleigen)'  )] ) ]"), ("//node[%fout%]", "//node[%fout%]")]


def test_macros():
    # macrodict = macrostrs2dict(teststrings)
    for (short, long) in testqueries:
        expansion = expandmacros(short)
        if expansion == long:
            print('OK:', expansion)
        else:
            print('NO:', expansion)
            print('--:', long)
