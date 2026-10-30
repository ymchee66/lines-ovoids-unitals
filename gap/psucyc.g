pick:=function(d,ord) local i; for i in [1..NrPrimitiveGroups(d)] do if Size(PrimitiveGroup(d,i))=ord and Transitivity(PrimitiveGroup(d,i))>=2 then return PrimitiveGroup(d,i); fi; od; return fail; end;
for q in [3,5,7,9,11] do
  d:=Gcd(3,q+1); ord:=q^3*(q^3+1)*(q^2-1)/d; G:=pick(q^3+1,ord);
  Print("q=",q," size ",Size(G),"\n");
  for c in ConjugacyClasses(G) do
    x:=Representative(c); o:=Order(x);
    if o=1 then continue; fi;
    ct:=Collected(CycleLengths(x,[1..q^3+1]));
    Print("  ord ",o," n=",Size(c)," type ",ct,"\n");
  od;
od;
QUIT;
