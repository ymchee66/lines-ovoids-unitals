Read("tom2.g");
pick:=function(d,ord) local i; for i in [1..NrPrimitiveGroups(d)] do if Size(PrimitiveGroup(d,i))=ord and Transitivity(PrimitiveGroup(d,i))>=2 then return PrimitiveGroup(d,i); fi; od; return fail; end;
DoitG(pick(28,6048),"U33");
DoitG(pick(65,29120),"Sz8");
DoitG(pick(65,62400),"U34");
QUIT;
