out:=OutputTextFile("hom2.txt",false); SetPrintFormattingStatus(out,false);
for d in [5..100] do
  for i in [1..NrPrimitiveGroups(d)] do
    G:=PrimitiveGroup(d,i);
    if IsNaturalAlternatingGroup(G) or IsNaturalSymmetricGroup(G) then continue; fi;
    if Length(Orbits(G,Combinations([1..d],2),OnSets))<>1 then continue; fi;
    h:=1; if Length(Orbits(G,Combinations([1..d],3),OnSets))=1 then h:=3; else h:=2; fi;
    AppendTo(out,d," ",i," ",Size(G)," ",h," \"",Name(G),"\"\n");
  od;
od;
CloseStream(out); QUIT;
