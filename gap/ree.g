Read("tom2.g");
pick:=function(d,ord) local i; for i in [1..NrPrimitiveGroups(d)] do if Size(PrimitiveGroup(d,i))=ord and Transitivity(PrimitiveGroup(d,i))>=2 then return PrimitiveGroup(d,i); fi; od; return fail; end;
DoitG(pick(28,1512),"R3");
DoitG(pick(126,126000),"U35");
QUIT;
