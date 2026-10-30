# orbit-length distribution of PSL(n,q) on k-subsets of PG(n-1,q) via table of marks
Doit:=function(n,q,name)
  local H,tom,M,subs,ord,ol,k,F,o,out,t0,i,j,poly,x,v;
  t0:=Runtime();
  H:=Action(SL(n,q),Set(List(Filtered(GF(q)^n,x->not IsZero(x)),NormedRowVector)),OnLines);
  v:=NrMovedPoints(H);
  tom:=TableOfMarks(H); M:=MatTom(tom); ord:=OrdersTom(tom);
  ol:=List([1..Length(ord)],i->List(Orbits(RepresentativeTom(tom,i),[1..v]),Length));
  ol:=List([1..Length(ord)],i->Concatenation(ol[i],List([1..v-Sum(ol[i])],j->1)));
  x:=Indeterminate(Rationals,"x");
  out:=OutputTextFile(Concatenation(name,".txt"),false); SetPrintFormattingStatus(out,false);
  AppendTo(out,"{\"v\":",v,",\"order\":",Size(H),",\"ord\":",ord,",\"counts\":{");
  for k in [2..QuoInt(v,2)] do
    F:=List(ol,L->CoefficientsOfUnivariatePolynomial(Product(L,l->1+x^l)+x^(v+1))[k+1]);
    # F[i] = sum_j M[i][j] o[j]  (M lower triangular in tom ordering: marks of U_i on H/U_j)
    o:=SolutionMat(M,F);
    AppendTo(out,"\"",k,"\":",o);
    if k<QuoInt(v,2) then AppendTo(out,","); fi;
  od;
  AppendTo(out,"}}\n"); CloseStream(out);
  Print(name," classes ",Length(ord)," time ",Runtime()-t0,"\n");
end;
