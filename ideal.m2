loadPackage "NumericalAlgebraicGeometry";
R = ZZ/911[f, rx, ry, rz, vx, vy, vz]
c = random(0, 10);

-- Function takes number of recievers and generates random parameters
generateRandomParameters = n -> (
    f := random(0, 10);
    fi := {};
    ri := {};
    vi := {};

    -- Generate random values
    for i from 1 to n do (
        fi = append(fi, random(0, 10));
            
        randVec1 := {random(-10, 10), random(-10, 10), random(-10, 10)};
        randVec2 := {random(-10, 10), random(-10, 10), random(-10, 10)};
        
        ri = append(ri, randVec1);
        vi = append(vi, randVec2);
    );

    return {f, fi, ri, vi};
);

-- Function constructs quations
constructEquations = (fi, ri, vi) -> (
    n = #fi;
    r := [rx, ry, rz];
    v := [vx, vy, vz];
    myEquations := {};
    for j from 0 to n - 1 do(
        xSq := (ri#j#0 - r#0) * (ri#j#0 - r#0);
        ySq := (ri#j#1 - r#1) * (ri#j#1 - r#1);
        zSq := (ri#j#2 - r#2) * (ri#j#2 - r#2);  
        pSq := xSq + ySq + zSq;
        lhs := pSq * c * c * (f - fi#j) * (f - fi#j);
        rhs := (ri#j#0 - r#0)*(vi#j#0 - v#0) + (ri#j#1 - r#1)*(vi#j#1 - v#1) + (ri#j#2 - r#2)*(vi#j#2 - v#2);
        rhs = f * rhs * rhs;
        equation := lhs - rhs;
        myEquations = append(myEquations, equation);
    );
    
    return myEquations;
);

parameters := generateRandomParameters(6);
F = constructEquations(parameters#0, parameters#1, parameters#2, parameters#3);
I = ideal F;
<< dim I;
<< degree I;