Read("tom2.g");
for q in [13,16,17,19,23,25,27,29,31,32,37,41,43,47,49,53,59,61,64,67,71,73,79,81,83,89,97] do
  DoitG(Line(q,"S"),Concatenation("S2_",String(q)));
  if q mod 2=1 then DoitG(Line(q,"G"),Concatenation("G2_",String(q))); fi;
  if not IsPrimeInt(q) then DoitG(Line(q,"P"),Concatenation("P2_",String(q))); fi;
od;
QUIT;
