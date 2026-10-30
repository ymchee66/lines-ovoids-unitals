DoitG:=function(H,name)
  local tom,M,ord,ol,k,F,o,out,t0,i,j,x,v;
  t0:=Runtime(); v:=NrMovedPoints(H);
  tom:=TableOfMarks(H); M:=MatTom(tom); ord:=OrdersTom(tom);
  ol:=List([1..Length(ord)],i->List(Orbits(RepresentativeTom(tom,i),[1..v]),Length));
  ol:=List([1..Length(ord)],i->Concatenation(ol[i],List([1..v-Sum(ol[i])],j->1)));
  x:=Indeterminate(Rationals,"x");
  out:=OutputTextFile(Concatenation(name,".txt"),false); SetPrintFormattingStatus(out,false);
  AppendTo(out,"{\"v\":",v,",\"order\":",Size(H),",\"ord\":",ord,",\"counts\":{");
  for k in [2..QuoInt(v,2)] do
    F:=List(ol,L->CoefficientsOfUnivariatePolynomial(Product(L,l->1+x^l)+x^(v+1))[k+1]);
    o:=SolutionMat(M,F);
    AppendTo(out,"\"",k,"\":",o);
    if k<QuoInt(v,2) then AppendTo(out,","); fi;
  od;
  AppendTo(out,"}}\n"); CloseStream(out);
  Print(name," classes ",Length(ord)," time ",Runtime()-t0,"\n");
end;
Line:=function(q,kind)
  local pts,G,f;
  pts:=Set(List(Filtered(GF(q)^2,x->not IsZero(x)),NormedRowVector));
  if kind="S" then G:=Action(SL(2,q),pts,OnLines);
  elif kind="G" then G:=Action(GL(2,q),pts,OnLines);
  else G:=Action(GL(2,q),pts,OnLines);
    f:=PermList(List(pts,p->Position(pts,NormedRowVector(List(p,c->c^Characteristic(GF(q)))))));
    G:=ClosureGroup(G,f);
  fi;
  return G;
end;
