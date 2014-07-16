def string_permutations(string):
  level=[]
  def permute(prefix, suffix):
    level.append(prefix)
    if len(suffix)==0:
      return
    for i in range(len(suffix)):
      permute(prefix + suffix[i], suffix[:i]+suffix[i+1:])
  permute("",string)
  return level


t = string_permutations("Kevin")
print t