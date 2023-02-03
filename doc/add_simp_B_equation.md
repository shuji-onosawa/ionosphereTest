$\vec{v}\cdot( \vec{v} \times \vec{B_{wave}}) ( = 0)$

$ =(\vec{v}_{\perp}+\vec{v_\parallel}) \cdot ((\vec{v}_{\perp}+\vec{v_\parallel})\times \vec{B_{wave}})$

$ = \vec{v_\parallel}\cdot(\vec{v_\parallel}\times\vec{B_{wave}}) + \vec{v_\perp}\cdot(\vec{v_\parallel}\times\vec{B_{wave}}) + \vec{v_\parallel}\cdot(\vec{v_\perp}\times\vec{B_{wave}}) + \vec{v_\perp}\cdot(\vec{v_\perp}\times\vec{B_{wave}})$

$ = \vec{v_\perp}\cdot(\vec{v_\parallel}\times\vec{B_{wave}}) + \vec{v_\parallel}\cdot(\vec{v_\perp}\times\vec{B_{wave}}) $

$\vec{v_\perp}\cdot(\vec{v_\parallel}\times\vec{B_{wave}}) = - \vec{v_\parallel}\cdot(\vec{v_\perp}\times\vec{B_{wave}}) $

**Assumption $B_{wave}$ is constant**

and 

**Assumption $\vec{B_{wave}}\perp\vec{E} $ and $\vec{B_{wave}}\perp\vec{B_0} $**

SO, 


$v_\perp v_\parallel B_{wave} =  v_\parallel v_\perp B_{wave} $

OR


$v_\perp v_\parallel B_{wave} = - v_\parallel v_\perp B_{wave} $



We choose

$v_\perp v_\parallel B_{wave} = - v_\parallel v_\perp B_{wave} $

so, 

$v_\perp v_\parallel = 0$

$\frac{dv_\perp}{dt}v_\parallel + \frac{dv_\parallel}{dt}v_\perp = 0$


---

$\vec{F_{Bwave}} =q((\vec{v}_{\perp}+\vec{v_\parallel})\times \vec{B_{wave}})$

$ = q\vec{v_\parallel}\times\vec{B_{wave}}  + q\vec{v_\perp}\times\vec{B_{wave}}$


Above assumption and result, we got 

$$F_{\perp Bwave} = qv_\parallel B_{wave}$$
$$F_{\parallel Bwave} = -qv_\perp B_{wave}$$

OR

$$F_{\perp Bwave} = -qv_\parallel B_{wave}$$
$$F_{\parallel Bwave} = qv_\perp B_{wave}$$

from equation.md

Because of 
$\frac{dW_\parallel}{dt} + \frac{d W_\perp}{dt} = \frac{dW}{dt} = qE v_\perp$

$\frac{dv_\perp}{dt} = \frac{qE}{m} - \frac{v_\parallel}{v_\perp}\frac{d v_\parallel}{dt} $

Mirror Force is...
$\frac{dv_\parallel}{dt} = v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}}$ 

$\lambda$ : Invarialnt latitude $L$ : L-shell $R_E$ : Earth Radius

So, 


$\frac{dv_\perp}{dt} = \frac{qE}{m} - \frac{v_\parallel}{v_\perp}\frac{d v_\parallel}{dt} $

$\frac{dv_\parallel}{dt} = v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} +q \frac{B_{wave}}{m}\frac{dv_\perp}{dt}$ 


$\frac{dv_\parallel}{dt} = v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} + q\frac{B_{wave}}{m}(\frac{qE}{m} - \frac{v_\parallel}{v_\perp}\frac{d v_\parallel}{dt} )$ 


$\frac{dv_\parallel}{dt} = v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} + q\frac{B_{wave}}{m}\frac{qE}{m} - q\frac{B_{wave}}{m}\frac{v_\parallel}{v_\perp}\frac{d v_\parallel}{dt}$ 


$\frac{dv_\parallel}{dt}(1- q\frac{B_{wave}}{m}\frac{v_\parallel}{v_\perp}) = v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} + q\frac{B_{wave}}{m}\frac{qE}{m}$ 


$\frac{dv_\parallel}{dt} = (1- q\frac{B_{wave}}{m}\frac{v_\parallel}{v_\perp})^{-1}\{v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} + q\frac{B_{wave}}{m}\frac{qE}{m}\}$ 

so, we got


$\frac{dv_\parallel}{dt} = (1- q\frac{B_{wave}}{m}\frac{v_\parallel}{v_\perp})^{-1}\{v_\perp^2\frac{1}{2}  \frac{1}{R_EL}\frac{3\sin\lambda(5\sin^2\lambda^2+3)}{\cos^{2}\lambda(1+3\sin^2\lambda)^{\frac{3}{2}}} +q \frac{B_{wave}}{m}\frac{qE}{m}\}$ 


$\frac{dv_\perp}{dt} = \frac{qE}{m} - \frac{v_\parallel}{v_\perp}\frac{d v_\parallel}{dt} $
