for q in [17,23,29] do
  pts:=Set(List(Filtered(GF(q)^2,x->not IsZero(x)),NormedRowVector));
  G:=Action(GL(2,q),pts,OnLines);
  Print("q=",q,"\n");
  for c in ConjugacyClassesSubgroups(G) do
    U:=Representative(c);
    if Size(U)>1 and IsPrimePowerInt(Size(U)) and Size(U) mod 2=0 then
      Print("  order ",Size(U)," n=",Size(c)," ",StructureDescription(U)," orbits ",Collected(List(Orbits(U,[1..q+1]),Length)),"\n");
    fi;
  od;
od;
QUIT;
