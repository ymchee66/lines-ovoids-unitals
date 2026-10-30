for n in [11,12,23,24] do
  G:=MathieuGroup(n); Print("M",n," ",Size(G)," ",List(GeneratorsOfGroup(G),g->ListPerm(g,n)),"\n");
od;
G:=PrimitiveGroup(12,Position(List([1..NrPrimitiveGroups(12)],i->Size(PrimitiveGroup(12,i))),7920)); Print("M11_12 ",Size(G)," ",List(GeneratorsOfGroup(G),g->ListPerm(g,12)),"\n");
QUIT;
